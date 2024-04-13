import sys
import os
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QTextEdit, QMessageBox, QProgressBar
from PyQt5.QtGui import QIcon

def check_ffmpeg_installed():
    try:
        # Run the winget command to check if ffmpeg is installed
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if 'ffmpeg version' in result.stdout:
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def install_ffmpeg():
    QMessageBox.warning(None, 'FFmpeg Not Found', 'FFmpeg is required for video conversion. Please install it using winget.')
    os.system("winget install ffmpeg")

    # Optionally, you can provide instructions on how to install ffmpeg using winget

class ConverterWorker(QThread):
    progressChanged = pyqtSignal(int)
    finished = pyqtSignal(list, list)

    def __init__(self, files):
        super().__init__()
        self.files = files

    def run(self):
        successful_conversions = []
        failed_conversions = []

        for file in self.files:
            output_file = f"{file.split('.')[0]}.mp4"
            command = ['ffmpeg', '-i', file, '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', output_file]
            try:
                result = subprocess.run(['ffprobe', '-i', file, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'], capture_output=True, text=True)
                total_duration = float(result.stdout)
                progress = 0
                self.progressChanged.emit(progress)
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while process.poll() is None:
                    line = process.stdout.readline().decode()
                    if 'time=' in line:
                        time_str = line.split('time=')[1].split()[0]
                        hours, minutes, seconds = time_str.split(':')
                        current_time_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
                        progress = int((current_time_seconds / total_duration) * 100)
                        self.progressChanged.emit(progress)
                process.communicate()
                successful_conversions.append(file)
                self.progressChanged.emit(100)
            except subprocess.CalledProcessError as e:
                failed_conversions.append(file)

        self.finished.emit(successful_conversions, failed_conversions)

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.files = []
        self.initUI()

    def initUI(self):
        if check_ffmpeg_installed():
            QMessageBox.warning(self,'FFMPEG Found', 'Try using the converter.')
        else:
            QMessageBox.warning(self,'No FFMPEG Found', 'Try using the converter after installing FFMPEG via winget procedure.')
            install_ffmpeg()
        self.setWindowTitle('AIONS - TS to MP4 Converter')
        self.setWindowIcon(QIcon('D:/Projects/Converter/images/icon.jpg'))
        self.setGeometry(100, 100, 500, 200)

        self.selectButton = QPushButton('Select TS files', self)
        self.selectButton.clicked.connect(self.selectFiles)
        self.convertButton = QPushButton('Convert to MP4', self)
        self.convertButton.clicked.connect(self.convertFiles)
        self.progressBar = QProgressBar(self)
        self.progressBar.setFixedWidth(200)

        layout = QVBoxLayout()
        layout.addWidget(self.selectButton)
        layout.addWidget(self.convertButton)
        layout.addWidget(self.progressBar)
        self.setLayout(layout)

        self.show()

    def selectFiles(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Select TS files", "", "TS Files (*.ts)", options=options)
        
        if files:
            self.files = files
            self.showSelectedFiles(files)
        else:
            QMessageBox.warning(self, 'No Files Selected', 'Please select TS files.')

    def convertFiles(self):
        if not self.files:
            QMessageBox.warning(self, 'No Files Selected', 'Please select TS files first.')
            return

        if not check_ffmpeg_installed():
            install_ffmpeg()
            return

        self.progressBar.setValue(0)
        self.worker = ConverterWorker(self.files)
        self.worker.progressChanged.connect(self.updateProgress)
        self.worker.finished.connect(self.handleConversionFinished)
        self.worker.start()

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def handleConversionFinished(self, successful_conversions, failed_conversions):
        if successful_conversions:
            QMessageBox.information(self, 'Conversion Complete',
                                    f"Conversion completed successfully for:\n\n{successful_conversions}")
        if failed_conversions:
            QMessageBox.warning(self, 'Conversion Failed',
                                 f"Conversion failed for:\n\n{failed_conversions}")

    def showSelectedFiles(self, files):
        self.selectedFilesWindow = QWidget()
        self.selectedFilesWindow.setWindowTitle('Selected TS Files')
        self.selectedFilesWindow.setGeometry(200, 200, 400, 300)

        self.filePathsTextEdit = QTextEdit()
        self.filePathsTextEdit.setReadOnly(True)
        self.filePathsTextEdit.setPlainText('\n'.join(files))

        layout = QVBoxLayout()
        layout.addWidget(self.filePathsTextEdit)
        self.selectedFilesWindow.setLayout(layout)

        self.selectedFilesWindow.show()

if __name__ == '__main__':
    app = QApplication([])
    converter = ConverterApp()
    sys.exit(app.exec_())