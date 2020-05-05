# This Python file uses the following encoding: utf-8
import sys
import os.path
import threading
from datetime import datetime
from PySide2 import QtGui, QtWidgets
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QLabel

from language import Language
from ui_mainwindow import Ui_MainWindow
from char_map import CharMap
from PySide2.QtCore import QEvent, QTimer, QSettings, QTranslator, QXmlStreamWriter, QIODevice, QFile, QCoreApplication, \
    Qt, QUrl, Signal, QThread
from PySide2.QtGui import QFont
from obswebsocket import obsws, requests


class ScoreBoard(object):
    totalTenth = 0
    tenth = 0
    useXml = True
    nr = 0
    first = True
    homeScore = 0
    homeTeam = ""
    awayScore = 0
    awayTeam = ""
    period = 1
    totalTimeSec = 0  # total timer seconds
    totalSetTimeSec = 0  # total seconds in set timer input
    totalToSec = 0  # total seconds in to timer input
    totalCurrentPeriodSec = 0  # total current period seconds
    startPeriodsec = 0  # total second of start current period
    stopPeriodsec = 0  # total seconds of end current period
    totalSetPeriodSec = 0  # total seconds of period input
    timerString = "00:00"  # timer clock string
    overTimeString = "00:00"  # overtime clock string
    periodTimeString = "00:00"  # period clock string
    halfTimeString = "00:00"  # halftime clock string
    minutes = 0  # timer minutes
    seconds = 0  # timer seconds
    setMinutes = 0  # minutes of set timer input
    setSeconds = 0  # seconds of set timer input
    setToMinutes = 0  # minutes of set "to" timer input
    setToSeconds = 0  # seconds of set "to" timer input
    setPeriodMinutes = 0  # minutes of set period input
    setPeriodSeconds = 0  # second of set period input
    overtimeMinutes = 0  # overtime minutes
    overtimeSeconds = 0  # overtime seconds
    toCheck = False  # if "to" checked
    timerRunning = False  # is timer running
    overtime = False  # is overtime



class Settings(object):
    writeFile = True
    writeXml = False
    writeObs = False
    stopWatch = True
    timer = False
    currentTime = False
    tenth = False
    halfTime = False
    prehalf = None
    defaultSpeed = 1000
    defaultTenthSpeed = 94
    speed = defaultSpeed
    tenthSpeed = defaultTenthSpeed
    timerPresetEnable = False
    timerPresetValue = None
    customSpeed = False
    customTenthSpeed = False


class Play(object):
    player = QMediaPlayer(None)
    playEnabled = False
    playPath = ""
    playVolume = 100


# ------------------------------------ T H R E A D ---------------------------------

# class setObsTextThread(QThread):
#
#     errorSignal = Signal(str)
#
#     def __init__(self, source, text):
#         QThread.__init__(self)
#
#         self.source = source
#         self.text = text
#         #print("Create thread")
#
#     def run(self):
#         self.errorSignal.connect(window.obs_connection_lost)
#         #print("Starting Thread")
#         try:
#             #print("thread try block")
#             window.obs.call(requests.SetSourceSettings(self.source, {'text': self.text}))
#         except:
#             self.errorSignal.emit("error")

# ----------------------------------------------------------------------------------




class Obs(object):
    connected = False
    host = "localhost"
    port = 4444
    password = ""
    inGameScene = ""
    inHalfTimeScene = ""
    clockSource = ""
    overTimeSource = ""
    halfTimeSource = ""
    homeSource = ""
    awaySource = ""
    homeGraphicSource = ""
    awayGraphicSource = ""
    homeScoreSource = ""
    periodSource = ""
    awayScoreSource = ""
    homeGraphicFile = ""
    awayGraphicFile = ""
    send = False
    errlist = []

class Dynamic(object):
    halfOn = False
    connectObsButtonOn = False
    connectObsLabelOn = False
    startServerOn = False


class Files(object):
    outDir = "output"
    iniFile = "config.ini"
    xmlFile = "output.xml"
    homeFile = "home.txt"
    awayFile = "away.txt"
    homeScoreFile = "homescore.txt"
    awayScoreFile = "awayscore.txt"
    timeFile = "time.txt"
    overTimeFile = "overtime.txt"
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
    overTimePath = os.path.join(outPath, overTimeFile)
    periodPath = os.path.join(outPath, periodFile)
    halfTimePath = os.path.join(outPath, halfTimeFile)
    try:
        os.mkdir(outPath)
    except FileExistsError:
        pass

    # @staticmethod
    # def save(filepath, value):
    #     if Settings.writeFile:
    #         file = open(filepath, "w")
    #         file.write(value)
    #         file.close()
    #     if Settings.writeXml:
    #         Files.write_xml()
    #     if Obs.connected:
    #         try:
    #             if filepath == Files.homePath:
    #                 window.obs.call(requests.SetSourceSettings(Obs.homeSource, {'text': value}))
    #             elif filepath == Files.awayPath:
    #                 window.obs.call(requests.SetSourceSettings(Obs.awaySource, {'text': value}))
    #             elif filepath == Files.homeScorePath:
    #                 window.obs.call(requests.SetSourceSettings(Obs.homeScoreSource, {'text': value}))
    #             elif filepath == Files.awayScorePath:
    #                 window.obs.call(requests.SetSourceSettings(Obs.awayScoreSource, {'text': value}))
    #             elif filepath == Files.periodPath:
    #                 window.obs.call(requests.SetSourceSettings(Obs.periodSource, {'text': value}))
    #             elif filepath == Files.timePath:
    #                 threading.Thread(target=window.set_time_obs, args=(Obs.clockSource, value)).start()
    #                 #myThread = setObsTextThread(Obs.clockSource, value)
    #                 #myThread.errorSignal.connect(window.obs_connection_lost)
    #                 #print("About to start")
    #                 #myThread.start()
    #             elif filepath == Files.overTimePath:
    #                 threading.Thread(target=window.set_time_obs, args=(Obs.overTimeSource, value)).start()
    #             elif filepath == Files.halfTimePath:
    #                 threading.Thread(target=window.set_time_obs, args=(Obs.halfTimeSource, value)).start()
    #         except:
    #             window.error_box("OBS connection", "Connection to OBS has been lost!")
    #             Obs.connected = False
    #             window.ui.ConnectObs_Label.setText("Not Connected")
    #
    # @staticmethod
    # def save_all():
    #     if Settings.writeFile:
    #         for x, y in zip([Files.homePath, Files.awayPath, Files.homeScorePath, Files.awayScorePath,
    #                          Files.timePath, Files.overTimePath, Files.periodPath, Files.halfTimePath],
    #                         [ScoreBoard.homeTeam, ScoreBoard.awayTeam, ScoreBoard.homeScore, ScoreBoard.awayScore,
    #                          ScoreBoard.timerString, ScoreBoard.overTimeString, ScoreBoard.period,
    #                          ScoreBoard.halfTimeString]):
    #             f = open(x, "w")
    #             f.write(str(y))
    #             f.close()
    #     if Settings.writeXml:
    #         Files.write_xml()
    #
    # @staticmethod
    # def write_xml():
    #     ScoreBoard.nr = + 1
    #     file = QFile(Files.xmlPath)
    #     file.open(QIODevice.WriteOnly)
    #     xml = QXmlStreamWriter(file)
    #     xml.setAutoFormatting(True)
    #     xml.writeStartDocument()
    #     xml.writeStartElement("items")
    #     xml.writeTextElement("timestamp", str(ScoreBoard.nr))
    #     xml.writeTextElement("HomeScore", str(ScoreBoard.homeScore))
    #     xml.writeTextElement("AwayScore", str(ScoreBoard.awayScore))
    #     xml.writeTextElement("HomeName", ScoreBoard.homeTeam)
    #     xml.writeTextElement("AwayName", ScoreBoard.awayTeam)
    #     xml.writeTextElement("Period", str(ScoreBoard.period))
    #     xml.writeTextElement("Clock", ScoreBoard.timerString)
    #     xml.writeTextElement("OverTimeClock", ScoreBoard.overTimeString)
    #     xml.writeTextElement("HlafTimeClock", ScoreBoard.halfTimeString)
    #     xml.writeEndElement()
    #     xml.writeEndDocument()
    #     file.close()


