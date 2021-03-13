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
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
from datetime import timedelta

class Perl(QMainWindow):
    # Constructor
    def __init__(self, ui, iconErr, iconSucc, iconMain):
        super(Perl, self).__init__()
        self.ui = ui

        # Iconos
        self.icoError = iconErr
        self.icoSucess = iconSucc
        self.setWindowIcon(QIcon(iconMain))
        
        # Atributos
        self.fechInicio = ""

        # Eventos
        self.ui.btnGenerarPerl.clicked.connect(self.dataActividades)
        self.ui.btnNuevoPerl.clicked.connect(self.nuevoCalculo)
        self.ui.btnGuardar.clicked.connect(self.generarReporte)
        self.ui.btnSalirPert.clicked.connect(self.exitApp)
        self.ui.btnCalcularPerl.clicked.connect(self.generateTable)
        self.ui.btnBorrarPerl.clicked.connect(self.borrarTable)
        self.ui.calendario.clicked.connect(self.obtenerFecha)
    
    # Método: Crea los encabezados de la tabla
    def showEncabezado(self):
        # Arreglo con nombres de encabezados
        self.header = ["Actividades", "Detalle", "Predecesora", "To", "Tn", "Tp"]
        
        # Bucle: Asigna nombre a los encabezados
        for indice, ancho in enumerate((105, 350, 110, 50, 50, 50), start=0):
            self.ui.tableInputActividades.setColumnWidth(indice, ancho)
            item = QTableWidgetItem(self.header[indice])
            item.setBackground(QtGui.QColor(22, 20, 90))
            self.ui.tableInputActividades.setHorizontalHeaderItem(indice, item)

    # Método: Muestra otra ventana para ingresar los datos
    def dataActividades(self):
        self.ui.groupBoxInputActv.setVisible(True)
        self.ui.tableInputActividades.clear()
        self.cantidadActividades = self.ui.inputAct.value()
        try:
            if (self.cantidadActividades < 27):
                self.ui.tableInputActividades.setRowCount(self.cantidadActividades)
                self.ui.tableInputActividades.setColumnCount(6)
                self.Actividades = []
            
                self.showEncabezado()
                    
                # Genera las letras del abecedario y las inserta en la columna actividad
                self.abec = list(map(chr, range(65, 91)))
                for i in range(self.cantidadActividades):
                    self.Actividades.append(self.abec[i])
                    celda = QTableWidgetItem(self.abec[i])
                    celda.setTextAlignment(Qt.AlignCenter)
                    celda.setFlags(Qt.ItemIsEnabled)
                    self.ui.tableInputActividades.setItem(i, 0, celda)
            else:
                self.ui.tableInputActividades.setRowCount(0)
                self.ui.tableInputActividades.setColumnCount(6)
                self.showEncabezado()
                raise Exception(f'Error: Sobrepasa el límite de las actividades')
                
        except Exception as err :
            msjErr = str(err)
            msgBox2 = QMessageBox()
            msgBox2.setText(msjErr)
            msgBox2.setWindowTitle("Error")
            msgBox2.setWindowIcon(QIcon(self.icoError))
            msgBox2.setStyleSheet("font-size: 14px; font-weight: bold; font-family: Century Gothic")
            msgBox2.exec_()

    # Método: Obtiene la fecha del calendario
    def obtenerFecha(self):
        self.fechInicio = self.ui.calendario.selectedDate().toPyDate()
    
    # Método: Obtine los días no laborables
    def getDiasNoLab(self):
        self.diasNoLab = []
        
        if(self.ui.diaLunes.isChecked()):
            dia = "Monday"
            self.diasNoLab.append(dia)
            
        if(self.ui.diaMartes.isChecked()):
            dia = "Tuesday"
            self.diasNoLab.append(dia)
            
        if(self.ui.diaMiercoles.isChecked()):
            dia = "Wednesday"
            self.diasNoLab.append(dia)
            
        if(self.ui.diaJueves.isChecked()):
            dia = "Thursday"
            self.diasNoLab.append(dia)
            
        if(self.ui.diaViernes.isChecked()):
            dia = "Friday"
            self.diasNoLab.append(dia)
            
        if(self.ui.diaSabado.isChecked()):
            dia = "Saturday"
            self.diasNoLab.append(dia)
            
        if(self.ui.diaDomingo.isChecked()):
            dia = "Sunday"
            self.diasNoLab.append(dia)
       
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
                        
                            newActividad = self.Actividades[f:]
                            if(listPrede[value] in newActividad):
                                raise Exception(f'El valor "{listPrede[value]}" no puede preceder de sí mismo ni de una actividad que no se ha realizado')


                    elif(c == 3 or c == 4 or c == 5):
                        valor = int(self.ui.tableInputActividades.item(f,c).text())
                    else:
                        valor = self.ui.tableInputActividades.item(f,c).text()
                        
                    filaData.append(str(valor))
                self.dataTablePerlInput.append(filaData)
            
            # Obtiene la fecha inicio
            if(self.fechInicio == ""):
                 raise Exception('Por favor, ingrese la fecha que inicia el proyecto')
            
            # Verifica días no laborables
            self.getDiasNoLab()
            
            return self.dataTablePerlInput, self.fechInicio
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
            self.ui.opacity_effectGeneraPert.setOpacity(0.3)
            self.ui.btnNuevoPerl.setEnabled(True)
            self.ui.opacity_effectNuevoPert.setOpacity(1) 
            self.ui.btnGuardar.setEnabled(True)
            self.ui.opacity_effectGuardar.setOpacity(1) 
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
                    celda = QTableWidgetItem(data[0][f][c])
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

        self.generateDate(filas)
        
    # Método: Calcula las fechas
    def calcuFecha(self, tiempo):
        self.fechaLab = self.fechInicio
        i = 0
        while(i < tiempo):
            if(i == 0):
                dia = self.fechInicio + timedelta(days=i)
            else:
                self.fechaLab = self.fechaLab + timedelta(days=1)
                diaActual = self.fechaLab.strftime("%A")
                
                if(diaActual in self.diasNoLab):
                    i -= 1
            i += 1

        return self.fechaLab
        
    # Método: Calcula e inserta las fechas
    def generateDate(self, filas):
       
        self.Ti1 = list(reversed(self.Ti1))
        self.Tj1 = list(reversed(self.Tj1))
        for f in range(filas):
            
            ti0 = self.Ti0[f]
            ti1 = self.Ti1[f]
            tj0 = self.Tj0[f]
            tj1 = self.Tj1[f]

            # Fecha Inicio Temprano
            fi0 = self.calcuFecha(ti0)
            diaStr = QTableWidgetItem(fi0.strftime("%d/%m/%Y"))
            diaStr.setTextAlignment(Qt.AlignCenter)
            self.ui.tableActividades.setItem(f,14,diaStr)
            
            # Fecha Inicio Tardio
            fi1 = self.calcuFecha(ti1)
            diaStr = QTableWidgetItem(fi1.strftime("%d/%m/%Y"))
            diaStr.setTextAlignment(Qt.AlignCenter)
            self.ui.tableActividades.setItem(f,15,diaStr)
            
            # Fecha Fin Temprano
            fj0 = self.calcuFecha(tj0)
            diaStr = QTableWidgetItem(fj0.strftime("%d/%m/%Y"))
            diaStr.setTextAlignment(Qt.AlignCenter)
            self.ui.tableActividades.setItem(f,16,diaStr)
            
            # Fecha Fin Tardio
            fj1 = self.calcuFecha(tj1)
            diaStr = QTableWidgetItem(fj1.strftime("%d/%m/%Y"))
            diaStr.setTextAlignment(Qt.AlignCenter)
            self.ui.tableActividades.setItem(f,17,diaStr)
            
        # Búcle: colorea las actividades críticas
        rutaCritica = [index for index in range(len(self.MTij)) if self.MTij[index] == 0]

        for ruta in rutaCritica:
            for col in range(18):
                data = self.ui.tableActividades.item(ruta,col).text()
                valor = QTableWidgetItem(data)
                valor.setBackground(QtGui.QColor(187, 187, 225))
                valor.setTextAlignment(Qt.AlignCenter)
                self.ui.tableActividades.setItem(ruta,col,valor)
        
        self.showResult(rutaCritica, filas)
    # Método: Muestra los resultados
    def showResult(self, rutaCritica, filas):
        self.rutaCritica = []
        for i in rutaCritica:
            self.rutaCritica.append(self.Actividades[i])
        
        rCritica = "-".join(self.rutaCritica)
        self.ui.lblRutaCritica.setText(f"Ruta Crítica: {rCritica}")
        self.ui.lblInicioProyecto.setText(f"Fecha Inicio: {self.fechInicio.strftime('%d/%m/%Y')}")
        self.ui.lblFinProyecto.setText(f"Fecha Final: {self.ui.tableActividades.item(filas-1,17).text()}")
        self.ui.lblDiasProyecto.setText(f"Total de días: {max(self.Tj0)}")
         
    # Método: Genera un nuevo ejercicio
    def nuevoCalculo(self):
        self.ui.tableActividades.clear()
        self.ui.tableInputActividades.clear()
        self.ui.groupBoxInputActv.setVisible(False)
        self.ui.groupBoxrResPerl.setVisible(False)
        self.ui.btnGenerarPerl.setEnabled(True)
        self.ui.opacity_effectGeneraPert.setOpacity(1)
        self.ui.btnNuevoPerl.setEnabled(False)
        self.ui.opacity_effectNuevoPert.setOpacity(0.3)
        self.ui.btnGuardar.setEnabled(False)
        self.ui.opacity_effectGuardar.setOpacity(0.3)
        self.ui.diaLunes.setChecked(False)
        self.ui.diaMartes.setChecked(False)
        self.ui.diaMiercoles.setChecked(False)
        self.ui.diaJueves.setChecked(False)
        self.ui.diaViernes.setChecked(False)
        self.ui.diaSabado.setChecked(False)
        self.ui.diaDomingo.setChecked(False)
        
    
    # Método: Borra las filas y datos de las checkboxs
    def borrarTable(self):
        self.ui.tableInputActividades.setRowCount(0)
        self.ui.diaLunes.setChecked(False)
        self.ui.diaMartes.setChecked(False)
        self.ui.diaMiercoles.setChecked(False)
        self.ui.diaJueves.setChecked(False)
        self.ui.diaViernes.setChecked(False)
        self.ui.diaSabado.setChecked(False)
        self.ui.diaDomingo.setChecked(False)
    
    # Método: Cierra el programa
    def exitApp(self):
        # app = QApplication([])
        # sys.exit(app.exec_())
        self.ui.widgetSimplex.setVisible(False)
        self.ui.widgetPerl.setVisible(False)
        self.ui.groupBoxInputActv.setVisible(False)
        
    # Método: Genera el reporte pdf
    def generarReporte(self):
        autor, accept = QInputDialog.getText(self, 'Generar Reporte','Ingrese el nombre de quien genera el reporte:')
        if(accept):
            try:
                doc = SimpleDocTemplate(f'Reporte_Pert.pdf', pagesize=landscape(A3), topMargin=12)
                alineacionTitulo = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=20, leading=40)
                alineacionTituloTabla = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=14, leading=40)
                alineacionAutor = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=11, leading=30)
                alineacionOpTable = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=12, leading=40)
                alineacionResultados = ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=12, leading=30)
                alineacionRestr = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=12, leading=30)
                
                story=[]
                titulo = "REPORTE MÉTODO PERT"
                
                if(autor != ""):
                    autor = f'AUTOR:  {autor.upper()}'
                else:
                    autor = ""
                    
                story.append(Paragraph(titulo, alineacionTitulo))
                story.append(Paragraph(autor, alineacionAutor))
                
                story.append(Paragraph(f"{self.ui.lblRutaCritica.text()}", alineacionResultados))
                story.append(Paragraph(f"{self.ui.lblInicioProyecto.text()}", alineacionResultados))  
                story.append(Paragraph(f"{self.ui.lblFinProyecto.text()}", alineacionResultados))
                story.append(Paragraph(f"{self.ui.lblDiasProyecto.text()}", alineacionResultados))
                
                self.fullTable = [self.header]
                for f in range(self.cantidadActividades):
                    self.arrayFila = []
                    for c in range(18):
                        item = self.ui.tableActividades.item(f,c).text()
                        self.arrayFila.append(item)
                     
                    self.fullTable.append(self.arrayFila)  
                       
                tabla = Table(self.fullTable, colWidths=[60,80,65,40,40,40,40,40,40,40,40,40,40,40,120,100,120,100], rowHeights=40)
                tabla.setStyle([
                        ('GRID',(0,0),(-1,-1),2,colors.black),
                        ('BOX',(0,0),(-1,-1),2,colors.black),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16145A')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#ffffff'))
                ])
                       
                story.append(tabla)
                        
                doc.build(story)
                
                msjErr = "Reporte generado correctamente"
                msgBox5 = QMessageBox()
                msgBox5.setText(msjErr)
                msgBox5.setWindowTitle("Éxito")
                msgBox5.setWindowIcon(QIcon(self.icoSucess))
                msgBox5.setStyleSheet("font-size: 14px; font-weight: bold; font-family: Century Gothic")
                msgBox5.exec_()

                os.system("Reporte_Pert.pdf && exit")

            except PermissionError:
                msjErr = "Ocurrió un error al generar el reporte"
                msgBox6 = QMessageBox()
                msgBox6.setText(msjErr)
                msgBox6.setWindowTitle("Error")
                msgBox6.setWindowIcon(QIcon(self.icoError))
                msgBox6.setStyleSheet("font-size: 14px; font-weight: bold; font-family: Century Gothic")
                msgBox6.exec_()