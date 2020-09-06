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
from PySide2.QtCore import QEvent, QTimer, QSettings, QTranslator, QXmlStreamWriter
from PySide2.QtCore import QIODevice, QFile, QCoreApplication, Qt, QUrl
from PySide2.QtGui import QFont, QPixmap
from obswebsocket import obsws, requests
from worker import MyServer


class ScoreBoard(object):

    scoreBoardDict = {'totalTenth': 0,
                      'tenth': 0,
                      'nr': 0,
                      'first': True,
                      'homeScore': 0,
                      'homeTeam': "",
                      'awayScore': 0,
                      'awayTeam': "",
                      'period': 1,
                      'totalTimeSec': 0,
                      'totalSetTimeSec': 0,
                      'totalToSec': 0,
                      'totalCurrentPeriodSec': 0,
                      'startPeriodsec': 0,
                      'stopPeriodsec': 0,
                      'totalSetPeriodSec': 0,
                      'timerString': "00:00",
                      'overTimeString': "00:00",
                      'periodTimeString': "00:00",
                      'halfTimeString': "00:00",
                      'minutes': 0,
                      'seconds': 0,
                      'setMinutes': 0,
                      'setSeconds': 0,
                      'setToMinutes': 0,
                      'setToSeconds': 0,
                      'setPeriodMinutes': 0,
                      'setPeriodSeconds': 0,
                      'overtimeMinutes': 0,
                      'overtimeSeconds': 0,
                      'toCheck': False,
                      'timerRunning': False,
                      'overtime': False,
                      'pregame': False
                      }
    


class Settings(object):

    settingsDict = {
        'writeFile': False,
        'writeXml': False,
        'writeObs': False,
        'stopWatch': True,
        'timer': False,
        'currentTime': False,
        'tenth': False,
        'halfTime': False,
        'defaultSpeed': 1000,
        'defaultTenthSpeed': 94,
        'speed': 1000,
        'tenthSpeed': 94,
        'timerPresetEnable': False,
        'timerPresetValue': 10,
        'customSpeed': False,
        'customTenthSpeed': False,
        'loadSettings': False,
        'saveData': False,
        'alwaysOnTop': False
    }


class Play(object):

    playDict = {
        'player': QMediaPlayer(),
        'playEnabled': False,
        'playPath': "",
        'playVolume': 50
    }


class Obs(object):

    obsDict = {
        'connected': False,
        'host': "localhost",
        'port': 4444,
        'password': "",
        'inGameScene': "",
        'inPreGameScene': "",
        'inHalfTimeScene': "",
        'clockSource': "",
        'overTimeSource': "",
        'halfTimeSource': "",
        'curTimeSource': "",
        'homeSource': "",
        'awaySource': "",
        'homeGraphicSource': "",
        'awayGraphicSource': "",
        'homeScoreSource': "",
        'periodSource': "",
        'awayScoreSource': "",
        'homeGraphicFile': "",
        'awayGraphicFile': "",
        'send': False,
        'errlist': []
    }


class Dynamic(object):

    dynamicDict = {
        'halfOn': False,
        'preOn': False,
        'connectObsButtonOn': False,
        'connectObsLabelOn': False,
        'startServerOn': False,
        'remoteStatus': False
    }



class Files(object):

    filesDict = {
        'outDir': "output",
        'iniFile': "config.ini",
        'xmlFile': "output.xml",
        'homeFile': "home.txt",
        'awayFile': "away.txt",
        'homeScoreFile': "homescore.txt",
        'awayScoreFile': "awayscore.txt",
        'timeFile': "time.txt",
        'overTimeFile': "overtime.txt",
        'periodFile': "period.txt",
        'halfTimeFile': "halftime.txt",
        'path': os.path.abspath(__file__)
    }
    filesDict['curPath'] = os.path.dirname(filesDict['path'])
    filesDict['outPath'] = os.path.join(filesDict['curPath'], filesDict['outDir'])
    filesDict['iniPath'] = os.path.join(filesDict['curPath'], filesDict['iniFile'])
    filesDict['xmlPath'] = os.path.join(filesDict['outPath'], filesDict['xmlFile'])
    filesDict['homePath'] = os.path.join(filesDict['outPath'], filesDict['homeFile'])
    filesDict['awayPath'] = os.path.join(filesDict['outPath'], filesDict['awayFile'])
    filesDict['homeScorePath'] = os.path.join(filesDict['outPath'], filesDict['homeScoreFile'])
    filesDict['awayScorePath'] = os.path.join(filesDict['outPath'], filesDict['awayScoreFile'])
    filesDict['timePath'] = os.path.join(filesDict['outPath'], filesDict['timeFile'])
    filesDict['overTimePath'] = os.path.join(filesDict['outPath'], filesDict['overTimeFile'])
    filesDict['periodPath'] = os.path.join(filesDict['outPath'], filesDict['periodFile'])
    filesDict['halfTimePath'] = os.path.join(filesDict['outPath'], filesDict['halfTimeFile'])
    
    
    try:
        os.mkdir(filesDict['outPath'])
    except FileExistsError:
        pass


class Keys(object):
    keysOn = False
    homeUp = []
    homeUp2 = []
    homeDown = []
    awayUp = []
    awayUp2 = []
    awayDown = []
    sartStop = []
    resetTime = []
    halfTime = []
    preGame = []
    resetScore = []
    swap = []
    periodUp = []
    periodDown = []
    stopSound = []
    remoteOnOff = []
    obsConDiscon = []
    keysDict = {
        'keysOn': False,
        'homeUp': [],
        'homeUp2': [],
        'homeDown': [],
        'awayUp': [],
        'awayUp2': [],
        'awayDown': [],
        'sartStop': [],
        'resetTime': [],
        'halfTime': [],
        'preGame': [],
        'resetScore': [],
        'swap': [],
        'periodUp': [],
        'periodDown': [],
        'stopSound': [],
        'remoteOnOff': [],
        'obsConDiscon': []
    }


def get_sec_from_time():
    return ScoreBoard.scoreBoardDict['minutes'] * 60 + ScoreBoard.scoreBoardDict['seconds']


def get_sec_from_settime():
    return ScoreBoard.scoreBoardDict['setMinutes'] * 60 + ScoreBoard.scoreBoardDict['setSeconds']


def get_sec_from_totime():
    return ScoreBoard.scoreBoardDict['setToMinutes'] * 60 + ScoreBoard.scoreBoardDict['setToSeconds']


def get_sec_from_period():
    return ScoreBoard.scoreBoardDict['setPeriodMinutes'] * 60 + ScoreBoard.scoreBoardDict['setPeriodSeconds']


def get_sec_from_end_period():
    return ScoreBoard.scoreBoardDict['period'] * ScoreBoard.scoreBoardDict['totalSetPeriodSec']


def get_sec_from_start_period():
    return (ScoreBoard.scoreBoardDict['period'] - 1) * ScoreBoard.scoreBoardDict['totalSetPeriodSec']