def get_sec_from_time():
    return ScoreBoard.minutes * 60 + ScoreBoard.seconds


def get_sec_from_settime():
    return ScoreBoard.setMinutes * 60 + ScoreBoard.setSeconds


def get_sec_from_totime():
    return ScoreBoard.setToMinutes * 60 + ScoreBoard.setToSeconds


def get_sec_from_period():
    return ScoreBoard.setPeriodMinutes * 60 + ScoreBoard.setPeriodSeconds


def get_sec_from_end_period():
    return ScoreBoard.period * ScoreBoard.totalSetPeriodSec


def get_sec_from_start_period():
    return (ScoreBoard.period - 1) * ScoreBoard.totalSetPeriodSec


def get_sec_from_current_period():
    return ScoreBoard.totalTimeSec - ScoreBoard.startPeriodsec


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.error = QtWidgets.QCheckBox(self)
        self.error.setChecked(False)
        self.error.setHidden(True)
        #self.sig = Signal(str)
        #self.myThread = None
        self.obs = obsws()
        self.timer = QTimer(self)
        self.translator = QTranslator()
        self.translator.load('mainwindow_pl_PL')
        app.installTranslator(self.translator)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.labelStatus = QLabel(self)
        self.connectObsStatus = QLabel(self)
        self.remoteConnectStatus = QLabel(self)
        self.remoteLabelStatus = QLabel(self)
        self.ui.statusbar.addWidget(self.labelStatus,1)
        self.ui.statusbar.addWidget(self.connectObsStatus,2)
        self.ui.statusbar.addWidget(self.remoteLabelStatus,1)
        self.ui.statusbar.addWidget(self.remoteConnectStatus,2)
        # Language.currentTextError = Language.iniTextError
        Language.retranslateUi()
        self.ui.retranslateUi(self)
        self.labelStatus.setText(Language.ConnectionToOBS)
        self.connectObsStatus.setText(self.ui.ConnectObs_Label.text())
        self.remoteLabelStatus.setText(Language.RemoteLabelStatus)
        self.remoteConnectStatus.setText(Language.NotConnected)
        self.ui.actionPolski.setChecked(True)
        self.start()

    def start(self):
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
        self.ui.ResetScore_Button.clicked.connect(self.on_reset_score)
        self.ui.Swap_Button.clicked.connect(self.on_swap_button)
        self.ui.To_Checkbox.stateChanged.connect(self.on_to_check)
        self.ui.HalfTime_Button.clicked.connect(self.on_half_time)
        self.ui.StopSound_Button.clicked.connect(self.play_sound)

        # -------------------- s e t t i n g s ---------------------------------

        self.ui.StopWatch_Radio.clicked.connect(self.on_stopwatch)
        self.ui.Timer_Radio.clicked.connect(self.on_timer)
        self.ui.CurrentTime_Radio.clicked.connect(self.on_current_time)
        self.ui.Always_on_top_Checkbox.stateChanged.connect(self.on_always_on_top)
        self.ui.OneTenth_Checkbox.stateChanged.connect(self.on_tenth)
        self.ui.MicroSpeed_CheckBox.stateChanged.connect(self.on_ten_speed)
        self.ui.Speed_CheckBox.stateChanged.connect(self.on_speed)
        self.ui.MicroSpeed_Input.valueChanged.connect(self.on_ten_input)
        self.ui.Speed_Input.valueChanged.connect(self.on_speed_input)
        self.ui.SpeedHelp_Button.clicked.connect(self.speed_help)
        self.ui.TimerPreset_Checkbox.stateChanged.connect(self.on_timer_preset)
        self.ui.TenM_Radio.toggled.connect(self.on_ten_radio)
        self.ui.TwelveM_Radio.toggled.connect(self.on_twelve_radio)
        self.ui.FifteenM_Radio.toggled.connect(self.on_fifteen_radio)
        self.ui.TwentyM_Radio.toggled.connect(self.on_twenty_radio)
        self.ui.ThirtyM_Radio.toggled.connect(self.on_thirty_radio)
        self.ui.FortyFiveM_Radio.toggled.connect(self.on_fortyfive_radio)
        self.ui.Use_Files_CheckBox.stateChanged.connect(self.on_use_files)
        self.ui.Use_Xml_CheckBox.stateChanged.connect(self.on_use_xml)

        # ----------------------- P L A Y ------------------------------------------

        self.ui.PlaySound_Checkbox.stateChanged.connect(self.on_play)
        self.ui.BrowseFile_Button.clicked.connect(self.on_play_browse)
        self.ui.BrowseFile_Input.editingFinished.connect(self.on_play_input)
        self.ui.TestSound_Button.clicked.connect(self.play_sound)
        self.ui.Volume_Slider.valueChanged.connect(self.on_volume)

        # ------------------------ O B S -------------------------------------------

        self.ui.ConnectObs_Button.clicked.connect(self.on_obs_button)
        self.ui.InGameScene_comboBox.currentIndexChanged[str].connect(self.obs_in_game_scene_set)
        self.ui.HalfTimeScene_comboBox.currentIndexChanged[str].connect(self.obs_half_time_scene_set)
        self.ui.ClockSource_comboBox.currentIndexChanged[str].connect(self.obs_clock_source_set)
        self.ui.OverTimeClockSource_comboBox.currentIndexChanged[str].connect(self.obs_overtime_clock_source_set)
        self.ui.HalfTimeClockSource_comboBox.currentIndexChanged[str].connect(self.obs_halftime_clock_source_set)
        self.ui.HomeSource_comboBox.currentIndexChanged[str].connect(self.obs_home_source_set)
        self.ui.AwaySource_comboBox.currentIndexChanged[str].connect(self.obs_away_source_set)
        self.ui.HomeScoreSource_comboBox.currentIndexChanged[str].connect(self.obs_home_score_source_set)
        self.ui.AwayScoreSource_comboBox.currentIndexChanged[str].connect(self.obs_away_score_source_set)
        self.ui.PeriodSource_comboBox.currentIndexChanged[str].connect(self.obs_period_source_set)
        self.ui.HomeGraphicSource_comboBox.currentIndexChanged[str].connect(self.obs_home_graphics_source_set)
        self.ui.AwayGraphicSource_comboBox.currentIndexChanged[str].connect(self.obs_away_graphics_source_set)
        self.ui.HomeGraphicFile_toolButton.clicked.connect(self.on_home_graphics_browse)
        self.ui.AwayGraphicFile_toolButton.clicked.connect(self.on_away_graphics_browse)
        self.error.stateChanged.connect(self.obs_connection_lost)
        self.ui.LoadObs_Button.clicked.connect(self.on_load_obs)
        self.ui.SaveObs_Button.clicked.connect(self.on_save_obs)

        # ----------------------------- R E M O T E  -----------------------------------

        self.ui.Remote_Button.clicked.connect(self.on_remote_button)

        self.save_all()

    # --------------------------------- S A V E ------------------------------------

    def save(self, filepath, value):
        if Settings.writeFile:
            file = open(filepath, "w")
            file.write(value)
            file.close()
        if Settings.writeXml:
            self.write_xml()
        if Obs.connected:
            try:
                if filepath == Files.homePath:
                    self.obs.call(requests.SetSourceSettings(Obs.homeSource, {'text': value}))
                elif filepath == Files.awayPath:
                    self.obs.call(requests.SetSourceSettings(Obs.awaySource, {'text': value}))
                elif filepath == Files.homeScorePath:
                    self.obs.call(requests.SetSourceSettings(Obs.homeScoreSource, {'text': value}))
                elif filepath == Files.awayScorePath:
                    self.obs.call(requests.SetSourceSettings(Obs.awayScoreSource, {'text': value}))
                elif filepath == Files.periodPath:
                    self.obs.call(requests.SetSourceSettings(Obs.periodSource, {'text': value}))
                elif filepath == Files.timePath:
                    threading.Thread(target=self.set_time_obs, args=(Obs.clockSource, value)).start()

                    #print("Startthread")
                    #setObsTextThread(Obs.clockSource, value).start()
                    #print("Stopthread")
                    #self.myThread.errorSignal.connect(window.obs_connection_lost)
                    #print("About to start")
                    #self.myThread.start()
                elif filepath == Files.overTimePath:
                    threading.Thread(target=self.set_time_obs, args=(Obs.overTimeSource, value)).start()
                elif filepath == Files.halfTimePath:
                    threading.Thread(target=self.set_time_obs, args=(Obs.halfTimeSource, value)).start()
            except:
                window.error_box(Language.ConnectionToOBS, Language.ConnectionOBSLost)
                self.obs_disconnect()
                #Obs.connected = False
                #window.ui.ConnectObs_Label.setText("Not Connected")

    def save_all(self):
        if Settings.writeFile:
            for x, y in zip([Files.homePath, Files.awayPath, Files.homeScorePath, Files.awayScorePath,
                             Files.timePath, Files.overTimePath, Files.periodPath, Files.halfTimePath],
                            [ScoreBoard.homeTeam, ScoreBoard.awayTeam, ScoreBoard.homeScore, ScoreBoard.awayScore,
                             ScoreBoard.timerString, ScoreBoard.overTimeString, ScoreBoard.period,
                             ScoreBoard.halfTimeString]):
                f = open(x, "w")
                f.write(str(y))
                f.close()
        if Settings.writeXml:
            Files.write_xml()


    def write_xml(self):
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
        xml.writeTextElement("OverTimeClock", ScoreBoard.overTimeString)
        xml.writeTextElement("HlafTimeClock", ScoreBoard.halfTimeString)
        xml.writeEndElement()
        xml.writeEndDocument()
        file.close()

    # ------------------------------- T I M E R ------------------------------------

    def start_timer(self):
        if not ScoreBoard.timerRunning:
            if Settings.timer and ScoreBoard.totalTimeSec == 0:
                Language.currentTextError = Language.timerError
                self.ui.Error_Text.setText(Language.currentTextError)
                QTimer.singleShot(3000, self.clear_error)
                return
            if Settings.tenth and ScoreBoard.totalTimeSec <= 60 and Settings.timer:
                speed = Settings.tenthSpeed if Settings.customTenthSpeed else Settings.defaultTenthSpeed
            else:
                speed = Settings.speed if Settings.customSpeed else Settings.defaultSpeed
            print("speed = ", speed)
            self.timer.start(speed)
            ScoreBoard.timerRunning = True
            self.ui.Start_Button.setText("STOP")
            self.timer_enable(False)
            self.settings_start_enable(True)
            ScoreBoard.first = True
        else:
            self.timer.stop()
            ScoreBoard.timerRunning = False
            self.ui.Start_Button.setText("START")
            if Settings.stopWatch:
                self.stopwatch_enable(True)
            elif Settings.timer:
                self.timer_enable(True)
                if Play.playEnabled:
                    self.play_sound()

    def tick(self):
        if not (Settings.tenth and Settings.timer and ScoreBoard.totalTimeSec <= 60):
            if Settings.currentTime:
                self.set_current_time()
                return
            if Settings.stopWatch and not Settings.halfTime:
                if not ScoreBoard.overtime:
                    ScoreBoard.seconds += 1
                    if ScoreBoard.seconds > 59:
                        ScoreBoard.minutes += 1
                        ScoreBoard.seconds = 0
                    ScoreBoard.totalTimeSec = get_sec_from_time()
                    ScoreBoard.totalPeriodSec = get_sec_from_current_period()
                    self.set_time()
                else:
                    ScoreBoard.overtimeSeconds += 1
                    if ScoreBoard.overtimeSeconds > 59:
                        ScoreBoard.overtimeSeconds = 0
                        ScoreBoard.overtimeMinutes += 1
                    self.set_overtime()
            elif Settings.timer and not Settings.halfTime:
                ScoreBoard.seconds -= 1
                if ScoreBoard.seconds == 0 and ScoreBoard.minutes == 0:
                    self.ui.Start_Button.clicked.emit()
                if ScoreBoard.seconds < 0:
                    if ScoreBoard.minutes >= 0:
                        ScoreBoard.minutes -= 1
                        ScoreBoard.seconds = 59
                    else:
                        self.ui.Start_Button.clicked.emit()
                ScoreBoard.totalTimeSec = get_sec_from_time()
                ScoreBoard.totalTenth = ScoreBoard.totalTimeSec * 10
                self.set_timer_time()
            elif Settings.halfTime:
                ScoreBoard.seconds += 1
                if ScoreBoard.seconds > 59:
                    ScoreBoard.minutes += 1
                    ScoreBoard.seconds = 0
                self.set_halftime()
        else:
            if ScoreBoard.first:
                ScoreBoard.Tenth = ScoreBoard.totalTenth % 10
                ScoreBoard.seconds = ScoreBoard.totalTenth // 10
                ScoreBoard.minutes = 0
                speed = Settings.tenthSpeed if Settings.customTenthSpeed else Settings.defaultTenthSpeed
                print("speed = ", speed)
                self.timer.start(speed)
                ScoreBoard.first = False
            # print("seconds = ", ScoreBoard.seconds, " tenth = ", ScoreBoard.tenth)
            ScoreBoard.tenth -= 1
            if ScoreBoard.tenth < 0:
                ScoreBoard.totalTenth -= 10
                ScoreBoard.seconds -= 1
                ScoreBoard.tenth = 9
            # print("minutes = ", ScoreBoard.minutes, " seconds = ", ScoreBoard.seconds)
            ScoreBoard.totalTimeSec = get_sec_from_time()
            ScoreBoard.totalPeriodSec = get_sec_from_current_period()
            if ScoreBoard.seconds == 0 and ScoreBoard.tenth == 0:
                ScoreBoard.first = True
                self.ui.Start_Button.clicked.emit()
            self.set_tenth_time()

    def settings_set_timer_enable(self, enable):
        self.ui.Seconds_Input.setEnabled(enable)
        self.ui.Minutes_Input.setEnabled(enable)

    def settings_set_period_enable(self, enable):
        self.ui.MinutesPeriod_Input.setEnabled(enable)
        self.ui.SecondsPeriod_Input.setEnabled(enable)

    def settings_up_period_enable(self, enable):
        self.ui.PeriodDOWN_Button.setEnabled(enable)
        self.ui.PeriodUP_Button.setEnabled(enable)

    def settings_to_enable(self, enable):
        if enable:
            self.ui.To_Checkbox.setEnabled(True)
            if self.ui.To_Checkbox.isChecked():
                self.ui.SecondsTo_Input.setEnabled(True)
                self.ui.MinutesTo_Input.setEnabled(True)
        else:
            self.ui.To_Checkbox.setEnabled(False)
            self.ui.SecondsTo_Input.setEnabled(False)
            self.ui.MinutesTo_Input.setEnabled(False)

    def settings_start_enable(self, enable):  # start button enable
        self.ui.Start_Button.setEnabled(enable)

    def settings_reset_enable(self, enable):
        self.ui.ResetTimer_Button.setEnabled(enable)

    def stopwatch_enable(self, enable):
        self.settings_set_timer_enable(enable)
        self.settings_to_enable(enable)
        self.settings_set_period_enable(enable)
        self.settings_up_period_enable(enable)
        self.settings_start_enable(enable)
        self.settings_reset_enable(enable)

    def timer_enable(self, enable):  # enable, disable widgets when timer is active
        self.settings_set_timer_enable(enable)
        self.settings_to_enable(not enable)
        self.settings_set_period_enable(enable)
        self.settings_up_period_enable(enable)
        self.settings_start_enable(enable)
        self.settings_reset_enable(enable)

    def current_time_enable(self, enable):  # disable widgets when current time displayed
        self.stopwatch_enable(enable)

    # ---------------------------- T I M E  I N P U T ------------------------------

    def on_period_input(self):
        if not ScoreBoard.timerRunning:
            ScoreBoard.setPeriodMinutes = self.ui.MinutesPeriod_Input.value()
            ScoreBoard.setPeriodSeconds = self.ui.SecondsPeriod_Input.value()
            ScoreBoard.totalSetPeriodSec = get_sec_from_period()
            ScoreBoard.startPeriodsec = get_sec_from_start_period()
            ScoreBoard.stopPeriodsec = get_sec_from_end_period()
            self.update_period_time()
            self.update_on_period(None)

    def on_time_input(self):
        ScoreBoard.setMinutes = self.ui.Minutes_Input.value()
        ScoreBoard.setSeconds = self.ui.Seconds_Input.value()
        ScoreBoard.totalSetTimeSec = get_sec_from_settime()
        ScoreBoard.minutes = ScoreBoard.setMinutes
        ScoreBoard.seconds = ScoreBoard.setSeconds
        ScoreBoard.totalTimeSec = get_sec_from_time()
        ScoreBoard.tenth = 0
        ScoreBoard.totalTenth = ScoreBoard.totalTimeSec * 10
        self.update_period_time()
        self.set_time()

    def set_time(self):
        ScoreBoard.timerString = "{:02d}:{:02d}".format(ScoreBoard.minutes, ScoreBoard.seconds)
        self.ui.Minutes_Input.valueChanged.disconnect()
        self.ui.Seconds_Input.valueChanged.disconnect()
        self.ui.Minutes_Input.setValue(ScoreBoard.minutes)
        self.ui.Seconds_Input.setValue(ScoreBoard.seconds)
        self.ui.Minutes_Input.valueChanged[int].connect(self.on_time_input)
        self.ui.Seconds_Input.valueChanged[int].connect(self.on_time_input)
        self.ui.Clock_Label.setText(ScoreBoard.timerString)
        if Settings.stopWatch:
            self.set_period_time()
        self.save(Files.timePath, ScoreBoard.timerString)
        if ScoreBoard.toCheck and ScoreBoard.timerRunning and ScoreBoard.totalTimeSec == ScoreBoard.totalToSec:
            self.ui.Start_Button.clicked.emit()
            return
        if ScoreBoard.totalTimeSec != 0 and ScoreBoard.totalTimeSec == ScoreBoard.stopPeriodsec:
            # print ("total = ", ScoreBoard.totalTimeSec, " periodEnd = ", ScoreBoard.stopPeriodsec)
            ScoreBoard.overtime = True

    def set_halftime(self):
        ScoreBoard.halfTimeString = "{:02d}:{:02d}".format(ScoreBoard.minutes, ScoreBoard.seconds)
        self.ui.HalfTimeClock_Label.setText(ScoreBoard.halfTimeString)
        self.save(Files.halfTimePath, ScoreBoard.halfTimeString)

    def set_timer_time(self):
        ScoreBoard.timerString = "{:02d}:{:02d}".format(ScoreBoard.minutes, ScoreBoard.seconds)
        self.ui.Minutes_Input.valueChanged.disconnect()
        self.ui.Seconds_Input.valueChanged.disconnect()
        self.ui.Minutes_Input.setValue(ScoreBoard.minutes)
        self.ui.Seconds_Input.setValue(ScoreBoard.seconds)
        self.ui.Minutes_Input.valueChanged[int].connect(self.on_time_input)
        self.ui.Seconds_Input.valueChanged[int].connect(self.on_time_input)
        self.ui.Clock_Label.setText(ScoreBoard.timerString)
        self.save(Files.timePath, ScoreBoard.timerString)

    def set_tenth_time(self):
        ScoreBoard.timerString = "{:02d}.{:01d}".format(ScoreBoard.seconds, ScoreBoard.tenth)
        Obs.send = False if ScoreBoard.tenth % 2 else True
        self.ui.Clock_Label.setText(ScoreBoard.timerString)
        if ScoreBoard.tenth == 9:
            self.ui.Minutes_Input.valueChanged.disconnect()
            self.ui.Seconds_Input.valueChanged.disconnect()
            self.ui.Minutes_Input.setValue(ScoreBoard.minutes)
            self.ui.Seconds_Input.setValue(ScoreBoard.seconds)
            self.ui.Minutes_Input.valueChanged[int].connect(self.on_time_input)
            self.ui.Seconds_Input.valueChanged[int].connect(self.on_time_input)
            # perseconds = get_sec_from_current_period()
            # ScoreBoard.periodTimeString = "{:02d}:{:02d}".format(0, perseconds)
            # self.ui.PeriodClock_Label.setText(ScoreBoard.periodTimeString)
        self.save(Files.timePath, ScoreBoard.timerString)

    def set_overtime(self):
        ScoreBoard.overTimeString = "{:02d}:{:02d}".format(ScoreBoard.overtimeMinutes, ScoreBoard.overtimeSeconds)
        self.ui.OverTimeClock_Label.setText(ScoreBoard.overTimeString)
        self.save(Files.overTimePath, ScoreBoard.overTimeString)

    def set_current_time(self):
        ScoreBoard.timerString = datetime.now().strftime("%H:%M:%S")
        self.ui.Clock_Label.setText(ScoreBoard.timerString)
        self.save(Files.timePath, ScoreBoard.timerString)

    # ------------------------- H O M E ----------------------------------------------

    def on_home_change(self):
        ScoreBoard.homeTeam = self.ui.HomeName_Input.text()

    def on_home_down(self):
        if ScoreBoard.homeScore > 0:
            ScoreBoard.homeScore -= 1
            self.ui.HomeScore_Label.setText(str(ScoreBoard.homeScore))
            self.save(Files.homeScorePath, str(ScoreBoard.homeScore))

    def on_home_up(self):
        ScoreBoard.homeScore += 1
        self.ui.HomeScore_Label.setText(str(ScoreBoard.homeScore))
        self.save(Files.homeScorePath, str(ScoreBoard.homeScore))

    def on_home_up2(self):
        ScoreBoard.homeScore += 2
        self.ui.HomeScore_Label.setText(str(ScoreBoard.homeScore))
        self.save(Files.homeScorePath, str(ScoreBoard.homeScore))

    # ------------------------- A W A Y -----------------------------------------

    def on_away_change(self):
        ScoreBoard.awayTeam = self.ui.AwayName_Input.text()

    def on_away_down(self):
        if ScoreBoard.awayScore > 0:
            ScoreBoard.awayScore -= 1
            self.ui.AwayScore_Label.setText(str(ScoreBoard.awayScore))
            self.save(Files.awayScorePath, str(ScoreBoard.awayScore))

    def on_away_up(self):
        ScoreBoard.awayScore += 1
        self.ui.AwayScore_Label.setText(str(ScoreBoard.awayScore))
        self.save(Files.awayScorePath, str(ScoreBoard.awayScore))

    def on_away_up2(self):
        ScoreBoard.awayScore += 2
        self.ui.AwayScore_Label.setText(str(ScoreBoard.awayScore))
        self.save(Files.awayScorePath, str(ScoreBoard.awayScore))

    # ------------------------- P E R I O D -------------------------------------

    def on_period_up(self):
        print("on period up")
        self.update_on_period(True)

    def on_period_down(self):
        print("on period down")
        self.update_on_period(False)

    def update_down_period(self):
        self.ui.Period_Label.setText(str(ScoreBoard.period))
        ScoreBoard.startPeriodsec = get_sec_from_start_period()
        ScoreBoard.stopPeriodsec = get_sec_from_end_period()
        self.set_period_time()

    def update_period_time(self):
        if ScoreBoard.totalSetPeriodSec != 0 and Settings.stopWatch:
            if ScoreBoard.totalSetTimeSec >= ScoreBoard.stopPeriodsec:
                print("period wyzej")
                ScoreBoard.period = ScoreBoard.totalSetTimeSec // ScoreBoard.totalSetPeriodSec + 1
                self.update_on_period(None)

            elif ScoreBoard.totalSetTimeSec < ScoreBoard.startPeriodsec:
                print("period nizej")
                ScoreBoard.period = ScoreBoard.totalSetTimeSec // ScoreBoard.totalSetPeriodSec + 1
                self.update_down_period()

    def set_period_time(self):
        perminute = get_sec_from_current_period() // 60
        perseconds = get_sec_from_current_period() % 60
        ScoreBoard.periodTimeString = "{:02d}:{:02d}".format(perminute, perseconds)
        self.ui.PeriodClock_Label.setText(ScoreBoard.periodTimeString)

    def update_on_period(self, where):
        print("update on period :", where)
        if not ScoreBoard.timerRunning or Settings.currentTime:
            self.reset_overtime()
            if where is None:
                ScoreBoard.period += 0
            elif where:
                ScoreBoard.period += 1
            else:
                if ScoreBoard.period > 1:
                    ScoreBoard.period -= 1
            self.ui.Period_Label.setText(str(ScoreBoard.period))
            if Settings.timer or Settings.currentTime:
                self.save(Files.periodPath, str(ScoreBoard.period))
                return
            ScoreBoard.totalSetPeriodSec = get_sec_from_period()
            ScoreBoard.startPeriodsec = get_sec_from_start_period()
            ScoreBoard.stopPeriodsec = get_sec_from_end_period()
            print("totalperoid = ", ScoreBoard.totalSetPeriodSec, " startperiod = ", ScoreBoard.startPeriodsec,
                  "  stopperiod = ", ScoreBoard.stopPeriodsec)
            if ScoreBoard.totalSetPeriodSec == 0:
                return
            if where is not None:
                ScoreBoard.minutes = ScoreBoard.startPeriodsec // 60
                ScoreBoard.seconds = ScoreBoard.startPeriodsec % 60
            ScoreBoard.totalSetTimeSec = get_sec_from_settime()
            ScoreBoard.totalTimeSec = get_sec_from_time()
            print("min= ", ScoreBoard.minutes, " sec= ", ScoreBoard.seconds)
            self.set_time()
        else:
            Language.currentTextError = Language.periodError
            self.ui.Error_Text.setText(Language.currentTextError)
            QTimer.singleShot(3000, self.clear_error)

    # -------------------------- T O   I N P U T ---------------------------------

    def on_to_check(self):
        if self.ui.To_Checkbox.isChecked():
            self.ui.MinutesTo_Input.setEnabled(True)
            self.ui.SecondsTo_Input.setEnabled(True)
            ScoreBoard.toCheck = True
        else:
            self.ui.MinutesTo_Input.setEnabled(False)
            self.ui.SecondsTo_Input.setEnabled(False)
            ScoreBoard.toCheck = False

    def on_to_input(self):
        ScoreBoard.setToMinutes = self.ui.MinutesTo_Input.value()
        ScoreBoard.setToSeconds = self.ui.SecondsTo_Input.value()
        ScoreBoard.totalToSec = get_sec_from_totime()

    # -------------------------- B U T T O N S ------------------------------------

    def on_update_team(self):
        self.save(Files.homePath, ScoreBoard.homeTeam)
        self.save(Files.awayPath, ScoreBoard.awayTeam)

    def on_reset_timer(self, period=1):
        if not period:
            period = 1
        print("period = ", period)
        ScoreBoard.period = period
        ScoreBoard.totalSetPeriodSec = get_sec_from_period()
        ScoreBoard.startPeriodsec = get_sec_from_start_period()
        ScoreBoard.stopPeriodsec = get_sec_from_end_period()
        if Settings.stopWatch or Settings.currentTime:
            ScoreBoard.minutes = ScoreBoard.startPeriodsec // 60
            ScoreBoard.seconds = ScoreBoard.startPeriodsec % 60
            ScoreBoard.setMinutes = ScoreBoard.minutes
            ScoreBoard.setSeconds = ScoreBoard.seconds
        elif Settings.timer:
            if Settings.timerPresetEnable:
                self.ui.MinutesPeriod_Input.setValue(Settings.timerPresetValue)
                self.ui.SecondsPeriod_Input.setValue(0)
            ScoreBoard.minutes = ScoreBoard.stopPeriodsec // 60
            ScoreBoard.seconds = ScoreBoard.stopPeriodsec % 60
            ScoreBoard.setMinutes = ScoreBoard.minutes
            ScoreBoard.setSeconds = ScoreBoard.seconds
        self.reset_overtime()
        ScoreBoard.first = True
        ScoreBoard.totalTimeSec = get_sec_from_time()
        ScoreBoard.totalSetTimeSec = get_sec_from_settime()
        ScoreBoard.totalCurrentPeriodSec = get_sec_from_current_period()
        self.ui.Period_Label.setText(str(ScoreBoard.period))
        self.set_period_time()
        self.set_input_time()
        self.set_time()

    def on_reset_score(self):
        ScoreBoard.awayScore = 0
        ScoreBoard.homeScore = 0
        self.ui.AwayScore_Label.setText(str(ScoreBoard.awayScore))
        self.ui.HomeScore_Label.setText(str(ScoreBoard.homeScore))
        self.save(Files.awayScorePath, str(ScoreBoard.awayScore))
        self.save(Files.homeScorePath, str(ScoreBoard.homeScore))

    def on_swap_button(self):
        temp = ScoreBoard.homeTeam
        ScoreBoard.homeTeam = ScoreBoard.awayTeam
        ScoreBoard.awayTeam = temp
        temp = ScoreBoard.homeScore
        ScoreBoard.homeScore = ScoreBoard.awayScore
        ScoreBoard.awayScore = temp
        self.on_update_team()
        self.ui.AwayName_Input.setText(ScoreBoard.awayTeam)
        self.ui.HomeName_Input.setText(ScoreBoard.homeTeam)
        self.ui.AwayScore_Label.setText(str(ScoreBoard.awayScore))
        self.ui.HomeScore_Label.setText(str(ScoreBoard.homeScore))
        self.save(Files.awayScorePath, str(ScoreBoard.awayScore))
        self.save(Files.homeScorePath, str(ScoreBoard.homeScore))

    def on_half_time(self):
        if ScoreBoard.timerRunning:
            self.start_timer()
        if not Settings.halfTime:
            Settings.halfTime = True
            self.on_period_up()
            ScoreBoard.minutes = 0
            ScoreBoard.seconds = 0
            Language.HalfTimeText = Language.HalfActive
            self.ui.HalfTime_Button.setText(Language.HalfTimeText)
            Dynamic.halfOn = True
            self.start_timer()
            if Obs.inHalfTimeScene != "":
                try:
                    self.obs.call(requests.SetCurrentScene(Obs.inHalfTimeScene))
                except:
                    pass

        else:
            Settings.halfTime = False
            if Obs.inGameScene != "":
                try:
                    self.obs.call(requests.SetCurrentScene(Obs.inGameScene))
                except:
                    pass
            self.ui.HalfTimeClock_Label.setText("00:00")
            self.save(Files.halfTimePath, "00:00")
            Language.HalfTimeText = Language.Half
            self.ui.HalfTime_Button.setText(Language.HalfTimeText)
            Dynamic.halfOn = False
            self.on_reset_timer(ScoreBoard.period)

    # ------------------------ S E T T I N G S ------------------------------------

    def on_use_files(self):
        if self.ui.Use_Files_CheckBox.isChecked():
            Settings.writeFile = True
        else:
            Settings.writeFile = False

    def on_use_xml(self):
        if self.ui.Use_Xml_CheckBox.isChecked():
            Settings.writeXml = True
        else:
            Settings.writeXml = False

    def on_stopwatch(self):
        self.ui.Clock_Label.setFont(QFont("Arial", 60))
        if ScoreBoard.timerRunning:
            self.start_timer()
        Settings.stopWatch = True
        Settings.timer = False
        Settings.currentTime = False
        self.on_reset_timer()
        self.stopwatch_enable(True)
        self.update_period_time()

    def on_timer(self):
        self.ui.Clock_Label.setFont(QFont("Arial", 60))
        if ScoreBoard.timerRunning:
            self.start_timer()
        Settings.stopWatch = False
        Settings.timer = True
        Settings.currentTime = False
        self.on_reset_timer()
        self.timer_enable(True)

    def on_current_time(self):
        self.ui.Clock_Label.setFont(QFont("Arial", 36))
        Settings.stopWatch = False
        Settings.timer = False
        Settings.currentTime = True
        self.current_time_enable(False)
        if ScoreBoard.timerRunning:
            self.start_timer()
        print("robię reset")
        self.on_reset_timer()
        self.start_timer()
        self.settings_up_period_enable(True)

    def on_always_on_top(self):
        if self.ui.Always_on_top_Checkbox.isChecked():
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
        self.show()

    def on_tenth(self):
        if self.ui.OneTenth_Checkbox.isChecked():
            Settings.tenth = True
        else:
            Settings.tenth = False

    def on_timer_preset(self):
        if self.ui.TimerPreset_Checkbox.isChecked():
            self.timer_presets_enable(True)
            if self.ui.TenM_Radio.isChecked():
                Settings.timerPresetValue = 10
            elif self.ui.FifteenM_Radio.isChecked():
                Settings.timerPresetValue = 15
            elif self.ui.TwelveM_Radio.isChecked():
                Settings.timerPresetValue = 12
            elif self.ui.TwentyM_Radio.isChecked():
                Settings.timerPresetValue = 20
            elif self.ui.ThirtyM_Radio.isChecked():
                Settings.timerPresetValue = 30
            elif self.ui.FortyFiveM_Radio.isChecked():
                Settings.timerPresetValue = 45
            print(Settings.timerPresetValue)
            if not ScoreBoard.timerRunning:
                self.on_reset_timer()
        else:
            self.timer_presets_enable(False)
            Settings.timerPresetValue = None

    def on_ten_radio(self):
        if self.ui.TenM_Radio.isChecked():
            Settings.timerPresetValue = 10
        if not ScoreBoard.timerRunning:
            self.on_reset_timer()

    def on_fifteen_radio(self):
        if self.ui.FifteenM_Radio.isChecked():
            Settings.timerPresetValue = 15
        if not ScoreBoard.timerRunning:
            self.on_reset_timer()

    def on_twelve_radio(self):
        if self.ui.TwelveM_Radio.isChecked():
            Settings.timerPresetValue = 12
        if not ScoreBoard.timerRunning:
            self.on_reset_timer()

    def on_twenty_radio(self):
        if self.ui.TwentyM_Radio.isChecked():
            Settings.timerPresetValue = 20
        if not ScoreBoard.timerRunning:
            self.on_reset_timer()

    def on_thirty_radio(self):
        if self.ui.ThirtyM_Radio.isChecked():
            Settings.timerPresetValue = 30
        if not ScoreBoard.timerRunning:
            self.on_reset_timer()

    def on_fortyfive_radio(self):
        if self.ui.FortyFiveM_Radio.isChecked():
            Settings.timerPresetValue = 45
        if not ScoreBoard.timerRunning:
            self.on_reset_timer()

    def on_ten_speed(self):
        if self.ui.MicroSpeed_CheckBox.isChecked():
            Settings.customTenthSpeed = True
            Settings.tenthSpeed = self.ui.MicroSpeed_Input.value()
        else:
            Settings.customTenthSpeed = False
            Settings.tenthSpeed = Settings.defaultTenthSpeed

    def on_speed(self):
        if self.ui.Speed_CheckBox.isChecked():
            Settings.customSpeed = True
            Settings.speed = self.ui.Speed_Input.value()
        else:
            Settings.customSpeed = False
            Settings.speed = Settings.defaultSpeed

    def on_ten_input(self):
        if Settings.customTenthSpeed:
            Settings.tenthSpeed = self.ui.MicroSpeed_Input.value()

    def on_speed_input(self):
        if Settings.customSpeed:
            Settings.speed = self.ui.Speed_Input.value()

    def speed_help(self):
        print("message")
        QMessageBox.about(self, Language.SpeedHelp, Language.ExplSpeedHelp)

    # ------------------------------ P L A Y ---------------------------------------

    def on_play(self):
        enable = True if self.ui.PlaySound_Checkbox.isChecked() else False
        self.ui.BrowseFile_Input.setEnabled(enable)
        self.ui.BrowseFile_Button.setEnabled(enable)
        self.ui.TestSound_Button.setEnabled(enable)
        self.ui.Volume_Slider.setEnabled(enable)
        Play.playEnabled = enable

    def on_play_browse(self):
        filename = QFileDialog.getOpenFileName(self, Language.OpenSound, "", Language.SoundFiles)

        path = os.path.abspath(filename[0])
        if os.path.isdir(path):
            path = ""
        print("filename = ", filename)
        print("path = ", path)
        print("filename[0] = ", filename[0])
        Play.playPath = path
        self.ui.BrowseFile_Input.setText(path)

    def on_play_input(self):
        Play.playPath = self.ui.BrowseFile_Input.text()
        print("play text = ", Play.playPath)

    def play_sound(self):
        state = Play.player.state()
        if state == QMediaPlayer.State.PlayingState:
            Play.player.stop()
            print("zatrzymuje")
            return
        if Play.playPath == "":
            print("wychodze")
            return
        print("zaczynam")
        # file = 'over.mp3'
        media = QUrl.fromLocalFile(Play.playPath)
        content = QMediaContent(media)
        Play.player.setMedia(content)
        Play.player.setVolume(Play.playVolume)
        Play.player.stateChanged.connect(self.state)
        Play.player.play()

    def state(self, state):
        if state == QMediaPlayer.State.PlayingState:
            self.ui.StopSound_Button.setHidden(False)
        elif state == QMediaPlayer.State.StoppedState:
            self.ui.StopSound_Button.setHidden(True)
        print(state)

    def on_volume(self, volume):
        self.ui.VolumeVal_Label.setText(str(volume))
        Play.player.setVolume(volume)
        Play.playVolume = volume

    # -------------------------- L A N G U A G E -----------------------------------

    def english(self):

        self.ui.actionPolski.setChecked(False)
        self.ui.actionEnglish.setChecked(True)
        app.removeTranslator(self.translator)
        self.translator.load('mainwindow_en_GB')
        app.installTranslator(self.translator)
        Language.retranslateUi()
        self.ui.retranslateUi(self)
        self.additional_translate()

    def polski(self):
        self.ui.actionPolski.setChecked(True)
        self.ui.actionEnglish.setChecked(False)
        app.removeTranslator(self.translator)
        self.translator.load('mainwindow_pl_PL')
        app.installTranslator(self.translator)
        Language.retranslateUi()
        self.ui.retranslateUi(self)
        self.additional_translate()

    def additional_translate(self):
        self.labelStatus.setText(Language.ConnectionToOBS)
        self.connectObsStatus.setText(self.ui.ConnectObs_Label.text())
        if Dynamic.halfOn:
            self.ui.HalfTime_Button.setText(Language.HalfActive)
        else:
            self.ui.HalfTime_Button.setText(Language.Half)
        if Dynamic.connectObsButtonOn:
            self.ui.ConnectObs_Button.setText(Language.Disconnect)
        else:
            self.ui.ConnectObs_Button.setText(Language.Connect)
        if Dynamic.connectObsLabelOn:
            self.set_text(Language.Connected)
            #self.ui.ConnectObs_Label.setText(Language.Connected)
        else:
            self.set_text(Language.NotConnected)
            #self.ui.ConnectObs_Label.setText(Language.NotConnected)

    # -------------------------------- O B S ---------------------------------------

    def error_box(self, title, text):
        QMessageBox.critical(self, title, text)

    def set_text(self, text):
        self.ui.ConnectObs_Label.setText(text)
        self.connectObsStatus.setText(text)
        return

    def on_obs_button(self):
        self.set_text(Language.Connecting)
        QTimer.singleShot(50, self.on_obs_button1)

    def on_obs_button1(self):

        self.obs = obsws(Obs.host, Obs.port, Obs.password)
        try:
            self.obs.connect()
            self.ui.ConnectObs_Button.setText(Language.Disconnect)
            self.set_text(Language.Connected)
            Dynamic.connectObsButtonOn = True
            Dynamic.connectObsLabelOn = True
            #self.ui.ConnectObs_Label.setText("Connected")
            #self.connectObsStatus.setText("Connected")
            Obs.connected = True
            self.ui.ConnectObs_Button.clicked.disconnect()
            self.ui.ConnectObs_Button.clicked.connect(self.obs_disconnect)
            scenes = self.obs.call(requests.GetSceneList()).getScenes()
            self.ui.InGameScene_comboBox.addItem("----------")
            self.ui.HalfTimeScene_comboBox.addItem("----------")
            self.ui.ClockSource_comboBox.addItem("----------")
            self.ui.OverTimeClockSource_comboBox.addItem("----------")
            self.ui.HalfTimeClockSource_comboBox.addItem("----------")
            self.ui.HomeSource_comboBox.addItem("----------")
            self.ui.AwaySource_comboBox.addItem("----------")
            self.ui.HomeScoreSource_comboBox.addItem("----------")
            self.ui.AwayScoreSource_comboBox.addItem("----------")
            self.ui.PeriodSource_comboBox.addItem("----------")

            self.ui.HomeGraphicSource_comboBox.addItem("----------")
            self.ui.AwayGraphicSource_comboBox.addItem("----------")

            for scene in scenes:
                self.ui.InGameScene_comboBox.addItem(scene['name'])
                self.ui.HalfTimeScene_comboBox.addItem(scene['name'])
            sources = self.obs.call(requests.GetSourcesList()).getSources()
            for source in sources:
                if source['typeId'].startswith("text"):
                    self.ui.ClockSource_comboBox.addItem(source['name'])
                    self.ui.OverTimeClockSource_comboBox.addItem(source['name'])
                    self.ui.HalfTimeClockSource_comboBox.addItem(source['name'])
                    self.ui.HomeSource_comboBox.addItem(source['name'])
                    self.ui.AwaySource_comboBox.addItem(source['name'])
                    self.ui.HomeScoreSource_comboBox.addItem(source['name'])
                    self.ui.AwayScoreSource_comboBox.addItem(source['name'])
                    self.ui.PeriodSource_comboBox.addItem(source['name'])
                elif source['typeId'].startswith("image"):
                    self.ui.HomeGraphicSource_comboBox.addItem(source['name'])
                    self.ui.AwayGraphicSource_comboBox.addItem(source['name'])
        except:
            self.error_box(Language.ConnectionToOBS, Language.ObsConError)
            self.set_text(Language.Connected)
            #self.ui.ConnectObs_Label.setText("Not Connected")

    def obs_disconnect(self):
        self.obs.disconnect()
        Obs.connected = False
        self.ui.InGameScene_comboBox.clear()
        self.ui.HalfTimeScene_comboBox.clear()
        self.ui.ClockSource_comboBox.clear()
        self.ui.ClockSource_comboBox.clear()
        self.ui.OverTimeClockSource_comboBox.clear()
        self.ui.HalfTimeClockSource_comboBox.clear()
        self.ui.HomeSource_comboBox.clear()
        self.ui.AwaySource_comboBox.clear()
        self.ui.HomeScoreSource_comboBox.clear()
        self.ui.AwayScoreSource_comboBox.clear()
        self.ui.PeriodSource_comboBox.clear()
        self.ui.HomeGraphicSource_comboBox.clear()
        self.ui.AwayGraphicSource_comboBox.clear()
        self.ui.ConnectObs_Button.setText(Language.Connect)
        self.set_text(Language.NotConnected)
        Dynamic.connectObsButtonOn = False
        Dynamic.connectObsLabelOn = False
        #self.ui.ConnectObs_Label.setText(QCoreApplication.translate("MainWindow", "Not Connected"))
        self.ui.ConnectObs_Button.clicked.disconnect()
        self.ui.ConnectObs_Button.clicked.connect(self.on_obs_button)


    def obs_clock_source_set(self, source):
        if int(self.ui.ClockSource_comboBox.currentIndex()) == 0:
            Obs.clockSource = ""
        else:
            Obs.clockSource = source

    def obs_overtime_clock_source_set(self, source):
        if int(self.ui.OverTimeClockSource_comboBox.currentIndex()) == 0:
            Obs.overTimeSource = ""
        else:
            Obs.overTimeSource = source

    def obs_halftime_clock_source_set(self, source):
        if int(self.ui.HalfTimeClockSource_comboBox.currentIndex()) == 0:
            Obs.halfTimeSource = ""
        else:
            Obs.halfTimeSource = source

    def obs_home_source_set(self, source):
        if int(self.ui.HomeSource_comboBox.currentIndex()) == 0:
            Obs.homeSource = ""
        else:
            Obs.homeSource = source

    def obs_away_source_set(self, source):
        if int(self.ui.AwaySource_comboBox.currentIndex()) == 0:
            Obs.awaySource = ""
        else:
            Obs.awaySource = source

    def obs_home_score_source_set(self, source):
        if int(self.ui.HomeScoreSource_comboBox.currentIndex()) == 0:
            Obs.homeScoreSource = ""
        else:
            Obs.homeScoreSource = source

    def obs_away_score_source_set(self, source):
        if int(self.ui.AwayScoreSource_comboBox.currentIndex()) == 0:
            Obs.awayScoreSource = ""
        else:
            Obs.awayScoreSource = source

    def obs_period_source_set(self, source):
        if int(self.ui.PeriodSource_comboBox.currentIndex()) == 0:
            Obs.periodSource = ""
        else:
            Obs.periodSource = source

    def obs_home_graphics_source_set(self, source):
        if int(self.ui.HomeGraphicSource_comboBox.currentIndex()) == 0:
            Obs.homeGraphicSource = ""
        else:
            Obs.homeGraphicSource = source

    def obs_away_graphics_source_set(self, source):
        if int(self.ui.AwayGraphicSource_comboBox.currentIndex()) == 0:
            Obs.awayGraphicSource = ""
        else:
            Obs.awayGraphicSource = source

    def obs_in_game_scene_set(self, scene):
        if int(self.ui.InGameScene_comboBox.currentIndex()) == 0:
            Obs.inGameScene = ""
        else:
            Obs.inGameScene = scene

    def obs_half_time_scene_set(self, scene):
        if int(self.ui.HalfTimeScene_comboBox.currentIndex()) == 0:
            Obs.inHalfTimeScene = ""
        else:
            Obs.inHalfTimeScene = scene

    def on_home_graphics_browse(self):
        filename = QFileDialog.getOpenFileName(self, Language.OpenImage, "", Language.ImageFiles)
        path = os.path.abspath(filename[0])
        if os.path.isdir(path):
            path = ""
            return
        Obs.homeGraphicFile = path
        self.ui.HomeGraphicFile_Input.setText(path)

    def on_away_graphics_browse(self):
        filename = QFileDialog.getOpenFileName(self, Language.OpenImage, "", Language.ImageFiles)
        path = os.path.abspath(filename[0])
        if os.path.isdir(path):
            path = ""
            return
        Obs.awayGraphicFile = path
        self.ui.AwayGraphicFile_Input.setText(path)

    def set_time_obs(self, source, time):
        try:
            self.obs.call(requests.SetSourceSettings(source, {'text': time}))
        except:
            print("CheckedTrue")
            self.error.setChecked(True)

    def obs_connection_lost(self):
        self.obs_disconnect()
        #Obs.connected = False
        #self.ui.ConnectObs_Label.setText("Not Connected")
        self.error.stateChanged.disconnect()
        self.error.setChecked(False)
        self.error.stateChanged.connect(self.obs_connection_lost)
        self.error_box(Language.ConnectionToOBS, Language.ConnectionOBSLost)

    def on_save_obs(self):
        if not Obs.connected:
            self.error_box(Language.SaveError, Language.MustConnect)
            return
        filename = QFileDialog.getSaveFileName(self, "Save OBS Settings", os.path.dirname(__file__), "OBS Settings Files (*.obs)")
        path = os.path.abspath(filename[0])
        if os.path.isdir(path):
            return
        settings = QSettings(path, QSettings.IniFormat)
        settings.setValue("ingamescene", Obs.inGameScene)
        settings.setValue("halftimescene", Obs.inHalfTimeScene)
        settings.setValue("clocksource", Obs.clockSource)
        settings.setValue("overtimeclocksource", Obs.overTimeSource)
        settings.setValue("halftimeclocksource", Obs.halfTimeSource)
        settings.setValue("homesource", Obs.homeSource)
        settings.setValue("awaysource", Obs.awaySource)
        settings.setValue("homescoresource", Obs.homeScoreSource)
        settings.setValue("awayscoresource", Obs.awayScoreSource)
        settings.setValue("periodsource", Obs.periodSource)
        settings.setValue("homegraphicsource", Obs.homeGraphicSource)
        settings.setValue("awaygraphicsource", Obs.awayGraphicSource)
        settings.setValue("homegraphicfile", Obs.homeGraphicFile)
        settings.setValue("awaygraphicfile", Obs.awayGraphicFile)

    def on_load_obs(self):
        if not Obs.connected:
            self.error_box("Błąd odczytu.", "Musisz być połączpny z Obs.")
            return
        filename = QFileDialog.getOpenFileName(self, "Load OBS Settings", os.path.dirname(__file__), "Obs Settings Files (*.obs)")
        path = os.path.abspath(filename[0])
        if os.path.isdir(path):
            return
        settings = QSettings(path, QSettings.IniFormat)
        if Obs.errlist:
            Obs.errlist.clear()
        self.load_obs_to(settings, self.ui.InGameScene_comboBox, "ingamescene", Obs.inGameScene)
        self.load_obs_to(settings, self.ui.HalfTimeScene_comboBox, "halftimescene", Obs.inHalfTimeScene)
        self.load_obs_to(settings, self.ui.ClockSource_comboBox, "clocksource", Obs.clockSource)
        self.load_obs_to(settings, self.ui.OverTimeClockSource_comboBox, "overtimeclocksource", Obs.overTimeSource)
        self.load_obs_to(settings, self.ui.HalfTimeClockSource_comboBox, "halftimeclocksource", Obs.halfTimeSource)
        self.load_obs_to(settings, self.ui.HomeSource_comboBox, "homesource", Obs.homeSource)
        self.load_obs_to(settings, self.ui.AwaySource_comboBox, "awaysource", Obs.awaySource)
        self.load_obs_to(settings, self.ui.HomeScoreSource_comboBox, "homescoresource", Obs.homeScoreSource)
        self.load_obs_to(settings, self.ui.AwayScoreSource_comboBox, "awayscoresource", Obs.awayScoreSource)
        self.load_obs_to(settings, self.ui.PeriodSource_comboBox, "periodsource", Obs.periodSource)
        self.load_obs_to(settings, self.ui.HomeGraphicSource_comboBox, "homegraphicsource", Obs.homeGraphicSource)
        self.load_obs_to(settings, self.ui.AwayGraphicSource_comboBox, "awaygraphicsource", Obs.awayGraphicSource)
        self.load_obs_file_to(settings, self.ui.HomeGraphicFile_Input, "homegraphicfile", Obs.homeGraphicFile)
        self.load_obs_file_to(settings, self.ui.AwayGraphicFile_Input, "awaygraphicfile", Obs.awayGraphicFile)

        if Obs.errlist:
            self.error_box("Sprawdź Zbiór Scen.", "Brak źródeł o nazwie:\n" + self.list_errlist())


    def load_obs_to(self, settings, widget, key, obsvar ):
        obsvar = settings.value(key, "", str)
        if widget.findText(obsvar) != -1 and obsvar != "":
            widget.setCurrentText(obsvar)
        elif obsvar == "":
            widget.setCurrentText("----------")
        else:
            Obs.errlist.append(obsvar)
            obsvar = ""
            widget.setCurrentText("----------")

    def load_obs_file_to(self, settings, widget, key, obsvar ):
        obsvar = settings.value(key, "", str)
        if not os.path.isfile(obsvar) and not obsvar == "":
            Obs.errlist.append("brak pliku: " + obsvar)
            obsvar = ""
        widget.setText(obsvar)

    def list_errlist(self):
        text = ""
        for error in Obs.errlist:
            text += "- " + error + "\n"
        return text

    # ----------------------------- R E M O T E  -----------------------------------

    def on_remote_button(self):
        if self.ui.Remote_Button.text() == Language.StartServer:
            self.ui.Remote_Button.setText(Language.StopServer)
        else:
            self.ui.Remote_Button.setText(Language.StartServer)




    # ------------------------------------------------------------------------------

    def clear_error(self):
        Language.currentTextError = Language.iniTextError
        self.ui.Error_Text.setText(Language.currentTextError)

    def set_time_from_sec(self, sec):
        ScoreBoard.minutes = sec // 60
        ScoreBoard.sconds = sec % 60
        ScoreBoard.timerString = "{:02d}:{:02d}".format(ScoreBoard.minutes, ScoreBoard.seconds)

    def set_settime_from_sec(self, sec):
        ScoreBoard.setMinutes = sec // 60
        ScoreBoard.setSeconds = sec % 60
        self.ui.Minutes_Input.setValue(ScoreBoard.setMinutes)
        self.ui.Seconds_Input.setValue(ScoreBoard.setSeconds)

    def set_totime_from_sec(self, sec):
        ScoreBoard.setToMinutes = sec // 60
        ScoreBoard.setToSeconds = sec % 60
        self.ui.MinutesTo_Input.setValue(ScoreBoard.setToMinutes)
        self.ui.SecondsTo_Input.setValue(ScoreBoard.setToSeconds)

    def set_period_from_sec(self, sec):
        ScoreBoard.setPeriodMinutes = sec // 60
        ScoreBoard.setPeriodSeconds = sec % 60
        self.ui.MinutesPeriod_Input.setValue(ScoreBoard.setPeriodMinutes)
        self.ui.SecondsPeriod_Input.setValue(ScoreBoard.setPeriodSeconds)

    def set_input_time(self):
        self.ui.Minutes_Input.valueChanged.disconnect()
        self.ui.Seconds_Input.valueChanged.disconnect()
        self.ui.Minutes_Input.setValue(ScoreBoard.minutes)
        self.ui.Seconds_Input.setValue(ScoreBoard.seconds)
        self.ui.Minutes_Input.valueChanged[int].connect(self.on_time_input)
        self.ui.Seconds_Input.valueChanged[int].connect(self.on_time_input)

    def reset_overtime(self):
        ScoreBoard.overtime = False
        ScoreBoard.overtimeMinutes = 0
        ScoreBoard.overtimeSeconds = 0
        self.set_overtime()

    def timer_presets_enable(self, enable):
        Settings.timerPresetEnable = enable
        self.ui.TenM_Radio.setEnabled(enable)
        self.ui.TwelveM_Radio.setEnabled(enable)
        self.ui.FifteenM_Radio.setEnabled(enable)
        self.ui.TwentyM_Radio.setEnabled(enable)
        self.ui.ThirtyM_Radio.setEnabled(enable)
        self.ui.FortyFiveM_Radio.setEnabled(enable)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
