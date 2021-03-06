from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from src.views.ui_mainWindow import Ui_MainWindow
import numpy as np
import sys, re, os, string, re
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch

class Perl(QMainWindow):
    # Constructor
    def __init__(self, ui, iconErr, iconSucc):
        super(Perl, self).__init__()
        self.ui = ui

        # Iconos
        self.icoError = iconErr
        self.icoSucess = iconSucc

        # Eventos
        # self.ui.btnGenerarPerl.clicked.connect(self.generateTable)
        self.ui.btnGenerarPerl.clicked.connect(self.dataActividades)
        self.ui.btnNuevoPerl.clicked.connect(self.nuevoCalculo)
        self.ui.btnCalcularPerl.clicked.connect(self.generateTable)
        self.ui.btnBorrarPerl.clicked.connect(self.deletaTable)
    
    # Método: Muestra otra ventana para ingresar los datos
    def dataActividades(self):
        self.ui.groupBoxInputActv.setVisible(True)
        self.ui.tableInputActividades.clear()
        self.cantidadActividades = self.ui.inputAct.value()
        self.ui.tableInputActividades.setRowCount(self.cantidadActividades)
        self.ui.tableInputActividades.setColumnCount(6)
        self.Actividades = []
        
        # Arreglo con nombres de encabezados
        self.header = ["Actividades", "Detalle", "Predecesora", "To", "Tn", "Tp"]
        
        # Bucle: Asigna nombre a los encabezados
        for indice, ancho in enumerate((105, 350, 110, 50, 50, 50), start=0):
            self.ui.tableInputActividades.setColumnWidth(indice, ancho)
            item = QTableWidgetItem(self.header[indice])
            item.setBackground(QtGui.QColor(22, 20, 90))
            self.ui.tableInputActividades.setHorizontalHeaderItem(indice, item)
            
        # Genera las letras del abecedario y las inserta en la columna actividad
        self.abec = list(map(chr, range(65, 91)))
        for i in range(self.cantidadActividades):
            self.Actividades.append(self.abec[i])
            celda = QTableWidgetItem(self.abec[i])
            celda.setTextAlignment(Qt.AlignCenter)
            celda.setFlags(Qt.ItemIsEnabled)
            self.ui.tableInputActividades.setItem(i, 0, celda)
      
    # Método: Valida la tabla
    def validarTable(self):
        # Bucle: Almacenamos todos los datos de la tabla
        try:
            self.dataTablePerlInput = []
            for f in range(self.cantidadActividades):
                filaData = []
                listPrede = []
                for c in range(6):
                    if(c == 2):
                        valor = self.ui.tableInputActividades.item(f,c).text()
                        regex = re.search(r"N/A|^[A-Z]{1}$|^[A-Z]{1}(-[A-Z]{1}){1,10}$", valor)
                        
                        if(regex == None):
                            raise Exception('Ingrese correctamente los precedentes.\nEj: "A" | "A-B".\nEn caso de no tener ingrese "N/A".')
                        
                        prede = regex.group()
                        listPrede = prede.split(sep="-")

                        for value in range(len(listPrede)):
                            if(listPrede[value] != "N/A" and not(listPrede[value] in self.Actividades)):
                                raise Exception(f'El valor "{listPrede[value]}" no corresponde a ninguna actividad existente')
                            
                    elif(c == 3 or c == 4 or c == 5):
                        valor = int(self.ui.tableInputActividades.item(f,c).text())
                    else:
                        valor = self.ui.tableInputActividades.item(f,c).text()
                        
                    filaData.append(str(valor))
                self.dataTablePerlInput.append(filaData)
 
            return self.dataTablePerlInput
        except AttributeError:
            msjErr = "Ingrese todos los valores correctamente"
            msgBox2 = QMessageBox()
            msgBox2.setText(msjErr)
            msgBox2.setWindowTitle("Error")
            msgBox2.setWindowIcon(QIcon(self.icoError))
            msgBox2.setStyleSheet("font-size: 14px; font-weight: bold; font-family: Century Gothic")
            msgBox2.exec_()
        except ValueError:
            msjErr = "Los valores de los tiempos deben ser número enteros"
            msgBox2 = QMessageBox()
            msgBox2.setText(msjErr)
            msgBox2.setWindowTitle("Error")
            msgBox2.setWindowIcon(QIcon(self.icoError))
            msgBox2.setStyleSheet("font-size: 14px; font-weight: bold; font-family: Century Gothic")
            msgBox2.exec_()
        except Exception as err:
            print(err)
            msjErr = str(err)
            msgBox2 = QMessageBox()
            msgBox2.setText(msjErr)
            msgBox2.setWindowTitle("Error")
            msgBox2.setWindowIcon(QIcon(self.icoError))
            msgBox2.setStyleSheet("font-size: 14px; font-weight: bold; font-family: Century Gothic")
            msgBox2.exec_()
    
    # Método: Genera la tabla
    def generateTable(self):
        self.ui.tableActividades.clear()
        self.cantidadActividades = self.ui.inputAct.value()
        
        data = self.validarTable()
        if(data != None):
            self.ui.groupBoxInputActv.setVisible(False)
            self.ui.groupBoxrResPerl.setVisible(True)
            self.ui.btnGenerarPerl.setEnabled(False)
            self.Predecesores = []
            
            self.ui.tableActividades.setRowCount(self.cantidadActividades)
            self.ui.tableActividades.setColumnCount(18)
            self.ui.tableActividades.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # Arreglo con nombres de encabezados
            self.header = ["Actividades", "Detalle", "Predecesora", "To", "Tn", "Tp", "Dij", "Oij", "Ti0", "Ti1", "Tj0", "Tj1", "MTi,j", "MLi,j", "Fecha Inicio Temprano", "Fecha Inicio Tardio", "Fecha Fin Temprano", "Fecha Fin Tardia"]
            
            # Bucle: Asigna nombre a los encabezados
            for indice, ancho in enumerate((105, 300, 105, 50, 50, 50, 50, 50, 50, 50, 50, 50, 60, 60, 300, 300, 300, 300), start=0):
                self.ui.tableActividades.setColumnWidth(indice, ancho)
                item = QTableWidgetItem(self.header[indice])
                item.setBackground(QtGui.QColor(22, 20, 90))
                self.ui.tableActividades.setHorizontalHeaderItem(indice, item)
                
            # Bucle: Inserta los valores en la tabla final
            for f in range(self.cantidadActividades):
                for c in range(6):
                    celda = QTableWidgetItem(data[f][c])
                    celda.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableActividades.setItem(f, c, celda)
            
            # Bucle: Obtiene los valores de la columna Predecesora
            for f in range(self.cantidadActividades):
                valor = self.ui.tableActividades.item(f,2).text()
                self.Predecesores.append(valor)
            
            self.calcularPerl()
             
    # Método: Calcula los valores de las tablas
    def calcularPerl(self):
        self.DijOij = self.calculaDijOij(self.cantidadActividades)
        self.calculaTiempos(self.cantidadActividades)
        
    # Método: Calcula el valor de Dij y Oij
    def calculaDijOij(self, filas):
        try:
            dij = []
            oij = []
            for f in range(filas):
                valores = []
                for c in range(3):
                    valor = int(self.ui.tableActividades.item(f,c+3).text())
                    valores.append(valor)
                
                valorDij = (valores[0] + (4 * valores[1]) + valores[2]) / 6
                valorDij = round(valorDij)
                dij.append(valorDij)
                
                valorOij = pow(((valores[2] - valores[0]) / 6), 2)
                valorOij = round(valorOij, 2)
                oij.append(valorOij)
                
                # Inserta los valores Dij en la tabla
                celdaDij = QTableWidgetItem(str(valorDij))
                celdaDij.setTextAlignment(Qt.AlignCenter)
                self.ui.tableActividades.setItem(f, 6, celdaDij)
                
                # Inserta los valores Oij en la tabla
                celdaOij = QTableWidgetItem(str(valorOij))
                celdaOij.setTextAlignment(Qt.AlignCenter)
                self.ui.tableActividades.setItem(f, 7, celdaOij)
                
            return dij, oij
        except Exception as err:
            print(err)
    
    # Méctodo: Calcula los tiempo
    def calculaTiempos(self, filas):
        # Calcula e inserta los valores de Ti0 y Tj0
        self.Ti0 = []
        self.Tj0 = []
        self.Ti1 = []
        self.Tj1 = []
        for f in range(filas):
            validarPrece = []
            valorPrece = self.ui.tableActividades.item(f,2).text()
            
            if(valorPrece == "N/A"):
                celdaTi0 = QTableWidgetItem(str(0))
                celdaTi0.setTextAlignment(Qt.AlignCenter)
                self.ui.tableActividades.setItem(f, 8, celdaTi0)
                self.Ti0.append(0)
                
                celdaTj0 = QTableWidgetItem(str(self.DijOij[0][f]))
                celdaTj0.setTextAlignment(Qt.AlignCenter)
                self.ui.tableActividades.setItem(f, 10, celdaTj0)
                self.Tj0.append(self.DijOij[0][f])
                
            else:
                listPrede = valorPrece.split(sep="-")
                for value in range(len(listPrede)):
                    indexFilaTc = self.Actividades.index(listPrede[value])
                    valorPreceTc = int(self.ui.tableActividades.item(indexFilaTc,10).text())
                    validarPrece.append(valorPreceTc)
                
                valorMax = max(validarPrece)
                celdaTi0 = QTableWidgetItem(str(valorMax))
                celdaTi0.setTextAlignment(Qt.AlignCenter)
                self.ui.tableActividades.setItem(f, 8, celdaTi0)
                self.Ti0.append(valorMax)
                
                celdaTj0 = QTableWidgetItem(str(valorMax + self.DijOij[0][f]))
                celdaTj0.setTextAlignment(Qt.AlignCenter)
                self.ui.tableActividades.setItem(f, 10, celdaTj0)
                self.Tj0.append(valorMax + self.DijOij[0][f])
                
        # Calcula e inserta los valores de Ti1 y Tj1
        lastFilaAct = len(self.Actividades)-1
        validarLastAct = []
        for i in range(lastFilaAct, -1, -1):
            validarPreceLast = []
            valorPreceLast = self.ui.tableActividades.item(i,2).text()
            
            if(len(self.Actividades) == i+1):
                vMax = max(self.Tj0)
                
                celdaTj1 = QTableWidgetItem(str(vMax))
                celdaTj1.setTextAlignment(Qt.AlignCenter)
                self.ui.tableActividades.setItem(i, 11, celdaTj1)
                self.Tj1.append(vMax)
                
                celdaTi1 = QTableWidgetItem(str(vMax - self.DijOij[0][i]))
                celdaTi1.setTextAlignment(Qt.AlignCenter)
                self.ui.tableActividades.setItem(i, 9, celdaTi1)
                self.Ti1.append(vMax - self.DijOij[0][i])
                
                listPredeLast = valorPreceLast.split(sep="-")
                validarLastAct.append(listPredeLast)
            else:
                listPredeLast = valorPreceLast.split(sep="-")
                validarLastAct.append(listPredeLast)
                
                indexFilaLast = []
                for value in range(len(validarLastAct)):
                    if(self.Actividades[i] in validarLastAct[value]):
                        predecesor = "-".join(validarLastAct[value])
                        index = [indice for indice in range(len(self.Predecesores)) if self.Predecesores[indice] == predecesor]
                        for ind in index:
                            if(not(ind in indexFilaLast)):
                                indexFilaLast.append(ind)
                        
                if(len(indexFilaLast) == 0):
                    valorTj0 = int(self.ui.tableActividades.item(i+1,11).text())
                    celdaTj1 = QTableWidgetItem(str(valorTj0))
                    celdaTj1.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableActividades.setItem(i, 11, celdaTj1)
                    self.Tj1.append(valorTj0)
                    
                    celdaTi1 = QTableWidgetItem(str(valorTj0 - self.DijOij[0][i]))
                    celdaTi1.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableActividades.setItem(i, 9, celdaTi1)
                    self.Ti1.append(valorTj0 - self.DijOij[0][i])
                else:
                    valorPreceMin = []
                    for valor in indexFilaLast:
                        valorTj0 = int(self.ui.tableActividades.item(valor,9).text())
                        valorPreceMin.append(valorTj0)
                    
                    valorMin = min(valorPreceMin)
                    celdaTj1 = QTableWidgetItem(str(valorMin))
                    celdaTj1.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableActividades.setItem(i, 11, celdaTj1)
                    self.Tj1.append(valorMin)
                    
                    celdaTi1 = QTableWidgetItem(str(valorMin - self.DijOij[0][i]))
                    celdaTi1.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableActividades.setItem(i, 9, celdaTi1)
                    self.Ti1.append(valorMin - self.DijOij[0][i])
                    
        # Ejecutamos el método para hallar las holguras
        self.calcularMtMl(filas)
        
    # Método: Genera los valores de los Margenes Totales y Libres
    def calcularMtMl(self, filas):
        print(f"Actividades: {self.Actividades}")
        print(f"Dij: {self.DijOij[0]}")
        print(f"Oij: {self.DijOij[1]}")
        print(f"Predecesora: {self.Predecesores}")
        print(f"Ti0: {self.Ti0}")
        print(f"Ti1: {list(reversed(self.Ti1))}")
        print(f"Tj0: {self.Tj0}")
        print(f"Tj1: {list(reversed(self.Tj1))}")
        
        self.MTij = []
        self.MLij = []
        tj1 = list(reversed(self.Tj1))
        ti0 = self.Ti0
        tj0 = self.Tj0
        dij = self.DijOij[0]
        
        for f in range(filas):
            mtij = (tj1[f] - ti0[f] - dij[f])
            celdaMTij = QTableWidgetItem(str(mtij))
            celdaMTij.setTextAlignment(Qt.AlignCenter)
            self.ui.tableActividades.setItem(f, 12, celdaMTij)
            self.MTij.append(mtij)

            mlij = (tj0[f] - ti0[f] - dij[f])
            celdaMLij = QTableWidgetItem(str(mlij))
            celdaMLij.setTextAlignment(Qt.AlignCenter)
            self.ui.tableActividades.setItem(f, 13, celdaMLij)
            self.MLij.append(mlij)
        
        # Búcle: colorea las actividades críticas
        rutaCritica = [index for index in range(len(self.MTij)) if self.MTij[index] == 0]
        print(f"Ruta Crítica: {rutaCritica}")
        for ruta in rutaCritica:
            for col in range(14):
                data = self.ui.tableActividades.item(ruta,col).text()
                print(f"Data: {data}")
                valor = QTableWidgetItem(data)
                valor.setBackground(QtGui.QColor(187, 187, 225))
                valor.setTextAlignment(Qt.AlignCenter)
                self.ui.tableActividades.setItem(ruta,col,valor)
                               
    # Método: Genera un nuevo ejercicio
    def nuevoCalculo(self):
        self.ui.tableActividades.clear()
        self.ui.tableInputActividades.setRowCount(0)
        self.ui.groupBoxrResPerl.setVisible(False)
        self.ui.groupBoxInputActv.setVisible(True)
        self.ui.btnGenerarPerl.setEnabled(True)
             
    # Método: Elimina las tablas
    def deletaTable(self):
        # Eliminar las tablas
        self.ui.tableInputActividades.setRowCount(0)
