from PyQt5.QtWidgets import *
from vista.ui_metodoSimplex import Ui_Form
import numpy as np
import sys, re

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
            self.ui.tableRestr.setEnabled(False) 
            self.ui.tableFuncObj.setEnabled(False) 
            self.ui.tableResult .setEnabled(False)
            
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
                    else:
                        if(c == 0):
                            item = "0"
                        elif(c == 1):
                            if(f <= fila+1):
                                incremento3 += 1
                                print(incremento3)
                                item = f"S{incremento3}"
                        else:
                            newFila = f - 2
                            newColu = c - 2
                            item = f"{self.matrizRestrNum[newFila][newColu]}"
                    
                    cellItem = QTableWidgetItem(item)
                    self.ui.tableResult.setItem(f,c,cellItem)
                            
        except Exception as err:
            print(f"Error f: {err}")  
        

    # Método: Elimina los datos de la tabla
    def deleteData(self):
        # Resetea las tablas y labels
        self.generateArrays()
        self.ui.tableResult.clear()
        self.ui.lblMaxZ.setText("")
        self.ui.lblRestricc.setText("")
        
        # Habilita el botón calcular y generar
        self.ui.btnCalcular.setEnabled(True)
        self.ui.btnGenerar.setEnabled(True)
        self.ui.tableFuncObj.setEnabled(True) 
        self.ui.tableRestr.setEnabled(True) 
        self.ui.tableResult .setEnabled(True)
        self.ui.tableFuncObj.destroy()
          
# Inicia la aplicación
if __name__ == '__main__':
    app = QApplication([])
    mi_App = Simplex()
    mi_App.show()
    sys.exit(app.exec_())
    
    