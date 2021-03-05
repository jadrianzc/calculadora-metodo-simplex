from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

class Ui_Form(object):
    def setupUi(self, Form):
        # FORM
        Form.setObjectName("Form")
        Form.resize(600, 600)
        Form.setMinimumSize(QtCore.QSize(600, 600))
        Form.setMaximumSize(QtCore.QSize(600, 600))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        Form.setFont(font)
        Form.setStyleSheet("background: #FEFEFE; font-size: 14px; font-weight: bold; font-family: Century Gothic")
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())