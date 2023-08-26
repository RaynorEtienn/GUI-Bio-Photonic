# Libraries to import
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QGridLayout, QPushButton, QProgressBar
import sys
from ParametersAutoModeWindowWidget import Parameters_AutoMode_Window

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

class Automatic_Mode_Widget(QWidget):
    """
    Widget used to use our AutoMode.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self):
        """
        Initialisation of our widget.
        """
        super().__init__()
        
        # Creating our parameters' window to show it later
        self.parametersAutoModeWindow = Parameters_AutoMode_Window()

        group_box = QGroupBox("Automatic Mode")
        self.setWindowTitle("Automatic Mode")

        # Creating the main layout
        layout = QGridLayout()
        
        # Creating and adding our settings
        self.parametersButton = QPushButton("Parameters")
        self.parametersButton.clicked.connect(lambda : self.parametersAutoModeWindow.show())

        self.startButton = QPushButton("START")

        self.progressionBar = QProgressBar()
        self.progressionBar.setStyleSheet("QProgressBar {border: 2px solid black; border-radius: 10px; text-align: center; margin: 0.5px; background-color: 7fadff; color: black;}"
                                          "QProgressBar::Chunk {background-color: #7fadff;}")
        self.progressionBar.setValue(0)

        layout.addWidget(self.parametersButton, 0, 2, 1, 1) # row = 0, column = 2, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.startButton, 0, 3, 1, 1) # row = 0, column = 3, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.progressionBar, 1, 2, 1, 2) # row = 1, column = 2, rowSpan = 1, columnSpan = 2
        
        group_box.setLayout(layout)

        main_layout = QGridLayout()
        main_layout.addWidget(group_box, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1 <=> QHBoxLayout or V

        self.setLayout(main_layout)


    def setEnabled(self, enabled):
        """
        Method used to set the style sheet of the widget, if he is enable or disable.

        Args:
            enabled (bool): enable or disable.
        """
        super().setEnabled(enabled)
        if enabled:
            self.setStyleSheet("background-color: #4472c4; border-radius: 10px; border-width: 2px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
            self.parametersButton.setStyleSheet("background: #7fadff; border-style: solid; border-width: 1px; font: bold; color: black")
            self.startButton.setStyleSheet("background: #7fadff; border-style: solid; border-width: 1px; font: bold; color: black")
            
        else:
            self.setStyleSheet("background-color: #bfbfbf; border-radius: 10px; border-width: 2px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
            self.parametersButton.setStyleSheet("background: white; border-style: solid; border-width: 1px; font: bold; color: black")
            self.startButton.setStyleSheet("background: white; border-style: solid; border-width: 1px; font: bold; color: black")
            

#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Automatic_Mode_Widget()
    window.show()

    sys.exit(app.exec_())
