import os
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QApplication, QMessageBox

CURRENT_DIR = os.curdir


# files in current working directory


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and dimensions
        self.setWindowTitle('Test_Data_splitter')
        self.setGeometry(100, 100, 400, 200)

        # Create a label and input field
        self.label = QLabel('DATASET:\t', self)
        self.label.move(50, 50)
        self.input_field = QLineEdit(self)
        self.input_field.move(150, 50)
        # Set the validator to accept only integers
        validator = QIntValidator(self)
        self.input_field.setValidator(validator)

        # Create a start button
        self.start_button = QPushButton('Split', self)
        self.start_button.move(150, 100)
        self.start_button.clicked.connect(self.start_clicked)

        # Create a text edit widget
        self.done_label = QLabel('Splitting done', self)
        self.done_label.setStyleSheet('color: green;')
        self.done_label.move(150, 150)
        self.done_label.setVisible(False)

    def start_clicked(self):
        if self.validate_input():
            # Get the input from the input field
            current_data_set = self.input_field.text()

            files_cwd = os.listdir(CURRENT_DIR)  # files im current working directory

            csv_files = list()

            for file in files_cwd:
                if file.endswith('.csv'):
                    csv_files.append(file)

            for file in csv_files:
                direction = file.split('_')[2].split('.')[0]
                target_folder = CURRENT_DIR + os.path.sep + direction
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                os.rename(file,
                          CURRENT_DIR + os.path.sep + target_folder + os.path.sep + str(current_data_set) + '_' + file)

            self.done_label.setVisible(True)
            # Hide the label after 3 seconds
            QTimer.singleShot(3000, self.hide_label)

    def validate_input(self):
        # Get the input value from the line edit
        input_value = self.input_field.text()

        # Check if the input value is valid
        try:
            int(input_value)
            return True
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Type in an integer!')
            return False

    def hide_label(self):
        self.done_label.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
