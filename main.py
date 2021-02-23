from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from vista.ui_metodoSimplex import Ui_Form
import numpy as np
import sys, re, math

class Simplex(QDialog):
    cantVariables = 0
    cantRestricciones = 0
    
    # Constructor
    def __init__(self):
        
        super(Simplex, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Eventos
        self.ui.btnGenerar.clicked.connect(self.generateArrays)
        self.ui.btnCalcular.clicked.connect(self.dataFuncObj)
        self.ui.btnCalcular.clicked.connect(self.dataRestr)
        self.ui.btnCalcular.clicked.connect(self.validarTabla)
        self.ui.btnNuevo.clicked.connect(self.deleteData)
        self.ui.btnCalPibote.clicked.connect(self.dataCurrentTable)
        self.ui.btnNextTabla.clicked.connect(self.nextTable)
        self.ui.btnSalir.clicked.connect(self.exitApp)
        
    # Método: Genera las matrices para ingresar la cantidad de variables y restricciones
    def generateArrays(self):
        self.cantVariables = self.ui.inputVar.value()
        self.cantRestricciones = self.ui.inputRes.value()
        
        self.tablaFuncionObjetivo(self.cantVariables)
        
        for i in range(self.cantVariables):
            item1 = QTableWidgetItem(f"x{i+1}")
            item1.setBackground(QtGui.QColor(0, 0, 0))
            self.ui.tableFuncObj.setHorizontalHeaderItem(i,item1)
           
        self.tablaRestriccion(self.cantVariables, self.cantRestricciones) 
        
        for j in range(self.cantVariables):
            item1 = QTableWidgetItem(f"x{j+1}")
            item1.setBackground(QtGui.QColor(0, 0, 0))
            self.ui.tableRestr.setHorizontalHeaderItem(j,item1)

        self.ui.btnCalcular.setEnabled(True)
    
    # Método: Genera la tabla de la función objetivo
    def tablaFuncionObjetivo(self, variables):
        self.ui.tableFuncObj.clear()
        self.ui.tableFuncObj.setRowCount(1)
        self.ui.tableFuncObj.setColumnCount(variables)
        
    # Método: Genera la tabla de las restricciones
    def tablaRestriccion(self, variables, restricciones):
        self.ui.tableRestr.clear()
        self.ui.tableRestr.setRowCount(restricciones)
        self.ui.tableRestr.setColumnCount(variables)
        
        for i in range(variables, variables+2):
            item = QTableWidgetItem(" ")
            self.ui.tableRestr.insertColumn(i)
            self.ui.tableRestr.setHorizontalHeaderItem(i, item)
            
        fila = 0
        colum = variables
        for j in range(restricciones):
            self.comboBox = QComboBox()
            self.comboBox.addItem("<=")
            self.ui.tableRestr.setCellWidget(fila, colum, self.comboBox)
            
            fila += 1
    
    # Método: Genera la función objetivo con las variables de holgura
    def dataFuncObj(self):
        self.cantVariables = self.ui.inputVar.value()
        self.cantRestricciones = self.ui.inputRes.value()
        self.validaFuncObj = True
        
        matrizFuncObj = []
        self.matrizFuncObjNum = []
        funcObj = "Max Z = "
        
        try:
            for i in range(self.cantVariables):
                item = self.ui.tableFuncObj.item(0, i)
                itemNum = int(item.text())
                self.matrizFuncObjNum.append(itemNum)
                matrizFuncObj.append(f"{item.text()}x{i+1}")
                     
            for j in range(self.cantRestricciones):
                self.matrizFuncObjNum.append(0)
                matrizFuncObj.append(f"{0}s{j+1}")
                
            funcObj += " + ".join(matrizFuncObj)
            
            # Crea un label con la función objetivo
            self.ui.lblMaxZ.setText(funcObj)
            self.ui.lblMaxZ.setAlignment(Qt.AlignCenter)
            self.ui.lblMaxZ.setStyleSheet("border: 1px solid #000; font-size: 18px")
            
        except Exception as err:
            print(f"Error: {err}")
            msjErr = "Por favor, ingrese la función objetivo"
            QMessageBox.about(self, "Error", msjErr)
            self.validaFuncObj = False
    
    # Método: Genera las restricciones con las variables de holgura
    def dataRestr(self):
        self.cantVariables = self.ui.inputVar.value()
        self.cantRestricciones = self.ui.inputRes.value()
        column = self.cantVariables
        fila = self.cantRestricciones
        self.validaRestr = True
        
        matrizRestr = []
        self.matrizRestrNum = []
        sujRestr = "S.R. :\n"
        
        try:
            # Bucle: incrementa las filas
            for i in range(fila):
                increment = 0
                restr = []
                divRestr = []
                matrizRestrVar = []
                restrBi = 0
                
                # Bucle: incrementa las columnas
                for j in range(column):
                    increment += 1
                    item = self.ui.tableRestr.item(i,j)
                    itemNum = int(item.text())
                    matrizRestrVar.append(itemNum)
                    divRestr.append(f"{item.text()}x{increment}")
                    
                # Carga las variables de holgura por cada fila
                matrizHolg = np.eye(fila)
                
                # Asigna la variable S de holgura
                divRestr.append(f"s{i+1}")
                restr.append(divRestr)
                
                # Valida el signo de desigualdad para cargar el signo "="
                itemVar = self.comboBox.currentText()
                if(itemVar == "<="):
                    restr.append(f"=")
                    
                # Bucle: controla los valores independientes
                for k in range(column+1, column+2):
                    item = self.ui.tableRestr.item(i,k)
                    itemNum = int(item.text())
                    restrBi = itemNum
                    restr.append(f"{item.text()}")
                    
                # Bucle: convierte cada item de la matriz de holgura a entero y se hace un append por ir formando la ecuación
                for h in range(fila):
                    intHolg = int(matrizHolg[i][h])
                    matrizRestrVar.append(intHolg)
                    
                # Se hace un append del valor Bi para formar la ecuación
                matrizRestrVar.append(restrBi)
                
                # Se genera una matriz bidimensional con todas las restricciones
                self.matrizRestrNum.append(matrizRestrVar)
            
                # Se genera una matriz bidimensional
                matrizRestr.append(restr)
            
            # Se formatea un string para crear el sistema de ecuación
            for matriz in range(len(matrizRestr)):
                string = " + ".join(matrizRestr[matriz][0])
                sr = f"{string} {matrizRestr[matriz][1]} {matrizRestr[matriz][2]}"
                sujRestr += f"   {sr}\n"
            
            # Crea un label con la función objetivo
            self.ui.lblRestricc.setText(sujRestr)
            self.ui.lblRestricc.setStyleSheet("border: 1px solid #000; font-size: 18px")
                    
        except Exception as err:
            print(f"Error: {err}")
            msjErr = "Por favor, ingrese las restricciones"
            QMessageBox.about(self, "Error", msjErr)
            self.validaRestr = False

    # Método: Valida los campos de función objetivo y de restricciones
    def validarTabla(self):
        if(self.validaFuncObj == True and self.validaRestr == True):
            # Ejecutar la función para generar las tablas
            self.generarTabla(self.cantVariables, self.cantRestricciones)
            # self.dataCurrentTable()
            
            # Deshabilita el botón calcular y generar
            self.ui.btnCalcular.setEnabled(False)
            self.ui.btnGenerar.setEnabled(False)
            # self.ui.btnNextTabla.setEnabled(True)
            self.ui.btnCalPibote.setEnabled(True)
            
            # Deshabilita las tablas
            self.ui.tableFuncObj.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.ui.tableRestr.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.ui.tableResult.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
    # Método: Valida la útima tabla
    def validaLastTable(self, cjZj, bi):
        z = float(self.ui.tableResult.item(self.fila-2, self.columna-1).text())
    
        count = 0
        for valor in cjZj:
            if(valor <= 0):
                count += 1
        
        if(count == len(cjZj)):
            bi.append(z)
            for indBi in range(len(bi)):
                newBi = round(bi[indBi],1)
                cellItem = QTableWidgetItem(str(newBi))
                self.ui.tableResult.setItem(indBi+2,self.columna-1,cellItem)
            


            return False
        else:
            return True
              
    # Método: Crea la primer tabla
    def generarTabla(self, column, fila):
        self.ui.tableResult.clear()
        fil = fila + 4
        col = fila + column + 3
        self.fila = fil
        self.columna = col
        
        # Genera las filas y columnas
        self.ui.tableResult.setRowCount(fil)
        self.ui.tableResult.setColumnCount(col)
        
        try:
            incremento3 = 0
            for f in range(fil):
                item = ""
                incremento = 0
                incremento2 = 0
                    
                for c in range(col):
                    # Valida primera fila
                    if((f == 0 and c == 0) or (f == 0 and c == col-1) or (f == fil-1 and c == 0) or (f == fil-1 and c == col-1) or (f == fil-2 and c == 0)):
                        item = ""
                    elif(f == 0 and c == 1):
                        item = "Cj"
                    elif(f == 0 and (c != 0 or c != 1)):
                        item = f"{self.matrizFuncObjNum[incremento]}"
                        incremento += 1
                    # Valida segunda fila
                    elif(f == 1 and c == 0):
                        item = "Cb"
                    elif(f == 1 and c == col-1):
                        item = "Bi"
                    elif(f == 1 and c == 1):
                        item = "Xb"
                    elif(f == 1 and (c != 0 or c != 1)):
                        if(c <= column+1):
                            incremento += 1
                            item = f"X{incremento}" 
                        else:
                            incremento2 += 1
                            item = f"S{incremento2}"
                    # Validar penúltima fila
                    elif(f == fil-2 and c == 1):
                            item = "Zj"
                    elif(f == fil-2 and (c != 0 or c != 1)):
                        item = "0"
                    # Validar última fila
                    elif(f == fil-1 and c == 1):
                        item = "Cj-Zj"
                    elif(f == fil-1 and (c != 0 or c != 1)):
                        item = f"{self.matrizFuncObjNum[incremento]}"
                        incremento += 1
                    # Valida primera y segunda columna
                    else:
                        if(c == 0):
                            item = "0"
                        elif(c == 1):
                            if(f <= fila+1):
                                incremento3 += 1
                                item = f"S{incremento3}"
                        else:
                            newFila = f - 2
                            newColu = c - 2
                            item = f"{self.matrizRestrNum[newFila][newColu]}"
                    
                    cellItem = QTableWidgetItem(item)
                    self.ui.tableResult.setItem(f,c,cellItem)
                           
        except Exception as err:
            print(f"Error f: {err}")  
    
    # Método: Obtener datos de la tabla actual
    def dataCurrentTable(self):
        restriccion = self.cantRestricciones
        variable = self.cantVariables
        filas = self.fila
        columnas = self.columna
        self.cjZj = []
        self.bi = []
        self.colVarEntr = []
        self.valorVarSali = []
        
        # Bucle: Obtiene los valores de self.Bi
        for b in range(restriccion):
            item = self.ui.tableResult.item(b+2, columnas-1)
            self.bi.append(float(item.text())) 
        
        # Bucle: Obtiene los valores de Cj-Zj
        for i in range(variable):
            item = self.ui.tableResult.item(filas-1,i+2)
            self.cjZj.append(float(item.text()))

        # Valida la última tabla
        self.lastTable = self.validaLastTable(self.cjZj, self.bi)
        print(self.lastTable)
        if(self.lastTable == False):
            msjErr = "Esta es la última tabla generada"
            QMessageBox.about(self, "Error", msjErr)
            self.ui.btnCalPibote.setEnabled(False)
            return
        
        # Encuentra el valor máximo de Cj-Zj, o llamado variable de entrada
        variableEntrada = max(self.cjZj)
        ve = self.ui.tableResult.item(1,self.cjZj.index(variableEntrada)+2).text()
        textVarEnt = f"V.E = {ve}"
        self.ui.lblVarEntrante.setText(textVarEnt)
        
        # Obtiene el indice de la variable de entrada
        indexColVariableEntrada = self.cjZj.index(variableEntrada) + 2
        
        # Bucle: Obtiene los valores de la columna de la variable de entrada
        for j in range(restriccion):
            item = self.ui.tableResult.item(j+2,indexColVariableEntrada)
            self.colVarEntr.append(float(item.text()))
        
        # Bucle: Realiza la división entre Bi y los valores de la columna de la variable de entrada
        for k in range(restriccion):
            try:
                valorVarSal = float(self.bi[k]) / float(self.colVarEntr[k])
                if(valorVarSal >= 0):
                    self.valorVarSali.append(round(valorVarSal, 4))
                else:
                    self.valorVarSali.append(round(valorVarSal, 4)*-100000000)                   
            except:
                self.self.valorVarSali.append(100000000)

        # Encuentra el valor mínimo entre Bi / valores de v.e, o llamado variable de salida
        variableSalida = min(self.valorVarSali)
        vs = self.ui.tableResult.item(self.valorVarSali.index(variableSalida)+2,1).text()
        textVarSal = f"V.S = {vs}"
        self.ui.lblVarSaliente.setText(textVarSal)     
        
         # Obtiene el indice de la variable de salida
        indexFilVariableSalida = self.valorVarSali.index(variableSalida) + 2

        # Ubicamos el pibote
        self.pibote = float(self.ui.tableResult.item(indexFilVariableSalida, indexColVariableEntrada).text())
        textPibo = f"Pibote = {self.pibote}"
        self.ui.lblPibote.setText(textPibo)   

        # Habilita botón siguiente tabla
        self.ui.btnCalPibote.setEnabled(False)
        self.ui.btnNextTabla.setEnabled(True)
        
    # Método: Genera la siguiente tabla
    def nextTable(self):
        restriccion = self.cantRestricciones
        variable = self.cantVariables
        filas = self.fila
        columnas = self.columna
        cjZj = []
        colVarEntr = []
        filVarSali = []
        bi = []
        valorVarSali = []
        
        #Bucle: Obtiene los valores de Bi
        for b in range(restriccion):
            item = self.ui.tableResult.item(b+2, columnas-1)
            bi.append(float(item.text())) 
        
        # Bucle: Obtiene los valores de Cj-Zj
        for i in range(variable):
            item = self.ui.tableResult.item(filas-1,i+2)
            cjZj.append(float(item.text()))
        
        # Encuentra el valor máximo de Cj-Zj, o llamado variable de entrada
        variableEntrada = max(cjZj)
        self.ui.lblVarEntrante.setText("")
        
        # Obtiene el indice de la variable de entrada
        self.indexColVariableEntrada = cjZj.index(variableEntrada) + 2
        
        # Bucle: Obtiene los valores de la columna de la variable de entrada
        for j in range(restriccion):
            item = self.ui.tableResult.item(j+2,self.indexColVariableEntrada)
            colVarEntr.append(float(item.text()))
        
        # Bucle: Realiza la división entre Bi y los valores de la columna de la variable de entrada
        for k in range(restriccion):
            try:
                valorVarSal = float(bi[k]) / float(colVarEntr[k])
                if(valorVarSal >= 0):
                    valorVarSali.append(round(valorVarSal, 4))
                else:
                    valorVarSali.append(round(valorVarSal, 4)*-100000000)                   
            except:
                valorVarSali.append(100000000)

        # Encuentra el valor mínimo entre Bi / valores de v.e, o llamado variable de salida
        variableSalida = min(valorVarSali)
        self.ui.lblVarSaliente.setText("")
        
        # Obtiene el indice de la variable de salida
        self.indexFilVariableSalida = valorVarSali.index(variableSalida) + 2

        # Ubicamos el pibote
        self.pibote = float(self.ui.tableResult.item(self.indexFilVariableSalida, self.indexColVariableEntrada).text())
        self.ui.lblPibote.setText("")
        
        # Bucle: Obtiene las variables para reemplazar en la tabla Cb y Xb
        for rem in range(2):
            item = self.ui.tableResult.item(rem,self.indexColVariableEntrada)
            cellItem = QTableWidgetItem(item.text())
            self.ui.tableResult.setItem(self.indexFilVariableSalida,rem,cellItem)
        
        # Bucle: Obtiene la fila pibote
        for p in range(variable+restriccion+1):
            item = self.ui.tableResult.item(self.indexFilVariableSalida,p+2)
            filVarSali.append(float(item.text()))
        
        # Bucle: Divide la fila pibote por el pibote
        filaPibote = []
        for new in filVarSali:
            try:
                item = float(new) / self.pibote
                filaPibote.append(round(item,4))
            except:
                filaPibote.append(0)
        
        # Bucle: Genera las nuevas filas
        control = False
        for nwFila in range(len(colVarEntr)):
            valBi = float(self.ui.tableResult.item(nwFila+2,columnas-1).text()) 
            valBiCompare = float(self.ui.tableResult.item(self.indexFilVariableSalida,columnas-1).text())

            div = valBi / colVarEntr[nwFila]
            divCompare = valBiCompare / self.pibote
            
            if(float(colVarEntr[nwFila]) == self.pibote and div <= divCompare and control == False):
                control = True
                for p in range(variable+restriccion+1):
                    item = float(filaPibote[p])
                    pibote = round(item,4)
                    cellItem = QTableWidgetItem(str(pibote))
                    self.ui.tableResult.setItem(self.indexFilVariableSalida,p+2,cellItem)
                    
            else:
                for p in range(variable+restriccion+1):
                    # Obtiene los valores de la fila anterior
                    antiguaFila = float(self.ui.tableResult.item(nwFila+2,p+2).text())
                    # Obtiene la multiplicación de las demás filas con el pibote
                    nuevaFila = float((filaPibote[p] * (colVarEntr[nwFila] * -1)))
                    # Realiza la suma para formar la nueva 
                    suma = nuevaFila + antiguaFila 
                    suma = round(suma, 4)
                    # Inserta los nuevos valores
                    cellItem = QTableWidgetItem(str(suma))
                    self.ui.tableResult.setItem(nwFila+2,p+2,cellItem)
    
        # Bucle: Genera los nuevo valores de Zj
        for uF in range(variable+restriccion+1):
            total = 0
            zj = 0
            for res in range(restriccion):
                valor = self.ui.tableResult.item(res+2, 0).text()
                valor2 = self.ui.tableResult.item(res+2, uF+2).text()
                
                total = float(valor) * float(valor2)
                zj += total
                zj = round(zj,4)
            
            cellItem = QTableWidgetItem(str(zj))
            self.ui.tableResult.setItem(filas-2,uF+2,cellItem)
        
        # Bucle: Genera los nuevos valores de Cj-Zj
        for colCj in range(variable+restriccion):
            cj = float(self.ui.tableResult.item(0, colCj+2).text())
            zj = float(self.ui.tableResult.item(filas-2, colCj+2).text())
            cjZj = cj - zj
            cjZj = round(cjZj,4)
            cellItem = QTableWidgetItem(str(cjZj))
            self.ui.tableResult.setItem(filas-1,colCj+2,cellItem)            
        
        # Habilita botón calcular pibote
        self.ui.btnCalPibote.setEnabled(True)
        self.ui.btnNextTabla.setEnabled(False)
    # Método: Elimina los datos de la tabla
    def deleteData(self):
        # Resetea las tablas y labels
        self.generateArrays()
        self.ui.tableResult.clear()
        self.ui.lblMaxZ.setText("")
        self.ui.lblRestricc.setText("")
        self.ui.lblPibote.setText("")
        self.ui.lblVarEntrante.setText("")
        self.ui.lblVarSaliente.setText("")
        
        # Habilita el botón generar
        self.ui.btnGenerar.setEnabled(True)
        self.ui.btnCalcular.setEnabled(False)
        self.ui.btnNextTabla.setEnabled(False)
        
        # Habilita las tablas 
        self.ui.tableFuncObj.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.ui.tableRestr.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
        # Eliminar las tablas
        self.ui.tableFuncObj.setColumnCount(0)
        self.ui.tableFuncObj.setRowCount(0)
        self.ui.tableRestr.setColumnCount(0)
        self.ui.tableRestr.setRowCount(0)
        self.ui.tableResult.setColumnCount(0)
        self.ui.tableResult.setRowCount(0)
        
    # Método: Cierra el programa
    def exitApp(self):
        app = QApplication([])
        sys.exit(app.exec_())

# Inicia la aplicación
if __name__ == '__main__':
    app = QApplication([])
    app.setStyle(QStyleFactory.create('Fusion'))
    mi_App = Simplex()
    mi_App.show()
    sys.exit(app.exec_())