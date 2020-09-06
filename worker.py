import sys
from PySide2.QtCore import QObject, Signal, QThread, Slot, QByteArray, QTimer
from PySide2.QtNetwork import QTcpSocket, QTcpServer, QHostAddress, QNetworkInterface
from language import Language

class Signals(QObject):
    updateNr = Signal(int)
    callFunc = Signal(str, str)
    getStatus = Signal(str)
    setStatus = Signal(str)

class MyServer(QTcpServer):
    onClose = Signal()
    onWrite = Signal(bytearray)

    def __init__(self, parent):
        super(MyServer, self).__init__(parent)
        self.listen(QHostAddress.AnyIPv4, 1234)
        listAddress = QNetworkInterface.allAddresses()
        self.list = ['localhost']
        print(listAddress)
        for address in listAddress:
            if address == QHostAddress.LocalHost or address.toIPv4Address():
                self.list.append(address.toString())
        self.list.sort(key=lambda x: (x[0].isdigit(), x))
        print("nasłuchuje na: ", self.list)
        self.parent = parent
        self.signal = Signals()
        self.status = Language.Listening
        self.listThread = []
        self.parent.ui.IP_Label.setText(Language.IpAddresses + ', '.join(self.list))
        self.parent.set_text_remote_status(Language.Listening)

    @Slot(str)
    def message_received(self, message):
        print("przysłano: ", message)
        if message == "homeup":
            self.parent.on_home_up()
            #self.send("home:"+self.parent.ui.HomeScore_Label.text())
        elif message == "homedown":
            self.parent.on_home_down()
        elif message == "awayup":
            self.parent.on_away_up()
        elif message == "awaydown":
            self.parent.on_away_down()
        elif message == "start":
            self.parent.start_timer()
        elif message == "pregame":
            self.parent.on_pregame()
        elif message == "halftime":
            self.parent.on_half_time()
        elif message == "periodup":
            self.parent.on_period_up()
        elif message == "perioddown":
            self.parent.on_period_down()

    @Slot(str, str)
    def call_func_parent(self, func, attr):
        getattr(self.parent, func)(attr)

    def send(self, message):
        self.onWrite.emit(message.encode("cp852"))
        print ("Wysłałem wiadomość: ", message)

    def incomingConnection(self, socketDescriptor):
        newThread = self.create_thread(socketDescriptor)
        self.listThread.append(newThread)
        QTimer.singleShot(1000, self.parent.save_all)
        print(self.listThread)

    def create_thread(self, socketDescriptor):
        worker = Worker(socketDescriptor)
        thread = QThread()
        self.onWrite.connect(worker.write_message)
        worker.signal.callFunc.connect(self.call_func_parent)
        worker.messageReceived.connect(self.message_received)
        worker.signal.getStatus.connect(self.getStatus)
        worker.signal.setStatus.connect(self.setStatus)
        self.signal.getStatus.connect(worker.getStatus)
        thread.started.connect(worker.start)
        worker.signal.updateNr.connect(self.update_nr_clients)
        worker.finished.connect(self.test)
        worker.moveToThread(thread)
        thread.worker = worker
        thread.start()
        return thread

    @Slot(int)
    def update_nr_clients(self, number):
        print("update nr = ", number)
        self.parent.update_nr_clients(number)

    @Slot(QThread)
    def test(self, thread):
        print("pierwsze")
        print(self.listThread)
        thread.quit()
        thread.deleteLater()
        self.listThread.remove(thread)
        QThread.sleep(1)
        print("drugie")
        print(self.listThread)
        if not self.listThread:  # and (not self.listWorker):
            self.parent.set_text_remote_status(Language.Listening)
            print("zmieniam opis na ", Language.Listening)

    def my_close(self):
        self.close()
        if self.listThread:
            self.send("Zamykam Wszystko.")
            copylistt = self.listThread.copy()
            for t in copylistt:
                self.test(t)
                self.update_nr_clients(len(self.listThread))
            Worker.nrOfClients = 0
            self.deleteLater()
        self.parent.set_text_remote_status(Language.NotConnected)
        self.parent.ui.IP_Label.setText(Language.IpAddressesDefault)
        self.status = Language.NotConnected

    @Slot()
    def getStatus(self):
        self.signal.getStatus.emit(self.status)

    @Slot(str)
    def setStatus(self, status):
        self.status = status
        self.signal.getStatus.emit(self.status)
        print("status in Server: ", self.status)


class Worker(QObject):
    nrOfClients = 0
    messageReceived = Signal(str)
    finished = Signal(QThread)

    def __init__(self, socket_id):
        super(Worker, self).__init__()
        self.socket_id = socket_id
        self.signal = Signals()
        self.serverStatus = None

    @Slot()
    def start(self):
        print("tworze socket")
        self.socket = QTcpSocket()
        if self.socket.setSocketDescriptor(self.socket_id):
            self.signal.callFunc.emit("set_text_remote_status", Language.Connected)
            self.signal.setStatus.emit(Language.Connected)
            Worker.nrOfClients += 1
            self.signal.updateNr.emit(Worker.nrOfClients)
            print("polaczylem")
            self.socket.write(QByteArray(b"Polaczony ze scoreboard\r\n"))

        else:
            print("nie polaczylem")
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
        self.deleteLater()
        self.finished.emit(self.thread())


    @Slot()
    def read_message(self):
        while self.socket.canReadLine():
            line = self.socket.readLine().trimmed().data().decode("cp852")
            self.messageReceived.emit(line)

    @Slot(QByteArray)
    def write_message(self, message):
        self.socket.write(message)
        self.socket.flush()

    @Slot(str)
    def setStatus(self, status):
        self.serverStatus = status
        print("status in set Worker: ", self.serverStatus)

    @Slot(str)
    def getStatus(self, status):
        self.serverStatus = status
        print("status in get Worker: ", self.serverStatus)
        pass

