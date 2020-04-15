import sys
from PyQt5.QtWidgets import QApplication,QFormLayout,QWidget,QPushButton,QLabel,QSpinBox,QHBoxLayout,QComboBox,QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
import math

### Form 1 Setup
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('DSD Sorting Layout Optimizer')
layout = QFormLayout()

### create combo boxes
stores=["423","435","450","665","694","6082","6093","6105","6161","6258","6279"]

combo1=QComboBox()
for store in stores:
    combo1.addItem(store) 

combo2=QComboBox()
for store in stores:
    combo2.addItem(store)

combo3=QComboBox()
for store in stores:
    combo3.addItem(store)

#### create demand spin boxes
store_1_demand_input=QSpinBox()
store_1_demand_input.setRange(0,1000000)

store_2_demand_input=QSpinBox()
store_2_demand_input.setRange(0,1000000)

store_3_demand_input=QSpinBox()
store_3_demand_input.setRange(0,1000000)

### create calculate function
def calculate_fxn(clicked):
    d1=store_1_demand_input.value()
    d2=store_2_demand_input.value()
    d3=store_3_demand_input.value()

    s1=combo1.currentText()
    s2=combo2.currentText()
    s3=combo3.currentText()

    dictionary={d1:s1, d2:s2, d3:s3}
    r=[d1,d2,d3]
    ranklist=sorted(r,reverse=1)
    
    print("calculating...")
    layout.addRow(QLabel("Ideal Sorting Layout\n\n"))

    aisle_widget1=QVBoxLayout()
    aisle_widget1.addWidget(QLabel("Dock 362:"))
    aisle_widget1.addWidget(QLabel("Store #"+ str(dictionary[ranklist[2]])))
    
    aisle_widget2=QVBoxLayout()
    aisle_widget2.addWidget(QLabel("Dock 363:"))
    aisle_widget2.addWidget(QLabel("Store #"+ str(dictionary[ranklist[1]])))

    aisle_widget3=QVBoxLayout()
    aisle_widget3.addWidget(QLabel("Docks 364 & 365:"))
    aisle_widget3.addWidget(QLabel("Store #"+ str(dictionary[ranklist[0]])))

    aisle_widgets=QHBoxLayout()
    aisle_widgets.addItem(aisle_widget1)
    aisle_widgets.addItem(aisle_widget2)
    aisle_widgets.addItem(aisle_widget3)

    layout.addRow(aisle_widgets)

### create clear function
def clear_fxn(clicked):
    combo1.setCurrentText(stores[0])
    combo2.setCurrentText(stores[0])
    combo3.setCurrentText(stores[0])
    store_1_demand_input.setValue(0)
    store_2_demand_input.setValue(0)
    store_3_demand_input.setValue(0)

clear_btn=QPushButton("Clear Form")
clear_btn.clicked.connect(clear_fxn)

### create button & connection
calculate_btn=QPushButton("Calculate")
calculate_btn.clicked.connect(calculate_fxn)

### create input Formatting
combo_widgets=QHBoxLayout()
combo_widgets.addWidget(QLabel("Store 1:"))
combo_widgets.addWidget(combo1)
combo_widgets.addWidget(QLabel("Store 2:"))
combo_widgets.addWidget(combo2)
combo_widgets.addWidget(QLabel("Store 3:"))
combo_widgets.addWidget(combo3)

spin_widgets=QHBoxLayout()
spin_widgets.addWidget(QLabel("Store 1 Demand:"))
spin_widgets.addWidget(store_1_demand_input)
spin_widgets.addWidget(QLabel("Store 2 Demand:"))
spin_widgets.addWidget(store_2_demand_input)
spin_widgets.addWidget(QLabel("Store 3 Demand:"))
spin_widgets.addWidget(store_3_demand_input)


### add rows
layout.addRow(combo_widgets)
layout.addRow(spin_widgets)
layout.addRow(clear_btn,calculate_btn)

###Form Rendering
window.setLayout(layout)
window.show()
sys.exit(app.exec_())