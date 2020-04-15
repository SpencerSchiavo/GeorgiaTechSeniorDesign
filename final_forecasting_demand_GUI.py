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
demand_label=QLabel("Average Seasonal Carton Demand: ")

### daily demand input
demand_input=QSpinBox()
demand_input.setRange(0,1000000)

### StDev demand label
stdev_label=QLabel("Standard Deviation of Carton Demand: ")

### StDev demand input
stdev_input=QSpinBox()
stdev_input.setRange(0,1000000)

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
def msgButtonClick():
    window.hide()
    new_win()

########################################################## begin compute constant fxn
def computeConstant(demand_input, stdev_input, avg_sort_time_input, reps, min_load_time_input, max_load_time_input):
        peak_carton_list = []
        overtimeArr = []
        associateArr = []
        associateCI1Arr = []
        associateCI2Arr = []
        beta = (stdev_input.value() ** 2) / demand_input.value()
        alpha = demand_input.value() / beta
        # demand_dist
        for i in range(reps):
            peak_carton_list.append(int(np.random.gamma(alpha, beta)))
        data = pd.read_csv('WSI_dimensional_data.csv')
        Volume = data['Volume']
        day_time_list = []
        pallet_time = []
        buffer_num = 1.4
        for j in range(len(peak_carton_list)):
            # sortlistadded
            sort_list = []
            for demand in range(peak_carton_list[j]):
                sort_list.append(avg_sort_time_input.value())
            # pallets calculated
            pallets = 0
            Vol = 0
            dims = np.random.choice(Volume, peak_carton_list[j])
            for i in range(len(dims)):
                if Vol + dims[i] > 115000:
                    pallets += 1
                    Vol = dims[i]
                else:
                    Vol += dims[i]
                if dims[i] > 23000:
                    sort_list[i] = sort_list[i] * 2
            # pallet_time
            pallet_time.append((np.random.uniform(min_load_time_input.value() * 60, max_load_time_input.value() * 60)))
            if pallets > 12:
                pallet_time[j] = pallet_time[j] * 2
            # individual_calculations
            # sum of all sorting times + sum of all loading times + constant value for wrapping times the buffer which accounts for staging
            day_time_list.append(
                ((sum(sort_list) + pallet_time[j] + pallets * 90) * buffer_num) / 3600)  ## Man-Hours in a day
        for associate in range(10):     ## 10 Associates
            for ind in range(len(day_time_list)):
                if (day_time_list[ind] / (associate + 1)) > 9:
                    overtimeArr.append(1)
                else:
                    overtimeArr.append(0)
            prop = sum(overtimeArr) / len(overtimeArr)
            associateArr.append(prop)
            associateCI1Arr.append(min(max(prop - (1.96 * ((prop * (1 - prop)) / reps) ** 0.5), 0), 100))
            associateCI2Arr.append(min(max(prop + (1.96 * ((prop * (1 - prop)) / reps) ** 0.5), 0), 100))
            overtimeArr = []
        return [associateArr, associateCI1Arr, associateCI2Arr]
########################################################## end compute constant fxn

########################################################## begin compute uniform fxn
def computeUniform(demand_input, stdev_input, min_sort_time_input, max_sort_time_input, reps, min_load_time_input, max_load_time_input):
    peak_carton_list = []
    overtimeArr = []
    associateArr = []
    associateCI1Arr = []
    associateCI2Arr = []
    beta = (stdev_input.value() ** 2) / demand_input.value()
    alpha = demand_input.value() / beta
    # demand_dist
    for i in range(reps):
        peak_carton_list.append(int(np.random.gamma(alpha, beta)))
    data = pd.read_csv('WSI_dimensional_data.csv')
    Volume = data['Volume']
    day_time_list = []
    pallet_time = []
    buffer_num = 1.4
    for j in range(len(peak_carton_list)):
        # sortlistadded
        sort_list = []
        for demand in range(peak_carton_list[j]):
            sort_list.append(np.random.uniform(min_sort_time_input.value(), max_sort_time_input.value()))
        # pallets calculated
        pallets = 0
        Vol = 0
        dims = np.random.choice(Volume, peak_carton_list[j])
        for i in range(len(dims)):
            if Vol + dims[i] > 115000:
                pallets += 1
                Vol = dims[i]
            else:
                Vol += dims[i]
            if dims[i] > 23000:
                sort_list[i] = sort_list[i] * 2
        # pallet_time
        pallet_time.append((np.random.uniform(min_load_time_input.value() * 60, max_load_time_input.value() * 60)))
        if pallets > 12:
            pallet_time[j] = pallet_time[j] * 2
        # individual_calculations
        # sum of all sorting times + sum of all loading times + constant value for wrapping times the buffer which accounts for staging
        day_time_list.append(
            ((sum(sort_list) + pallet_time[j] + pallets * 90) * buffer_num) / 3600)  ## Man-Hours in a day
    for associate in range(10):  ## 10 Associates
        for ind in range(len(day_time_list)):
            if (day_time_list[ind] / (associate + 1)) > 9:
                overtimeArr.append(1)
            else:
                overtimeArr.append(0)
        prop = sum(overtimeArr) / len(overtimeArr)
        associateArr.append(prop)
        associateCI1Arr.append(min(max(prop - (1.96 * ((prop * (1 - prop)) / reps) ** 0.5), 0), 100))
        associateCI2Arr.append(min(max(prop + (1.96 * ((prop * (1 - prop)) / reps) ** 0.5), 0), 100))
        overtimeArr = []
    print(reps)
    return [associateArr, associateCI1Arr, associateCI2Arr]