def get_sec_from_current_period():
    return ScoreBoard.scoreBoardDict['totalTimeSec'] - ScoreBoard.scoreBoardDict['startPeriodsec']


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.settings = QSettings(Files.filesDict['iniPath'], QSettings.IniFormat)
        self.vk = 0
        self.setObjectName("MainWindow")
        self.error = QtWidgets.QCheckBox(self)
        self.error.setChecked(False)
        self.error.setHidden(True)
        self.server = None
        self.obs = obsws()
        self.timer = QTimer(self)
        self.translator = QTranslator()
        self.translator.load('mainwindow_pl_PL')
        app.installTranslator(self.translator)
        Language.currentLanguage = "polski"
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.labelStatus = QLabel(self)
        self.connectObsStatus = QLabel(self)
        self.remoteConnectStatus = QLabel(self)
        self.remoteLabelStatus = QLabel(self)
        self.remoteNrLabelStatus = QLabel(self)
        self.remoteNrConnStatus = QLabel(self)
        self.ui.statusbar.addWidget(self.labelStatus, 1)
        self.ui.statusbar.addWidget(self.connectObsStatus, 2)
        self.ui.statusbar.addWidget(self.remoteLabelStatus, 1)
        self.ui.statusbar.addWidget(self.remoteConnectStatus, 2)
        self.ui.statusbar.addWidget(self.remoteNrLabelStatus, 2)
        self.ui.statusbar.addWidget(self.remoteNrConnStatus, )
        Language.retranslateUi()
        self.ui.retranslateUi(self)
        self.labelStatus.setText(Language.ConnectionToOBS)
        self.connectObsStatus.setText(self.ui.ConnectObs_Label.text())
        self.remoteLabelStatus.setText(Language.RemoteLabelStatus)
        self.remoteConnectStatus.setText(Language.NotConnected)
        self.remoteNrLabelStatus.setText(Language.NrOfConnections)
        self.remoteNrConnStatus.setText("-")
        self.ui.actionPolski.setChecked(True)
        self.ui.Save_Data_CheckBox.setEnabled(False)
        self.ui.Speed_Input.setValue(Settings.settingsDict['defaultSpeed'])
        self.ui.MicroSpeed_Input.setValue(Settings.settingsDict['defaultTenthSpeed'])
        self.pm = QPixmap("greydot16.png")

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
        self.ui.To_Checkbox.toggled.connect(self.on_to_check)
        self.ui.MinutesTo_Input.valueChanged[int].connect(self.on_to_input)
        self.ui.SecondsTo_Input.valueChanged[int].connect(self.on_to_input)
        self.ui.Start_Button.clicked.connect(self.start_timer)
        self.ui.UpdateTeam_Button.clicked.connect(self.on_update_team)
        self.ui.HomeName_Input.editingFinished.connect(self.on_home_change)
        self.ui.AwayName_Input.editingFinished.connect(self.on_away_change)
        self.ui.ResetTimer_Button.clicked.connect(self.on_reset_timer)
        self.ui.ResetScore_Button.clicked.connect(self.on_reset_score)
        self.ui.Swap_Button.clicked.connect(self.on_swap_button)
        self.ui.HalfTime_Button.clicked.connect(self.on_half_time)
        self.ui.StopSound_Button.setVisible(False)
        self.ui.StopSound_Button.clicked.connect(self.play_sound)
        self.ui.PreGame_Button.clicked.connect(self.on_pregame)
        self.ui.ImageLabel.setPixmap(self.pm);
        self.ui.ImageLabel.setScaledContents(True);

        # -------------------- s e t t i n g s ---------------------------------

        self.ui.StopWatch_Radio.toggled.connect(self.on_stopwatch)
        self.ui.Timer_Radio.toggled.connect(self.on_timer)
        self.ui.CurrentTime_Radio.toggled.connect(self.on_current_time)
        self.ui.Always_on_top_Checkbox.toggled.connect(self.on_always_on_top)
        self.ui.OneTenth_Checkbox.toggled.connect(self.on_tenth)
        self.ui.MicroSpeed_CheckBox.toggled.connect(self.on_ten_speed)
        self.ui.Speed_CheckBox.toggled.connect(self.on_speed)
        self.ui.MicroSpeed_Input.valueChanged.connect(self.on_ten_input)
        self.ui.Speed_Input.valueChanged.connect(self.on_speed_input)
        self.ui.SpeedHelp_Button.clicked.connect(self.speed_help)
        self.ui.TimerPreset_Checkbox.toggled.connect(self.on_timer_preset)
        self.ui.TenM_Radio.toggled.connect(self.on_ten_radio)
        self.ui.TwelveM_Radio.toggled.connect(self.on_twelve_radio)
        self.ui.FifteenM_Radio.toggled.connect(self.on_fifteen_radio)
        self.ui.TwentyM_Radio.toggled.connect(self.on_twenty_radio)
        self.ui.ThirtyM_Radio.toggled.connect(self.on_thirty_radio)
        self.ui.FortyFiveM_Radio.toggled.connect(self.on_fortyfive_radio)
        self.ui.Use_Files_CheckBox.toggled.connect(self.on_use_files)
        self.ui.Use_Xml_CheckBox.toggled.connect(self.on_use_xml)
        self.ui.Save_Data_CheckBox.toggled.connect(self.on_save_data)

        # ----------------------- P L A Y ------------------------------------------

        self.ui.PlaySound_Checkbox.toggled.connect(self.on_play)
        self.ui.BrowseFile_Button.clicked.connect(self.on_play_browse)
        self.ui.BrowseFile_Input.editingFinished.connect(self.on_play_input)
        self.ui.TestSound_Button.clicked.connect(self.play_sound)
        self.ui.Volume_Slider.valueChanged.connect(self.on_volume)

        # ------------------------ O B S -------------------------------------------

        self.ui.ConnectObs_Button.clicked.connect(self.on_obs_button)
        self.ui.InGameScene_comboBox.currentIndexChanged[str].connect(self.obs_in_game_scene_set)
        self.ui.HalfTimeScene_comboBox.currentIndexChanged[str].connect(self.obs_half_time_scene_set)
        self.ui.PreGameScene_comboBox.currentIndexChanged[str].connect(self.obs_pre_game_scene_set)
        self.ui.ClockSource_comboBox.currentIndexChanged[str].connect(self.obs_clock_source_set)
        self.ui.OverTimeClockSource_comboBox.currentIndexChanged[str].connect(self.obs_overtime_clock_source_set)
        self.ui.HalfTimeClockSource_comboBox.currentIndexChanged[str].connect(self.obs_halftime_clock_source_set)
        self.ui.CurTimeSource_comboBox.currentIndexChanged[str].connect(self.obs_curtime_clock_source_set)
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

        # ---------------------------- H O T K E Y S -----------------------------------

        self.ui.Hotkey_Checkbox.toggled.connect(self.on_hotkeys)
        print("settings: ", self.settings.value('settings/loadSettings', False, bool))
        if self.settings.value('settings/loadSettings', False, bool):
            print("starting load")
            self.load_settings()
        else:
            self.ui.Load_Settings_CheckBox.toggled.connect(self.on_load_settings)

    # --------------------------------- S A V E ------------------------------------

    def save(self, filepath, value):
        if Settings.settingsDict['writeFile']:
            print("save in files")
            file = open(filepath, "w")
            file.write(value)
            file.close()
        if Settings.settingsDict['writeXml']:
            print("save in xml")
            self.write_xml()
        if Obs.obsDict['connected']:
            try:
                if filepath == Files.filesDict['homePath']:
                    self.obs.call(requests.SetSourceSettings(Obs.obsDict['homeSource'], {'text': value}))
                elif filepath == Files.filesDict['awayPath']:
                    self.obs.call(requests.SetSourceSettings(Obs.obsDict['awaySource'], {'text': value}))
                elif filepath == Files.filesDict['homeScorePath']:
                    self.obs.call(requests.SetSourceSettings(Obs.obsDict['homeScoreSource'], {'text': value}))
                elif filepath == Files.filesDict['awayScorePath']:
                    self.obs.call(requests.SetSourceSettings(Obs.obsDict['awayScoreSource'], {'text': value}))
                elif filepath == Files.filesDict['periodPath']:
                    self.obs.call(requests.SetSourceSettings(Obs.obsDict['periodSource'], {'text': value}))
                elif filepath == Files.filesDict['timePath']:
                    threading.Thread(target=self.set_time_obs, args=(Obs.obsDict['clockSource'], " "+value+" ")).start()
                    if Settings.settingsDict['currentTime']:
                        threading.Thread(target=self.set_time_obs, args=(Obs.obsDict['curTimeSource'], value)).start()
                elif filepath == Files.filesDict['overTimePath']:
                    threading.Thread(target=self.set_time_obs, args=(Obs.obsDict['overTimeSource'], value)).start()
                elif filepath == Files.filesDict['halfTimePath']:
                    threading.Thread(target=self.set_time_obs, args=(Obs.obsDict['halfTimeSource'], value)).start()

            except:
                window.error_box(Language.ConnectionToOBS, Language.ConnectionOBSLost)
                self.obs_disconnect()
                #Obs.obsDict['connected'] = False
                #window.ui.ConnectObs_Label.setText("Not Connected")
        if self.server and self.server.status == Language.Connected:
            print("save in server")
            try:
                if filepath == Files.filesDict['homePath']:
                    self.server.send("Home:"+value)
                elif filepath == Files.filesDict['awayPath']:
                    self.server.send("Away:"+value)
                elif filepath == Files.filesDict['homeScorePath']:
                    self.server.send("HomeScore:"+value+"\r\n")
                elif filepath == Files.filesDict['awayScorePath']:
                    self.server.send("AwayScore:"+value+"\r\n")
                elif filepath == Files.filesDict['periodPath']:
                    self.server.send("Period:"+value)
                elif filepath == Files.filesDict['timePath']:
                    threading.Thread(target=self.set_time_remote, args=("Time:"+value,)).start()
                elif filepath == Files.filesDict['overTimePath']:
                    threading.Thread(target=self.set_time_remote, args=("Overtime:"+value,)).start()
                elif filepath == Files.filesDict['halfTimePath']:
                    threading.Thread(target=self.set_time_remote, args=("Halftime:"+value,)).start()
            except:
                pass

    def save_all(self):
        print("zaczynam save_all")
        if Settings.settingsDict['writeFile']:
            print("save_all in files")
            for x, y in zip([Files.filesDict['homePath'], Files.filesDict['awayPath'], Files.filesDict['homeScorePath'], Files.filesDict['awayScorePath'],
                             Files.filesDict['timePath'], Files.filesDict['overTimePath'], Files.filesDict['periodPath'], Files.filesDict['halfTimePath']],
                            [ScoreBoard.scoreBoardDict['homeTeam'], ScoreBoard.scoreBoardDict['awayTeam'], ScoreBoard.scoreBoardDict['homeScore'], ScoreBoard.scoreBoardDict['awayScore'],
                             ScoreBoard.scoreBoardDict['timerString'], ScoreBoard.scoreBoardDict['overTimeString'], ScoreBoard.scoreBoardDict['period'],
                             ScoreBoard.scoreBoardDict['halfTimeString']]):
                f = open(x, "w")
                f.write(str(y))
                f.close()
        if Settings.settingsDict['writeXml']:
            print("save_all in xml")
            self.write_xml()
        print("server: ", self.server)
        if self.server:
            print("serverStatus: ", self.server.status)
        print("Language.Connected: "+Language.Connected)
        if self.server and self.server.status == Language.Connected:
            print("save_all in server")
            self.server.send("Home:" + ScoreBoard.scoreBoardDict['homeTeam'])
            self.server.send("Away:" + ScoreBoard.scoreBoardDict['awayTeam'])
            self.server.send("HomeScore:" + str(ScoreBoard.scoreBoardDict['homeScore']))
            self.server.send("AwayScore:" + str(ScoreBoard.scoreBoardDict['awayScore']))
            self.server.send("Period:" + str(ScoreBoard.scoreBoardDict['period']))
            threading.Thread(target=self.set_time_remote, args=("Time:" + ScoreBoard.scoreBoardDict['timerString'],)).start()
            threading.Thread(target=self.set_time_remote, args=("Overtime:" + ScoreBoard.scoreBoardDict['overTimeString'],)).start()
            threading.Thread(target=self.set_time_remote, args=("Halftime:" + ScoreBoard.scoreBoardDict['halfTimeString'],)).start()


    def write_xml(self):
        ScoreBoard.scoreBoardDict['nr'] += 1
        file = QFile(Files.filesDict['xmlPath'])
        file.open(QIODevice.WriteOnly)
        xml = QXmlStreamWriter(file)
        xml.setAutoFormatting(True)
        xml.writeStartDocument()
        xml.writeStartElement("items")
        xml.writeTextElement("timestamp", str(ScoreBoard.scoreBoardDict['nr']))
        xml.writeTextElement("HomeScore", str(ScoreBoard.scoreBoardDict['homeScore']))
        xml.writeTextElement("AwayScore", str(ScoreBoard.scoreBoardDict['awayScore']))
        xml.writeTextElement("HomeName", ScoreBoard.scoreBoardDict['homeTeam'])
        xml.writeTextElement("AwayName", ScoreBoard.scoreBoardDict['awayTeam'])
        xml.writeTextElement("Period", str(ScoreBoard.scoreBoardDict['period']))
        xml.writeTextElement("Clock", ScoreBoard.scoreBoardDict['timerString'])
        xml.writeTextElement("OverTimeClock", ScoreBoard.scoreBoardDict['overTimeString'])
        xml.writeTextElement("HlafTimeClock", ScoreBoard.scoreBoardDict['halfTimeString'])
        xml.writeEndElement()
        xml.writeEndDocument()
        file.close()

    # ------------------------------- T I M E R ------------------------------------

    def start_timer(self):
        if not ScoreBoard.scoreBoardDict['timerRunning']:
            if Settings.settingsDict['timer'] and ScoreBoard.scoreBoardDict['totalTimeSec'] == 0:
                Language.currentTextError = Language.timerError
                self.ui.Error_Text.setText(Language.currentTextError)
                QTimer.singleShot(3000, self.clear_error)
                return
            if Settings.settingsDict['tenth'] and ScoreBoard.scoreBoardDict['totalTimeSec'] <= 60 and Settings.settingsDict['timer']:
                speed = Settings.settingsDict['tenthSpeed'] if Settings.settingsDict['customTenthSpeed'] else Settings.settingsDict['defaultTenthSpeed']
            else:
                speed = Settings.settingsDict['speed'] if Settings.settingsDict['customSpeed'] else Settings.settingsDict['defaultSpeed']
            print("speed = ", speed)
            self.timer.start(speed)
            ScoreBoard.scoreBoardDict['timerRunning'] = True
            self.ui.Start_Button.setText("STOP")
            self.timer_enable(False)
            self.settings_start_enable(True)
            ScoreBoard.scoreBoardDict['first'] = True
        else:
            self.timer.stop()
            ScoreBoard.scoreBoardDict['timerRunning'] = False
            self.ui.Start_Button.setText("START")
            if Settings.settingsDict['stopWatch']:
                self.stopwatch_enable(True)
            elif Settings.settingsDict['timer']:
                self.timer_enable(True)
                if Play.playDict['playEnabled']:
                    self.play_sound()
        self.scoreboard_change()

    def tick(self):
        if not (Settings.settingsDict['tenth'] and Settings.settingsDict['timer'] and ScoreBoard.scoreBoardDict['totalTimeSec'] <= 60):
            if Settings.settingsDict['currentTime']:
                self.set_current_time()
                return
            if Settings.settingsDict['stopWatch'] and not Settings.settingsDict['halfTime']:
                if not ScoreBoard.scoreBoardDict['overtime']:
                    ScoreBoard.scoreBoardDict['seconds'] += 1
                    if ScoreBoard.scoreBoardDict['seconds'] > 59:
                        ScoreBoard.scoreBoardDict['minutes'] += 1
                        ScoreBoard.scoreBoardDict['seconds'] = 0
                    ScoreBoard.scoreBoardDict['totalTimeSec'] = get_sec_from_time()
                    ScoreBoard.scoreBoardDict['totalPeriodSec'] = get_sec_from_current_period()
                    self.set_time()
                else:
                    ScoreBoard.scoreBoardDict['overtimeSeconds'] += 1
                    if ScoreBoard.scoreBoardDict['overtimeSeconds'] > 59:
                        ScoreBoard.scoreBoardDict['overtimeSeconds'] = 0
                        ScoreBoard.scoreBoardDict['overtimeMinutes'] += 1
                    self.set_overtime()
            elif Settings.settingsDict['timer'] and not Settings.settingsDict['halfTime']:
                ScoreBoard.scoreBoardDict['seconds'] -= 1
                if ScoreBoard.scoreBoardDict['seconds'] == 0 and ScoreBoard.scoreBoardDict['minutes'] == 0:
                    self.ui.Start_Button.clicked.emit()
                if ScoreBoard.scoreBoardDict['seconds'] < 0:
                    if ScoreBoard.scoreBoardDict['minutes'] >= 0:
                        ScoreBoard.scoreBoardDict['minutes'] -= 1
                        ScoreBoard.scoreBoardDict['seconds'] = 59
                    else:
                        self.ui.Start_Button.clicked.emit()
                ScoreBoard.scoreBoardDict['totalTimeSec'] = get_sec_from_time()
                ScoreBoard.scoreBoardDict['totalTenth'] = ScoreBoard.scoreBoardDict['totalTimeSec'] * 10
                self.set_timer_time()
            elif Settings.settingsDict['halfTime']:
                ScoreBoard.scoreBoardDict['seconds'] += 1
                if ScoreBoard.scoreBoardDict['seconds'] > 59:
                    ScoreBoard.scoreBoardDict['minutes'] += 1
                    ScoreBoard.scoreBoardDict['seconds'] = 0
                self.set_halftime()
        else:
            if ScoreBoard.scoreBoardDict['first']:
                ScoreBoard.scoreBoardDict['Tenth'] = ScoreBoard.scoreBoardDict['totalTenth'] % 10
                ScoreBoard.scoreBoardDict['seconds'] = ScoreBoard.scoreBoardDict['totalTenth'] // 10
                ScoreBoard.scoreBoardDict['minutes'] = 0
                speed = Settings.settingsDict['tenthSpeed'] if Settings.settingsDict['customTenthSpeed'] else Settings.settingsDict['defaultTenthSpeed']
                print("speed = ", speed)
                self.timer.start(speed)
                ScoreBoard.scoreBoardDict['first'] = False
            ScoreBoard.scoreBoardDict['tenth'] -= 1
            if ScoreBoard.scoreBoardDict['tenth'] < 0:
                ScoreBoard.scoreBoardDict['totalTenth'] -= 10
                ScoreBoard.scoreBoardDict['seconds'] -= 1
                ScoreBoard.scoreBoardDict['tenth'] = 9
            ScoreBoard.scoreBoardDict['totalTimeSec'] = get_sec_from_time()
            ScoreBoard.scoreBoardDict['totalPeriodSec'] = get_sec_from_current_period()
            if ScoreBoard.scoreBoardDict['seconds'] == 0 and ScoreBoard.scoreBoardDict['tenth'] == 0:
                ScoreBoard.scoreBoardDict['first'] = True
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
        if not ScoreBoard.scoreBoardDict['timerRunning']:
            ScoreBoard.scoreBoardDict['setPeriodMinutes'] = self.ui.MinutesPeriod_Input.value()
            ScoreBoard.scoreBoardDict['setPeriodSeconds'] = self.ui.SecondsPeriod_Input.value()
            ScoreBoard.scoreBoardDict['totalSetPeriodSec'] = get_sec_from_period()
            ScoreBoard.scoreBoardDict['startPeriodsec'] = get_sec_from_start_period()
            ScoreBoard.scoreBoardDict['stopPeriodsec'] = get_sec_from_end_period()
            self.update_period_time()
            self.update_on_period(None)
            self.scoreboard_change()

    def on_time_input(self):
        ScoreBoard.scoreBoardDict['setMinutes'] = self.ui.Minutes_Input.value()
        ScoreBoard.scoreBoardDict['setSeconds'] = self.ui.Seconds_Input.value()
        ScoreBoard.scoreBoardDict['totalSetTimeSec'] = get_sec_from_settime()
        ScoreBoard.scoreBoardDict['minutes'] = ScoreBoard.scoreBoardDict['setMinutes']
        ScoreBoard.scoreBoardDict['seconds'] = ScoreBoard.scoreBoardDict['setSeconds']
        ScoreBoard.scoreBoardDict['totalTimeSec'] = get_sec_from_time()
        ScoreBoard.scoreBoardDict['tenth'] = 0
        ScoreBoard.scoreBoardDict['totalTenth'] = ScoreBoard.scoreBoardDict['totalTimeSec'] * 10
        self.update_period_time()
        self.set_time()

    def set_time(self):
        ScoreBoard.scoreBoardDict['timerString'] = "{:02d}:{:02d}".format(ScoreBoard.scoreBoardDict['minutes'], ScoreBoard.scoreBoardDict['seconds'])
        self.ui.Minutes_Input.valueChanged.disconnect()
        self.ui.Seconds_Input.valueChanged.disconnect()
        self.ui.Minutes_Input.setValue(ScoreBoard.scoreBoardDict['minutes'])
        self.ui.Seconds_Input.setValue(ScoreBoard.scoreBoardDict['seconds'])
        self.ui.Minutes_Input.valueChanged[int].connect(self.on_time_input)
        self.ui.Seconds_Input.valueChanged[int].connect(self.on_time_input)
        self.ui.Clock_Label.setText(ScoreBoard.scoreBoardDict['timerString'])
        if Settings.settingsDict['stopWatch']:
            self.set_period_time()
        self.save(Files.filesDict['timePath'], ScoreBoard.scoreBoardDict['timerString'])
        if ScoreBoard.scoreBoardDict['toCheck'] and ScoreBoard.scoreBoardDict['timerRunning'] and ScoreBoard.scoreBoardDict['totalTimeSec'] == ScoreBoard.scoreBoardDict['totalToSec']:
            self.ui.Start_Button.clicked.emit()
            return
        if ScoreBoard.scoreBoardDict['totalTimeSec'] != 0 and ScoreBoard.scoreBoardDict['totalTimeSec'] == ScoreBoard.scoreBoardDict['stopPeriodsec']:
            # print ("total = ", ScoreBoard.scoreBoardDict['totalTimeSec'], " periodEnd = ", ScoreBoard.scoreBoardDict['stopPeriodsec'])
            ScoreBoard.scoreBoardDict['overtime'] = True
        self.scoreboard_change()

    def set_halftime(self):
        ScoreBoard.scoreBoardDict['halfTimeString'] = "{:02d}:{:02d}".format(ScoreBoard.scoreBoardDict['minutes'], ScoreBoard.scoreBoardDict['seconds'])
        self.ui.HalfTimeClock_Label.setText(ScoreBoard.scoreBoardDict['halfTimeString'])
        self.save(Files.filesDict['halfTimePath'], ScoreBoard.scoreBoardDict['halfTimeString'])
        self.scoreboard_change()

    def set_timer_time(self):
        ScoreBoard.scoreBoardDict['timerString'] = "{:02d}:{:02d}".format(ScoreBoard.scoreBoardDict['minutes'], ScoreBoard.scoreBoardDict['seconds'])
        self.ui.Minutes_Input.valueChanged.disconnect()
        self.ui.Seconds_Input.valueChanged.disconnect()
        self.ui.Minutes_Input.setValue(ScoreBoard.scoreBoardDict['minutes'])
        self.ui.Seconds_Input.setValue(ScoreBoard.scoreBoardDict['seconds'])
        self.ui.Minutes_Input.valueChanged[int].connect(self.on_time_input)
        self.ui.Seconds_Input.valueChanged[int].connect(self.on_time_input)
        self.ui.Clock_Label.setText(ScoreBoard.scoreBoardDict['timerString'])
        self.save(Files.filesDict['timePath'], ScoreBoard.scoreBoardDict['timerString'])
        self.scoreboard_change()

    def set_tenth_time(self):
        ScoreBoard.scoreBoardDict['timerString'] = "{:02d}.{:01d}".format(ScoreBoard.scoreBoardDict['seconds'], ScoreBoard.scoreBoardDict['tenth'])
        Obs.obsDict['send'] = False if ScoreBoard.scoreBoardDict['tenth'] % 2 else True
        self.ui.Clock_Label.setText(ScoreBoard.scoreBoardDict['timerString'])
        if ScoreBoard.scoreBoardDict['tenth'] == 9:
            self.ui.Minutes_Input.valueChanged.disconnect()
            self.ui.Seconds_Input.valueChanged.disconnect()
            self.ui.Minutes_Input.setValue(ScoreBoard.scoreBoardDict['minutes'])
            self.ui.Seconds_Input.setValue(ScoreBoard.scoreBoardDict['seconds'])
            self.ui.Minutes_Input.valueChanged[int].connect(self.on_time_input)
            self.ui.Seconds_Input.valueChanged[int].connect(self.on_time_input)
        self.save(Files.filesDict['timePath'], ScoreBoard.scoreBoardDict['timerString'])
        self.scoreboard_change()

    def set_overtime(self):
        ScoreBoard.scoreBoardDict['overTimeString'] = "{:02d}:{:02d}".format(ScoreBoard.scoreBoardDict['overtimeMinutes'], ScoreBoard.scoreBoardDict['overtimeSeconds'])
        self.ui.OverTimeClock_Label.setText(ScoreBoard.scoreBoardDict['overTimeString'])
        self.save(Files.filesDict['overTimePath'], ScoreBoard.scoreBoardDict['overTimeString'])
        self.scoreboard_change()

    def set_current_time(self):
        ScoreBoard.scoreBoardDict['timerString'] = datetime.now().strftime("%H:%M:%S")
        self.ui.Clock_Label.setText(ScoreBoard.scoreBoardDict['timerString'])
        self.save(Files.filesDict['timePath'], ScoreBoard.scoreBoardDict['timerString'])
        self.scoreboard_change()

    # ------------------------- H O M E ----------------------------------------------

    def on_home_change(self):
        ScoreBoard.scoreBoardDict['homeTeam'] = self.ui.HomeName_Input.text()
        self.save(Files.filesDict['homePath'], str(ScoreBoard.scoreBoardDict['homeTeam']))
        self.scoreboard_change()


    def on_home_down(self):
        if ScoreBoard.scoreBoardDict['homeScore'] > 0:
            ScoreBoard.scoreBoardDict['homeScore'] -= 1
            self.ui.HomeScore_Label.setText(str(ScoreBoard.scoreBoardDict['homeScore']))
            self.save(Files.filesDict['homeScorePath'], str(ScoreBoard.scoreBoardDict['homeScore']))
            self.scoreboard_change()

    def on_home_up(self):
        ScoreBoard.scoreBoardDict['homeScore'] += 1
        self.ui.HomeScore_Label.setText(str(ScoreBoard.scoreBoardDict['homeScore']))
        self.save(Files.filesDict['homeScorePath'], str(ScoreBoard.scoreBoardDict['homeScore']))
        self.scoreboard_change()

    def on_home_up2(self):
        ScoreBoard.scoreBoardDict['homeScore'] += 2
        self.ui.HomeScore_Label.setText(str(ScoreBoard.scoreBoardDict['homeScore']))
        self.save(Files.filesDict['homeScorePath'], str(ScoreBoard.scoreBoardDict['homeScore']))
        self.scoreboard_change()

    # ------------------------- A W A Y -----------------------------------------

    def on_away_change(self):
        ScoreBoard.scoreBoardDict['awayTeam'] = self.ui.AwayName_Input.text()
        self.save(Files.filesDict['awayPath'], str(ScoreBoard.scoreBoardDict['awayTeam']))
        self.scoreboard_change()

    def on_away_down(self):
        if ScoreBoard.scoreBoardDict['awayScore'] > 0:
            ScoreBoard.scoreBoardDict['awayScore'] -= 1
            self.ui.AwayScore_Label.setText(str(ScoreBoard.scoreBoardDict['awayScore']))
            self.save(Files.filesDict['awayScorePath'], str(ScoreBoard.scoreBoardDict['awayScore']))
            self.scoreboard_change()

    def on_away_up(self):
        ScoreBoard.scoreBoardDict['awayScore'] += 1
        self.ui.AwayScore_Label.setText(str(ScoreBoard.scoreBoardDict['awayScore']))
        self.save(Files.filesDict['awayScorePath'], str(ScoreBoard.scoreBoardDict['awayScore']))
        self.scoreboard_change()

    def on_away_up2(self):
        ScoreBoard.scoreBoardDict['awayScore'] += 2
        self.ui.AwayScore_Label.setText(str(ScoreBoard.scoreBoardDict['awayScore']))
        self.save(Files.filesDict['awayScorePath'], str(ScoreBoard.scoreBoardDict['awayScore']))
        self.scoreboard_change()

    # ------------------------- P E R I O D -------------------------------------

    def on_period_up(self):
        print("on period up")
        self.update_on_period(True)

    def on_period_down(self):
        print("on period down")
        self.update_on_period(False)

    def update_down_period(self):
        self.ui.Period_Label.setText(str(ScoreBoard.scoreBoardDict['period']))
        ScoreBoard.scoreBoardDict['startPeriodsec'] = get_sec_from_start_period()
        ScoreBoard.scoreBoardDict['stopPeriodsec'] = get_sec_from_end_period()
        self.set_period_time()

    def update_period_time(self):
        if ScoreBoard.scoreBoardDict['totalSetPeriodSec'] != 0 and Settings.settingsDict['stopWatch']:
            if ScoreBoard.scoreBoardDict['totalSetTimeSec'] >= ScoreBoard.scoreBoardDict['stopPeriodsec']:
                print("period wyzej")
                ScoreBoard.scoreBoardDict['period'] = ScoreBoard.scoreBoardDict['totalSetTimeSec'] // ScoreBoard.scoreBoardDict['totalSetPeriodSec'] + 1
                self.update_on_period(None)

            elif ScoreBoard.scoreBoardDict['totalSetTimeSec'] < ScoreBoard.scoreBoardDict['startPeriodsec']:
                print("period nizej")
                ScoreBoard.scoreBoardDict['period'] = ScoreBoard.scoreBoardDict['totalSetTimeSec'] // ScoreBoard.scoreBoardDict['totalSetPeriodSec'] + 1
                self.update_down_period()

    def set_period_time(self):
        perminute = get_sec_from_current_period() // 60
        perseconds = get_sec_from_current_period() % 60
        ScoreBoard.scoreBoardDict['periodTimeString'] = "{:02d}:{:02d}".format(perminute, perseconds)
        self.ui.PeriodClock_Label.setText(ScoreBoard.scoreBoardDict['periodTimeString'])
        self.scoreboard_change()

    def update_on_period(self, where):
        print("update on period :", where)
        if not ScoreBoard.scoreBoardDict['timerRunning'] or Settings.settingsDict['currentTime']:
            self.reset_overtime()
            if where is None:
                ScoreBoard.scoreBoardDict['period'] += 0
            elif where:
                ScoreBoard.scoreBoardDict['period'] += 1
            else:
                if ScoreBoard.scoreBoardDict['period'] > 1:
                    ScoreBoard.scoreBoardDict['period'] -= 1
            self.ui.Period_Label.setText(str(ScoreBoard.scoreBoardDict['period']))
            if Settings.settingsDict['timer'] or Settings.settingsDict['currentTime']:
                self.save(Files.filesDict['periodPath'], str(ScoreBoard.scoreBoardDict['period']))
                return
            ScoreBoard.scoreBoardDict['totalSetPeriodSec'] = get_sec_from_period()
            ScoreBoard.scoreBoardDict['startPeriodsec'] = get_sec_from_start_period()
            ScoreBoard.scoreBoardDict['stopPeriodsec'] = get_sec_from_end_period()
            print("totalperoid = ", ScoreBoard.scoreBoardDict['totalSetPeriodSec'], " startperiod = ", ScoreBoard.scoreBoardDict['startPeriodsec'],
                  "  stopperiod = ", ScoreBoard.scoreBoardDict['stopPeriodsec'])
            if ScoreBoard.scoreBoardDict['totalSetPeriodSec'] == 0:
                return
            if where is not None:
                ScoreBoard.scoreBoardDict['minutes'] = ScoreBoard.scoreBoardDict['startPeriodsec'] // 60
                ScoreBoard.scoreBoardDict['seconds'] = ScoreBoard.scoreBoardDict['startPeriodsec'] % 60
            ScoreBoard.scoreBoardDict['totalSetTimeSec'] = get_sec_from_settime()
            ScoreBoard.scoreBoardDict['totalTimeSec'] = get_sec_from_time()
            print("min= ", ScoreBoard.scoreBoardDict['minutes'], " sec= ", ScoreBoard.scoreBoardDict['seconds'])
            self.set_time()
        else:
            Language.currentTextError = Language.periodError
            self.ui.Error_Text.setText(Language.currentTextError)
            QTimer.singleShot(3000, self.clear_error)
        self.scoreboard_change()

    # -------------------------- T O   I N P U T ---------------------------------

    def on_to_check(self):
        if self.ui.To_Checkbox.isChecked():
            self.ui.MinutesTo_Input.setEnabled(True)
            self.ui.SecondsTo_Input.setEnabled(True)
            ScoreBoard.scoreBoardDict['toCheck'] = True
        else:
            self.ui.MinutesTo_Input.setEnabled(False)
            self.ui.SecondsTo_Input.setEnabled(False)
            ScoreBoard.scoreBoardDict['toCheck'] = False
        self.scoreboard_change()

    def on_to_input(self):
        ScoreBoard.scoreBoardDict['setToMinutes'] = self.ui.MinutesTo_Input.value()
        ScoreBoard.scoreBoardDict['setToSeconds'] = self.ui.SecondsTo_Input.value()
        ScoreBoard.scoreBoardDict['totalToSec'] = get_sec_from_totime()
        self.scoreboard_change()

    # -------------------------- B U T T O N S ------------------------------------


        

    def on_update_team(self):
        self.save(Files.filesDict['homePath'], ScoreBoard.scoreBoardDict['homeTeam'])
        self.save(Files.filesDict['awayPath'], ScoreBoard.scoreBoardDict['awayTeam'])

    def on_reset_timer(self, period=1):
        if not period:
            period = 1
        print("period = ", period)
        ScoreBoard.scoreBoardDict['period'] = period
        ScoreBoard.scoreBoardDict['totalSetPeriodSec'] = get_sec_from_period()
        ScoreBoard.scoreBoardDict['startPeriodsec'] = get_sec_from_start_period()
        ScoreBoard.scoreBoardDict['stopPeriodsec'] = get_sec_from_end_period()
        if Settings.settingsDict['stopWatch'] or Settings.settingsDict['currentTime']:
            ScoreBoard.scoreBoardDict['minutes'] = ScoreBoard.scoreBoardDict['startPeriodsec'] // 60
            ScoreBoard.scoreBoardDict['seconds'] = ScoreBoard.scoreBoardDict['startPeriodsec'] % 60
            ScoreBoard.scoreBoardDict['setMinutes'] = ScoreBoard.scoreBoardDict['minutes']
            ScoreBoard.scoreBoardDict['setSeconds'] = ScoreBoard.scoreBoardDict['seconds']
        elif Settings.settingsDict['timer']:
            if Settings.settingsDict['timerPresetEnable']:
                self.ui.MinutesPeriod_Input.setValue(Settings.settingsDict['timerPresetValue'])
                self.ui.SecondsPeriod_Input.setValue(0)
            ScoreBoard.scoreBoardDict['minutes'] = ScoreBoard.scoreBoardDict['stopPeriodsec'] // 60
            ScoreBoard.scoreBoardDict['seconds'] = ScoreBoard.scoreBoardDict['stopPeriodsec'] % 60
            ScoreBoard.scoreBoardDict['setMinutes'] = ScoreBoard.scoreBoardDict['minutes']
            ScoreBoard.scoreBoardDict['setSeconds'] = ScoreBoard.scoreBoardDict['seconds']
        self.reset_overtime()
        ScoreBoard.scoreBoardDict['first'] = True
        ScoreBoard.scoreBoardDict['totalTimeSec'] = get_sec_from_time()
        ScoreBoard.scoreBoardDict['totalSetTimeSec'] = get_sec_from_settime()
        ScoreBoard.scoreBoardDict['totalCurrentPeriodSec'] = get_sec_from_current_period()
        self.ui.Period_Label.setText(str(ScoreBoard.scoreBoardDict['period']))
        self.set_period_time()
        self.set_input_time()
        self.set_time()

    def on_reset_score(self):
        ScoreBoard.scoreBoardDict['awayScore'] = 0
        ScoreBoard.scoreBoardDict['homeScore'] = 0
        self.ui.AwayScore_Label.setText(str(ScoreBoard.scoreBoardDict['awayScore']))
        self.ui.HomeScore_Label.setText(str(ScoreBoard.scoreBoardDict['homeScore']))
        self.save(Files.filesDict['awayScorePath'], str(ScoreBoard.scoreBoardDict['awayScore']))
        self.save(Files.filesDict['homeScorePath'], str(ScoreBoard.scoreBoardDict['homeScore']))
        self.scoreboard_change()

    def on_swap_button(self):
        temp = ScoreBoard.scoreBoardDict['homeTeam']
        ScoreBoard.scoreBoardDict['homeTeam'] = ScoreBoard.scoreBoardDict['awayTeam']
        ScoreBoard.scoreBoardDict['awayTeam'] = temp
        temp = ScoreBoard.scoreBoardDict['homeScore']
        ScoreBoard.scoreBoardDict['homeScore'] = ScoreBoard.scoreBoardDict['awayScore']
        ScoreBoard.scoreBoardDict['awayScore'] = temp
        self.on_update_team()
        self.ui.AwayName_Input.setText(ScoreBoard.scoreBoardDict['awayTeam'])
        self.ui.HomeName_Input.setText(ScoreBoard.scoreBoardDict['homeTeam'])
        self.ui.AwayScore_Label.setText(str(ScoreBoard.scoreBoardDict['awayScore']))
        self.ui.HomeScore_Label.setText(str(ScoreBoard.scoreBoardDict['homeScore']))
        self.save(Files.filesDict['awayScorePath'], str(ScoreBoard.scoreBoardDict['awayScore']))
        self.save(Files.filesDict['homeScorePath'], str(ScoreBoard.scoreBoardDict['homeScore']))
        self.scoreboard_change()

    def on_half_time(self):
        if ScoreBoard.scoreBoardDict['timerRunning']:
            self.start_timer()
        if ScoreBoard.scoreBoardDict['pregame']:
            self.on_pregame()
        if not Settings.settingsDict['halfTime']:
            Settings.settingsDict['halfTime'] = True
            self.on_period_up()
            ScoreBoard.scoreBoardDict['minutes'] = 0
            ScoreBoard.scoreBoardDict['seconds'] = 0
            Language.HalfTimeText = Language.HalfActive
            self.ui.HalfTime_Button.setText(Language.HalfTimeText)
            Dynamic.dynamicDict['halfOn'] = True
            self.start_timer()
            if Obs.obsDict['inHalfTimeScene'] != "":
                try:
                    self.obs.call(requests.SetCurrentScene(Obs.obsDict['inHalfTimeScene']))
                except:
                    pass

        else:
            Settings.settingsDict['halfTime'] = False
            if Obs.obsDict['inGameScene'] != "":
                try:
                    self.obs.call(requests.SetCurrentScene(Obs.obsDict['inGameScene']))
                except:
                    pass
            self.ui.HalfTimeClock_Label.setText("00:00")
            self.save(Files.filesDict['halfTimePath'], "00:00")
            Language.HalfTimeText = Language.Half
            self.ui.HalfTime_Button.setText(Language.HalfTimeText)
            Dynamic.dynamicDict['halfOn'] = False
            self.on_reset_timer(ScoreBoard.scoreBoardDict['period'])

    def on_pregame(self):
        if (ScoreBoard.scoreBoardDict['timerRunning'] and not Settings.settingsDict['currentTime']) or ScoreBoard.scoreBoardDict['period'] > 1:
            return
        if not ScoreBoard.scoreBoardDict['pregame']:
            self.pm = QPixmap("reddot16.png")
            self.ui.ImageLabel.setPixmap(self.pm)
            ScoreBoard.scoreBoardDict['pregame'] = True
            self.ui.CurrentTime_Radio.setChecked(True)
            if Obs.obsDict['inPreGameScene'] != "":
                try:
                    self.obs.call(requests.SetCurrentScene(Obs.obsDict['inPreGameScene']))
                except:
                    pass

        else:
            self.pm = QPixmap("greydot16.png")
            self.ui.ImageLabel.setPixmap(self.pm)
            ScoreBoard.scoreBoardDict['pregame'] = False
            self.ui.StopWatch_Radio.setChecked(True)
            if Obs.obsDict['inGameScene'] != "":
                try:
                    self.obs.call(requests.SetCurrentScene(Obs.obsDict['inGameScene']))
                except:
                    pass

    # ------------------------ S E T T I N G S ------------------------------------

    def on_load_settings(self, checked):
        if checked:
            Settings.settingsDict['loadSettings'] = True
            self.ui.Save_Data_CheckBox.setEnabled(True)
        else:
            Settings.settingsDict['loadSettings'] = False
            self.ui.Save_Data_CheckBox.setEnabled(False)
        self.save_settings(checked)

    def save_settings(self, checked):
        if not checked:
            self.settings.setValue('settings/loadSettings', False)

        else:
            self.settings_change()
            self.keys_change()
            self.language_change()
            self.play_change()
            self.obs_change()
            self.scoreboard_change()


    def scoreboard_change(self):
        if Settings.settingsDict['saveData']:
            self.settings.beginGroup('scoreBoard')
            for key, value in ScoreBoard.scoreBoardDict.items():
                self.settings.setValue(key, value)
            self.settings.endGroup()

    def settings_change(self):
        if Settings.settingsDict['loadSettings']:
            self.settings.beginGroup('settings')
            for key, value in Settings.settingsDict.items():
                print(key, value)
                self.settings.setValue(key, value)
            self.settings.endGroup()

    def remote_change(self):
        if Settings.settingsDict['loadSettings']:
            self.settings.beginGroup('remote')
            if Dynamic.dynamicDict['startServerOn']:
                self.settings.setValue('startServerOn', True)
            else:
                self.settings.setValue('startServerOn', False)
            self.settings.endGroup()

    def keys_change(self):
        if Settings.settingsDict['loadSettings']:
            self.settings.beginGroup('keys')
            for key, value in Keys.keysDict.items():
                if value or value == False:
                    self.settings.setValue(key, value)
                else:
                    self.settings.setValue(key, [0, 0])
            self.settings.endGroup()

    def play_change(self):
        if Settings.settingsDict['loadSettings']:
            self.settings.beginGroup('play')
            for key, value in Play.playDict.items():
                if key == 'player':
                    continue
                self.settings.setValue(key, value)
            self.settings.endGroup()

    def obs_change(self):
        if Settings.settingsDict['loadSettings']:
            self.settings.beginGroup('obs')
            for key, value in Obs.obsDict.items():
                if key == 'errList':
                    continue
                self.settings.setValue(key, value)
            self.settings.endGroup()

    def language_change(self):
        if Settings.settingsDict['loadSettings']:
            self.settings.beginGroup('language')
            self.settings.setValue('currentLanguage', Language.currentLanguage)
            self.settings.endGroup()

    def load_settings(self):
        self.ui.Load_Settings_CheckBox.setChecked(False)
        self.settings_load()
        # self.play_load()
        # self.keys_load()
        # self.language_load()
        # self.remote_load()
        # self.obs_load()
        self.ui.Load_Settings_CheckBox.toggled.connect(self.on_load_settings)
        self.ui.Load_Settings_CheckBox.setChecked(True)


    def settings_load(self):
        self.settings.beginGroup('settings')
        for key in ['writeFile', 'writeXml', 'stopWatch', 'timer', 'currentTime', 'tenth', 'timerPresetEnable', 'customSpeed',
                    'customTenthSpeed', 'saveData', 'alwaysOnTop']:
            Settings.settingsDict[key] = self.settings.value(key, False, bool)
            print(key, " = ", Settings.settingsDict[key])
        for key in ['speed', 'tenthSpeed', 'timerPresetValue']:
            Settings.settingsDict[key] = self.settings.value(key, 0, int)
            print(key, " = ", Settings.settingsDict[key])
        self.settings.endGroup()
        print('setting speed = ', Settings.settingsDict['speed'])
        self.ui.Speed_Input.setValue(Settings.settingsDict['speed'])
        print('setting micro speed = ', Settings.settingsDict['tenthSpeed'])
        self.ui.MicroSpeed_Input.setValue(Settings.settingsDict['tenthSpeed'])

        if Settings.settingsDict['writeFile']:
            self.ui.Use_Files_CheckBox.setChecked(True)
        if Settings.settingsDict['writeXml']:
            self.ui.Use_Xml_CheckBox.setChecked(True)
        print("stopwatch: ", Settings.settingsDict['stopWatch'])
        if Settings.settingsDict['stopWatch']:
            self.ui.StopWatch_Radio.setChecked(True)
        print("timer: ", Settings.settingsDict['timer'])
        if Settings.settingsDict['timer']:
            self.ui.Timer_Radio.setChecked(True)
        print("currenttime: ", Settings.settingsDict['currentTime'])
        if Settings.settingsDict['currentTime']:
            self.ui.CurrentTime_Radio.setChecked(True)
        if Settings.settingsDict['tenth']:
            self.ui.OneTenth_Checkbox.setChecked(True)
        if Settings.settingsDict['customSpeed']:
            self.ui.Speed_CheckBox.setChecked(True)
        if Settings.settingsDict['customTenthSpeed']:
            self.ui.MicroSpeed_CheckBox.setChecked(True)
        if Settings.settingsDict['timerPresetEnable']:
            self.ui.TimerPreset_Checkbox.setChecked(True)
        if Settings.settingsDict['timerPresetValue'] == 10:
            self.ui.TenM_Radio.setChecked(True)
        elif Settings.settingsDict['timerPresetValue'] == 12:
            self.ui.TwelveM_Radio.setChecked(True)
        elif Settings.settingsDict['timerPresetValue'] == 15:
            self.ui.FifteenM_Radio.setChecked(True)
        elif Settings.settingsDict['timerPresetValue'] == 20:
            self.ui.TwentyM_Radio.setChecked(True)
        elif Settings.settingsDict['timerPresetValue'] == 30:
            self.ui.ThirtyM_Radio.setChecked(True)
        elif Settings.settingsDict['timerPresetValue'] == 45:
            self.ui.FortyFiveM_Radio.setChecked(True)
        if Settings.settingsDict['saveData']:
            self.ui.Save_Data_CheckBox.setEnabled(True)
            self.ui.Save_Data_CheckBox.setChecked(True)
        if Settings.settingsDict['alwaysOnTop']:
            self.ui.Always_on_top_Checkbox.setChecked(True)


    def on_save_data(self):
        if self.ui.Save_Data_CheckBox.isChecked():
            Settings.settingsDict['saveData'] = True
            self.scoreboard_change()
            self.settings_change()
        else:
            Settings.settingsDict['saveData'] = False
            self.settings_change()

    def on_use_files(self):
        if self.ui.Use_Files_CheckBox.isChecked():
            Settings.settingsDict['writeFile'] = True
        else:
            Settings.settingsDict['writeFile'] = False
        self.settings_change()

    def on_use_xml(self):
        if self.ui.Use_Xml_CheckBox.isChecked():
            Settings.settingsDict['writeXml'] = True
        else:
            Settings.settingsDict['writeXml'] = False
        self.settings_change()

    def on_stopwatch(self):
        self.ui.Clock_Label.setFont(QFont("Arial", 60))
        if ScoreBoard.scoreBoardDict['timerRunning']:
            self.start_timer()
        Settings.settingsDict['stopWatch'] = True
        Settings.settingsDict['timer'] = False
        Settings.settingsDict['currentTime'] = False
        self.on_reset_timer()
        self.stopwatch_enable(True)
        self.update_period_time()
        self.settings_change()

    def on_timer(self):
        self.ui.Clock_Label.setFont(QFont("Arial", 60))
        if ScoreBoard.scoreBoardDict['timerRunning']:
            self.start_timer()
        Settings.settingsDict['stopWatch'] = False
        Settings.settingsDict['timer'] = True
        Settings.settingsDict['currentTime'] = False
        self.on_reset_timer()
        self.timer_enable(True)
        self.settings_change()


    def on_current_time(self):
        self.ui.Clock_Label.setFont(QFont("Arial", 36))
        Settings.settingsDict['stopWatch'] = False
        Settings.settingsDict['timer'] = False
        Settings.settingsDict['currentTime'] = True
        self.current_time_enable(False)
        if ScoreBoard.scoreBoardDict['timerRunning']:
            self.start_timer()
        print("robię reset")
        self.on_reset_timer()
        self.start_timer()
        self.settings_up_period_enable(True)
        self.settings_change()


    def on_always_on_top(self):
        if self.ui.Always_on_top_Checkbox.isChecked():
            Settings.settingsDict['alwaysOnTop'] = True
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            Settings.settingsDict['alwaysOnTop'] = False
        self.show()
        self.settings_change()


    def on_tenth(self):
        if self.ui.OneTenth_Checkbox.isChecked():
            Settings.settingsDict['tenth'] = True
        else:
            Settings.settingsDict['tenth'] = False
        self.settings_change()


    def on_timer_preset(self):
        if self.ui.TimerPreset_Checkbox.isChecked():
            self.timer_presets_enable(True)
            if self.ui.TenM_Radio.isChecked():
                Settings.settingsDict['timerPresetValue'] = 10
            elif self.ui.FifteenM_Radio.isChecked():
                Settings.settingsDict['timerPresetValue'] = 15
            elif self.ui.TwelveM_Radio.isChecked():
                Settings.settingsDict['timerPresetValue'] = 12
            elif self.ui.TwentyM_Radio.isChecked():
                Settings.settingsDict['timerPresetValue'] = 20
            elif self.ui.ThirtyM_Radio.isChecked():
                Settings.settingsDict['timerPresetValue'] = 30
            elif self.ui.FortyFiveM_Radio.isChecked():
                Settings.settingsDict['timerPresetValue'] = 45
            print(Settings.settingsDict['timerPresetValue'])
            if not ScoreBoard.scoreBoardDict['timerRunning']:
                self.on_reset_timer()
        else:
            self.timer_presets_enable(False)
        self.settings_change()


    def on_ten_radio(self):
        if self.ui.TenM_Radio.isChecked():
            Settings.settingsDict['timerPresetValue'] = 10
        if not ScoreBoard.scoreBoardDict['timerRunning']:
            self.on_reset_timer()
        self.settings_change()


    def on_fifteen_radio(self):
        if self.ui.FifteenM_Radio.isChecked():
            Settings.settingsDict['timerPresetValue'] = 15
        if not ScoreBoard.scoreBoardDict['timerRunning']:
            self.on_reset_timer()
        self.settings_change()


    def on_twelve_radio(self):
        if self.ui.TwelveM_Radio.isChecked():
            Settings.settingsDict['timerPresetValue'] = 12
        if not ScoreBoard.scoreBoardDict['timerRunning']:
            self.on_reset_timer()
        self.settings_change()


    def on_twenty_radio(self):
        if self.ui.TwentyM_Radio.isChecked():
            Settings.settingsDict['timerPresetValue'] = 20
        if not ScoreBoard.scoreBoardDict['timerRunning']:
            self.on_reset_timer()
        self.settings_change()


    def on_thirty_radio(self):
        if self.ui.ThirtyM_Radio.isChecked():
            Settings.settingsDict['timerPresetValue'] = 30
        if not ScoreBoard.scoreBoardDict['timerRunning']:
            self.on_reset_timer()
        self.settings_change()


    def on_fortyfive_radio(self):
        if self.ui.FortyFiveM_Radio.isChecked():
            Settings.settingsDict['timerPresetValue'] = 45
        if not ScoreBoard.scoreBoardDict['timerRunning']:
            self.on_reset_timer()
        self.settings_change()


    def on_ten_speed(self):
        if self.ui.MicroSpeed_CheckBox.isChecked():
            Settings.settingsDict['customTenthSpeed'] = True
            Settings.settingsDict['tenthSpeed'] = self.ui.MicroSpeed_Input.value()
        else:
            Settings.settingsDict['customTenthSpeed'] = False
            Settings.settingsDict['tenthSpeed'] = Settings.settingsDict['defaultTenthSpeed']
        self.settings_change()


    def on_speed(self):
        if self.ui.Speed_CheckBox.isChecked():
            Settings.settingsDict['customSpeed'] = True
            Settings.settingsDict['speed'] = self.ui.Speed_Input.value()
        else:
            Settings.settingsDict['customSpeed'] = False
            Settings.settingsDict['speed'] = Settings.settingsDict['defaultSpeed']
        self.settings_change()


    def on_ten_input(self):
        if Settings.settingsDict['customTenthSpeed']:
            Settings.settingsDict['tenthSpeed'] = self.ui.MicroSpeed_Input.value()
            print("Settings.settingsDict['tenthSpeed'] = ", Settings.settingsDict['tenthSpeed'])
            self.settings_change()


    def on_speed_input(self):
        if Settings.settingsDict['customSpeed']:
            Settings.settingsDict['speed'] = self.ui.Speed_Input.value()
            self.settings_change()

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
        Play.playDict['playEnabled'] = enable
        self.play_change()

    def on_play_browse(self):
        filename = QFileDialog.getOpenFileName(self, Language.OpenSound, "", Language.SoundFiles)

        path = os.path.abspath(filename[0])
        if os.path.isdir(path):
            path = ""
        print("filename = ", filename)
        print("path = ", path)
        print("filename[0] = ", filename[0])
        Play.playDict['playPath'] = path
        self.ui.BrowseFile_Input.setText(path)
        self.play_change()

    def on_play_input(self):
        Play.playDict['playPath'] = self.ui.BrowseFile_Input.text()
        print("play text = ", Play.playDict['playPath'])
        self.play_change()

    def play_sound(self):
        state = Play.playDict['player'].state()
        if state == QMediaPlayer.State.PlayingState:
            Play.playDict['player'].stop()
            print("zatrzymuje")
            return
        if Play.playDict['playPath'] == "":
            print("wychodze")
            return
        print("zaczynam")
        # file = 'over.mp3'
        media = QUrl.fromLocalFile(Play.playDict['playPath'])
        content = QMediaContent(media)
        Play.playDict['player'].setMedia(content)
        Play.playDict['player'].setVolume(Play.playDict['playVolume'])
        Play.playDict['player'].stateChanged.connect(self.state)
        Play.playDict['player'].play()

    def state(self, state):
        if state == QMediaPlayer.State.PlayingState:
            self.ui.StopSound_Button.setHidden(False)
        elif state == QMediaPlayer.State.StoppedState:
            self.ui.StopSound_Button.setHidden(True)
        print(state)

    def on_volume(self, volume):
        self.ui.VolumeVal_Label.setText(str(volume))
        Play.playDict['player'].setVolume(volume)
        Play.playDict['playVolume'] = volume
        self.play_change()

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
        self.language_change()

    def polski(self):
        self.ui.actionPolski.setChecked(True)
        self.ui.actionEnglish.setChecked(False)
        app.removeTranslator(self.translator)
        self.translator.load('mainwindow_pl_PL')
        app.installTranslator(self.translator)
        Language.retranslateUi()
        self.ui.retranslateUi(self)
        self.additional_translate()
        self.language_change()

    def additional_translate(self):
        self.labelStatus.setText(Language.ConnectionToOBS)
        self.connectObsStatus.setText(self.ui.ConnectObs_Label.text())
        self.remoteLabelStatus.setText(Language.RemoteLabelStatus)
        self.remoteConnectStatus.setText(self.ui.Status_Label.text())
        self.remoteNrLabelStatus.setText(Language.NrOfConnections)
        if Dynamic.dynamicDict['halfOn']:
            self.ui.HalfTime_Button.setText(Language.HalfActive)
        else:
            self.ui.HalfTime_Button.setText(Language.Half)
        if Dynamic.dynamicDict['connectObsButtonOn']:
            self.ui.ConnectObs_Button.setText(Language.Disconnect)
        else:
            self.ui.ConnectObs_Button.setText(Language.Connect)
        if Dynamic.dynamicDict['connectObsLabelOn']:
            self.set_text_obs_status(Language.Connected)
        else:
            self.set_text_obs_status(Language.NotConnected)
        if Dynamic.dynamicDict['startServerOn']:
            self.ui.Remote_Button.setText(Language.StopServer)
            self.set_text_ip(True)
        else:
            self.ui.Remote_Button.setText(Language.StartServer)
            self.set_text_ip(False)
        if Dynamic.dynamicDict['remoteStatus'] is None:
            self.set_text_remote_status(Language.Listening)
        elif Dynamic.dynamicDict['remoteStatus']:
            self.set_text_remote_status(Language.Connected)
        else:
            self.set_text_remote_status(Language.NotConnected)

    # -------------------------------- O B S ---------------------------------------

    def error_box(self, title, text):
        QMessageBox.critical(self, title, text)

    def set_text_obs_status(self, text):
        self.ui.ConnectObs_Label.setText(text)
        self.connectObsStatus.setText(text)
        return

    def on_obs_button(self):
        self.set_text_obs_status(Language.Connecting)
        QTimer.singleShot(50, self.on_obs_button1)

    def on_obs_button1(self):

        self.obs = obsws(Obs.obsDict['host'], Obs.obsDict['port'], Obs.obsDict['password'])
        try:
            self.obs.connect()
            self.ui.ConnectObs_Button.setText(Language.Disconnect)
            self.set_text_obs_status(Language.Connected)
            Dynamic.dynamicDict['connectObsButtonOn'] = True
            Dynamic.dynamicDict['connectObsLabelOn'] = True
            Obs.obsDict['connected'] = True
            self.ui.ConnectObs_Button.clicked.disconnect()
            self.ui.ConnectObs_Button.clicked.connect(self.obs_disconnect)
            scenes = self.obs.call(requests.GetSceneList()).getScenes()
            self.ui.InGameScene_comboBox.addItem("----------")
            self.ui.HalfTimeScene_comboBox.addItem("----------")
            self.ui.PreGameScene_comboBox.addItem("----------")
            self.ui.ClockSource_comboBox.addItem("----------")
            self.ui.OverTimeClockSource_comboBox.addItem("----------")
            self.ui.HalfTimeClockSource_comboBox.addItem("----------")
            self.ui.CurTimeSource_comboBox.addItem("----------")
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
                self.ui.PreGameScene_comboBox.addItem(scene['name'])
            sources = self.obs.call(requests.GetSourcesList()).getSources()
            for source in sources:
                if source['typeId'].startswith("text"):
                    self.ui.ClockSource_comboBox.addItem(source['name'])
                    self.ui.OverTimeClockSource_comboBox.addItem(source['name'])
                    self.ui.HalfTimeClockSource_comboBox.addItem(source['name'])
                    self.ui.CurTimeSource_comboBox.addItem(source['name'])
                    self.ui.HomeSource_comboBox.addItem(source['name'])
                    self.ui.AwaySource_comboBox.addItem(source['name'])
                    self.ui.HomeScoreSource_comboBox.addItem(source['name'])
                    self.ui.AwayScoreSource_comboBox.addItem(source['name'])
                    self.ui.PeriodSource_comboBox.addItem(source['name'])
                elif source['typeId'].startswith("image"):
                    self.ui.HomeGraphicSource_comboBox.addItem(source['name'])
                    self.ui.AwayGraphicSource_comboBox.addItem(source['name'])
        except IOError as e:
            print(e)
            self.error_box(Language.ConnectionToOBS, Language.ObsConError)
            self.set_text_obs_status(Language.NotConnected)
        self.obs_change()

    def obs_disconnect(self):
        self.obs.disconnect()
        Obs.obsDict['connected'] = False
        self.ui.InGameScene_comboBox.clear()
        self.ui.HalfTimeScene_comboBox.clear()
        self.ui.PreGameScene_comboBox.clear()
        self.ui.ClockSource_comboBox.clear()
        self.ui.ClockSource_comboBox.clear()
        self.ui.OverTimeClockSource_comboBox.clear()
        self.ui.HalfTimeClockSource_comboBox.clear()
        self.ui.CurTimeSource_comboBox.clear()
        self.ui.HomeSource_comboBox.clear()
        self.ui.AwaySource_comboBox.clear()
        self.ui.HomeScoreSource_comboBox.clear()
        self.ui.AwayScoreSource_comboBox.clear()
        self.ui.PeriodSource_comboBox.clear()
        self.ui.HomeGraphicSource_comboBox.clear()
        self.ui.AwayGraphicSource_comboBox.clear()
        self.ui.ConnectObs_Button.setText(Language.Connect)
        self.set_text_obs_status(Language.NotConnected)
        Dynamic.dynamicDict['connectObsButtonOn'] = False
        Dynamic.dynamicDict['connectObsLabelOn'] = False
        self.ui.ConnectObs_Button.clicked.disconnect()
        self.ui.ConnectObs_Button.clicked.connect(self.on_obs_button)
        self.obs_change()


    def obs_clock_source_set(self, source):
        if int(self.ui.ClockSource_comboBox.currentIndex()) == 0:
            Obs.obsDict['clockSource'] = ""
        else:
            Obs.obsDict['clockSource'] = source
        self.obs_change()

    def obs_overtime_clock_source_set(self, source):
        if int(self.ui.OverTimeClockSource_comboBox.currentIndex()) == 0:
            Obs.obsDict['overTimeSource'] = ""
        else:
            Obs.obsDict['overTimeSource'] = source
        self.obs_change()

    def obs_halftime_clock_source_set(self, source):
        if int(self.ui.HalfTimeClockSource_comboBox.currentIndex()) == 0:
            Obs.obsDict['halfTimeSource'] = ""
        else:
            Obs.obsDict['halfTimeSource'] = source
        self.obs_change()

    def obs_curtime_clock_source_set(self, source):
        if int(self.ui.CurTimeSource_comboBox.currentIndex()) == 0:
            Obs.obsDict['curTimeSource'] = ""
        else:
            Obs.obsDict['curTimeSource'] = source
        self.obs_change()

    def obs_home_source_set(self, source):
        if int(self.ui.HomeSource_comboBox.currentIndex()) == 0:
            Obs.obsDict['homeSource'] = ""
        else:
            Obs.obsDict['homeSource'] = source
        self.obs_change()

    def obs_away_source_set(self, source):
        if int(self.ui.AwaySource_comboBox.currentIndex()) == 0:
            Obs.obsDict['awaySource'] = ""
        else:
            Obs.obsDict['awaySource'] = source
        self.obs_change()

    def obs_home_score_source_set(self, source):
        if int(self.ui.HomeScoreSource_comboBox.currentIndex()) == 0:
            Obs.obsDict['homeScoreSource'] = ""
        else:
            Obs.obsDict['homeScoreSource'] = source
        self.obs_change()

    def obs_away_score_source_set(self, source):
        if int(self.ui.AwayScoreSource_comboBox.currentIndex()) == 0:
            Obs.obsDict['awayScoreSource'] = ""
        else:
            Obs.obsDict['awayScoreSource'] = source
        self.obs_change()

    def obs_period_source_set(self, source):
        if int(self.ui.PeriodSource_comboBox.currentIndex()) == 0:
            Obs.obsDict['periodSource'] = ""
        else:
            Obs.obsDict['periodSource'] = source
        self.obs_change()

    def obs_home_graphics_source_set(self, source):
        if int(self.ui.HomeGraphicSource_comboBox.currentIndex()) == 0:
            Obs.obsDict['homeGraphicSource'] = ""
        else:
            Obs.obsDict['homeGraphicSource'] = source
            if Obs.obsDict['homeGraphicFile'] != "":
                self.obs.call(requests.SetSourceSettings(source, {'file': Obs.obsDict['homeGraphicFile']}))
        self.obs_change()

    def obs_away_graphics_source_set(self, source):
        if int(self.ui.AwayGraphicSource_comboBox.currentIndex()) == 0:
            Obs.obsDict['awayGraphicSource'] = ""
        else:
            Obs.obsDict['awayGraphicSource'] = source
            if Obs.obsDict['awayGraphicFile'] != "":
                self.obs.call(requests.SetSourceSettings(source, {'file': Obs.obsDict['awayGraphicFile']}))
        self.obs_change()

    def obs_in_game_scene_set(self, scene):
        if int(self.ui.InGameScene_comboBox.currentIndex()) == 0:
            Obs.obsDict['inGameScene'] = ""
        else:
            Obs.obsDict['inGameScene'] = scene
        self.obs_change()

    def obs_half_time_scene_set(self, scene):
        if int(self.ui.HalfTimeScene_comboBox.currentIndex()) == 0:
            Obs.obsDict['inHalfTimeScene'] = ""
        else:
            Obs.obsDict['inHalfTimeScene'] = scene
        self.obs_change()

    def obs_pre_game_scene_set(self, scene):
        if int(self.ui.PreGameScene_comboBox.currentIndex()) == 0:
            Obs.obsDict['inPreGameScene'] = ""
        else:
            Obs.obsDict['inPreGameScene'] = scene
        self.obs_change()

    def on_home_graphics_browse(self):
        filename = QFileDialog.getOpenFileName(self, Language.OpenImage, "", Language.ImageFiles)
        path = os.path.abspath(filename[0])
        if os.path.isdir(path):
            path = ""
            return
        Obs.obsDict['homeGraphicFile'] = path
        self.ui.HomeGraphicFile_Input.setText(path)
        if Obs.obsDict['homeGraphicSource'] != "":
            self.obs.call(requests.SetSourceSettings(Obs.obsDict['homeGraphicSource'], {'file': path}))

        self.obs_change()

    def on_away_graphics_browse(self):
        filename = QFileDialog.getOpenFileName(self, Language.OpenImage, "", Language.ImageFiles)
        path = os.path.abspath(filename[0])
        if os.path.isdir(path):
            path = ""
            return
        Obs.obsDict['awayGraphicFile'] = path
        self.ui.AwayGraphicFile_Input.setText(path)
        if Obs.obsDict['awayGraphicSource'] != "":
            self.obs.call(requests.SetSourceSettings(Obs.obsDict['awayGraphicSource'], {'file': path}))
        self.obs_change()

    def set_time_obs(self, source, time):
        try:
            self.obs.call(requests.SetSourceSettings(source, {'text': time}))
        except:
            print("CheckedTrue")
            self.error.setChecked(True)

    def obs_connection_lost(self):
        self.obs_disconnect()
        self.error.stateChanged.disconnect()
        self.error.setChecked(False)
        self.error.stateChanged.connect(self.obs_connection_lost)
        self.error_box(Language.ConnectionToOBS, Language.ConnectionOBSLost)

    def on_save_obs(self):
        if not Obs.obsDict['connected']:
            self.error_box(Language.SaveError, Language.MustConnect)
            return
        filename = QFileDialog.getSaveFileName(self, "Save OBS Settings", os.path.dirname(__file__), "OBS Settings Files (*.obs)")
        path = os.path.abspath(filename[0])
        if os.path.isdir(path):
            return
        settings = QSettings(path, QSettings.IniFormat)
        settings.setValue("ingamescene", Obs.obsDict['inGameScene'])
        settings.setValue("halftimescene", Obs.obsDict['inHalfTimeScene'])
        settings.setValue("pregamescene", Obs.obsDict['inPreGameScene'])
        settings.setValue("clocksource", Obs.obsDict['clockSource'])
        settings.setValue("overtimeclocksource", Obs.obsDict['overTimeSource'])
        settings.setValue("halftimeclocksource", Obs.obsDict['halfTimeSource'])
        settings.setValue("curtimeclocksource", Obs.obsDict['curTimeSource'])
        settings.setValue("homesource", Obs.obsDict['homeSource'])
        settings.setValue("awaysource", Obs.obsDict['awaySource'])
        settings.setValue("homescoresource", Obs.obsDict['homeScoreSource'])
        settings.setValue("awayscoresource", Obs.obsDict['awayScoreSource'])
        settings.setValue("periodsource", Obs.obsDict['periodSource'])
        settings.setValue("homegraphicsource", Obs.obsDict['homeGraphicSource'])
        settings.setValue("awaygraphicsource", Obs.obsDict['awayGraphicSource'])
        settings.setValue("homegraphicfile", Obs.obsDict['homeGraphicFile'])
        settings.setValue("awaygraphicfile", Obs.obsDict['awayGraphicFile'])

    def on_load_obs(self):
        if not Obs.obsDict['connected']:
            self.error_box("Błąd odczytu.", "Musisz być połączpny z Obs.obsDict['']")
            return
        filename = QFileDialog.getOpenFileName(self, "Load OBS Settings", os.path.dirname(__file__), "Obs Settings Files (*.obs)")
        path = os.path.abspath(filename[0])
        if os.path.isdir(path):
            return
        settings = QSettings(path, QSettings.IniFormat)
        if Obs.obsDict['errlist']:
            Obs.obsDict['errlist'].clear()
        self.load_obs_to(settings, self.ui.InGameScene_comboBox, "ingamescene", Obs.obsDict['inGameScene'])
        self.load_obs_to(settings, self.ui.HalfTimeScene_comboBox, "halftimescene", Obs.obsDict['inHalfTimeScene'])
        self.load_obs_to(settings, self.ui.PreGameScene_comboBox, "pregamescene", Obs.obsDict['inPreGameScene'])
        self.load_obs_to(settings, self.ui.ClockSource_comboBox, "clocksource", Obs.obsDict['clockSource'])
        self.load_obs_to(settings, self.ui.OverTimeClockSource_comboBox, "overtimeclocksource", Obs.obsDict['overTimeSource'])
        self.load_obs_to(settings, self.ui.HalfTimeClockSource_comboBox, "halftimeclocksource", Obs.obsDict['halfTimeSource'])
        self.load_obs_to(settings, self.ui.CurTimeSource_comboBox, "curtimeclocksource",
                         Obs.obsDict['curTimeSource'])
        self.load_obs_to(settings, self.ui.HomeSource_comboBox, "homesource", Obs.obsDict['homeSource'])
        self.load_obs_to(settings, self.ui.AwaySource_comboBox, "awaysource", Obs.obsDict['awaySource'])
        self.load_obs_to(settings, self.ui.HomeScoreSource_comboBox, "homescoresource", Obs.obsDict['homeScoreSource'])
        self.load_obs_to(settings, self.ui.AwayScoreSource_comboBox, "awayscoresource", Obs.obsDict['awayScoreSource'])
        self.load_obs_to(settings, self.ui.PeriodSource_comboBox, "periodsource", Obs.obsDict['periodSource'])
        self.load_obs_to(settings, self.ui.HomeGraphicSource_comboBox, "homegraphicsource", Obs.obsDict['homeGraphicSource'])
        self.load_obs_to(settings, self.ui.AwayGraphicSource_comboBox, "awaygraphicsource", Obs.obsDict['awayGraphicSource'])
        self.load_obs_file_to(settings, self.ui.HomeGraphicFile_Input, "homegraphicfile", Obs.obsDict['homeGraphicFile'])
        self.load_obs_file_to(settings, self.ui.AwayGraphicFile_Input, "awaygraphicfile", Obs.obsDict['awayGraphicFile'])

        if Obs.obsDict['errlist']:
            self.error_box("Sprawdź Zbiór Scen.", "Brak źródeł o nazwie:\n" + self.list_errlist())


    def load_obs_to(self, settings, widget, key, obsvar ):
        obsvar = settings.value(key, "", str)
        if widget.findText(obsvar) != -1 and obsvar != "":
            widget.setCurrentText(obsvar)
        elif obsvar == "":
            widget.setCurrentText("----------")
        else:
            Obs.obsDict['errlist'].append(obsvar)
            obsvar = ""
            widget.setCurrentText("----------")

    def load_obs_file_to(self, settings, widget, key, obsvar ):
        obsvar = settings.value(key, "", str)
        if not os.path.isfile(obsvar) and not obsvar == "":
            Obs.obsDict['errlist'].append("brak pliku: " + obsvar)
            obsvar = ""
        widget.setText(obsvar)

    def list_errlist(self):
        text = ""
        for error in Obs.obsDict['errlist']:
            text += "- " + error + "\n"
        return text

    # ----------------------------- R E M O T E  -----------------------------------

    def on_remote_button(self):
        if self.ui.Remote_Button.text() == Language.StartServer:
            self.ui.Remote_Button.setText(Language.StopServer)
            Dynamic.dynamicDict['startServerOn'] = True
            self.server = MyServer(self)
        else:
            self.ui.Remote_Button.setText(Language.StartServer)
            Dynamic.dynamicDict['startServerOn'] = False
            self.server.my_close()
            self.server = None
        self.remote_change()

    def set_text_remote_status(self, text):
        self.ui.Status_Label.setText(text)
        self.remoteConnectStatus.setText(text)
        if text == Language.NotConnected:
            Dynamic.dynamicDict['remoteStatus'] = False
            self.ui.Status_Label.setStyleSheet(u"color: rgb(255, 0, 0);")
        elif text == Language.Listening:
            Dynamic.dynamicDict['remoteStatus'] = None
            self.ui.Status_Label.setStyleSheet(u"color: rgb(0, 0, 255);")
        elif text == Language.Connected:
            Dynamic.dynamicDict['remoteStatus'] = True
            self.ui.Status_Label.setStyleSheet(u"color: rgb(0, 255, 0);")

    def set_text_ip(self, onoff):
        if not onoff:
            self.ui.IP_Label.setText(Language.IpAddressesDefault)
        else:
            self.ui.IP_Label.setText(Language.IpAddresses + ', '.join(self.server.list))

    def update_nr_clients(self, number):
        print("Execute update.")
        self.remoteNrConnStatus.setText(str(number))

    def set_time_remote(self, time):
        try:
            self.server.send(time)
        except:
            print("CheckedTrue")
            self.error.setChecked(True)

    # --------------------------------- H O T K E Y S ------------------------------

    def on_hotkeys(self):
        if self.ui.Hotkey_Checkbox.isChecked():
            self.enable_hotkeys(True)

        else:
            self.enable_hotkeys(False)


    def enable_hotkeys(self, enable):
        self.ui.HomeUp_Key.event
        self.ui.HomeUp_Key.setEnabled(enable)
        self.ui.HomeUp2_Key.setEnabled(enable)
        self.ui.HomeDwn_Key.setEnabled(enable)
        self.ui.AwayUp_Key.setEnabled(enable)
        self.ui.AwayUp2_Key.setEnabled(enable)
        self.ui.AwayDwn_Key.setEnabled(enable)
        self.ui.StartStop_Key.setEnabled(enable)
        self.ui.ResetTimer_Key.setEnabled(enable)
        self.ui.HalfTime_Key.setEnabled(enable)
        self.ui.ResetScore_Key.setEnabled(enable)
        self.ui.SwapTeams_Key.setEnabled(enable)
        self.ui.PeriodUp_Key.setEnabled(enable)
        self.ui.PeriodDwn_Key.setEnabled(enable)
        self.ui.StopSund_Key.setEnabled(enable)
        self.ui.RemoteOnOff_Key.setEnabled(enable)
        self.ui.ObsConnect_Key.setEnabled(enable)
        if enable:
            self.ui.HomeUp_Key.installEventFilter(self)
            self.ui.HomeUp2_Key.installEventFilter(self)
            self.ui.HomeDwn_Key.installEventFilter(self)
            self.ui.AwayUp_Key.installEventFilter(self)
            self.ui.AwayUp2_Key.installEventFilter(self)
            self.ui.AwayDwn_Key.installEventFilter(self)
            self.ui.StartStop_Key.installEventFilter(self)
            self.ui.ResetTimer_Key.installEventFilter(self)
            self.ui.HalfTime_Key.installEventFilter(self)
            self.ui.ResetScore_Key.installEventFilter(self)
            self.ui.SwapTeams_Key.installEventFilter(self)
            self.ui.PeriodUp_Key.installEventFilter(self)
            self.ui.PeriodDwn_Key.installEventFilter(self)
            self.ui.StopSund_Key.installEventFilter(self)
            self.ui.RemoteOnOff_Key.installEventFilter(self)
            self.ui.ObsConnect_Key.installEventFilter(self)
            #app.installEventFilter(self)
            self.installEventFilter(self)
            self.ui.Settings.installEventFilter(self)

        else:
            self.ui.HomeUp_Key.removeEventFilter(self)
            self.ui.HomeUp2_Key.removeEventFilter(self)
            self.ui.HomeDwn_Key.removeEventFilter(self)
            self.ui.AwayUp_Key.removeEventFilter(self)
            self.ui.AwayUp2_Key.removeEventFilter(self)
            self.ui.AwayDwn_Key.removeEventFilter(self)
            self.ui.StartStop_Key.removeEventFilter(self)
            self.ui.ResetTimer_Key.removeEventFilter(self)
            self.ui.HalfTime_Key.removeEventFilter(self)
            self.ui.ResetScore_Key.removeEventFilter(self)
            self.ui.SwapTeams_Key.removeEventFilter(self)
            self.ui.PeriodUp_Key.removeEventFilter(self)
            self.ui.PeriodDwn_Key.removeEventFilter(self)
            self.ui.StopSund_Key.removeEventFilter(self)
            self.ui.RemoteOnOff_Key.removeEventFilter(self)
            self.ui.ObsConnect_Key.removeEventFilter(self)
            self.removeEventFilter(self)
            self.ui.Settings.removeEventFilter(self)

    def eventFilter(self, watched, event):
        if isinstance(event, QtGui.QKeyEvent):
            pass
            if event.isAutoRepeat():
                pass
                return True
        else:
            return False
        if event.type() is QEvent.KeyPress:
            # if watched.objectName() == "MainWindowWindow":
            #     print("wychodze")
            #     return False
            # print("watched", watched)
            self.vk = event.nativeVirtualKey()
            mod = event.modifiers()
            intmod = int(mod)
            if self.vk in [16, 17, 18]:
                self.vk = 0
            print("vk = ", self.vk)
            print("intmod = " , intmod)
            name = CharMap.get(self.vk)
            if watched is self.ui.HomeUp_Key:
                if self.vk == 46:
                   if self.check_del(watched, Keys.keysDict['homeUp']):
                        return True

                self.ui.HomeUp_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['homeUp'] = [self.vk, intmod]

                ktory = 1
                return True
            elif watched is self.ui.HomeUp2_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['homeUp2']):
                        return True
                self.ui.HomeUp2_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['homeUp2'] = [self.vk, intmod]
                ktory = 2
                return True
            elif watched is self.ui.HomeDwn_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['homeDown']):
                        return True

                self.ui.HomeDwn_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['homeDown'] = [self.vk, intmod]
                ktory = 3
                return True
            elif watched is self.ui.AwayUp_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['awayUp']):
                        return True
                self.ui.AwayUp_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['awayUp'] = [self.vk, intmod]
                ktory = 4
                return True
            elif watched is self.ui.AwayUp2_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['awayUp2']):
                        return True
                self.ui.AwayUp2_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['awayUp2'] = [self.vk, intmod]
                return True
            elif watched is self.ui.AwayDwn_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['awayDown']):
                        return True

                self.ui.AwayDwn_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['awayDown'] = [self.vk, intmod]
                return True
            elif watched is self.ui.StartStop_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['sartStop']):
                        return True

                self.ui.StartStop_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['sartStop'] = [self.vk, intmod]
                return True
            elif watched is self.ui.ResetTimer_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['resetTime']):
                        return True

                self.ui.ResetTimer_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['resetTime'] = [self.vk, intmod]
                return True
            elif watched is self.ui.HalfTime_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['halfTime']):
                        return True

                self.ui.HalfTime_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['halfTime'] = [self.vk, intmod]
                return True
            elif watched is self.ui.ResetScore_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['resetScore']):
                        return True

                self.ui.ResetScore_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['resetScore'] = [self.vk, intmod]
                return True
            elif watched is self.ui.SwapTeams_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['swap']):
                        return True

                self.ui.SwapTeams_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['swap'] = [self.vk, intmod]
                return True
            elif watched is self.ui.PeriodUp_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['periodUp']):
                        return True

                self.ui.PeriodUp_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['periodUp'] = [self.vk, intmod]
                return True
            elif watched is self.ui.PeriodDwn_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['periodDown']):
                        return True

                self.ui.PeriodDwn_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['periodDown'] = [self.vk, intmod]
                return True
            elif watched is self.ui.StopSund_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['stopSound']):
                        return True

                self.ui.StopSund_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['stopSound'] = [self.vk, intmod]
                return True
            elif watched is self.ui.RemoteOnOff_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['remoteOnOff']):
                        return True

                self.ui.RemoteOnOff_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['remoteOnOff'] = [self.vk, intmod]
                return True
            elif watched is self.ui.ObsConnect_Key:
                if self.vk == 46:
                    if self.check_del(watched, Keys.keysDict['obsConDiscon']):
                        return True

                self.ui.ObsConnect_Key.setText((QtGui.QKeySequence(intmod).toString()) + name)
                Keys.keysDict['obsConDiscon'] = [self.vk, intmod]
                return True
            else:
                ktory = 0
            # self.vk = event.nativeVirtualKey()
            # mod = event.modifiers()
            # intmod = int(mod)
            # if self.vk in [16,17,18]:
            #     self.vk = 0
            # name = CharMap.get(self.vk)
            # print("watched", watched.objectName())
            if ktory == 1:
                # print("ktory 1")
                # self.key1 = self.vk
                # self.control1 = mod
                # self.ui.lineEdit.setText((QtGui.QKeySequence(intmod).toString())+name)
                # self.Settings.setValue("key1",self.vk)
                # self.Settings.setValue("control1",intmod)
                # print(self.key1, intmod)
                return True
            elif ktory == 2:
                # print("ktory 2")
                # self.key2 = self.vk
                # self.control2 = mod
                # self.ui.lineEdit_2.setText((QtGui.QKeySequence(intmod).toString())+name)
                # self.Settings.setValue("key2", self.vk)
                # self.Settings.setValue("control2", intmod)
                return True
            else:
                key_action = False
                if [self.vk, mod] == Keys.keysDict['homeUp']:  # self.key1 and mod == self.control1:
                    self.on_home_up()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['homeUp2']:
                    self.on_home_up2()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['homeDown']:
                    self.on_home_down()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['awayUp']:
                    self.on_away_up()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['awayUp2']:
                    self.on_away_up2()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['awayDown']:
                    self.on_away_down()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['sartStop']:
                    self.start_timer()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['resetTime']:
                    self.on_reset_timer()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['halfTime']:
                    self.on_half_time()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['resetScore']:
                    self.on_reset_score()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['swap']:
                    self.on_swap_button()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['periodUp']:
                    self.on_period_up()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['periodDown']:
                    self.on_period_down()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['stopSound']:
                    # self.
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['remoteOnOff']:
                    self.on_remote_button()
                    key_action = True
                if [self.vk, mod] == Keys.keysDict['obsConDiscon']:
                    self.ui.ConnectObs_Button.clicked.emit()
                    key_action = True
                if key_action:
                    return True

        return False


    def check_del(self, keyHolder:QLabel, keyList:list):
        if keyHolder.text() == "":
            return False
        else:
            keyHolder.clear()
            self.vk = 0
            keyList.clear()
            return True






    # ------------------------------------------------------------------------------

    def clear_error(self):
        Language.currentTextError = Language.iniTextError
        self.ui.Error_Text.setText(Language.currentTextError)

    def set_time_from_sec(self, sec):
        ScoreBoard.scoreBoardDict['minutes'] = sec // 60
        ScoreBoard.scoreBoardDict['sconds'] = sec % 60
        ScoreBoard.scoreBoardDict['timerString'] = "{:02d}:{:02d}".format(ScoreBoard.scoreBoardDict['minutes'], ScoreBoard.scoreBoardDict['seconds'])

    def set_settime_from_sec(self, sec):
        ScoreBoard.scoreBoardDict['setMinutes'] = sec // 60
        ScoreBoard.scoreBoardDict['setSeconds'] = sec % 60
        self.ui.Minutes_Input.setValue(ScoreBoard.scoreBoardDict['setMinutes'])
        self.ui.Seconds_Input.setValue(ScoreBoard.scoreBoardDict['setSeconds'])

    def set_totime_from_sec(self, sec):
        ScoreBoard.scoreBoardDict['setToMinutes'] = sec // 60
        ScoreBoard.scoreBoardDict['setToSeconds'] = sec % 60
        self.ui.MinutesTo_Input.setValue(ScoreBoard.scoreBoardDict['setToMinutes'])
        self.ui.SecondsTo_Input.setValue(ScoreBoard.scoreBoardDict['setToSeconds'])

    def set_period_from_sec(self, sec):
        ScoreBoard.scoreBoardDict['setPeriodMinutes'] = sec // 60
        ScoreBoard.scoreBoardDict['setPeriodSeconds'] = sec % 60
        self.ui.MinutesPeriod_Input.setValue(ScoreBoard.scoreBoardDict['setPeriodMinutes'])
        self.ui.SecondsPeriod_Input.setValue(ScoreBoard.scoreBoardDict['setPeriodSeconds'])

    def set_input_time(self):
        self.ui.Minutes_Input.valueChanged.disconnect()
        self.ui.Seconds_Input.valueChanged.disconnect()
        self.ui.Minutes_Input.setValue(ScoreBoard.scoreBoardDict['minutes'])
        self.ui.Seconds_Input.setValue(ScoreBoard.scoreBoardDict['seconds'])
        self.ui.Minutes_Input.valueChanged[int].connect(self.on_time_input)
        self.ui.Seconds_Input.valueChanged[int].connect(self.on_time_input)

    def reset_overtime(self):
        ScoreBoard.scoreBoardDict['overtime'] = False
        ScoreBoard.scoreBoardDict['overtimeMinutes'] = 0
        ScoreBoard.scoreBoardDict['overtimeSeconds'] = 0
        self.set_overtime()

    def timer_presets_enable(self, enable):
        Settings.settingsDict['timerPresetEnable'] = enable
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
