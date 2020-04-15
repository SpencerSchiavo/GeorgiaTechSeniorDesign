import sys
from PyQt5.QtWidgets import QApplication,QFormLayout,QLineEdit,QWidget,QPushButton,QLabel,QSpinBox,QSlider,QCheckBox,QHBoxLayout,QMessageBox
from PyQt5.QtGui import QIcon,QIntValidator, QDoubleValidator
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

### Form 1 Setup
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('DSD Workforce Planning Optimizer')
layout = QFormLayout()

############################## Begin Outputs #########################################
### Form 2 Setup
############################## End Outputs  #########################################

### daily demand label
demand_label=QLabel("Today's Carton Demand: ")

### daily demand input
demand_input=QSpinBox()
demand_input.setRange(0,1000000)

### associate count input
associate_input=QSpinBox()
associate_input.setRange(0,100)

### min sort time checkbox
def grey_box(state):
    if state > 0:
        min_sort_time_input.setValue(0)
        min_sort_time_input.setEnabled(0)
    else:
        min_sort_time_input.setEnabled(1)

min_sort_cb = QCheckBox("I don't know")
min_sort_cb.stateChanged.connect(grey_box)

### max sort time checkbox
def grey_box2(state):
    if state > 0:
        max_sort_time_input.setValue(0)
        max_sort_time_input.setEnabled(0)
    else:
        max_sort_time_input.setEnabled(1)

max_sort_cb = QCheckBox("I don't know")
max_sort_cb.stateChanged.connect(grey_box2)

### avg sort time checkbox
def grey_box3(state):
    if state > 0:
        avg_sort_time_input.setValue(0)
        avg_sort_time_input.setEnabled(0)
    else:
        avg_sort_time_input.setEnabled(1)

avg_sort_cb = QCheckBox("I don't know")
avg_sort_cb.stateChanged.connect(grey_box3)


### min sort time input
min_sort_time_input=QSpinBox()
min_sort_time_input.setRange(0,9999)


### max sort time input
max_sort_time_input=QSpinBox()
max_sort_time_input.setRange(0,9999)


### avg sort time input
avg_sort_time_input=QSpinBox()
avg_sort_time_input.setRange(0,9999)


### min load time input
min_load_time_input=QSpinBox()
min_load_time_input.setRange(0,9999)

### max time input
max_load_time_input=QSpinBox()
max_load_time_input.setRange(0,9999)


### num replications input
def valuechange():
	reps = reps_input.value()
	return(reps)

reps_input=QSlider()
reps_input.setOrientation(1)
reps_input.setTickPosition(0)
reps_input.setRange(100,10000)
reps_input.valueChanged.connect(valuechange)


### calculate nums fxn
def msgButtonClick(i):
    if i.text()=='OK':
        window.hide()
        new_win()
    else:
        pass

