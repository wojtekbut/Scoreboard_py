import sys
import threading

from PySide2.QtCore import QObject, Signal, QThread, Slot, QByteArray, QTimer
from PySide2.QtNetwork import QTcpSocket, QTcpServer, QHostAddress

from language import Language

class Signals(QObject):
    updateNr = Signal(int)
    callFunc = Signal(str, str)

class MyServer(QTcpServer):
    status = "Not Connected"
    licznik = 1
    listWorker = []
    listThread = []
    onClose = Signal()
    onWrite = Signal(bytearray)

    def __init__(self, parent):
        super(MyServer, self).__init__(parent)
        self.listen(QHostAddress.AnyIPv4, 1234)
        self.server = None
        self.parent = parent
        self.signal = Signals()
        MyServer.status = "Listening..."
        self.parent.set_text_remote_status(Language.Listening)

    @Slot(str)
    def message_received(self, message):
        print("przysłano: ", message)
        if message == "homeup":
            self.parent.on_home_up()
        elif message == "homedown":
            self.parent.on_home_down()

    def str_to_class(self, classname):
        return getattr(sys.modules[__name__], classname)

    @Slot(str, str)
    def call_func_parent(self, func, attr):
        getattr(self.parent, func)(attr)

    def send(self, message):
        self.onWrite.emit(message.encode("cp852"))
        print ("Wysłałem wiadomość: ", message)

    def incomingConnection(self, socketDescriptor):
        w = Worker(socketDescriptor)
        MyServer.listWorker.append(w)
        t = QThread()
        MyServer.listThread.append(t)
        w.moveToThread(t)
        self.onWrite.connect(MyServer.listWorker[-1].write_message)
        MyServer.listWorker[-1].signal.callFunc.connect(self.call_func_parent)
        MyServer.listWorker[-1].messageReceived.connect(self.message_received)
        MyServer.listThread[-1].started.connect(MyServer.listWorker[-1].start)
        #MyServer.listThread[-1].signal.updateNr.connect(self.update_nr_clients)
        MyServer.listWorker[-1].signal.updateNr.connect(self.update_nr_clients)
        MyServer.listWorker[-1].finished.connect(self.test)
        #MyServer.listWorker[-1].finished.connect(MyServer.listThread[-1].quit)
        #MyServer.listWorker[-1].finished.connect(MyServer.listWorker[-1].deleteLater)
        #MyServer.listThread[-1].finished.connect(MyServer.listThread[-1].deleteLater)
        MyServer.listThread[-1].start()
        #self.parent.save_all()
        #threading.Thread(target=self.parent.save_all).start()   #, args=("Time:" + value,)).start()
        QTimer.singleShot(1000, self.parent.save_all)
        print(MyServer.listWorker)
        print(MyServer.listThread)
        #self.onclose.connect(MyServer.list[-1].myabort)
        #self.onwrite[bytearray].connect(MyServer.list[-1].write_message)
        #MyServer.list[-1].finished.connect(MyServer.list[-1].deleteLater)

    @Slot(int)
    def update_nr_clients(self, number):
        print("update nr = ", number)
        self.parent.update_nr_clients(number)

    @Slot(QObject, QThread)
    def test(self, worker, thread):
        print("pierwsze")
        print(MyServer.listWorker)
        print(MyServer.listThread)

        MyServer.listWorker.remove(worker)
        worker.deleteLater()
        MyServer.listThread.remove(thread)
        thread.quit()
        thread.deleteLater()
        QThread.sleep(1)
        print("drugie")
        print(MyServer.listWorker)
        print(MyServer.listThread)
        if (not MyServer.listThread) and (not MyServer.listWorker):
            self.parent.set_text_remote_status(Language.Listening)
            print("zmieniam opis na Nasłuchuję.")

    def my_close(self):
        self.close()
        if MyServer.listWorker:
            self.send("Zamykam Wszystko.")
            copylistw = MyServer.listWorker.copy()
            copylistt = MyServer.listThread.copy()
            for w, t in zip(copylistw, copylistt):
                self.test(w, t)
                self.update_nr_clients(len(MyServer.listWorker))
            Worker.nrOfClients = 0
            self.deleteLater()
        self.parent.set_text_remote_status(Language.NotConnected)
        MyServer.status = "Not Connected"


class Worker(QObject):
    nrOfClients = 0
    messageReceived = Signal(str)
    finished = Signal(QObject, QThread)

    def __init__(self, socket_id):
        super(Worker, self).__init__()
        self.socket_id = socket_id
        self.signal = Signals()

    @Slot()
    def start(self):
        print("tworze socket")
        self.socket = QTcpSocket()
        if self.socket.setSocketDescriptor(self.socket_id):
            self.signal.callFunc.emit("set_text_remote_status", Language.Connected)
            MyServer.status = "Connected"
            Worker.nrOfClients += 1
            self.signal.updateNr.emit(Worker.nrOfClients)
            print("polaczylem")
        else:
            print("nie polaczylem")
        self.socket.write(QByteArray(b"Polaczony ze scoreboard\r\n"))
        #self.socket.flush()

        self.socket.disconnected.connect(self.socket.deleteLater)
        self.socket.disconnected.connect(self.ending)
        self.socket.readyRead.connect(self.read_message)

    @Slot()
    def ending(self):
        Worker.nrOfClients -= 1
        print("ending in worker")
        self.signal.updateNr.emit(Worker.nrOfClients)
        print(self)
        print(self.thread())
        self.finished.emit(self, self.thread())


    @Slot()
    def read_message(self):
        while self.socket.canReadLine():
            line = self.socket.readLine().trimmed().data().decode("cp852")
            self.messageReceived.emit(line)

    @Slot(QByteArray)
    def write_message(self, message):
        self.socket.write(message)
        self.socket.flush()
