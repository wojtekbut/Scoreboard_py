from PySide2.QtCore import QCoreApplication

class Language(object):
    textError = QCoreApplication.translate("MainWindow", u"Error Output:<br><div style=\"color:red\">You must stop the timer before reset it.</div>", None)
    iniTextError = QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Error Output:</p></body></html>", None)
    periodError = QCoreApplication.translate("MainWindow", u"Error Output:<br><div style=\"color:red\">You must stop the timer change period.</div>", None)
    timerError = QCoreApplication.translate("MainWindow", u"Error Output:<br><div style=\"color:red\">You must set time before run Timer.</div>", None)
    currentTextError = iniTextError
    @staticmethod
    def retranslateUi():
        Language.textError = QCoreApplication.translate("MainWindow", u"Error Output:<br><div style=\"color:red\">You must stop the timer before reset it.</div>", None)
        Language.iniTextError = QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Error Output:</p></body></html>", None)
        Language.periodError = QCoreApplication.translate("MainWindow", u"Error Output:<br><div style=\"color:red\">You must stop the timer change period.</div>", None)
        Language.timerError = QCoreApplication.translate("MainWindow", u"Error Output:<br><div style=\"color:red\">You must set time before run Timer.</div>", None)
