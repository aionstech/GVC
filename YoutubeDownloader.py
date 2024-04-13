import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox, QTextEdit, QCheckBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from pytube import YouTube
import subprocess
import os

class YouTubeDownloaderWorker(QThread):
    progressChanged = pyqtSignal(int)
    finishedDownloading = pyqtSignal(str)

    def __init__(self, url, resolution, output_folder, custom_name, convert_to_mp3):
        super().__init__()
        self.url = url
        self.resolution = resolution
        self.output_folder = output_folder
        self.custom_name = custom_name
        self.convert_to_mp3 = convert_to_mp3
        self.outputfile = ""

    def run(self):
        try:
            yt = YouTube(self.url)
            stream = yt.streams.get_by_resolution(self.resolution)
            if stream:
                output_name = self.custom_name
                self.finishedDownloading.emit(f"Downloading {yt.title} from YouTube as Video")
                output_path = self.output_folder+"/"+output_name
                vid = stream.download(output_path)
                mp4path = os.path.normpath(vid)
                #output_path = output_path+"/"+"video.mp4"
                #print("after file path change = "+output_path)
                self.outputfile = output_path
                self.finishedDownloading.emit(f"Downloaded: {mp4path} ")
            else:
                self.finishedDownloading.emit("No stream available for the selected resolution.")
            
            if self.convert_to_mp3:
                self.finishedDownloading.emit("Converting to MP3...")
                self.converttomp3(self.outputfile,output_path)

        except Exception as e:
            self.finishedDownloading.emit(str(e))

    def converttomp3(self,mp4path,outputfolder):
        try:
            mp3path = outputfolder+"/audio.mp3"
            subprocess.run(['ffmpeg','-i',mp4path,mp3path],check=True)
            self.finishedDownloading.emit(f"Finished Converting to: {mp3path}")
        except Exception as e:
            self.finishedDownloading.emit(f"Conversion to MP3 failed: {str(e)}")


        

class VideoConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.youtube_url_edit = QLineEdit()
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["Highest","1080p", "720p", "480p", "360p"])
        self.custom_name_edit = QLineEdit()
        self.convert_mp3_checkbox = QCheckBox("Also Convert to MP3")
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.downloadYouTubeVideo)
        self.youtube_console_box = QTextEdit()
        self.youtube_console_box.setReadOnly(True)

        layout.addWidget(QLabel("YouTube Video URL:"))
        layout.addWidget(self.youtube_url_edit)
        layout.addWidget(QLabel("Resolution:"))
        layout.addWidget(self.resolution_combo)
        layout.addWidget(QLabel("Folder Name on Desktop:"))
        layout.addWidget(self.custom_name_edit)
        layout.addWidget(self.convert_mp3_checkbox)
        layout.addWidget(self.download_button)
        layout.addWidget(self.youtube_console_box)

        self.setLayout(layout)
        self.setWindowTitle("YouTube Video and MP3 Downloader")
        self.setWindowIcon(QIcon('D:/Projects/Converter/images/YTDW.png'))

    def downloadYouTubeVideo(self):
        url = self.youtube_url_edit.text()
        if not url:
            self.youtube_console_box.append("Please enter a valid YouTube URL.")
            return

        resolution_text = self.resolution_combo.currentText()
        resolution_code = self.getResolutionCode(resolution_text)

        output_folder = QFileDialog.getExistingDirectory(self, 'Select Output Folder', '')
        if not output_folder:
            self.youtube_console_box.append("Please select an output folder.")
            return

        if self.worker and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()

        self.worker = YouTubeDownloaderWorker(url, resolution_code, output_folder, self.custom_name_edit.text(), self.convert_mp3_checkbox.isChecked())
        self.worker.finishedDownloading.connect(self.handleDownloadFinished)
        self.worker.progressChanged.connect(self.updateProgress)
        self.worker.start()

    def handleDownloadFinished(self, message):
        self.youtube_console_box.append(message)

    def updateProgress(self, value):
        # You can implement progress updating if needed
        pass

    def getResolutionCode(self, resolution_text):
        if resolution_text == "Highest":
            return "highest"
        elif resolution_text == "1080p":
            return "1080p"
        elif resolution_text == "720p":
            return "720p"
        elif resolution_text == "480p":
            return "480p"
        elif resolution_text == "360p":
            return "360p"
        else:
            return "highest"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = VideoConverter()
    downloader.show()
    sys.exit(app.exec_())