########################################################## end compute uniform fxn

########################################################## begin compute triangular fxn
def computeTriangular(demand_input, stdev_input, min_sort_time_input, max_sort_time_input, avg_sort_time_input, reps, min_load_time_input, max_load_time_input):
    peak_carton_list = []
    overtimeArr = []
    associateArr = []
    associateCI1Arr = []
    associateCI2Arr = []
    beta = (stdev_input.value() ** 2) / demand_input.value()
    alpha = demand_input.value() / beta
    # demand_dist
    for i in range(reps):
        peak_carton_list.append(int(np.random.gamma(alpha, beta)))
    data = pd.read_csv('WSI_dimensional_data.csv')
    Volume = data['Volume']
    day_time_list = []
    pallet_time = []
    buffer_num = 1.4
    for j in range(len(peak_carton_list)):
        # sortlistadded
        sort_list = []
        for demand in range(peak_carton_list[j]):
            sort_list.append(np.random.triangular(min_sort_time_input.value(), avg_sort_time_input.value(), max_sort_time_input.value()))
        # pallets calculated
        pallets = 0
        Vol = 0
        dims = np.random.choice(Volume, peak_carton_list[j])
        for i in range(len(dims)):
            if Vol + dims[i] > 115000:
                pallets += 1
                Vol = dims[i]
            else:
                Vol += dims[i]
            if dims[i] > 23000:
                sort_list[i] = sort_list[i] * 2
        # pallet_time
        pallet_time.append((np.random.uniform(min_load_time_input.value() * 60, max_load_time_input.value() * 60)))
        if pallets > 12:
            pallet_time[j] = pallet_time[j] * 2
        # individual_calculations
        # sum of all sorting times + sum of all loading times + constant value for wrapping times the buffer which accounts for staging
        day_time_list.append(
            ((sum(sort_list) + pallet_time[j] + pallets * 90) * buffer_num) / 3600)  ## Hours in a day
    for associate in range(10):  ## 10 Associates
        for ind in range(len(day_time_list)):
            if (day_time_list[ind] / (associate + 1)) > 9:
                overtimeArr.append(1)
            else:
                overtimeArr.append(0)
        prop = sum(overtimeArr) / len(overtimeArr)
        associateArr.append(prop)
        associateCI1Arr.append(min(max(prop - (1.96 * ((prop * (1 - prop)) / reps) ** 0.5), 0), 100))
        associateCI2Arr.append(min(max(prop + (1.96 * ((prop * (1 - prop)) / reps) ** 0.5), 0), 100))
        overtimeArr = []
    return [associateArr, associateCI1Arr, associateCI2Arr]
########################################################## end compute triangular fxn
        
