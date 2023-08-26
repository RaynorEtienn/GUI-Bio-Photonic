# Libraries to import
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QPushButton, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon

#-------------------------------------------------------------------------------------------------------

# Colors
"""
Colors :    Green  : #c5e0b4
            Blue   : #4472c4
            Orange : #c55a11
            Beige  : #fff2cc
            Grey1  : #f2f2f2
            Grey2  : #bfbfbf
"""

#-------------------------------------------------------------------------------------------------------

class Pattern_Choice_Window(QWidget):
    """
    Widget used to choice the pattern.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self, patternNumber):
        """
        Initialisation of our widget.

        Args:
            patternNumber (int): number of our the pattern choice.
        """
        super().__init__()
        self.path = None
        self.width = 500
        self.height = 500

        # Set title
        self.setWindowTitle("Pattern " + str(patternNumber) + " Choice")
        self.setWindowIcon(QIcon("IOGSLogo.jpg"))

        # Creating widgets, setting their style sheet and adding them to the layout
        layout = QGridLayout()

        patternlabel = QLabel("Pattern " + str(patternNumber))
        patternlabel.setStyleSheet("border-style: none;")

        self.patternChoicePushButton = QPushButton("Pattern Choice")
        self.patternChoicePushButton.clicked.connect(lambda : self.directory())

        self.patternSave = QPushButton("Save Pattern")
        self.patternSave.clicked.connect(lambda : self.hide())

        self.patternView = QLabel()
        self.patternView.setStyleSheet("background-color: #4472c4; border-width: 2px; padding: 20px;")

        layout.addWidget(patternlabel, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.patternChoicePushButton, 0, 1, 1, 3) # row = 0, column = 1, rowSpan = 1, columnSpan = 3
        layout.addWidget(self.patternSave, 2, 0, 1, 2) # row = 2, column = 0, rowSpan = 1, columnSpan = 2
        layout.addWidget(self.patternView, 3, 1, 3, 3) # row = 3, column = 1, rowSpan = 3, columnSpan = 3

        self.setLayout(layout)

    def getSmallText(self):
        """
        Method used to show the picture selected.

        Returns:
            str: the string that must be show on the pattern choice button.
        """
        if self.path != None:  
            # Split the string by '/'
            end = self.path.split('/')
            
            # Return the last part of the split
            return end[-1]
        return 'Empty'

    def directory(self):
        """
        Method used to select a file in .tiff.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_filter = "BMP files (*.bmp)"
        path, _ = QFileDialog.getOpenFileName(None, "Select File", "", file_filter, options=options)
        if path:
            self.path = path
            self.patternChoicePushButton.setText(self.getSmallText())
            print(f"Selected file : {self.path}")
            self.preview()
        else:
            print("No file selected.")

    def preview(self):
        """
        A method used to show the image selected.
        """
        # Load the Pattern from the file
        pixmap = QPixmap(self.path)

        # Check if the pattern loaded successfully
        if pixmap.isNull():
            print('Failed to load the pattern:', self.path)
            return

        # Resize the pattern to the desired width and height
        pixmap = pixmap.scaled(self.width, self.height)

        # Set the pattern pixmap to the label
        self.patternView.setPixmap(pixmap)

        # Resize the label to fit the pattern size
        self.patternView.resize(pixmap.width(), pixmap.height())

    def setEnabled(self, enabled):
        """
        Method used to set the style sheet of the widget, if he is enable or disable.

        Args:
            enabled (bool): enable or disable.
        """
        super().setEnabled(enabled)
        if enabled:
            self.setStyleSheet("background-color: #c55a11; border-radius: 10px; border-width: 1px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
            self.patternChoicePushButton.setStyleSheet("background: #ff8d3f; color: black;")
            self.patternSave.setStyleSheet("background: #ff8d3f; color: black;")
        
        else:
            self.setStyleSheet("background-color: #bfbfbf; border-radius: 10px; border-width: 1px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
            self.patternChoicePushButton.setStyleSheet("background: white; color: black;")
            self.patternSave.setStyleSheet("background: white; color: black;")

    def showEvent(self, event) -> None:
        """
        A method designed to be launch each time the widget is .show() .

        Args:
            event (event): I don't really know.
        """
        self.preview()

#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Pattern_Choice_Window(1)
    window.show()

    sys.exit(app.exec_())
