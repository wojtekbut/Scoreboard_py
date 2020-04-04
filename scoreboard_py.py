# This Python file uses the following encoding: utf-8
import sys
import os.path
from PySide2 import QtGui
from PySide2.QtWidgets import QApplication, QMainWindow
from ui_mainwindow import Ui_MainWindow
from char_map import CharMap
from PySide2.QtCore import QEvent, QTimer, QSettings, QTranslator, QXmlStreamWriter, QIODevice, QFile


class ScoreBoard(object):
    defaultSpeed = 1000
    useXml = True
    nr = 0
    homeScore = 0
    homeTeam = ""
    awayScore = 0
    awayTeam = ""
    period = 1
    minutes = 0
    seconds = 0
    setMinutes = 0
    setSeconds = 0
    timerString = "00:00"
    extraTimeString = "00:00"
    periodTimeString = "00:00"
    halfTimeString = "00:00"
    setToMinutes = 0
    setToSeconds = 0
    setPeriodMinutes = 0
    setPeriodSeconds = 0
    toCheck = False
    timerRuning = False

class Settings(object):
    writeXml = False

class Files(object):
    outDir = "output"
    iniFile = "config.ini"
    xmlFile = "output.xml"
    homeFile = "home.txt"
    awayFile = "away.txt"
    homeScoreFile = "homescore.txt"
    awayScoreFile = "awayscore.txt"
    timeFile = "time.txt"
    extraTimeFile = "extratime.txt"
    periodFile = "period.txt"
    halfTimeFile = "halftime.txt"
    path = os.path.abspath(__file__)
    curPath = os.path.dirname(path)
    outPath = os.path.join(curPath, outDir)
    iniPath = os.path.join(curPath, iniFile)
    xmlPath = os.path.join(outPath, xmlFile)
    homePath = os.path.join(outPath, homeFile)
    awayPath = os.path.join(outPath, awayFile)
    homeScorePath = os.path.join(outPath, homeScoreFile)
    awayScorePath = os.path.join(outPath, awayScoreFile)
    timePath = os.path.join(outPath, timeFile)
    extraTimePath = os.path.join(outPath, extraTimeFile)
    periodPath = os.path.join(outPath, periodFile)
    halfTimePath = os.path.join(outPath, halfTimeFile)
    try:
        os.mkdir(outPath)
    except FileExistsError:
        pass

    @staticmethod
    def save(filepath, value):
        file = open(filepath, "w")
        file.write(value)
        file.close()
        if Settings.writeXml:
            Files.write_xml()

    @staticmethod
    def save_all():
        for x, y in zip([Files.homePath, Files.awayPath, Files.homeScorePath, Files.awayScoreFile,
                         Files.timePath, Files.extraTimePath, Files.periodPath, Files.halfTimePath],
                        [ScoreBoard.homeTeam, ScoreBoard.awayTeam, ScoreBoard.homeScore, ScoreBoard.awayScore,
                         ScoreBoard.timerString, ScoreBoard.extraTimeString, ScoreBoard.period,
                         ScoreBoard.halfTimeString]):
            f = open(x, "w")
            f.write(str(y))
            f.close()
        if Settings.writeXml:
            Files.write_xml()

    @staticmethod
    def write_xml():
        ScoreBoard.nr = + 1
        file = QFile(Files.xmlPath)
        file.open(QIODevice.WriteOnly)
        xml = QXmlStreamWriter(file)
        xml.setAutoFormatting(True)
        xml.writeStartDocument()
        xml.writeStartElement("items")
        xml.writeTextElement("timestamp", str(ScoreBoard.nr))
        xml.writeTextElement("HomeScore", str(ScoreBoard.homeScore))
        xml.writeTextElement("AwayScore", str(ScoreBoard.awayScore))
        xml.writeTextElement("HomeName", ScoreBoard.homeTeam)
        xml.writeTextElement("AwayName", ScoreBoard.awayTeam)
        xml.writeTextElement("Period", str(ScoreBoard.period))
        xml.writeTextElement("Clock", ScoreBoard.timerString)
        xml.writeTextElement("ExtraClock", ScoreBoard.extraTimeString)
        xml.writeTextElement("HlafTimeClock", ScoreBoard.halfTimeString)
        xml.writeEndElement()
        xml.writeEndDocument()
        file.close()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.translator = QTranslator()
        self.translator.load('mainwindow_pl_PL')
        app.installTranslator(self.translator)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.ui.actionPolski.setChecked(True)
        self.start()

    def start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.ui.actionEnglish.triggered.connect(self.english)
        self.ui.actionPolski.triggered.connect(self.polski)
        self.ui.HomeDOWN_Button.clicked.connect(self.on_home_down)
        self.ui.HomeUP_Button.clicked.connect(self.on_home_up)
        self.ui.HomeUP2_Button.clicked.connect(self.on_home_up2)
        self.ui.AwayDOWN_Button.clicked.connect(self.on_away_down)
        self.ui.AwayUP_Button.clicked.connect(self.on_away_up)
        self.ui.AwayUp2_Button.clicked.connect(self.on_away_up2)
        self.ui.PeriodUP_Button.clicked.connect(self.on_period_up)
        self.ui.PeriodDOWN_Button.clicked.connect(self.on_period_down)
        self.ui.Minutes_Input.valueChanged[int].connect(self.on_time_input)
        self.ui.Seconds_Input.valueChanged[int].connect(self.on_time_input)
        self.ui.MinutesPeriod_Input.valueChanged[int].connect(self.on_period_input)
        self.ui.SecondsPeriod_Input.valueChanged[int].connect(self.on_period_input)
        self.ui.To_Checkbox.stateChanged.connect(self.on_to_check)
        self.ui.MinutesTo_Input.valueChanged[int].connect(self.on_to_input)
        self.ui.SecondsTo_Input.valueChanged[int].connect(self.on_to_input)
        self.ui.Start_Button.clicked.connect(self.start_timer)
        self.ui.UpdateTeam_Button.clicked.connect(self.on_update_team)
        self.ui.HomeName_Input.editingFinished.connect(self.on_home_change)
        self.ui.AwayName_Input.editingFinished.connect(self.on_away_change)
        self.ui.ResetTimer_Button.clicked.connect(self.on_reset_timer)
    # -------------------- s e t t i n g s ---------------------------------
        self.ui.Use_Xml_CheckBox.stateChanged.connect(self.on_use_xml)

        Files.save_all()

    # ------------------------------- T I M E R ------------------------------------

    def on_reset_timer(self):
        ScoreBoard.minutes = 0
        ScoreBoard.seconds = 0
        ScoreBoard.setMinutes = 0
        ScoreBoard.setSeconds = 0


    def start_timer(self):
        if not ScoreBoard.timerRuning:
            speed = ScoreBoard.defaultSpeed
            self.timer.start(1000)
            ScoreBoard.timerRuning = True
            self.ui.Start_Button.setText("STOP")
        else:
            self.timer.stop()
            ScoreBoard.timerRuning = False
            self.ui.Start_Button.setText("START")

    def tick(self):
        ScoreBoard.seconds +=1
        if ScoreBoard.seconds >59:
            ScoreBoard.minutes +=1
            ScoreBoard.seconds = 0
        self.set_time()

    # ---------------------------- T I M E  I N P U T ------------------------------

    def on_period_input(self):
        ScoreBoard.setPeriodMinutes = self.ui.MinutesPeriod_Input.value()
        ScoreBoard.setPeriodSeconds = self.ui.SecondsPeriod_Input.value()

    def on_time_input(self):
        ScoreBoard.setMinutes = self.ui.Minutes_Input.value()
        ScoreBoard.setSeconds = self.ui.Seconds_Input.value()
        if not ScoreBoard.timerRuning:
            ScoreBoard.minutes = ScoreBoard.setMinutes
            ScoreBoard.seconds = ScoreBoard.setSeconds
            self.set_time()

    def set_time(self):
        ScoreBoard.timerString = "{:02d}:{:02d}".format(ScoreBoard.minutes, ScoreBoard.seconds)
        self.ui.Clock_Label.setText(ScoreBoard.timerString)
        Files.save(Files.timePath, ScoreBoard.timerString)

    # ------------------------- H O M E ----------------------------------------------

    def on_home_change(self):
        ScoreBoard.homeTeam = self.ui.HomeName_Input.text()

    def on_home_down(self):
        if ScoreBoard.homeScore > 0:
            ScoreBoard.homeScore -= 1
            self.ui.HomeScore_Label.setText(str(ScoreBoard.homeScore))
            Files.save(Files.homeScorePath, str(ScoreBoard.homeScore))

    def on_home_up(self):
        ScoreBoard.homeScore += 1
        self.ui.HomeScore_Label.setText(str(ScoreBoard.homeScore))
        Files.save(Files.homeScorePath, str(ScoreBoard.homeScore))

    def on_home_up2(self):
        ScoreBoard.homeScore += 2
        self.ui.HomeScore_Label.setText(str(ScoreBoard.homeScore))
        Files.save(Files.homeScorePath, str(ScoreBoard.homeScore))

    # ------------------------- A W A Y -----------------------------------------

    def on_away_change(self):
        ScoreBoard.awayTeam = self.ui.AwayName_Input.text()

    def on_away_down(self):
        if ScoreBoard.awayScore > 0:
            ScoreBoard.awayScore -= 1
            self.ui.AwayScore_Label.setText(str(ScoreBoard.awayScore))
            Files.save(Files.awayScorePath, str(ScoreBoard.awayScore))

    def on_away_up(self):
        ScoreBoard.awayScore += 1
        self.ui.AwayScore_Label.setText(str(ScoreBoard.awayScore))
        Files.save(Files.awayScorePath, str(ScoreBoard.awayScore))

    def on_away_up2(self):
        ScoreBoard.awayScore += 2
        self.ui.AwayScore_Label.setText(str(ScoreBoard.awayScore))
        Files.save(Files.awayScorePath, str(ScoreBoard.awayScore))

    # ------------------------- P E R I O D -------------------------------------

    def on_period_up(self):
        ScoreBoard.period += 1
        self.ui.Period_Label.setText(str(ScoreBoard.period))
        self.update_on_period()

    def on_period_down(self):
        if ScoreBoard.period > 1:
            ScoreBoard.period -= 1
            self.ui.Period_Label.setText(str(ScoreBoard.period))
            self.update_on_period()

    def update_on_period(self):
        if not ScoreBoard.timerRuning:
            seconds = (ScoreBoard.period - 1) * (ScoreBoard.setPeriodMinutes * 60 + ScoreBoard.setPeriodSeconds)
            ScoreBoard.minutes = seconds // 60
            ScoreBoard.seconds = seconds % 60
            self.set_time()

    # -------------------------- T O   I N P U T ---------------------------------

    def on_to_check(self):
        if self.ui.To_Checkbox.isChecked():
            self.ui.MinutesTo_Input.setEnabled(True)
            self.ui.SecondsTo_Input.setEnabled(True)
        else:
            self.ui.MinutesTo_Input.setEnabled(False)
            self.ui.SecondsTo_Input.setEnabled(False)

    def on_to_input(self):
        ScoreBoard.setToMinutes = self.ui.MinutesTo_Input.value()
        ScoreBoard.setToSeconds = self.ui.SecondsTo_Input.value()

    # -------------------------- B U T T O N S ------------------------------------

    def on_update_team(self):
        Files.save(Files.homePath, ScoreBoard.homeTeam)
        Files.save(Files.awayPath, ScoreBoard.awayTeam)

    # ------------------------ S E T T I N G S ------------------------------------

    def on_use_xml(self):
        if self.ui.Use_Xml_CheckBox.isChecked():
            Settings.writeXml = True
        else:
            Settings.writeXml = False



    # -------------------------- L A N G U A G E ----------------------------------

    def english(self):
        self.ui.actionPolski.setChecked(False)
        self.ui.actionEnglish.setChecked(True)
        self.translator.load('mainwindow_en_GB')
        app.installTranslator(self.translator)
        self.ui.retranslateUi(self)

    def polski(self):
        self.ui.actionPolski.setChecked(True)
        self.ui.actionEnglish.setChecked(False)
        self.translator.load('mainwindow_pl_PL')
        app.installTranslator(self.translator)
        self.ui.retranslateUi(self)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
