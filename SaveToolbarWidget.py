# Libraries to import
import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QPushButton, QLabel, QPushButton
import glob
from PIL import Image
import numpy as np

#-------------------------------------------------------------------------------------------------------

class Save_Widget(QWidget):
    """
    Widget used to save our current image.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self):
        """
        Initialisation of the Widget.
        """
        super().__init__()
        
        self.path = None

        # Setting the style sheet
        self.setStyleSheet("background-color: #bfbfbf; border-radius: 10px; border-width: 1px;"
                           "border-color: black; padding: 6px; font: bold 12px; color: black;"
                           "text-align: center; border-style: solid;")

        self.setWindowTitle("Parameters AutoMode Window")

        # Creating and adding widgets into our layout
        mainLayout = QGridLayout()

        directoryLabel = QLabel("Directory")
        directoryLabel.setStyleSheet("border-style: none;")

        self.directoryPushButton = QPushButton("Directory")

        self.savePushButton = QPushButton("Save Image")

        mainLayout.addWidget(self.directoryPushButton, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1
        mainLayout.addWidget(self.savePushButton, 0, 1, 1, 1) # row = 0, column = 1, rowSpan = 1, columnSpan = 1

        self.setLayout(mainLayout)

    def saveImage(self, array):
        """
        Method used to save an array in .tiff in a folder with an incrementing filename.

        Args:
            array (np.darray()): array of the image.
        """
        # Set the beginningFilename according to the path set by the directory method
        if self.path is None or self.path == '':
            beginningFilename = 'Snap_*.tiff'
        else:
            beginningFilename = self.path + '/Snap_*.tiff'

        # Get the number of existing image files in the folder
        image_files = glob.glob(beginningFilename)
        num_images = len(image_files)

        # Increment the image number by 1 relative to the total number of existing images
        next_image_number = num_images + 1

        # Format the image file name
        image_filename = f"Snap_{next_image_number:02d}.tiff"

        # Create a PIL Image object from the array
        image = Image.fromarray(np.uint8(array))

        # Set the endingFilename according to the path set by the directory method
        if self.path is None or self.path == '':
            endingFilename = image_filename
        else:
            endingFilename = self.path + '/' + image_filename

        # Save the image as a TIFF file
        image.save(endingFilename)

        print(f"Array saved as {endingFilename}\n")

    def setMode(self, mode):
        """
        Method used to set the color mode of utilisation.

        Args:
            mode (str): "Automatic" = Blue, "Manual" = Orange
        """
        if mode == "Manual":
            self.directoryPushButton.setStyleSheet("background: #ff8d3f;")
            self.savePushButton.setStyleSheet("background: #ff8d3f;")
        elif mode == "Automatic":
            self.directoryPushButton.setStyleSheet("background: #7fadff;")
            self.savePushButton.setStyleSheet("background: #7fadff;")

#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Save_Widget()
    window.show()

    sys.exit(app.exec_())
