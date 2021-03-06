from PySide2.QtCore import QCoreApplication

class Language(object):
    textError = QCoreApplication.translate("MainWindow", u"Error Output:<br><div style=\"color:red\">You must stop the timer before reset it.</div>", None)
    iniTextError = QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Error Output:</p></body></html>", None)
    periodError = QCoreApplication.translate("MainWindow", u"Error Output:<br><div style=\"color:red\">You must stop the timer change period.</div>", None)
    timerError = QCoreApplication.translate("MainWindow", u"Error Output:<br><div style=\"color:red\">You must set time before run Timer.</div>", None)
    currentTextError = iniTextError

    ConnectionToOBS = QCoreApplication.translate("MainWindow", "Connection to OBS: ", None)
    NotConnected = QCoreApplication.translate("MainWindow", "Not Connected", None)
    Connected = QCoreApplication.translate("MainWindow", "Connected", None)
    Connecting = QCoreApplication.translate("MainWindow", "Connecting...", None)
    ConnectionOBSLost = QCoreApplication.translate("MainWindow", "Connection to OBS has been lost!", None)
    HalfActive = QCoreApplication.translate("MainWindow", "HalfTime\nAcive", None)
    Half = QCoreApplication.translate("MainWindow", "HalfTime", None)
    SpeedHelp = QCoreApplication.translate("MainWindow", "Speed Help", None)
    ExplSpeedHelp = QCoreApplication.translate("MainWindow", "Explain how the Speed works.", None)
    OpenSound = QCoreApplication.translate("MainWindow", "Open Sound", None)
    SoundFiles = QCoreApplication.translate("MainWindow", "Sound Files (*.wav *.mp3)", None)
    Disconnect = QCoreApplication.translate("MainWindow", "Disconnect", None)
    Connect = QCoreApplication.translate("MainWindow", "Connect", None)
    ObsConError = QCoreApplication.translate("MainWindow", "Can't connect to OBS!", None)
    OpenImage = QCoreApplication.translate("MainWindow", "Open Image", None)
    ImageFiles = QCoreApplication.translate("MainWindow", "Image Files (*.jpg *.png)", None)
    SaveError = QCoreApplication.translate("MainWindow", "Save Error.", None)
    LoadError = QCoreApplication.translate("MainWindow", "Load Error.", None)
    MustConnect = QCoreApplication.translate("MainWindow", "You must be connected to OBS!", None)
    SaveObsSettings = QCoreApplication.translate("MainWindow", "Save OBS settings.", None)
    LoadObsSettings = QCoreApplication.translate("MainWindow", "Load OBS settings.", None)
    ObsSettingsFiles = QCoreApplication.translate("MainWindow", "OBS Settings Files (*.obs)", None)
    CheckSceneCollection = QCoreApplication.translate("MainWindow", "Check Scene Collection!", None)
    NoSources = QCoreApplication.translate("MainWindow", "No such sources name:\n", None)
    NoFile = QCoreApplication.translate("MainWindow", "No such file: ", None)
    StartServer = QCoreApplication.translate("MainWindow", "Start Server", None)
    StopServer = QCoreApplication.translate("MainWindow", "Stop Server", None)
    RemoteLabelStatus = QCoreApplication.translate("MainWindow", "Remote Connection: ", None)
    Listening = QCoreApplication.translate("MainWindow", "Listening...", None)
    NrOfConnections = QCoreApplication.translate("MainWindow", "Number of Connections: ", None)
    IpAddresses = QCoreApplication.translate("MainWindow","My IP addresses: ", None)
    IpAddressesDefault = QCoreApplication.translate("MainWindow","Default IP: 127.0.0.1/Localhost | Port: 1234", None)

    currentLanguage = ""

    HalfTimeText = Half

    @staticmethod
    def retranslateUi():
        Language.textError = QCoreApplication.translate("MainWindow", u"Error Output:<br><div style=\"color:red\">You must stop the timer before reset it.</div>", None)
        Language.iniTextError = QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Error Output:</p></body></html>", None)
        Language.periodError = QCoreApplication.translate("MainWindow", u"Error Output:<br><div style=\"color:red\">You must stop the timer change period.</div>", None)
        Language.timerError = QCoreApplication.translate("MainWindow", u"Error Output:<br><div style=\"color:red\">You must set time before run Timer.</div>", None)
        Language.ConnectionToOBS = QCoreApplication.translate("MainWindow", "Connection to OBS: ", None)
        Language.NotConnected = QCoreApplication.translate("MainWindow", "Not Connected", None)
        Language.Connected = QCoreApplication.translate("MainWindow", "Connected", None)
        Language.Connecting = QCoreApplication.translate("MainWindow", "Connecting...", None)
        Language.ConnectionOBSLost = QCoreApplication.translate("MainWindow", "Connection to OBS has been lost!", None)
        Language.HalfActive = QCoreApplication.translate("MainWindow", "HalfTime\nAcive", None)
        Language.Half = QCoreApplication.translate("MainWindow", "HalfTime", None)
        Language.SpeedHelp = QCoreApplication.translate("MainWindow", "Speed Help", None)
        Language.ExplSpeedHelp = QCoreApplication.translate("MainWindow", "Explain how the Speed works.", None)
        Language.OpenSound = QCoreApplication.translate("MainWindow", "Open Sound", None)
        Language.SoundFiles = QCoreApplication.translate("MainWindow", "Sound Files (*.wav *.mp3)", None)
        Language.Disconnect = QCoreApplication.translate("MainWindow", "Disconnect", None)
        Language.Connect = QCoreApplication.translate("MainWindow", "Connect", None)
        Language.ObsConError = QCoreApplication.translate("MainWindow", "Can't connect to OBS!", None)
        Language.OpenImage = QCoreApplication.translate("MainWindow", "Open Image", None)
        Language.ImageFiles = QCoreApplication.translate("MainWindow", "Image Files (*.jpg *.png)", None)
        Language.SaveError = QCoreApplication.translate("MainWindow", "Save Error.", None)
        Language.LoadError = QCoreApplication.translate("MainWindow", "Load Error.", None)
        Language.MustConnect = QCoreApplication.translate("MainWindow", "You must be connected to OBS!", None)
        Language.SaveObsSettings = QCoreApplication.translate("MainWindow", "Save OBS settings.", None)
        Language.LoadObsSettings = QCoreApplication.translate("MainWindow", "Load OBS settings.", None)
        Language.ObsSettingsFiles = QCoreApplication.translate("MainWindow", "OBS Settings Files (*.obs)", None)
        Language.CheckSceneCollection = QCoreApplication.translate("MainWindow", "Check Scene Collection!", None)
        Language.NoSources = QCoreApplication.translate("MainWindow", "No such sources name:\n", None)
        Language.NoFile = QCoreApplication.translate("MainWindow", "No such file: ", None)
        Language.StartServer = QCoreApplication.translate("MainWindow", "Start Server", None)
        Language.StopServer = QCoreApplication.translate("MainWindow", "Stop Server", None)
        Language.RemoteLabelStatus = QCoreApplication.translate("MainWindow", "Remote Connection: ", None)
        Language.Listening = QCoreApplication.translate("MainWindow", "Listening...", None)
        Language.NrOfConnections = QCoreApplication.translate("MainWindow", "Number of Connections: ", None)
        Language.IpAddresses = QCoreApplication.translate("MainWindow", "My IP addresses: ", None)
        Language.IpAddressesDefault = QCoreApplication.translate("MainWindow", "Default IP: 127.0.0.1/Localhost | Port: 1234", None)

        if Language.HalfTimeText == Language.Half:
            Language.HalfTimeText = Language.Half
            print("language = half")
        elif Language.HalfTimeText == Language.HalfActive:
            Language.HalfTimeText = Language.HalfActive
            print("language = halfactive")
        else:
            print("language = nothing")