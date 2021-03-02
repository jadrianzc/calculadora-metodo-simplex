from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from Simplex import Simplex
from vista.ui_mainWindow import Ui_MainWindow
import sys, os

class MainWindow(QMainWindow):
    # Constructor
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Resolver Ruta
        def resolver_ruta(ruta_relativa):
            if hasattr(sys, "_MEIPASS"):
                return os.path.join(sys._MEIPASS, ruta_relativa)
            return os.path.join(os.path.abspath("."), ruta_relativa)
        
        self.icoMain = resolver_ruta("conta.ico")
        self.setWindowIcon(QIcon(self.icoMain))
        
        self.ui.actionSimplex.triggered.connect(self.showSimplexUI)
        self.ui.actionPerl_CPM.triggered.connect(self.showPerlUI)
        
    def showSimplexUI(self):
        # self.simplex.open()
        self.ui.widgetPerl.setVisible(False)
        self.ui.widgetSimplex.setVisible(True)
        self.simplex = Simplex(self.ui)
        self.simplex.deleteData()
        

    def showPerlUI(self):
        self.ui.widgetSimplex.setVisible(False)
        self.ui.widgetPerl.setVisible(True)
    
# Inicia la aplicación
if __name__ == '__main__':    
    app = QApplication([])
    app.setStyle(QStyleFactory.create('Fusion'))
    mi_App = MainWindow()
    mi_App.show()
    sys.exit(app.exec_())