from PyQt5.QtWidgets import *
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
        self.ui.btnNuevo.clicked.connect(self.deleteData)
        self.ui.btnNextTabla.clicked.connect(self.nextTable)
        
    # Método: Genera las matrices para ingresar la cantidad de variables y restricciones
    def generateArrays(self):
        self.cantVariables = self.ui.inputVar.value()
        self.cantRestricciones = self.ui.inputRes.value()
        
        nombreColum = []
        for i in range(self.cantVariables):
            nombreColum.append(f"x{i+1}")
        
        self.tablaFuncionObjetivo(self.cantVariables)
        self.ui.tableFuncObj.setHorizontalHeaderLabels(nombreColum)
        self.tablaRestriccion(self.cantVariables, self.cantRestricciones)
        self.ui.tableRestr.setHorizontalHeaderLabels(nombreColum)
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
        
        # Ejecuta la función para generar las restricciones
        self.dataRestr(self.cantVariables, self.cantRestricciones)
        
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
            self.ui.lblMaxZ.setStyleSheet("border: 1px solid #3232C0;")
            
            # Ejecutar la función para generar las tablas
            self.generarTabla(self.cantVariables, self.cantRestricciones)
            
            # Deshabilita el botón calcular y generar
            self.ui.btnCalcular.setEnabled(False)
            self.ui.btnGenerar.setEnabled(False)
            
            # Deshabilita las tablas
            self.ui.tableFuncObj.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.ui.tableRestr.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.ui.tableResult.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
        except Exception as err:
            print(f"Error: {err}")
    
    # Método: Genera las restricciones con las variables de holgura
    def dataRestr(self, column, fila):
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
                sujRestr += f"\t{sr}\n"
            
            # Crea un label con la función objetivo
            self.ui.lblRestricc.setText(sujRestr)
            self.ui.lblRestricc.setStyleSheet("border: 1px solid #FF5733;")
                    
        except Exception as err:
            print(f"Error: {err}")
            
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
        
        # Bucle: Obtiene los valores de Bi
        for b in range(restriccion):
            item = self.ui.tableResult.item(b+2, columnas-1)
            bi.append(int(item.text()))
        print(f"Bi: {bi}")   
        
        # Bucle: Obtiene los valores de Cj-Zj
        for i in range(variable):
            item = self.ui.tableResult.item(filas-1,i+2)
            cjZj.append(int(item.text()))
        print(f"Cj-Zj: {cjZj}")
        
        # Encuentra el valor máximo de Cj-Zj, o llamado variable de entrada
        variableEntrada = max(cjZj)
        
        # Obtiene el indice de la variable de entrada
        indexColVariableEntrada = cjZj.index(variableEntrada) + 2
        
        # Bucle: Obtiene los valores de la columna de la variable de entrada
        for j in range(restriccion):
            item = self.ui.tableResult.item(j+2,indexColVariableEntrada)
            colVarEntr.append(int(item.text()))
        print(f"v.e: {colVarEntr}")
        
        # Bucle: Realiza la división entre Bi y los valores de la columna de la variable de entrada
        for k in range(restriccion):
            try:
                valorVarSal = float(bi[k]) / float(colVarEntr[k])
                valorVarSali.append(round(valorVarSal, 3))
            except:
                valorVarSali.append(0)
        print(f"división: {valorVarSali}")

        # Encuentra el valor mínimo entre Bi / valores de v.e, o llamado variable de salida
        variableSalida = min(valorVarSali)
        
        # Obtiene el indice de la variable de salida
        indexFilVariableSalida = valorVarSali.index(variableSalida) + 2

        # Ubicamos el pibote
        pibote = float(self.ui.tableResult.item(indexFilVariableSalida, indexColVariableEntrada).text())
        print(f"Pibote: {pibote}")
        
        # Bucle: Obtiene la fila pibote
        for p in range(variable+restriccion+1):
            item = self.ui.tableResult.item(indexFilVariableSalida,p+2)
            filVarSali.append(int(item.text()))
        print(f"v.s: {filVarSali}")
        
        # Bucle: Divide la fila pibote por el pibote
        filaPibote = []
        for new in filVarSali:
            item = float(new) / pibote
            filaPibote.append(round(item,3))
        print(f"Fila New Pibote: {filaPibote}")
        
        # Bucle: Genera las nuevas filas
        newFilas = []
        for nwFila in colVarEntr:
            n = []
            antiguaFila = []
            if(float(nwFila) != pibote):
                indexF = colVarEntr.index(nwFila)
                for p in range(variable+restriccion+1):
                    item = float(self.ui.tableResult.item(indexF+2,p+2).text())
                    antiguaFila.append(round(item, 3))
                
                for fPibo in filaPibote:
                    item = float(fPibo * (nwFila * -1)) 
                    n.append(item)
            
                suma = np.array(antiguaFila) + np.array(n)
                newFilas.append(suma.tolist())

                # CAMBIAR FOR INICIAL POR EL LEN DE COLVARENTR 
                for f in range(len(newFilas)):
                    print(f"List: {newFilas[f]}")
                    for nF in range(variable+restriccion+1):
                        print(f"X: {newFilas[f][nF]}")
                        item = newFilas[f][nF]
                #cellItem = QTableWidgetItem(str(item))
                #self.ui.tableResult.setItem(indexF+2,p+2,cellItem)
        """ for f in range(len(newFilas)):
            print(f"List: {newFilas[f]}")
            for nF in range(variable+restriccion+1):
                print(f"X: {newFilas[f][nF]}")
                item = newFilas[f][nF] """
                
        print(f"Nuevas Filas: {newFilas}")
        
    # Método: Elimina los datos de la tabla
    def deleteData(self):
        # Resetea las tablas y labels
        self.generateArrays()
        self.ui.tableResult.clear()
        self.ui.lblMaxZ.setText("")
        self.ui.lblRestricc.setText("")
        
        # Habilita el botón generar
        self.ui.btnGenerar.setEnabled(True)
        self.ui.btnCalcular.setEnabled(False)
        
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
          
# Inicia la aplicación
if __name__ == '__main__':
    app = QApplication([])
    mi_App = Simplex()
    mi_App.show()
    sys.exit(app.exec_())
    
    