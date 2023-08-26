# Libraries to import
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGroupBox, QGridLayout, QPushButton, QComboBox
import sys
from LedIndicatorWidget import *
import libPIEZO

#-------------------------------------------------------------------------------------------------------

# Colors
"""
Colors :    Green  : #c5e0b4
            Blue   : #4472c4    ( 68, 114, 196)
             Light : #7fadff    (127, 173, 255)
            Orange : #c55a11    (197,  90,  17)
             Light : #ff8d3f    (255, 141,  63)
            Beige  : #fff2cc
            Grey1  : #f2f2f2
            Grey2  : #bfbfbf
"""

#-------------------------------------------------------------------------------------------------------

class Hardware_Connection_Widget(QWidget):
    """
    Widget used to set our hardware connection.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self):
        """
        Initialisation of our widget.
        """
        super().__init__()
        self.piezoConnected = False

        # Creating our piezo class
        self.piezo = libPIEZO.piezo()
        self.comList = self.piezo.listSerialHardware()
        
        # Creating a QBox to setup the widget
        group_box = QGroupBox("Hardware Connection")
        self.setWindowTitle("Hardware Connection")

        # Creating the main layout
        layout = QGridLayout()
        
        # Creating and adding our sub-widgets
        labelPiezo = QLabel("Piezo")
        labelPiezo.setStyleSheet("border-style: none")

        # Creating a LED Widget for our piezo Hardware
        self.led = LedIndicator(self)
        self.led.setDisabled(True)  # Make the led non clickable

        self.led.on_color_1 = QColor(255, 0, 0)
        self.led.on_color_2 = QColor(176, 0, 0)
        self.led.off_color_1 = QColor(0, 0, 0)
        self.led.off_color_2 = QColor(156, 0, 0)

        self.hardwareSelectionComboBox = QComboBox()
        self.hardwareSelectionComboBox.setStyleSheet("background: #fff2cc; border-style: solid; border-width: 1px; font: bold; color: black;")
        self.hardwareSelectionComboBox.addItems([str(com) for com in self.piezo.listSerialHardware()])

        self.connectionPushButton = QPushButton("Connection")
        self.connectionPushButton.clicked.connect(lambda : self.connection())

        layout.addWidget(labelPiezo, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.led, 1, 0, 1, 1) # row = 1, column = 0, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.hardwareSelectionComboBox, 0, 1, 1, 1) # row = 0, column = 1, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.connectionPushButton, 1, 1, 1, 1) # row = 1, column = 1, rowSpan = 1, columnSpan = 1
        
        group_box.setLayout(layout)

        main_layout = QGridLayout()
        main_layout.addWidget(group_box, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1 <=> QHBoxLayout or V

        self.setLayout(main_layout)

    def connection(self):
        """
        A method used to connect the piezo to the interface.
        """
        self.piezo.setSerialCom(self.hardwareSelectionComboBox.currentText()[:5])
        self.piezo.connect()
        if self.piezo.isConnected():
            self.piezoConnected = True
            self.connectionPushButton.setEnabled(False)
            self.led.setChecked(True)
            self.connectionPushButton.setStyleSheet("background-color: white; color: black;")
            vers = self.piezo.getHWVersion()
            print(f'Version = {vers}')

            position1, position2 = self.piezo.getPosition()
            print(f'Position_um = {position1} / Position_nm = {position2}')

    def setEnabled(self, enabled):
        """
        Method used to set the style sheet of the widget, if he is enable or disable.

        Args:
            enabled (bool): enable or disable.
        """
        super().setEnabled(enabled)
        if enabled:
            self.setStyleSheet("background-color: #c55a11; border-radius: 10px; border-width: 2px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
            if not self.piezoConnected:
                self.connectionPushButton.setStyleSheet("background: #ff8d3f; border-style: solid; border-width: 1px; font: bold; color: black")
        
        else:
            self.setStyleSheet("background-color: #bfbfbf; border-radius: 10px; border-width: 2px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
            self.connectionPushButton.setStyleSheet("background: white; border-style: solid; border-width: 1px; font: bold; color: black")   

#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Hardware_Connection_Widget()
    window.show()

    sys.exit(app.exec_())
