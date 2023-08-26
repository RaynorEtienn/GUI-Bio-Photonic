# Libraries to import
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGroupBox, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
import sys
from PatternChoiceWindowWidget import Pattern_Choice_Window
import libDMD
import numpy
import PIL.Image

#-------------------------------------------------------------------------------------------------------

class DMD_Settings_Widget(QWidget):
    """
    Widget used to set our DMD settings.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self):
        """
        Initialisation of our widget.
        """
        super().__init__()
        self.DMDHardware =  None
        self.patternsLoaded = [[],[],[]]

        self.setStyleSheet("background-color: #c55a11; border-radius: 10px; border-width: 1px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
        
        group_box = QGroupBox("DMD Settings")
        self.setWindowTitle("DMD Settings")

        #Creating pattern choice window to show them later
        self.patternChoiceWindowWidget1 = Pattern_Choice_Window(1)
        self.patternChoiceWindowWidget2 = Pattern_Choice_Window(2)
        self.patternChoiceWindowWidget3 = Pattern_Choice_Window(3)

        self.patternChoiceWindowWidget1.path = r"MiresDMD\mires\mire 256\Mire256_pix_decalee_0_quarts.bmp"
        self.patternChoiceWindowWidget2.path = r"MiresDMD\mires\mire 256\Mire256_pix_decalee_1_quarts.bmp"
        self.patternChoiceWindowWidget3.path = r"MiresDMD\mires\mire 256\Mire256_pix_decalee_2_quarts.bmp"

        # Creating and adding our widgets to the mainlayout
        layout = QGridLayout()
        
        self.resetPushButton = QPushButton("Reset")
        self.resetPushButton.clicked.connect(lambda : self.resetPatternsLoaded())

        self.viewTestPushButton = QPushButton("View Test")
        self.viewTestPushButton.clicked.connect(lambda : self.ApercuPushButton())

        self.testPushButton = QPushButton("TEST")
        self.testPushButton.clicked.connect(lambda : self.TestPushButton())

        self.patternChoiceLoad1 = Pattern_Choice_Load_Widget(1)
        self.patternChoiceLoad1.patternChoicePushButton.clicked.connect(lambda : self.patternChoiceWindowWidget1.show())
        self.patternChoiceLoad1.loadButton.clicked.connect(lambda : self.PatternLoad1())

        self.patternChoiceWindowWidget1.patternSave.clicked.connect(
            lambda : self.patternChoiceLoad1.patternChoicePushButton.setText(
                self.getSmallText(self.patternChoiceWindowWidget1.path)))

        self.patternChoiceLoad2 = Pattern_Choice_Load_Widget(2)
        self.patternChoiceLoad2.patternChoicePushButton.clicked.connect(lambda : self.patternChoiceWindowWidget2.show())
        self.patternChoiceLoad2.loadButton.clicked.connect(lambda : self.PatternLoad2())

        self.patternChoiceWindowWidget2.patternSave.clicked.connect(
            lambda : self.patternChoiceLoad2.patternChoicePushButton.setText(
                self.getSmallText(self.patternChoiceWindowWidget2.path)))

        self.patternChoiceLoad3 = Pattern_Choice_Load_Widget(3)
        self.patternChoiceLoad3.patternChoicePushButton.clicked.connect(lambda : self.patternChoiceWindowWidget3.show())
        self.patternChoiceLoad3.loadButton.clicked.connect(lambda : self.PatternLoad3())

        self.patternChoiceWindowWidget3.patternSave.clicked.connect(
            lambda : self.patternChoiceLoad3.patternChoicePushButton.setText(
                self.getSmallText(self.patternChoiceWindowWidget3.path)))

        layout.addWidget(self.resetPushButton, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.viewTestPushButton, 0, 2, 1, 1) # row = 0, column = 2, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.testPushButton, 0, 3, 1, 1) # row = 0, column = 3, rowSpan = 1, columnSpan = 1
        layout.addWidget(self.patternChoiceLoad1, 1, 0, 1, 4) # row = 1, column = 0, rowSpan = 1, columnSpan = 4
        layout.addWidget(self.patternChoiceLoad2, 2, 0, 1, 4) # row = 2, column = 0, rowSpan = 1, columnSpan = 4
        layout.addWidget(self.patternChoiceLoad3, 3, 0, 1, 4) # row = 3, column = 0, rowSpan = 1, columnSpan = 4

        group_box.setLayout(layout)

        main_layout = QGridLayout()
        main_layout.addWidget(group_box, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1 <=> QHBoxLayout or V
        
        self.setLayout(main_layout)

    def getSmallText(self, input_string):
        """
        Method used to show the picture selected.

        Returns:
            str: the string that must be show on the pattern choice button.
        """
        if input_string != None:  
            # Split the string by '/'
            end = input_string.split('/')
            
            # Return the last part of the split
            return end[-1]
        return 'Empty'

    def ApercuPushButton(self):
        """
        Method used when the Apercu push button is clicked.
        """
        self.patternTestWidget = Pattern_Test_Widget()
        self.patternTestWidget.show()

    def resetDMD(self):
        """
        Method used to reset the DMD.
        """
        if self.DMDHardware == None :
            self.DMDHardware=libDMD.dmd()

        self.DMDHardware.reset()

    def launchSequence(self, pattern):
        if self.DMDHardware == None :
            self.DMDHardware=libDMD.dmd()

        self.DMDHardware.stopsequence()

        self.DMDHardware.changemode(3)

        exposure=[1000000]
        dark_time=[0]
        trigger_in=[False]
        trigger_out=[1]

        self.DMDHardware.defsequence([pattern], exposure, trigger_in, dark_time, trigger_out, 0)

        self.DMDHardware.startsequence()
        print("\n")

    def TestPushButton(self):
        """
        Method used when the Test push button is clicked.
        """
        image = (numpy.asarray(PIL.Image.open(
            r"C:\Users\TP02\Desktop\InterfaceBioPhot\MiresDMD\mires\mire 256\Mire256_pix_decalee_0_quarts.bmp")))

        self.launchSequence(image)

    def PatternLoad1(self):
        """
        Method used when the Pattern Load 1 push button is clicked.
        """
        if self.patternChoiceWindowWidget1.path != None:
            self.patternsLoaded[0] = numpy.asarray(PIL.Image.open(self.patternChoiceWindowWidget1.path))

            self.launchSequence(self.patternsLoaded[0])

            print(f"{self.getSmallText(self.patternChoiceWindowWidget1.path)} : loaded.\n")

    def PatternLoad2(self):
        """
        Method used when the Pattern Load 2 push button is clicked.
        """
        if self.patternChoiceWindowWidget2.path != None:
            self.patternsLoaded[1] = numpy.asarray(PIL.Image.open(self.patternChoiceWindowWidget2.path))

            self.launchSequence(self.patternsLoaded[1])

            print(f"{self.getSmallText(self.patternChoiceWindowWidget2.path)} : loaded.\n")

    def PatternLoad3(self):
        """
        Method used when the Pattern Load 3 push button is clicked.
        """
        if self.patternChoiceWindowWidget3.path != None:
            self.patternsLoaded[2] = numpy.asarray(PIL.Image.open(self.patternChoiceWindowWidget3.path))

            self.launchSequence(self.patternsLoaded[2])

            print(f"{self.getSmallText(self.patternChoiceWindowWidget3.path)} : loaded.\n")

    def PatternLoad(self, patternPath):
        """
        Method used to load a pattern by is path.

        Args:
            patternPath (str): path of the pattern.
        """
        pattern = numpy.asarray(PIL.Image.open(patternPath))

        self.launchSequence(pattern)

        print(f"{self.getSmallText(patternPath)} : loaded.\n")

    def resetPatternsLoaded(self):
        """
        Method used to reset the pattern selections.
        """
        self.patternChoiceWindowWidget1.path = r"MiresDMD\mires\mire 256\Mire256_pix_decalee_0_quarts.bmp"
        self.patternChoiceWindowWidget2.path = r"MiresDMD\mires\mire 256\Mire256_pix_decalee_1_quarts.bmp"
        self.patternChoiceWindowWidget3.path = r"MiresDMD\mires\mire 256\Mire256_pix_decalee_2_quarts.bmp"
        self.patternsLoaded = [[],[],[]]

        self.patternChoiceLoad1.patternChoicePushButton.setText("Pattern Choice")
        self.patternChoiceLoad2.patternChoicePushButton.setText("Pattern Choice")
        self.patternChoiceLoad3.patternChoicePushButton.setText("Pattern Choice")

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
            self.resetPushButton.setStyleSheet("background: #ff8d3f; color: black; border-width: 1px;")
            self.viewTestPushButton.setStyleSheet("background: #ff8d3f; color: black; border-width: 1px;")
            self.testPushButton.setStyleSheet("background: #ff8d3f; color: black; border-width: 1px;")
            self.patternChoiceLoad1.setEnabled(True)
            self.patternChoiceLoad2.setEnabled(True)
            self.patternChoiceLoad3.setEnabled(True)
        
        else:
            self.setStyleSheet("background-color: #bfbfbf; border-radius: 10px; border-width: 2px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
            self.resetPushButton.setStyleSheet("background: white; color: black; border-width: 1px;")
            self.viewTestPushButton.setStyleSheet("background: white; color: black; border-width: 1px;")
            self.testPushButton.setStyleSheet("background: white; color: black; border-width: 1px;")
            self.patternChoiceLoad1.setEnabled(False)
            self.patternChoiceLoad2.setEnabled(False)
            self.patternChoiceLoad3.setEnabled(False)       

    def showPatternsLoaded(self):
        """
        A method to show the patterns loaded.
        """
        print(self.patternsLoaded)

    def listNotEmpty(self, lst):
        """
        A method that remove [] from a list of lists

        Args:
            lst (list): list of lists

        Returns:
            list: list without []
        """
        return [sublst for sublst in lst if sublst != []]

#-------------------------------------------------------------------------------------------------------

class Pattern_Choice_Load_Widget(QWidget):
    """
    Widget used to choose our Pattern.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self, patternNumber):
        """
        Initialisation of our widget.
        """
        super().__init__()
        self.setStyleSheet("")

        # Creating and adding our widgets to our layout
        layout = QGridLayout()

        patternNumberLabel = QLabel("Pattern " + str(patternNumber))
        patternNumberLabel.setStyleSheet("border-style: none; color: white;")

        self.patternChoicePushButton = QPushButton("Pattern Choice")
        
        self.loadButton = QPushButton("LOAD")
        
        layout.addWidget(patternNumberLabel, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1 
        layout.addWidget(self.patternChoicePushButton, 0, 1, 1, 2) # row = 0, column = 1, rowSpan = 1, columnSpan = 2
        layout.addWidget(self.loadButton, 0, 3, 1, 1) # row = 0, column = 3, rowSpan = 1, columnSpan = 1 

        self.setLayout(layout)
        
    def setEnabled(self, enabled):
        """
        Method used to set the style sheet of the widget, if he is enable or disable.

        Args:
            enabled (bool): enable or disable.
        """
        super().setEnabled(enabled)
        if enabled:
            self.patternChoicePushButton.setStyleSheet("background: #ff8d3f; color: black; border-width: 1px;")
            self.loadButton.setStyleSheet("background: #ff8d3f; color: black; border-width: 1px;")
        
        else:
            self.patternChoicePushButton.setStyleSheet("background: white; color: black; border-width: 1px;")
            self.loadButton.setStyleSheet("background: white; color: black; border-width: 1px;")

#-------------------------------------------------------------------------------------------------------

class Pattern_Test_Widget(QWidget):
    """
    Widget used to choose our Pattern.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self):
        """
        Initialisation of our widget.
        """
        super().__init__()

        self.setWindowTitle('Pattern Example')
        self.setWindowIcon(QIcon("IOGSLogo.jpg"))

        self.width = 500
        self.height = 500

        mainLayout = QGridLayout()

        # Create a label widget to display the Pattern
        label = QLabel()

        # Load the Pattern from the file
        pixmap = QPixmap(r'MiresDMD\mires\mire 256\Mire256_pix_decalee_0_quarts.bmp')

        # Check if the pattern loaded successfully
        if pixmap.isNull():
            print('Failed to load the pattern:', r'MiresDMD\mires\mire 256\Mire256_pix_decalee_0_quarts.bmp')
            return

        # Resize the pattern to the desired width and height
        pixmap = pixmap.scaled(self.width, self.height)

        # Set the pattern pixmap to the label
        label.setPixmap(pixmap)

        # Resize the label to fit the pattern size
        label.resize(pixmap.width(), pixmap.height())

        mainLayout.addWidget(label)
        self.setLayout(mainLayout)

#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DMD_Settings_Widget()
    window.show()

    sys.exit(app.exec_())