def new_win():
    window1 = QWidget()
    window1.setWindowTitle('DSD Workforce Planning Optimizer')
    layout1 = QFormLayout()
    
    ### Overtime Prob w/ current headcount label
    current_overtime_label_1=QLabel("Probability of Overtime w/ 1 Associates:")
    current_overtime_label_2=QLabel("Probability of Overtime w/ 2 Associates:")
    current_overtime_label_3=QLabel("Probability of Overtime w/ 3 Associates:")
    current_overtime_label_4=QLabel("Probability of Overtime w/ 4 Associates:")
    current_overtime_label_5=QLabel("Probability of Overtime w/ 5 Associates:")
    current_overtime_label_6=QLabel("Probability of Overtime w/ 6 Associates:")
    current_overtime_label_7=QLabel("Probability of Overtime w/ 7 Associates:")
    current_overtime_label_8=QLabel("Probability of Overtime w/ 8 Associates:")
    current_overtime_label_9=QLabel("Probability of Overtime w/ 9 Associates:")
    current_overtime_label_10=QLabel("Probability of Overtime w/ 10 Associates:")

    ### overtime calculations
    if  min_sort_time_input.value()==0 or  max_sort_time_input.value()==0:
        reps=valuechange()
        out_list=computeConstant(demand_input, stdev_input, avg_sort_time_input, reps, min_load_time_input, max_load_time_input)
        
        give_or_take_1 = round((out_list[2][0]-out_list[0][0]),2)*100
        current_overtime_1=QLabel(str(round(out_list[0][0]*100,2))+"% (\u00B1"+str(give_or_take_1)+'%)')

        give_or_take_2 = round((out_list[2][1]-out_list[0][1]),2)*100
        current_overtime_2=QLabel(str(round(out_list[0][1]*100,2))+"% (\u00B1"+str(give_or_take_2)+'%)')

        give_or_take_3 = round((out_list[2][2]-out_list[0][2]),2)*100
        current_overtime_3=QLabel(str(round(out_list[0][2]*100,2))+"% (\u00B1"+str(give_or_take_3)+'%)')

        give_or_take_4 = round((out_list[2][3]-out_list[0][3]),2)*100
        current_overtime_4=QLabel(str(round(out_list[0][3]*100,2))+"% (\u00B1"+str(give_or_take_4)+'%)')

        give_or_take_5 = round((out_list[2][4]-out_list[0][4]),2)*100
        current_overtime_5=QLabel(str(round(out_list[0][4]*100,2))+"% (\u00B1"+str(give_or_take_5)+'%)')

        give_or_take_6 = round((out_list[2][5]-out_list[0][5]),2)*100
        current_overtime_6=QLabel(str(round(out_list[0][5]*100,2))+"% (\u00B1"+str(give_or_take_6)+'%)')

        give_or_take_7 = round((out_list[2][6]-out_list[0][6]),2)*100
        current_overtime_7=QLabel(str(round(out_list[0][6]*100,2))+"% (\u00B1"+str(give_or_take_7)+'%)')

        give_or_take_8 = round((out_list[2][7]-out_list[0][7]),2)*100
        current_overtime_8=QLabel(str(round(out_list[0][7]*100,2))+"% (\u00B1"+str(give_or_take_8)+'%)')

        give_or_take_9 = round((out_list[2][8]-out_list[0][8]),2)*100
        current_overtime_9=QLabel(str(round(out_list[0][8]*100,2))+"% (\u00B1"+str(give_or_take_9)+'%)')

        give_or_take_10 = round((out_list[2][9]-out_list[0][9]),2)*100
        current_overtime_10=QLabel(str(round(out_list[0][9]*100,2))+"% (\u00B1"+str(give_or_take_10)+'%)')

        print(reps)
        print("using Spence's constant algo")

    if  avg_sort_time_input.value()==0:
        reps=valuechange()
        out_list=computeUniform(demand_input, stdev_input, min_sort_time_input, max_sort_time_input, reps, min_load_time_input, max_load_time_input)
        
        give_or_take_1 = round((out_list[2][0]-out_list[0][0]),2)*100
        current_overtime_1=QLabel(str(round(out_list[0][0]*100,2))+"% (\u00B1"+str(give_or_take_1)+'%)')

        give_or_take_2 = round((out_list[2][1]-out_list[0][1]),2)*100
        current_overtime_2=QLabel(str(round(out_list[0][1]*100,2))+"% (\u00B1"+str(give_or_take_2)+'%)')

        give_or_take_3 = round((out_list[2][2]-out_list[0][2]),2)*100
        current_overtime_3=QLabel(str(round(out_list[0][2]*100,2))+"% (\u00B1"+str(give_or_take_3)+'%)')

        give_or_take_4 = round((out_list[2][3]-out_list[0][3]),2)*100
        current_overtime_4=QLabel(str(round(out_list[0][3]*100,2))+"% (\u00B1"+str(give_or_take_4)+'%)')

        give_or_take_5 = round((out_list[2][4]-out_list[0][4]),2)*100
        current_overtime_5=QLabel(str(round(out_list[0][4]*100,2))+"% (\u00B1"+str(give_or_take_5)+'%)')

        give_or_take_6 = round((out_list[2][5]-out_list[0][5]),2)*100
        current_overtime_6=QLabel(str(round(out_list[0][5]*100,2))+"% (\u00B1"+str(give_or_take_6)+'%)')

        give_or_take_7 = round((out_list[2][6]-out_list[0][6]),2)*100
        current_overtime_7=QLabel(str(round(out_list[0][6]*100,2))+"% (\u00B1"+str(give_or_take_7)+'%)')

        give_or_take_8 = round((out_list[2][7]-out_list[0][7]),2)*100
        current_overtime_8=QLabel(str(round(out_list[0][7]*100,2))+"% (\u00B1"+str(give_or_take_8)+'%)')

        give_or_take_9 = round((out_list[2][8]-out_list[0][8]),2)*100
        current_overtime_9=QLabel(str(round(out_list[0][8]*100,2))+"% (\u00B1"+str(give_or_take_9)+'%)')

        give_or_take_10 = round((out_list[2][9]-out_list[0][9]),2)*100
        current_overtime_10=QLabel(str(round(out_list[0][9]*100,2))+"% (\u00B1"+str(give_or_take_10)+'%)')

        print("using Spence's uniform algo")

    if  avg_sort_time_input.value()!=0 and min_sort_time_input.value()!=0 and max_sort_time_input.value()!=0:
        reps=valuechange()
        out_list=computeTriangular(demand_input, stdev_input, min_sort_time_input, max_sort_time_input, avg_sort_time_input,reps, min_load_time_input, max_load_time_input)
        
        give_or_take_1 = round((out_list[2][0]-out_list[0][0]),2)*100
        current_overtime_1=QLabel(str(round(out_list[0][0]*100,2))+"% (\u00B1"+str(give_or_take_1)+'%)')

        give_or_take_2 = round((out_list[2][1]-out_list[0][1]),2)*100
        current_overtime_2=QLabel(str(round(out_list[0][1]*100,2))+"% (\u00B1"+str(give_or_take_2)+'%)')

        give_or_take_3 = round((out_list[2][2]-out_list[0][2]),2)*100
        current_overtime_3=QLabel(str(round(out_list[0][2]*100,2))+"% (\u00B1"+str(give_or_take_3)+'%)')

        give_or_take_4 = round((out_list[2][3]-out_list[0][3]),2)*100
        current_overtime_4=QLabel(str(round(out_list[0][3]*100,2))+"% (\u00B1"+str(give_or_take_4)+'%)')

        give_or_take_5 = round((out_list[2][4]-out_list[0][4]),2)*100
        current_overtime_5=QLabel(str(round(out_list[0][4]*100,2))+"% (\u00B1"+str(give_or_take_5)+'%)')

        give_or_take_6 = round((out_list[2][5]-out_list[0][5]),2)*100
        current_overtime_6=QLabel(str(round(out_list[0][5]*100,2))+"% (\u00B1"+str(give_or_take_6)+'%)')

        give_or_take_7 = round((out_list[2][6]-out_list[0][6]),2)*100
        current_overtime_7=QLabel(str(round(out_list[0][6]*100,2))+"% (\u00B1"+str(give_or_take_7)+'%)')

        give_or_take_8 = round((out_list[2][7]-out_list[0][7]),2)*100
        current_overtime_8=QLabel(str(round(out_list[0][7]*100,2))+"% (\u00B1"+str(give_or_take_8)+'%)')

        give_or_take_9 = round((out_list[2][8]-out_list[0][8]),2)*100
        current_overtime_9=QLabel(str(round(out_list[0][8]*100,2))+"% (\u00B1"+str(give_or_take_9)+'%)')

        give_or_take_10 = round((out_list[2][9]-out_list[0][9]),2)*100
        current_overtime_10=QLabel(str(round(out_list[0][9]*100,2))+"% (\u00B1"+str(give_or_take_10)+'%)')

        print("using Spence's triangular algo")

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
    layout1.addRow(current_overtime_label_1,current_overtime_1)
    layout1.addRow(current_overtime_label_2,current_overtime_2)
    layout1.addRow(current_overtime_label_3,current_overtime_3)
    layout1.addRow(current_overtime_label_4,current_overtime_4)
    layout1.addRow(current_overtime_label_5,current_overtime_5)
    layout1.addRow(current_overtime_label_6,current_overtime_6)
    layout1.addRow(current_overtime_label_7,current_overtime_7)
    layout1.addRow(current_overtime_label_8,current_overtime_8)
    layout1.addRow(current_overtime_label_9,current_overtime_9)
    layout1.addRow(current_overtime_label_10,current_overtime_10)
    layout1.addRow(clear_btn3,clear_btn2)


    ###Form 2 Rendering
    window1.setLayout(layout1)
    window1.show()

calculate_btn=QPushButton("Calculate")
calculate_btn.clicked.connect(msgButtonClick)
#returnValue = calculate_btn.exec()

### clear form fxn
def clear_form(clicked):
    demand_input.setValue(0)
    stdev_input.setValue(0)
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

layout.addRow(stdev_label,stdev_input)

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