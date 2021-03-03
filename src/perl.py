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
        self.ui = ui
        
        # Eventos
        self.ui.btnGenerarPerl.clicked.connect(self.generateTable)
        self.ui.btnCalcularPerl.clicked.connect(self.calcularPerl)
    
    # Método: Genera la tabla
    def generateTable(self):
        self.ui.tableActividades.clear()
        self.cantidadActividades = self.ui.inputAct.value()
        self.ui.tableActividades.setRowCount(self.cantidadActividades)
        self.ui.tableActividades.setColumnCount(17)
        
        # Arreglo con nombres de encabezados
        self.header = ["Actividades", "Detalle", "Predecesora", "To", "Tn", "Tp", "Di,j", "Ti0", "Ti1", "Tj0", "Tj1", "MTi,j", "MLi,j", "Fecha Inicio Temprano", "Fecha Inicio Tardio", "Fecha Fin Temprano", "Fecha Fin Tardia"]
        
        # Bucle: Asigna nombre a los encabezados
        for indice, ancho in enumerate((105, 300, 105, 50, 50, 50, 50, 50, 50, 50, 50, 60, 60, 300, 300, 300, 300), start=0):
            self.ui.tableActividades.setColumnWidth(indice, ancho)
            item = QTableWidgetItem(self.header[indice])
            item.setBackground(QtGui.QColor(22, 20, 90))
            self.ui.tableActividades.setHorizontalHeaderItem(indice, item)
            
            # Genera las letras del abecedario y las inserta en la columna actividad
            self.abec = list(map(chr, range(65, 91)))
            for i in range(self.cantidadActividades):
                celda = QTableWidgetItem(self.abec[i])
                celda.setTextAlignment(Qt.AlignCenter)
                self.ui.tableActividades.setItem(i, 0, celda)
        
    # Método: Calcula los valores de las tablas
    def calcularPerl(self):
        self.Dij = self.calculaDij(self.cantidadActividades)
        
    # Método: Calcula el valor de Dij
    def calculaDij(self, filas):
        dij = []
        for f in range(filas):
            valores = []
            for c in range(3):
                valor = int(self.ui.tableActividades.item(f,c+3).text())
                valores.append(valor)
            
            valorDij = (valores[0] + (4 * valores[1]) + valores[2]) / 6
            valorDij = round(valorDij)
            dij.append(valorDij)
            
            # Inserta los valores Dij en la tabla
            celda = QTableWidgetItem(str(valorDij))
            celda.setTextAlignment(Qt.AlignCenter)
            self.ui.tableActividades.setItem(f, 6, celda)
            
        return dij