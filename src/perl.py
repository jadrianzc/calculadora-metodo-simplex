from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from src.views.ui_mainWindow import Ui_MainWindow
import numpy as np
import sys, re, os
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