########################################################## begin compute constant fxn
def computeConstant(demand_input, associate_input, avg_sort_time_input,reps, min_load_time_input, max_load_time_input):
    bufferNum=1.4
    manHoursList = []
    overtimeCurrent = []
    overtimeOptimal = []
    outputList = []
    data = pd.read_csv('WSI_dimensional_data.csv')
    volume = data['Volume']
    for i in range(reps):
        sort_list = []
        for carton in range(demand_input):
            sort_list.append(avg_sort_time_input)
        # dimensional data
        pallets = 0
        vol = 0
        dims = np.random.choice(volume, demand_input)
        for i in range(len(dims)):
            if vol + dims[i] > 115000:
                pallets += 1
                vol = dims[i]
            else:
                vol += dims[i]
            if dims[i] > 23000:
                sort_list[i] = sort_list[i] * 2
        loading_time = np.random.uniform(min_load_time_input * 60, max_load_time_input * 60)
        if pallets > 12:
            loading_time = loading_time * 2
        # sum of all sorting times + sum of all loading times
        # + constant value for wrapping times the buffer which accounts for staging
        manHours = ((sum(sort_list) + loading_time + pallets * 90) * bufferNum) / 3600
        manHoursList.append(manHours)
    if (sum(manHoursList) / reps) < 18:
        optimal_associates = 2
        no_hours_optimal = (sum(manHoursList) / reps) / 2
    else:
        optimal_associates = math.ceil((sum(manHoursList) / reps) / 9)
        no_hours_optimal = (sum(manHoursList) / reps) / optimal_associates
    no_hours_current = (sum(manHoursList) / reps) / associate_input
    for j in range(len(manHoursList)):
        if (manHoursList[j] / associate_input) > 9:
            overtimeCurrent.append(1)
        else:
            overtimeCurrent.append(0)
        if (manHoursList[j] / optimal_associates) > 9:
            overtimeOptimal.append(1)
        else:
            overtimeOptimal.append(0)
    currentProportion = sum(overtimeCurrent) / len(overtimeCurrent)
    optimalProportion = sum(overtimeOptimal) / len(overtimeOptimal)
    currentCI = [max(currentProportion - (1.96 * ((currentProportion * (1 - currentProportion)) / reps) ** 0.5), 0),
        currentProportion + (1.96 * ((currentProportion * (1 - currentProportion)) / reps) ** 0.5)]
    optimalCI = [max(optimalProportion - (1.96 * ((optimalProportion * (1 - optimalProportion)) / reps) ** 0.5), 0),
        optimalProportion + (1.96 * ((optimalProportion * (1 - optimalProportion)) / reps) ** 0.5)]
    outputList = [associate_input, no_hours_current, currentProportion, currentCI[0], currentCI[1],
                    optimal_associates, no_hours_optimal, optimalProportion, optimalCI[0], optimalCI[1]]
    return outputList
########################################################## end compute constant fxn


########################################################## begin compute uniform fxn
def computeUniform(demand_input, associate_input, min_sort_time_input, max_sort_time_input, reps, min_load_time_input, max_load_time_input):
    bufferNum=1.4
    manHoursList = []
    overtimeCurrent = []
    overtimeOptimal = []
    outputList = []
    data = pd.read_csv('WSI_dimensional_data.csv')
    volume = data['Volume']
    for i in range(reps):
        sort_list = []
        for carton in range(demand_input):
            sort_list.append(np.random.uniform(min_sort_time_input, max_sort_time_input))
        # dimensional data
        pallets = 0
        vol = 0
        dims = np.random.choice(volume, demand_input)
        for i in range(len(dims)):
            if vol + dims[i] > 115000:
                pallets += 1
                vol = dims[i]
            else:
                vol += dims[i]
            if dims[i] > 23000:
                sort_list[i] = sort_list[i] * 2
        loading_time = np.random.uniform(min_load_time_input * 60, max_load_time_input * 60)
        if pallets > 12:
            loading_time = loading_time * 2
        # sum of all sorting times + sum of all loading times
        # + constant value for wrapping times the buffer which accounts for staging
        manHours = ((sum(sort_list) + loading_time + pallets * 90) * bufferNum) / 3600
        manHoursList.append(manHours)
    if (sum(manHoursList) / reps) < 18:
        optimal_associates = 2
        no_hours_optimal = (sum(manHoursList) / reps) / 2
    else:
        optimal_associates = math.ceil((sum(manHoursList) / reps) / 9)
        no_hours_optimal = (sum(manHoursList) / reps) / optimal_associates
    no_hours_current = (sum(manHoursList) / reps) / associate_input
    for j in range(len(manHoursList)):
        if (manHoursList[j] / associate_input) > 9:
            overtimeCurrent.append(1)
        else:
            overtimeCurrent.append(0)
        if (manHoursList[j] / optimal_associates) > 9:
            overtimeOptimal.append(1)
        else:
            overtimeOptimal.append(0)
    currentProportion = sum(overtimeCurrent) / len(overtimeCurrent)
    optimalProportion = sum(overtimeOptimal) / len(overtimeOptimal)
    currentCI = [max(currentProportion - (1.96 * ((currentProportion * (1 - currentProportion)) / reps) ** 0.5), 0),
        currentProportion + (1.96 * ((currentProportion * (1 - currentProportion)) / reps) ** 0.5)]
    optimalCI = [max(optimalProportion - (1.96 * ((optimalProportion * (1 - optimalProportion)) / reps) ** 0.5), 0),
        optimalProportion + (1.96 * ((optimalProportion * (1 - optimalProportion)) / reps) ** 0.5)]
    outputList = [associate_input, no_hours_current, currentProportion, currentCI[0], currentCI[1],
                    optimal_associates, no_hours_optimal, optimalProportion, optimalCI[0], optimalCI[1]]
    return outputList
