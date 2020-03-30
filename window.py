# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_app.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

## 2 GUIs in one app - 1 for daily demand & 1 for seasonal demand

## Work on all zeroes test case

import pandas as pd
import numpy as np
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        ## INITIAL SETUP ##
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        ## PUSH BUTTON SETUP ##
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(650, 800, 150, 100))
        self.pushButton.setObjectName("pushButton")
        ## INPUT BOXES SETUP ##
        self.meanDemandInput = QtWidgets.QLineEdit(self.centralwidget)
        self.meanDemandInput.setGeometry(QtCore.QRect(50, 200, 130, 50))
        self.meanDemandInput.setText("")
        self.meanDemandInput.setObjectName("meanDemandInput")
        self.associatesInput = QtWidgets.QLineEdit(self.centralwidget)
        self.associatesInput.setGeometry(QtCore.QRect(300, 200, 130, 50))
        self.associatesInput.setText("")
        self.associatesInput.setObjectName("associatesInput")
        self.minTimeInput = QtWidgets.QLineEdit(self.centralwidget)
        self.minTimeInput.setGeometry(QtCore.QRect(550, 200, 130, 50))
        self.minTimeInput.setText("")
        self.minTimeInput.setObjectName("minTimeInput")
        self.maxTimeInput = QtWidgets.QLineEdit(self.centralwidget)
        self.maxTimeInput.setGeometry(QtCore.QRect(800, 200, 130, 50))
        self.maxTimeInput.setText("")
        self.maxTimeInput.setObjectName("maxTimeInput")
        self.meanTimeInput = QtWidgets.QLineEdit(self.centralwidget)
        self.meanTimeInput.setGeometry(QtCore.QRect(1050, 200, 130, 50))
        self.meanTimeInput.setText("")
        self.meanTimeInput.setObjectName("meanTimeInput")
        self.inputs = [self.meanDemandInput, self.associatesInput,
                       self.minTimeInput, self.maxTimeInput, self.meanTimeInput]
        ## OUTPUT BOXES SETUP ##
        self.currentHours = QtWidgets.QTextBrowser(self.centralwidget)
        self.currentHours.setGeometry(QtCore.QRect(250, 500, 141, 111))
        self.currentHours.setObjectName("currentHours")
        self.optimalHours = QtWidgets.QTextBrowser(self.centralwidget)
        self.optimalHours.setGeometry(QtCore.QRect(650, 500, 141, 111))
        self.optimalHours.setObjectName("optimalHours")
        self.optimalAss = QtWidgets.QTextBrowser(self.centralwidget)
        self.optimalAss.setGeometry(QtCore.QRect(1000, 500, 141, 111))
        self.optimalAss.setObjectName("optimalAss")
        self.outputs = [self.currentHours, self.optimalHours, self.optimalAss]
        ## LABELS SETUP ##
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 150, 250, 30))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(290, 150, 250, 30))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(200, 450, 250, 30))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(600, 450, 250, 30))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(950, 450, 250, 30))
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(560, 150, 250, 30))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(790, 150, 250, 30))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(1040, 150, 250, 30))
        self.label_9.setObjectName("label_9")
        ## MENU & TOOL BAR SETUP ##
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        ## PUSH BUTTON ACTIONS ##
        self.pushButton.clicked.connect(self.buttonClicked)
        ## VALIDATORS
        self.onlyInt = QIntValidator()
        self.meanDemandInput.setValidator(self.onlyInt)
        self.associatesInput.setValidator(self.onlyInt)
        self.onlyDouble = QDoubleValidator()
        self.meanTimeInput.setValidator(self.onlyDouble)
        ## RETRANSLATING ##
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def buttonClicked(self):
        for output in self.outputs: ## Clears all output boxes
            output.clear()
        b0 = (self.meanDemandInput.text() != "")
        b1 = (self.meanTimeInput.text() != "")
        b2 = (self.maxTimeInput.text() != "")
        b3 = (self.minTimeInput.text() != "")
        b4 = (self.associatesInput.text() != "")
        if (b0 and b1 and b4 and  not b2 and not b3):
            outList = self.computeConstant(int(self.meanDemandInput.text()),
                                           int(self.associatesInput.text()),
                                           float(self.meanTimeInput.text()), 1.4)
        elif (b0 and b2 and b3 and b4 and not b1):
            outList = self.computeUniform(int(self.meanDemandInput.text()),
                                           int(self.associatesInput.text()),
                                           float(self.minTimeInput.text()),
                                           float(self.maxTimeInput.text()), 1.4)
        elif (b0 and b1 and b2 and b3 and b4):
            outList = self.computeTriangular(int(self.meanDemandInput.text()),
                                          int(self.associatesInput.text()),
                                          float(self.minTimeInput.text()),
                                          float(self.maxTimeInput.text()),
                                          float(self.minTimeInput.text()), 1.4)
        else:
            outList = ["", "", ""]
        self.currentHours.insertPlainText(str(outList[1]))
        self.optimalHours.insertPlainText(str(outList[2]))
        self.optimalAss.insertPlainText(str(outList[0]))

    #########   START SCRIPTING FUNCTIONS    #########

    # Computes the optimal number of associates w/ respective day-hours
    @staticmethod
    def computeConstant(dailyDemand, numAssociates, constantSort, bufferNum):    ## CHANGE THIS
        sort_list = []
        for carton in range(dailyDemand):
            sort_list.append(constantSort)
        data = pd.read_csv('WSI_dimensional_data.csv')
        volume = data['Volume']
        # dimensional data
        pallets = 0
        vol = 0
        dims = np.random.choice(volume, dailyDemand)
        for i in range(len(dims)):
            if vol + dims[i] > 115000:
                pallets += 1
                vol = dims[i]
            else:
                vol += dims[i]
            if dims[i] > 23000:
                sort_list[i] = sort_list[i] * 2
        loading_time = np.random.uniform(1200, 1800)
        if pallets > 12:
            loading_time = loading_time * 2
        # sum of all sorting times + sum of all loading times
        # + constant value for wrapping times the buffer which accounts for staging
        manHours = ((sum(sort_list) + loading_time + pallets * 90) * bufferNum) / 3600
        no_hours_current = manHours / numAssociates
        if manHours < 18:
            optimal_associates = 2
            no_hours_optimal = manHours / 2
        else:
            optimal_associates = math.ceil(manHours / 9)
            no_hours_optimal = manHours / optimal_associates
        outputList = [optimal_associates, no_hours_current, no_hours_optimal]
        return outputList

    @staticmethod
    def computeUniform(dailyDemand, numAssociates, minSort, maxSort, bufferNum):
        sort_list = []
        for carton in range(dailyDemand):
            sort_list.append(np.random.uniform(minSort, maxSort))
        data = pd.read_csv('WSI_dimensional_data.csv')
        volume = data['Volume']
        pallets = 0
        vol = 0
        dims = np.random.choice(volume, dailyDemand)
        for i in range(len(dims)):
            if vol + dims[i] > 115000:
                pallets += 1
                vol = dims[i]
            else:
                vol += dims[i]
            if dims[i] > 23000:
                sort_list[i] = sort_list[i] * 2
        loading_time = np.random.uniform(1200, 1800)
        if pallets > 12:
            loading_time = loading_time * 2
        # sum of all sorting times + sum of all loading times
        # + constant value for wrapping times the buffer which accounts for staging
        manHours = ((sum(sort_list) + loading_time + pallets * 90) * bufferNum) / 3600
        no_hours_current = manHours / numAssociates
        if manHours < 18:
            optimal_associates = 2
            no_hours_optimal = manHours / 2
        else:
            optimal_associates = math.ceil(manHours / 9)
            no_hours_optimal = manHours / optimal_associates
        outputList = [optimal_associates, no_hours_current, no_hours_optimal]
        return outputList

    @staticmethod
    def computeTriangular(dailyDemand, numAssociates, minSort, maxSort, meanSort, bufferNum):
        sort_list = []
        for carton in range(dailyDemand):
            sort_list.append(np.random.triangular(minSort, meanSort, maxSort))
        data = pd.read_csv('WSI_dimensional_data.csv')
        volume = data['Volume']
        pallets = 0
        vol = 0
        dims = np.random.choice(volume, dailyDemand)
        for i in range(len(dims)):
            if vol + dims[i] > 115000:
                pallets += 1
                vol = dims[i]
            else:
                vol += dims[i]
            if dims[i] > 23000:
                sort_list[i] = sort_list[i] * 2
        loading_time = np.random.uniform(1200, 1800)
        if pallets > 12:
            loading_time = loading_time * 2
        # sum of all sorting times + sum of all loading times
        # + constant value for wrapping times the buffer which accounts for staging
        manHours = ((sum(sort_list) + loading_time + pallets * 90) * bufferNum) / 3600
        no_hours_current = manHours / numAssociates
        if manHours < 18:
            optimal_associates = 2
            no_hours_optimal = manHours / 2
        else:
            optimal_associates = math.ceil(manHours / 9)
            no_hours_optimal = manHours / optimal_associates
        outputList = [optimal_associates, no_hours_current, no_hours_optimal]
        return outputList

    #########   END SCRIPTING FUNCTIONS    #########

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Calculate"))
        self.label.setText(_translate("MainWindow", "Demand"))
        self.label_2.setText(_translate("MainWindow", "Current Associates"))
        self.label_3.setText(_translate("MainWindow", "Number Hours w/ Current"))
        self.label_4.setText(_translate("MainWindow", "Number Hours w/ Optimal"))
        self.label_5.setText(_translate("MainWindow", "Optimal Number Associates"))
        self.label_7.setText(_translate("MainWindow", "Min Time to Sort"))
        self.label_8.setText(_translate("MainWindow", "Max Time to Sort"))
        self.label_9.setText(_translate("MainWindow", "Mean Time to Sort"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
