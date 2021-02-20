from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        # FORM
        Form.setObjectName("Form")
        Form.resize(1280, 720)
        Form.setMinimumSize(QtCore.QSize(1280, 720))
        Form.setMaximumSize(QtCore.QSize(1920, 1080))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        Form.setFont(font)
        Form.setStyleSheet("")
        # GROUP BOX DATOS
        self.groupBoxDatos = QtWidgets.QGroupBox(Form)
        self.groupBoxDatos.setGeometry(QtCore.QRect(30, 10, 450, 171))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxDatos.setFont(font)
        self.groupBoxDatos.setObjectName("groupBoxDatos")
        # LABEL VARIABLE
        self.lblVar = QtWidgets.QLabel(self.groupBoxDatos)
        self.lblVar.setGeometry(QtCore.QRect(40, 30, 300, 20))
        self.lblVar.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblVar.setFont(font)
        self.lblVar.setAutoFillBackground(False)
        self.lblVar.setStyleSheet("")
        self.lblVar.setObjectName("lblVar")
        # INPUT VARIABLE
        self.inputVar = QtWidgets.QSpinBox(self.groupBoxDatos)
        self.inputVar.setGeometry(QtCore.QRect(350, 30, 40, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.inputVar.setFont(font)
        self.inputVar.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.inputVar.setToolTipDuration(-27)
        self.inputVar.setKeyboardTracking(True)
        self.inputVar.setMinimum(2)
        self.inputVar.setObjectName("inputVar")
        # LABEL RESTRICCIONES
        self.lblRes = QtWidgets.QLabel(self.groupBoxDatos)
        self.lblRes.setGeometry(QtCore.QRect(40, 60, 300, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblRes.setFont(font)
        self.lblRes.setStyleSheet("")
        self.lblRes.setObjectName("lblRes")
        # INPUT RESTRICCIONES
        self.inputRes = QtWidgets.QSpinBox(self.groupBoxDatos)
        self.inputRes.setGeometry(QtCore.QRect(350, 60, 40, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.inputRes.setFont(font)
        self.inputRes.setMinimum(1)
        self.inputRes.setObjectName("inputRes")
        # BTN GENERAR
        self.btnGenerar = QtWidgets.QPushButton(self.groupBoxDatos)
        self.btnGenerar.setGeometry(QtCore.QRect(175, 120, 80, 30))
        self.btnGenerar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnGenerar.setObjectName("btnGenerar")
        # GROUP BOX FUNCIÓN OBJETIVA
        self.groupBoxFuncObj = QtWidgets.QGroupBox(Form)
        self.groupBoxFuncObj.setGeometry(QtCore.QRect(30, 200, 450, 150))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxFuncObj.setFont(font)
        self.groupBoxFuncObj.setObjectName("groupBoxFuncObj")
        # LABEL MAX Z
        self.lblTextMaxZ = QtWidgets.QLabel(self.groupBoxFuncObj)
        self.lblTextMaxZ.setGeometry(QtCore.QRect(20, 30, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblTextMaxZ.setFont(font)
        self.lblTextMaxZ.setObjectName("lblTextMaxZ")
        # TABLA FUNCIÓN OBJETIVA
        self.tableFuncObj = QtWidgets.QTableWidget(self.groupBoxFuncObj)
        self.tableFuncObj.setGeometry(QtCore.QRect(30, 60, 400, 75))
        self.tableFuncObj.setObjectName("tableFuncObj")
        self.tableFuncObj.setColumnCount(0)
        self.tableFuncObj.setRowCount(0)
        self.tableFuncObj.verticalHeader().setVisible(False)
        self.tableFuncObj.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter and QtCore.Qt.AlignVCenter and QtCore.Qt.AlignCenter)
        self.tableFuncObj.horizontalHeader().setDefaultSectionSize(50)
        self.tableFuncObj.setStyleSheet("border: none; font-size: 16px; font-weight: bold; vertical-align: middle; font-family: Century Gothic")
        # GROUP BOX RESTRICCIONES
        self.groupBoxRestriccion = QtWidgets.QGroupBox(Form)
        self.groupBoxRestriccion.setGeometry(QtCore.QRect(30, 360, 450, 260))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxRestriccion.setFont(font)
        self.groupBoxRestriccion.setObjectName("groupBoxRestriccion")
        # TABLA RESTRICCIONES
        self.tableRestr = QtWidgets.QTableWidget(self.groupBoxRestriccion)
        self.tableRestr.setGeometry(QtCore.QRect(10, 30, 430, 220))
        self.tableRestr.setObjectName("tableRestr")
        self.tableRestr.setColumnCount(0)
        self.tableRestr.setRowCount(0)
        self.tableRestr.verticalHeader().setVisible(False)
        self.tableRestr.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter and QtCore.Qt.AlignVCenter and QtCore.Qt.AlignCenter)
        self.tableRestr.horizontalHeader().setDefaultSectionSize(50)
        self.tableRestr.setStyleSheet("border: none; font-size: 16px; font-weight: bold; vertical-align: middle; font-family: Century Gothic")
        # GROUP BOX ACCIONES
        self.groupBoxAcciones = QtWidgets.QGroupBox(Form)
        self.groupBoxAcciones.setGeometry(QtCore.QRect(30, 630, 450, 100))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxAcciones.setFont(font)
        self.groupBoxAcciones.setObjectName("groupBoxAcciones")
        # BTN CALCULAR
        self.btnCalcular = QtWidgets.QPushButton(self.groupBoxAcciones)
        self.btnCalcular.setGeometry(QtCore.QRect(20, 40, 80, 30))
        self.btnCalcular.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnCalcular.setObjectName("btnCalcular")
        self.btnCalcular.setEnabled(False)
        # BTN SIGUIENTE TABLA
        self.btnNextTabla = QtWidgets.QPushButton(self.groupBoxAcciones)
        self.btnNextTabla.setGeometry(QtCore.QRect(120, 40, 120, 30))
        self.btnNextTabla.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnNextTabla.setObjectName("btnNextTabla")
        # BTN NUEVO 
        self.btnNuevo = QtWidgets.QPushButton(self.groupBoxAcciones)
        self.btnNuevo.setGeometry(QtCore.QRect(260, 40, 80, 30))
        self.btnNuevo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnNuevo.setObjectName("btnNuevo")
        # BTN SALIR
        self.btnSalir = QtWidgets.QPushButton(self.groupBoxAcciones)
        self.btnSalir.setGeometry(QtCore.QRect(360, 40, 80, 30))
        self.btnSalir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSalir.setObjectName("btnSalir")
        # GROUP BOX RESULTADO
        self.groupBoxResul = QtWidgets.QGroupBox(Form)
        self.groupBoxResul.setGeometry(QtCore.QRect(550, 10, 790, 719))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxResul.setFont(font)
        self.groupBoxResul.setObjectName("groupBoxResul")
        # LABEL FUNCION OBJETIVO
        self.lblMaxZ = QtWidgets.QLabel(self.groupBoxResul)
        self.lblMaxZ.setGeometry(QtCore.QRect(20, 30, 750, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        self.lblMaxZ.setFont(font)
        self.lblMaxZ.setObjectName("lblMaxZ")
        # LABEL RESTRICCIONES
        self.lblRestricc = QtWidgets.QLabel(self.groupBoxResul)
        self.lblRestricc.setGeometry(QtCore.QRect(20, 60, 750, 150))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        self.lblRestricc.setFont(font)
        self.lblRestricc.setObjectName("lblRestricc")
        # TABLA RESULTADO
        self.tableResult = QtWidgets.QTableWidget(self.groupBoxResul)
        self.tableResult.setGeometry(QtCore.QRect(20, 220, 750, 220))
        self.tableResult.setObjectName("tableResult")
        self.tableResult.setColumnCount(0)
        self.tableResult.setRowCount(0)
        self.tableResult.verticalHeader().setVisible(False)
        self.tableResult.horizontalHeader().setVisible(False)
        self.tableResult.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter and QtCore.Qt.AlignVCenter and QtCore.Qt.AlignCenter)
        self.tableResult.horizontalHeader().setDefaultSectionSize(70)
        self.tableResult.setStyleSheet("border: none; font-size: 16px; font-weight: bold; font-family: Century Gothic")
        
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Calculadora Método Simplex"))
        self.groupBoxDatos.setTitle(_translate("Form", "Datos"))
        self.lblVar.setText(_translate("Form", "Ingrese el número de variables:"))
        self.lblRes.setText(_translate("Form", "Ingrese el número de restricciones:"))
        self.btnGenerar.setText(_translate("Form", "GENERAR"))
        self.groupBoxRestriccion.setTitle(_translate("Form", "Restricciones"))
        self.lblTextMaxZ.setText(_translate("Form", "MAX Z ="))
        self.groupBoxFuncObj.setTitle(_translate("Form", "Función Objetivo"))
        self.groupBoxAcciones.setTitle(_translate("Form", "Acciones"))
        self.btnCalcular.setText(_translate("Form", "CALCULAR"))
        self.btnNextTabla.setText(_translate("Form", "SIGUIENTE TABLA"))
        self.btnNuevo.setText(_translate("Form", "NUEVO"))
        self.btnSalir.setText(_translate("Form", "SALIR"))
        self.groupBoxResul.setTitle(_translate("Form", "Resultado"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