########################################################## end compute uniform fxn


########################################################## begin compute triangular fxn
def computeTriangular(demand_input, associate_input, min_sort_time_input, max_sort_time_input, avg_sort_time_input, reps, min_load_time_input,max_load_time_input):
    bufferNum=1.4
    manHoursList = []
    overtimeCurrent = []
    overtimeOptimal = []
    outputList = []
    data = pd.read_csv('WSI_dimensional_data.csv')
    volume = data['Volume']
    for i in range(reps):
        sort_list = []
        for carton in range(demand_input):
            sort_list.append(np.random.triangular(min_sort_time_input, avg_sort_time_input, max_sort_time_input))
        # dimensional data
        pallets = 0
        vol = 0
        dims = np.random.choice(volume, demand_input)
        for i in range(len(dims)):
            if vol + dims[i] > 115000:
                pallets += 1
                vol = dims[i]
            else:
                vol += dims[i]
            if dims[i] > 23000:
                sort_list[i] = sort_list[i] * 2
        loading_time = np.random.uniform(min_load_time_input * 60, max_load_time_input * 60)
        if pallets > 12:
            loading_time = loading_time * 2
        # sum of all sorting times + sum of all loading times
        # + constant value for wrapping times the buffer which accounts for staging
        manHours = ((sum(sort_list) + loading_time + pallets * 90) * bufferNum) / 3600
        manHoursList.append(manHours)
    if (sum(manHoursList) / reps) < 18:
        optimal_associates = 2
        no_hours_optimal = (sum(manHoursList) / reps) / 2
    else:
        optimal_associates = math.ceil((sum(manHoursList) / reps) / 9)
        no_hours_optimal = (sum(manHoursList) / reps) / optimal_associates
    no_hours_current = (sum(manHoursList) / reps) / associate_input
    for j in range(len(manHoursList)):
        if (manHoursList[j] / associate_input) > 9:
            overtimeCurrent.append(1)
        else:
            overtimeCurrent.append(0)
        if (manHoursList[j] / optimal_associates) > 9:
            overtimeOptimal.append(1)
        else:
            overtimeOptimal.append(0)
    currentProportion = sum(overtimeCurrent) / len(overtimeCurrent)
    optimalProportion = sum(overtimeOptimal) / len(overtimeOptimal)
    currentCI = [
        max(currentProportion - (1.96 * ((currentProportion * (1 - currentProportion)) / reps) ** 0.5), 0),
        currentProportion + (1.96 * ((currentProportion * (1 - currentProportion)) / reps) ** 0.5)]
    optimalCI = [
        max(optimalProportion - (1.96 * ((optimalProportion * (1 - optimalProportion)) / reps) ** 0.5), 0),
        optimalProportion + (1.96 * ((optimalProportion * (1 - optimalProportion)) / reps) ** 0.5)]
    outputList = [associate_input, no_hours_current, currentProportion, currentCI[0], currentCI[1],
                    optimal_associates, no_hours_optimal, optimalProportion, optimalCI[0], optimalCI[1]]
    print(manHoursList[0:50])
    return outputList
########################################################## end compute triangular fxn

