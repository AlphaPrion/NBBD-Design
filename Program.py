import sys
from NBB import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QCheckBox,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedLayout,
    QTableWidget,
    QTableWidgetItem,
    QSpinBox,
    QMessageBox
)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Neighbor Balanced Block Design")
        self.setMinimumSize(800,400)

        mainLayout = QVBoxLayout()
        dualPane = QHBoxLayout()
        inputsPane = QVBoxLayout()

        # number of treatments input
        treatmentsLayout = QHBoxLayout()
        treatmentsLayout.addWidget(QLabel("Number of Treatments:"))
        self.elementsInput = QSpinBox()
        self.elementsInput.setRange(3,13)
        self.elementsInput.setFixedWidth(100)
        treatmentsLayout.addWidget(self.elementsInput)
        inputsPane.addLayout(treatmentsLayout)

        # number of blocks input
        blocksLayout = QHBoxLayout()
        blocksLayout.addWidget(QLabel("Number of Blocks:"))
        self.blocksInput = QSpinBox()
        self.blocksInput.setRange(1, self.elementsInput.value())
        self.blocksInput.setFixedWidth(100)
        blocksLayout.addWidget(self.blocksInput)
        inputsPane.addLayout(blocksLayout)

        # check for control input
        self.controlInput = QCheckBox()
        self.controlInput.setText("Include Control")
        inputsPane.addWidget(self.controlInput)

        self.themeInput = QCheckBox()
        self.themeInput.setText("Colour Coded")
        inputsPane.addWidget(self.themeInput)

        # clear and enter buttons
        buttonLayout = QHBoxLayout()
        generateButton = QPushButton("Generate")
        generateButton.clicked.connect(self.generate)
        clearButton = QPushButton("Clear")
        clearButton.clicked.connect(self.elementsInput.clear)
        clearButton.clicked.connect(self.blocksInput.clear)
        buttonLayout.addWidget(clearButton)
        buttonLayout.addWidget(generateButton)
        inputsPane.addLayout(buttonLayout)
        buttonLayout.setContentsMargins(0, 250, 0, 0)
        inputsPane.addStretch(0)

        # table of results, majority in function
        self.resultsGrid = QTableWidget()

        # list of previous generations
        self.history = QTableWidget()
        self.history.setColumnCount(1)
        self.history.horizontalHeader().setDefaultSectionSize(self.width())
        self.history.horizontalHeader().hide()

        # make sure no more blocks are requested than elements, and handle
        # the unusual behaviour for certain numbers of elements
        self.elementsInput.valueChanged.connect(self.inputRange)
        self.blocksInput.valueChanged.connect(self.inputRange)

        # create tabs layout
        tabsPane = QStackedLayout()
        resultsTabs = QTabWidget()  
        resultsTabs.addTab(self.resultsGrid, str("Results"))
        resultsTabs.addTab(self.history, str("History"))
        tabsPane.addWidget(resultsTabs)

        dualPane.addLayout(inputsPane)
        dualPane.addLayout(tabsPane, 70)
        mainLayout.addLayout(dualPane)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def generate(self):
        try:
            control = int(not self.controlInput.isChecked())
            numOfElements = int(self.elementsInput.text())
            numOfBlocks = int(self.blocksInput.text())

            blocks = NBB.generate(numOfElements, numOfBlocks, control)

            self.resultsGrid.setColumnCount(len(blocks[0])+4)
            self.resultsGrid.setRowCount(len(blocks))
            self.resultsGrid.horizontalHeader().setDefaultSectionSize(1)
            self.resultsGrid.horizontalHeader().hide()
            self.resultsGrid.verticalHeader().setStyleSheet("font-weight: bold")
            self.resultsGrid.verticalHeader().setDefaultSectionSize(1)
            self.resultsGrid.setShowGrid(False)

            for block in range(len(blocks)):
                self.resultsGrid.setItem(block,0,QTableWidgetItem(str(blocks[block][len(blocks[block])-1])))
                self.resultsGrid.setItem(block,1,QTableWidgetItem("|"))

                for element in range(len(blocks[block])):
                    item = QTableWidgetItem(str(blocks[block][element]))
                    if self.themeInput.isChecked():
                        colour = QColor()
                        colourRange = 359//numOfElements
                        colour.setHsv(blocks[block][element]*colourRange,150,255)
                        item.setBackground(colour)
                    self.resultsGrid.setItem(block, element+2, item)

                self.resultsGrid.setItem(block, len(blocks[block])+2, QTableWidgetItem("|"))
                self.resultsGrid.setItem(block, len(blocks[block])+3, QTableWidgetItem(str(blocks[block][0])))


            if not self.history.findItems(QTableWidgetItem(str(blocks)[1:-1]).text(), Qt.MatchFlag.MatchContains):
                rows = self.history.rowCount()
                self.history.insertRow(rows)
                self.history.setItem(rows, 0, QTableWidgetItem(str(blocks)[1:-1]))
                self.history.resizeColumnsToContents()

        except:
            warning = QMessageBox(self)
            warning.setWindowTitle("Warning")
            warning.setText("Please enter the required number of blocks and treatments")
            warning.exec()


    def inputRange(self):
        
        if self.elementsInput.value() == 6 and self.blocksInput.value() >= 5:
            self.blocksInput.setMaximum(4)
            warning = QMessageBox(self)
            warning.setWindowTitle("Warning")
            warning.setText("Due to the nature of the design used, only 4 blocks can be created of 6 elements")
            warning.exec()

        elif self.elementsInput.value() in {10, 12} and self.blocksInput.value() >= self.elementsInput.value():
            self.blocksInput.setMaximum(self.elementsInput.value()-1)
            warning = QMessageBox(self)
            warning.setWindowTitle("Warning")
            warning.setText("Due to the nature of the design used, only "+str(self.elementsInput.value()-1)+" blocks can be created of "+str(self.elementsInput.value())+" elements")
            warning.exec()
            
        else:
            self.blocksInput.setMaximum(self.elementsInput.value())

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()