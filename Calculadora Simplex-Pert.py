from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from src.simplex import Simplex
from src.perl import Perl
from src.views.ui_mainWindow import Ui_MainWindow
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
        
        # Icono ventana
        self.icoMain = resolver_ruta("./src/assets/InvOpeLogo.ico")
        self.icoError = resolver_ruta("./src/assets/cancelar.ico")
        self.icoSucess = resolver_ruta("./src/assets/check.ico")
        self.setWindowIcon(QIcon(self.icoMain))

        # Imagenes
        self.img = resolver_ruta("./src/assets/welcome2.png")
        pixmap = QPixmap(self.img)
        self.ui.label.setPixmap(pixmap)
        self.ui.label.setAlignment(Qt.AlignCenter)
        
        # Eventos
        self.ui.actionSimplex.triggered.connect(self.showSimplexUI)
        self.ui.actionPerl_CPM.triggered.connect(self.showPerlUI)

    # Método: Muestra la interfaz del método simplex  
    def showSimplexUI(self):
        self.ui.widgetPerl.setVisible(False)
        self.ui.widgetSimplex.setVisible(True)
        self.simplex = Simplex(self.ui, self.icoError, self.icoSucess, self.icoMain)
        self.simplex.deleteData()

    # Método: Muestra la interfaz del modelo de redes
    def showPerlUI(self):
        self.ui.widgetSimplex.setVisible(False)
        self.ui.widgetPerl.setVisible(True)
        self.ui.groupBoxInputActv.setVisible(False)
        self.perl = Perl(self.ui, self.icoError, self.icoSucess, self.icoMain)
    
# Inicia la aplicación
if __name__ == '__main__':    
    app = QApplication([])
    app.setStyle(QStyleFactory.create('Fusion'))
    mi_App = MainWindow()
    mi_App.show()
    sys.exit(app.exec_())