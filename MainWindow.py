# Libraries to import
import sys
import os
import glob
from PIL import Image
import numpy as np

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QFileDialog, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from CameraWidget import Camera_Widget
from SensorSettingsWidget import Sensor_Settings_Widget
from HardwareConnectionWidget import Hardware_Connection_Widget
from DMDSettingsWidget import DMD_Settings_Widget
from AutomaticModeWidget import Automatic_Mode_Widget
from PiezoControlWidget import Piezo_Control_Widget
from ModeWidget import Mode_Widget
from SaveToolbarWidget import Save_Widget

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

class Main_Widget(QWidget):
    """
    Main Widget of our Main Window.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self, mode = "Automatic"):
        """
        Initialisation of the main Widget.
        """
        super().__init__()

        # Set some initialisation variables
        self.setStyleSheet("background: #f2f2f2;")
        self.mode = mode
        self.path = None
        self.scanFolderPath = None

        # Create the several widgets for the MainWidget
        self.cameraWidget = Camera_Widget()
        self.sensorSettingsWidget = Sensor_Settings_Widget()
        self.hardwareConnectionWidget = Hardware_Connection_Widget()
        self.DMDSettingsWidget = DMD_Settings_Widget()
        self.automaticModeWidget = Automatic_Mode_Widget()
        self.piezoControlWidget = Piezo_Control_Widget()

        # Create the several widgets for the Toolbar
        self.modeWidget = Mode_Widget(mode = self.mode)
        self.saveWidget = Save_Widget()

        # Setting the save function and directory between the saveButton and the cameraWidget
        self.saveWidget.directoryPushButton.clicked.connect(lambda : self.directory())
        self.saveWidget.savePushButton.clicked.connect(
            lambda : self.saveWidget.saveImage(self.cameraWidget.cameraFrame))
    
        # Setting the save function and the folder function between the saveButton and the parameters window
        self.automaticModeWidget.parametersAutoModeWindow.directoryPushButton.clicked.connect(
            lambda : self.directory())
        self.automaticModeWidget.parametersAutoModeWindow.saveParametersPushButton.clicked.connect(
            lambda : self.saveParameters())

        # Setting the move function in manual mode
        self.piezoControlWidget.ZAxis.slider.valueChanged.connect(lambda : self.movePiezo())
        self.piezoControlWidget.FineZ.slider.valueChanged.connect(lambda : self.movePiezo())

        # Setting the automatic start button 
        self.automaticModeWidget.startButton.clicked.connect(
            lambda : self.launchScan())

        # Setting a reset DMD button
        self.resetDMDPushButton = QPushButton("Reset DMD")
        self.resetDMDPushButton.clicked.connect(lambda : self.DMDSettingsWidget.resetDMD())

        # Setting the utilisation mode of the application and launching the next updates
        self.setMode()
        self.modeWidget.toggle.stateChanged.connect(lambda : self.changeMode())

        # Create and add the widgets into the layout
        layoutMain = QGridLayout()
        self.setLayout(layoutMain)

        layoutMain.addWidget(self.cameraWidget, 0, 0, 4, 4) # row = 0, column = 0, rowSpan = 4, columnSpan = 4
        layoutMain.addWidget(self.sensorSettingsWidget, 4, 0, 3, 4) # row = 4, column = 0, rowSpan = 3, columnSpan = 4
        layoutMain.addWidget(self.hardwareConnectionWidget, 0, 5, 1, 4) # row = 0, column = 5, rowSpan = 1, columnSpan = 4
        layoutMain.addWidget(self.DMDSettingsWidget, 1, 5, 2, 4) # row = 1, column = 5, rowSpan = 2, columnSpan = 4
        layoutMain.addWidget(self.automaticModeWidget, 3, 5, 1, 4) # row = 3, column = 5, rowSpan = 1, columnSpan = 4
        layoutMain.addWidget(self.piezoControlWidget, 4, 5, 3, 4) # row = 4, column = 5, rowSpan = 3, columnSpan = 4

        self.cameraWidget.connectCamera()
        self.cameraWidget.launchVideo()

        self.initSettings()

    # General methods used by the interface
    def initSettings(self):
        """
        Method used to setup the settings.
        """
        # Initialisation of the exposure setting
        self.sensorSettingsWidget.exposureTime.floatListToSelect = self.cameraWidget.generateExpositionRangeList(1000)
        self.sensorSettingsWidget.exposureTime.slider.setRange(0, len(self.sensorSettingsWidget.exposureTime.floatListToSelect) - 1)

        self.sensorSettingsWidget.exposureTime.slider.valueChanged.connect(
            lambda : self.cameraWidget.camera.set_exposure(self.sensorSettingsWidget.exposureTime.value))

        self.sensorSettingsWidget.exposureTime.setValue(self.sensorSettingsWidget.exposureTime.floatListToSelect[-1])

        # Initialisation of the FPS setting
        minFPS, maxFPS = self.cameraWidget.getFPSRange()
        self.sensorSettingsWidget.FPS.slider.setMinimum(minFPS)
        self.sensorSettingsWidget.FPS.slider.setMaximum(maxFPS)

        self.sensorSettingsWidget.FPS.slider.valueChanged.connect(
            lambda : self.cameraWidget.camera.set_frame_rate(self.sensorSettingsWidget.FPS.getValue()))
        self.sensorSettingsWidget.FPS.slider.valueChanged.connect(
            lambda : print(f"FPS : {self.cameraWidget.camera.get_frame_rate()}"))
        
        self.sensorSettingsWidget.FPS.setValue(self.sensorSettingsWidget.FPS.getValue())

        # Initialisation of the BlackLevel setting
        self.sensorSettingsWidget.blackLevel.slider.setMinimum(0)
        self.sensorSettingsWidget.blackLevel.slider.setMaximum(256)
        self.sensorSettingsWidget.blackLevel.setValue(int(self.cameraWidget.camera.get_black_level())) # camera's blacklevel

        self.sensorSettingsWidget.blackLevel.slider.valueChanged.connect(
            lambda : self.cameraWidget.camera.set_black_level(self.sensorSettingsWidget.blackLevel.getValue()))

    def setMode(self):
        """
        Method used to set the utilization mode of the application.
        """
        if self.mode == "Manual":
            self.sensorSettingsWidget.setEnabled(True)
            self.hardwareConnectionWidget.setEnabled(True)
            self.DMDSettingsWidget.setEnabled(True)
            self.automaticModeWidget.setEnabled(False)
            self.piezoControlWidget.setEnabled(True)
            self.cameraWidget.setColor("blue")
            self.saveWidget.setMode(self.mode)
            self.automaticModeWidget.parametersAutoModeWindow.setEnabled(False)
            self.DMDSettingsWidget.patternChoiceWindowWidget1.setEnabled(True)
            self.DMDSettingsWidget.patternChoiceWindowWidget2.setEnabled(True)
            self.DMDSettingsWidget.patternChoiceWindowWidget3.setEnabled(True)
            self.resetDMDPushButton.setStyleSheet("background: #ff8d3f; color: black; border-width: 1px;")

        elif self.mode == "Automatic":
            self.sensorSettingsWidget.setEnabled(False)
            self.hardwareConnectionWidget.setEnabled(False)
            self.DMDSettingsWidget.setEnabled(False)
            self.automaticModeWidget.setEnabled(True)
            self.piezoControlWidget.setEnabled(False)
            self.cameraWidget.setColor("blue")
            self.saveWidget.setMode(self.mode)
            self.automaticModeWidget.parametersAutoModeWindow.setEnabled(True)
            self.DMDSettingsWidget.patternChoiceWindowWidget1.setEnabled(False)
            self.DMDSettingsWidget.patternChoiceWindowWidget2.setEnabled(False)
            self.DMDSettingsWidget.patternChoiceWindowWidget3.setEnabled(False)
            self.resetDMDPushButton.setStyleSheet("background: #7fadff; color: black; border-width: 1px;")

    def changeMode(self):
        """
        Method used to change the utilisation mode of the application.
        """
        if self.mode == "Automatic":
            self.mode = "Manual"
            self.setMode()

        elif self.mode == "Manual":
            self.mode = "Automatic"
            self.setMode()

    # Methods less used by the interface
    def movePiezo(self):
        """
        Method used to move the piezo in manual mode.
        """
        if self.hardwareConnectionWidget.piezoConnected : 
            self.hardwareConnectionWidget.piezo.movePosition(
                self.piezoControlWidget.ZAxis.getValue(),
                self.piezoControlWidget.FineZ.getValue()
            )
            
            ZAxis, FineZ = self.hardwareConnectionWidget.piezo.getPosition()
            print(f"Piezo at : {ZAxis} um, {FineZ} nm")

    def directory(self):
        """
        Method used to select a directory to save the parameters and the images into.
        """
        dialog = QFileDialog()
        self.path = dialog.getExistingDirectory(None, "Select Folder")
        self.saveWidget.path = self.path
        self.automaticModeWidget.parametersAutoModeWindow.path = self.path
        self.saveWidget.directoryPushButton.setText('Directory : ' + self.getSmallText())
        self.automaticModeWidget.parametersAutoModeWindow.directoryPushButton.setText('Directory : ' + self.getSmallText())

    def getSmallText(self):
        """
        Method used to show the directory where the pictures are saved.

        Returns:
            str: the string that must be on the directory push button.
        """
        if self.path == None or self.path == '': 
            return 'Here' 
        
        # Split the string by '/'
        end = self.path.split('/')
        # Return the last part of the split
        return end[-1]

    # Method used to launch the scan and its sub-methods
    def launchScan(self):
        """
        Method used to scan in automatic mode.
        """
        # Read the parameters and get the Z Displacement and the Z Step
        try :
            parameters = self.readParameters()
        except FileNotFoundError :
            return print("'parameters.txt' required : use 'Parameters' button in 'Automatic Mode'")
        except ValueError :
            return print("Some values in 'parameters.txt' are not correct.\nAcquisition impossible.")
            
        if not self.hardwareConnectionWidget.piezo.isConnected():
            self.hardwareConnectionWidget.connection()
            if not self.hardwareConnectionWidget.piezo.isConnected():
                return print("The Hardwara for the Piezo is not connected : you must connect it first.")

        z_displacement, z_step = parameters['Z Displacement'], parameters['Z Step']
        
        # Set the camera with the values of the parameter file
        Exposure, FPS, BlackLevel = parameters['Exposure time'], parameters['FPS'], parameters['BlackLevel']
        self.sensorSettingsWidget.exposureTime.setValue(Exposure)
        self.sensorSettingsWidget.FPS.setValue(FPS)
        self.sensorSettingsWidget.blackLevel.setValue(BlackLevel)

        # Take the list of the Zs
        zs_list = self.calculateZs(z_displacement, z_step)

        # Create a folder to save the scans
        self.createScanFolder()

        for index, z in enumerate(zs_list):
            z_axis, fine_z = z
            self.hardwareConnectionWidget.piezo.movePosition(
                z_axis, fine_z
            )

            ZAxis, FineZ = self.hardwareConnectionWidget.piezo.getPosition()
            print(f"Piezo at : {ZAxis} um, {FineZ} nm\n")

            # Save Image with pattern
            for pattern in parameters['Patterns']:
                pattern_number = pattern['Pattern Number']
                pattern_path = pattern['Pattern Path']
                self.DMDSettingsWidget.PatternLoad(pattern_path)
                self.cameraWidget.refreshGraph()
                self.saveImage(pattern_number)

            # Set up the prograssion bar
            progression = 100 * (index+1) // len(zs_list)
            self.automaticModeWidget.progressionBar.setValue(progression)
            self.printProgressBar(progression, 100, suffix = "\n\n")
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(lambda : self.setProgressBarTo0())
        self.timer.start()

    def saveParameters(self):
        """
        Method used to save the data into the right folder.
        """
        if self.path is None:
            filename = "parameters.txt"
        else:
            filename = self.path + "/parameters.txt"

        # Securities 
        if ( self.automaticModeWidget.parametersAutoModeWindow.zDisplacementLine.text() ) == "" or ( not self.automaticModeWidget.parametersAutoModeWindow.zDisplacementLine.text().isdigit() ):
            return print("You must enter a correct value as Z Displacement : an integer.")
        
        if ( self.automaticModeWidget.parametersAutoModeWindow.zStepLine.text() ) == "" or ( not self.automaticModeWidget.parametersAutoModeWindow.zStepLine.text().isdigit() ):
            return print("You must enter a correct value as Z Step Line : an integer.")

        with open(filename, "w") as file:
            file.write(f"Z Displacement = {self.automaticModeWidget.parametersAutoModeWindow.zDisplacementLine.text()}\n")
            file.write(f"Z Step = {self.automaticModeWidget.parametersAutoModeWindow.zStepLine.text()}\n")
            file.write("\n")
            file.write("Camera settings :\n")
            file.write(f"Exposure time = {self.sensorSettingsWidget.exposureTime.value}\n")
            file.write(f"FPS = {self.sensorSettingsWidget.FPS.getValue()}\n")
            file.write(f"BlackLevel = {self.sensorSettingsWidget.blackLevel.getValue()}\n")
            file.write("\n")
            file.write("Patterns loaded :\n")
            file.write(f"Pattern 1 = {self.DMDSettingsWidget.patternChoiceWindowWidget1.path}\n")
            file.write(f"Pattern 2 = {self.DMDSettingsWidget.patternChoiceWindowWidget2.path}\n")
            file.write(f"Pattern 3 = {self.DMDSettingsWidget.patternChoiceWindowWidget3.path}\n")

        self.automaticModeWidget.parametersAutoModeWindow.hide()

    def readParameters(self):
        """
        A method used to read the different parameters.

        Args:
            file_path (str): path to the parameters file.

        Returns:
            dict: dictionary of parameters.
        """
        parameters = {'Patterns': []}
        if self.path is None or self.path == "":
            file_path = "parameters.txt"
        else:
            file_path = self.path + "/parameters.txt"

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('Z Displacement'):
                    z_displacement = int(line.split('=')[1].strip())
                    parameters['Z Displacement'] = z_displacement
                elif line.startswith('Z Step'):
                    z_step = int(line.split('=')[1].strip())
                    parameters['Z Step'] = z_step
                elif line.startswith('Exposure time'):
                    exposure_time = float(line.split('=')[1].strip())
                    parameters['Exposure time'] = exposure_time
                elif line.startswith('FPS'):
                    fps = int(line.split('=')[1].strip())
                    parameters['FPS'] = fps
                elif line.startswith('BlackLevel'):
                    black_level = int(line.split('=')[1].strip())
                    parameters['BlackLevel'] = black_level
                elif line.startswith('Pattern '):
                    pattern_parts = line.split('=')
                    pattern_number = int(pattern_parts[0].split()[-1])
                    pattern_path = pattern_parts[1].strip()
                    parameters['Patterns'].append({'Pattern Number': pattern_number, 'Pattern Path': pattern_path})

        return parameters
       
    def calculateZs(self, z_displacement, z_step):
        """
        A method used to set up the different values that will set the piezo.

        Args:
            z_displacement (int): Z Displacement in um.
            z_step (int): Z Step in nm.

        Returns:
            list of tuples: list of the Z Displacement and Z Step in um and nm.
        """
        zs_axis = []
        fine_zs = []
        current_z = 0

        while current_z <= z_displacement:
            z_axis = int(current_z)
            fine_z = int((current_z - z_axis) * 1000)
            zs_axis.append(z_axis)
            fine_zs.append(fine_z)

            current_z += z_step*10**-3

            if current_z > z_displacement:
                z_axis = int(z_displacement)
                fine_z = int((z_displacement - z_axis) * 1000)
                zs_axis.append(z_axis)
                fine_zs.append(fine_z)
                break

        combined_zs = [[zs_axis[i], fine_zs[i]] for i in range(len(zs_axis) - 1)]
        return combined_zs

    def createScanFolder(self):
        """
        Method used to create a new folder to save our scans.
        """
        if self.path == None or self.path == "":
            self.path = os.getcwd()
            self.saveWidget.directoryPushButton.setText('Directory : ' + self.getSmallText())
            self.automaticModeWidget.parametersAutoModeWindow.directoryPushButton.setText('Directory : ' + self.getSmallText())

 
        base_foldername = self.path + "/Scan_"
        print(base_foldername)

        scan_number = 1

        while os.path.exists(f"{base_foldername}{scan_number}"):
            scan_number += 1

        self.scanFolderPath = f"{base_foldername}{scan_number}"
        os.makedirs(self.scanFolderPath)

    def saveImage(self, patternNumber):
        """
        Method used to save an array in .tiff in a folder with an incrementing filename.

        Args:
            patternNumber (int): Pattern number for the image.
        """
        # Set the beginningFilename according to the path set by the directory method
        beginningFilename = self.scanFolderPath + '\Snap_*_*.tiff'

        # Get the number of existing image files in the folder
        image_files = glob.glob(os.path.join(self.scanFolderPath, beginningFilename))
        num_images = len(image_files)

        # Increment the image number by 1 relative to the total number of existing images
        next_image_number = num_images + 1

        # Format the image file name
        image_filename = f"Snap_{next_image_number:02d}_{patternNumber}.tiff"

        # Create a PIL Image object from the array
        image = Image.fromarray(np.uint8(self.cameraWidget.cameraFrame))

        # Set the endingFilename according to the path set by the directory method
        if self.path is None or self.path == '':
            endingFilename = image_filename
        else:
            endingFilename = os.path.join(self.scanFolderPath, image_filename)

        # Save the image as a TIFF file
        image.save(endingFilename)

        print(f"Array saved as : {endingFilename}\n")

    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
        """
        Method used to print a progression bar in the consol.

        Args:
            iteration (int): represents the current iteration or progress.
            total (int): represents the total number of iterations or the maximum value of the progress.
            prefix (str, optional): is a string that appears before the progress bar.. Defaults to ''.
            suffix (str, optional): is a string that appears after the progress bar. Defaults to ''.
            decimals (int, optional): specifies the number of decimal places to display for the percentage.. Defaults to 1.
            length (int, optional): determines the length of the progress bar in characters.. Defaults to 50.
            fill (str, optional): is the character used to represent the progress.. Defaults to '█'.
        """
        percent = f'{(100 * (iteration / float(total))):.{decimals}f}'
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='')
        if iteration == total:
            print("\n\n-------------------- Scan done. --------------------\n\n\n")
    
    def setProgressBarTo0(self):
        """
        Method used to set the progress bar to 0.
        """
        self.automaticModeWidget.progressionBar.setValue(0)
        self.timer.stop

#-------------------------------------------------------------------------------------------------------

class Main_Window(QMainWindow):
    """
    Our main window.

    Args:
        QMainWindow (class): QMainWindow can contain several widgets.
    """
    def __init__(self, mode = "Automatic"):
        """
        Initialisation of the main Window.
        """
        super(Main_Window, self).__init__()

        # Variable
        self.mode = mode

        # Define Window title and logo
        self.setWindowTitle("TP : Microscope à illumination structurée")
        self.setWindowIcon(QIcon("IOGSLogo.jpg"))
        
        # Get the relative values of the screen to set up the whole thing
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()

        # Calculate the desired relative coordinates
        relative_x_window = screen_rect.width() * 0.0025  # Relative X-coordinate
        relative_y_window = screen_rect.height() * 0.05  # Relative Y-coordinate
        relative_width_window = screen_rect.width() * 0.650  # Relative width
        relative_height_window = screen_rect.height() * (0.9) # Relative height

        self.setGeometry(int(relative_x_window), int(relative_y_window), int(relative_width_window), int(relative_height_window))

        # Set the widget as the central widget of the window
        self.mainWidget = Main_Widget(mode = self.mode)
        self.setCentralWidget(self.mainWidget)

        # Same thing for the windows
        relative_x_pattern_window = screen_rect.width() * 0.6575  # Relative X-coordinate
        relative_y_pattern_window = screen_rect.height() * 0.05  # Relative Y-coordinate
        relative_width_pattern_window = screen_rect.width() * (1-0.650-0.0025*3)  # Relative width
        relative_height_pattern_window = screen_rect.height() * (0.625) # Relative height

        self.mainWidget.DMDSettingsWidget.patternChoiceWindowWidget1.setGeometry(
            int(relative_x_pattern_window),
            int(relative_y_pattern_window), 
            int(relative_width_pattern_window), 
            int(relative_height_pattern_window))
        
        self.mainWidget.DMDSettingsWidget.patternChoiceWindowWidget2.setGeometry(
            int(relative_x_pattern_window), 
            int(relative_y_pattern_window + screen_rect.height() * (0.025)), 
            int(relative_width_pattern_window),
              int(relative_height_pattern_window))
        
        self.mainWidget.DMDSettingsWidget.patternChoiceWindowWidget3.setGeometry(
            int(relative_x_pattern_window), 
            int(relative_y_pattern_window + screen_rect.height() * (0.05)), 
            int(relative_width_pattern_window), 
            int(relative_height_pattern_window))

        self.mainWidget.automaticModeWidget.parametersAutoModeWindow.setGeometry(
            int(relative_x_pattern_window), 
            int(relative_y_pattern_window + screen_rect.height() * (0.05) + relative_height_pattern_window + screen_rect.height() * (0.025) * 2),
            int(relative_width_pattern_window), 
            int(0.9-(relative_y_pattern_window + screen_rect.height() * (0.05) + relative_height_pattern_window + screen_rect.height() * (0.025))))

        # Creating the toolbar
        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setStyleSheet("background-color: #bfbfbf; border-radius: 10px; border-width: 1px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
        
        # Connecting the modeWidget to the Toolbar
        self.setMode()
        self.mainWidget.modeWidget.toggle.stateChanged.connect(lambda : self.setMode())

        # Adding Widgets to the Toolbar
        self.toolbar.addWidget(self.mainWidget.modeWidget)
        self.toolbar.addWidget(self.mainWidget.saveWidget)
        self.toolbar.addWidget(self.mainWidget.resetDMDPushButton)

    def setMode(self):
        """
        Method used to set the utilization mode of the application.
        """
        if self.mainWidget.mode == "Manual":
            self.toolbar.setStyleSheet("background-color: #c55a11; border-radius: 10px; border-width: 2px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")

        elif self.mainWidget.mode == "Automatic":
            self.toolbar.setStyleSheet("background-color: #4472c4; border-radius: 10px; border-width: 2px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: white;"
                           "text-align: center; border-style: solid;")
            
#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Main_Window()
    window.show()

    sys.exit(app.exec_())
    