def popup_message(clicked):
    msgBox = QMessageBox()

    if  min_sort_time_input.value()==0 or  max_sort_time_input.value()==0:
        reps=valuechange()
        out_list=computeConstant(demand_input.value(), associate_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())
        give_or_take = round((out_list[4]-out_list[2]),2)*100

        if out_list[0]==out_list[5]:
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("You have today's optimal team size...\nLet's do this!")
            msgBox.setInformativeText('Click "OK" to view projections.\nClick "Cancel" to go back.')
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        else:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("You may experience some inefficiencies...\nConsider adjusting today's team size.")
            msgBox.setDetailedText("Current Probability of Overtime: "+(str(out_list[2]*100))+"% (\u00B1"+str(give_or_take)+'%)\n\nCurrent Estimated Work Duration: '+str(round(out_list[1],1))+' hours')
            msgBox.setInformativeText('Click "OK" to view recommendations.\nClick "Show Details" to view current projections\nClick "Cancel" to go back.')
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        print("using constant fxn...")

    if  avg_sort_time_input.value()==0:
        reps=valuechange()
        out_list=computeUniform(demand_input.value(), associate_input.value(),min_sort_time_input.value(),max_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())
        give_or_take = round((out_list[4]-out_list[2]),2)*100

        if out_list[0]==out_list[5]:
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("You have today's optimal team size...\nLet's do this!")
            msgBox.setInformativeText('Click "OK" to view projections.\nClick "Cancel" to go back.')
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        else:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("You may experience some inefficiencies...\nConsider adjusting today's team size.")
            msgBox.setDetailedText("Current Probability of Overtime: "+(str(out_list[2]*100))+"% (\u00B1"+str(give_or_take)+'%)\n\nCurrent Estimated Work Duration: '+str(round(out_list[1],1))+' hours')
            msgBox.setInformativeText('Click "OK" to view recommendations.\nClick "Show Details" to view current projections\nClick "Cancel" to go back.')
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        print("using uniform fxn...")

    if  avg_sort_time_input.value()!=0 and min_sort_time_input.value()!=0 and max_sort_time_input.value()!=0:
        reps=valuechange()
        out_list=computeTriangular(demand_input.value(), associate_input.value(),min_sort_time_input.value(),max_sort_time_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())
        give_or_take = round((out_list[4]-out_list[2]),2)*100

        if out_list[0]==out_list[5]:
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("You have today's optimal team size...\nLet's do this!")
            msgBox.setInformativeText('Click "OK" to view projections.\nClick "Cancel" to go back.')
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        else:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("You may experience some inefficiencies...\nConsider adjusting today's team size.")
            msgBox.setDetailedText("Current Probability of Overtime: "+(str(out_list[2]*100))+"% (\u00B1"+str(give_or_take)+'%)\n\nCurrent Estimated Work Duration: '+str(round(out_list[1],1))+' hours')
            msgBox.setInformativeText('Click "OK" to view recommendations.\nClick "Show Details" to view current projections\nClick "Cancel" to go back.')
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        print("using triangular fxn...")
    
    msgBox.buttonClicked.connect(msgButtonClick)
    returnValue = msgBox.exec()
    return out_list
        
        
