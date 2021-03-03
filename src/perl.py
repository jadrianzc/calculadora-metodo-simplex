from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from src.views.ui_mainWindow import Ui_MainWindow
import numpy as np
import sys, re, os, string
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch

class Perl(QMainWindow):
    # Constructor
    def __init__(self, ui):
        super(Perl, self).__init__()
        # self.ui = ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Eventos
        self.ui.btnGenerarPerl.clicked.connect(self.generateTable)
    
    # Método: Genera la tabla
    def generateTable(self):
        self.ui.tableActividades.clear()
        self.cantidadActividades = self.ui.inputAct.value()
        self.ui.tableActividades.setRowCount(self.cantidadActividades)
        self.ui.tableActividades.setColumnCount(17)
        
        self.header = ["Actividades", "Detalle", "Predecesora", "To", "Tn", "Tp", "Di,j", "Ti0", "Ti1", "Tj0", "Tj1", "MTi,j", "MLi,j", "Fecha Inicio Temprano", "Fecha Inicio Tardio", "Fecha Fin Temprano", "Fecha Fin Tardia"]
        
        for indice, ancho in enumerate((105, 300, 105, 50, 50, 50, 50, 50, 50, 50, 50, 60, 60, 300, 300, 300, 300), start=0):
            self.ui.tableActividades.setColumnWidth(indice, ancho)
            item = QTableWidgetItem(self.header[indice])
            item.setBackground(QtGui.QColor(22, 20, 90))
            self.ui.tableActividades.setHorizontalHeaderItem(indice, item)
            
            self.abec = list(map(chr, range(65, 91)))
            for i in range(self.cantidadActividades):
                celda = QTableWidgetItem(self.abec[i])
                celda.setTextAlignment(Qt.AlignCenter)
                self.ui.tableActividades.setItem(i, 0, celda)
            
# Inicia la aplicación
if __name__ == '__main__':    
    app = QApplication([])
    app.setStyle(QStyleFactory.create('Fusion'))
    mi_App = Perl()
    mi_App.show()
    sys.exit(app.exec_())