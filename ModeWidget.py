# Libraries to import
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QApplication, QLabel
from AnimatedToggleWidget import AnimatedToggle

#-------------------------------------------------------------------------------------------------------

class Mode_Widget(QWidget):
    """
    Widget used to set our utilization mode.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self, mode = "Manual"):
        """
        Initialisation of our widget.
        """
        super().__init__()

        # Adding an animated toogle widget
        self.toggle = AnimatedToggle(
                checked_color = "#c55a11",
                pulse_checked_color = "#50c55a11", 
                unchecked_color = "#4472c4",
                pulse_unchecked_color = "#504472c4")
        
        # Adding labels to help the comprehension
        labelAutomatic = QLabel("Automatic")
        labelAutomatic.setStyleSheet("font: bold; color: white; border-style: none;")

        labelManual = QLabel("Manual")
        labelManual.setStyleSheet("font: bold; color: white; border-style: none;")

        # Setting the initial value
        if mode == "Manual":
            self.toggle.setCheckState(2)
        elif mode == "Automatic":
            self.toggle.setCheckState(0)
        
        # Adding all to the mainLayout
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(labelAutomatic)
        mainLayout.addWidget(self.toggle)
        mainLayout.addWidget(labelManual)

        self.setLayout(mainLayout)

#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication([])
    w = Mode_Widget()
    w.show()
    app.exec_()