def new_win():
    window1 = QWidget()
    window1.setWindowTitle('DSD Workforce Planning Optimizer')
    layout1 = QFormLayout()
    
    if min_sort_time_input.value()==0 or  max_sort_time_input.value()==0:
        reps=valuechange()
        give_or_take2 = round(computeConstant(demand_input.value(), associate_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[9]
        -computeConstant(demand_input.value(), associate_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[7],2)*100
        print("using constant output")
        optimal_headcount=QLabel(str(computeConstant(demand_input.value(), associate_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[5])+' employees')
        optimal_hours=QLabel(str(round(computeConstant(demand_input.value(), associate_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[6],1))+' hours')
        optimal_overtime=QLabel(str(computeConstant(demand_input.value(), associate_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[7]*100)+"% (\u00B1"+str(give_or_take2)+'%)')

    if avg_sort_time_input.value()==0:
        reps=valuechange()
        give_or_take2 = round(computeConstant(demand_input.value(), associate_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[9]
        -computeConstant(demand_input.value(), associate_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[7],2)*100
        print("using uniform output")
        optimal_headcount=QLabel(str(computeUniform(demand_input.value(), associate_input.value(),min_sort_time_input.value(),max_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[5])+' employees')
        optimal_hours=QLabel(str(round(computeUniform(demand_input.value(), associate_input.value(),min_sort_time_input.value(),max_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[6],1))+' hours')
        optimal_overtime=QLabel(str(computeUniform(demand_input.value(), associate_input.value(),min_sort_time_input.value(),max_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[7]*100)+"% (\u00B1"+str(give_or_take2)+'%)')

    if avg_sort_time_input.value()!=0 and min_sort_time_input.value()!=0 and max_sort_time_input.value()!=0:
        reps=valuechange()
        give_or_take2 = round(computeConstant(demand_input.value(), associate_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[9]
        -computeConstant(demand_input.value(), associate_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[7],2)*100
        print("using triangular output")
        optimal_headcount=QLabel(str(computeTriangular(demand_input.value(), associate_input.value(),min_sort_time_input.value(),max_sort_time_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[5])+' employees')
        optimal_hours=QLabel(str(round(computeTriangular(demand_input.value(), associate_input.value(),min_sort_time_input.value(),max_sort_time_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[6],1))+' hours')
        optimal_overtime=QLabel(str(computeTriangular(demand_input.value(), associate_input.value(),min_sort_time_input.value(),max_sort_time_input.value(),avg_sort_time_input.value(),reps, min_load_time_input.value(), max_load_time_input.value())[7]*100)+"% (\u00B1"+str(give_or_take2)+'%)')

    ### Optimal Headcount label
    optimal_headcount_label=QLabel("Recommended team size: ")

    ### Hours Needed w/ optimal headcount label
    optimal_hours_label=QLabel("New Estimated Work Duration: ")

    ### Overtime Prob w/ current headcount label
    optimal_overtime_label=QLabel("New Probability of Needing Overtime: ")

    ### clear form fxn
    def restart_form(clicked):
        window1.hide()
        window.show()
        clear_form(1)

    clear_btn2=QPushButton("New Calculation")
    clear_btn2.clicked.connect(restart_form)

    ###  fxn
    def update_form(clicked):
        window1.hide()
        window.show()

    clear_btn3=QPushButton("Go Back")
    clear_btn3.clicked.connect(update_form)

    ### add rows 
    layout1.addRow(optimal_headcount_label,optimal_headcount)
    layout1.addRow(optimal_hours_label,optimal_hours)
    layout1.addRow(optimal_overtime_label,optimal_overtime)
    layout1.addRow(clear_btn3,clear_btn2)


    ###Form 2 Rendering
    window1.setLayout(layout1)
    window1.show()

calculate_btn=QPushButton("Calculate")
calculate_btn.clicked.connect(popup_message)

### clear form fxn
def clear_form(clicked):
    demand_input.setValue(0)
    associate_input.setValue(0)
    min_sort_time_input.setValue(0)
    min_sort_cb.setChecked(0)
    max_sort_time_input.setValue(0)
    max_sort_cb.setChecked(0)
    avg_sort_cb.setChecked(0)
    avg_sort_time_input.setValue(0)
    min_load_time_input.setValue(0)
    max_load_time_input.setValue(0)
    reps_input.setValue(100)

clear_btn=QPushButton("Clear Form")
clear_btn.clicked.connect(clear_form)

### add rows 
layout.addRow(demand_label,demand_input)
layout.addRow(QLabel("Today's Associate Headcount: "),associate_input)

min_sort_widgets=QHBoxLayout()
min_sort_widgets.addWidget(min_sort_time_input)
min_sort_widgets.addWidget(min_sort_cb)
layout.addRow(QLabel("Quickest Sorting Time Possible (seconds): "),min_sort_widgets)

max_sort_widgets=QHBoxLayout()
max_sort_widgets.addWidget(max_sort_time_input)
max_sort_widgets.addWidget(max_sort_cb)
layout.addRow(QLabel("Slowest Sorting Time Possible (seconds): "),max_sort_widgets)

avg_sort_widgets=QHBoxLayout()
avg_sort_widgets.addWidget(avg_sort_time_input)
avg_sort_widgets.addWidget(avg_sort_cb)
layout.addRow(QLabel("Average Sorting Time (seconds): "),avg_sort_widgets)


layout.addRow(QLabel("Quickest Loading Time Possible (mins): "),min_load_time_input)
layout.addRow(QLabel("Slowest Loading Time Possible (mins): "),max_load_time_input)

reps_widgets=QHBoxLayout()
reps_widgets.addWidget(QLabel("Less Accurate\n(100 simulations)"))
reps_widgets.addWidget(reps_input)
reps_widgets.addWidget(QLabel("More Accurate\n(10,000 simulations)"))
layout.addRow(QLabel("Result Accuracy: "),reps_widgets)

layout.addRow(clear_btn, calculate_btn)

###Form Rendering
window.setLayout(layout)
window.show()
sys.exit(app.exec_())