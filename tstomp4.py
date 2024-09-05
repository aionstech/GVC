import sys
import ffmpeg
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt

class TSConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('TS to MP4 Converter')
        
        # Layout
        layout = QVBoxLayout()
        
        # QLabel centered at the top
        self.label = QLabel('Convert TS Videos to MP4', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # Button for file selection
        self.button = QPushButton('Select TS Files', self)
        self.button.clicked.connect(self.select_files)
        layout.addWidget(self.button)
        
        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def select_files(self):
        options = QFileDialog.Option.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(self, 'Select TS Files', '', 'TS Files (*.ts)', options=options)
        if files:
            self.convert_files(files)

    def convert_files(self, files):
        for file in files:
            output_file = file.replace('.ts', '.mp4')
            try:
                ffmpeg.input(file).output(output_file).run(overwrite_output=True)
            except ffmpeg.Error as e:
                print(f"Error converting file: {e.stderr.decode('utf8')}")
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")

        self.show_completion_message()

    def show_completion_message(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText("All files have been successfully converted!")
        msg_box.setWindowTitle("Conversion Complete")
        msg_box.exec()

def main():
    app = QApplication(sys.argv)
    converter = TSConverter()
    converter.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
