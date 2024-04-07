import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox,QTabWidget
from PyQt5.QtWidgets import QCheckBox,QTextEdit,QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

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



class VideoConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.input_path_label = QLabel("Input Video Paths:")
        self.input_path_label.setStyleSheet("color:white;")
        self.input_path_edit = QLineEdit()
        self.input_path_edit.setStyleSheet("color:white;")
        self.input_path_button = QPushButton("Browse")
        self.input_path_button.setStyleSheet("color:white;")
        self.input_path_button.clicked.connect(self.browseInputFiles)

        self.output_folder_label = QLabel("Output Folder:")
        self.output_folder_label.setStyleSheet("color:white;")
        self.output_folder_edit = QLineEdit()
        self.output_folder_edit.setStyleSheet("color:white;")
        self.output_folder_button = QPushButton("Browse")
        self.output_folder_button.setStyleSheet("color:white;")
        self.output_folder_button.clicked.connect(self.browseOutputFolder)

        self.file_type_label = QLabel("File Type:")
        self.file_type_label.setStyleSheet("color:white;")
        self.file_type_combo = QComboBox()
        self.file_type_combo.setStyleSheet("color:white;")
        self.file_type_combo.addItems(["mp4", "avi", "webm"])

        self.convert_button = QPushButton("Convert")
        self.convert_button.setStyleSheet("color:white;")
        self.convert_button.clicked.connect(self.resizeVideos)

        layout.addWidget(self.input_path_label)
        layout.addWidget(self.input_path_edit)
        layout.addWidget(self.input_path_button)

        layout.addWidget(self.output_folder_label)
        layout.addWidget(self.output_folder_edit)
        layout.addWidget(self.output_folder_button)

        layout.addWidget(self.file_type_label)
        layout.addWidget(self.file_type_combo)

        layout.addWidget(self.convert_button)

        self.setLayout(layout)
        self.setWindowTitle("Video Converter")

    def browseInputFiles(self):
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(self, 'Open files', '', 'Video files (*.mp4 *.avi *.mov *.ts)')
        if file_paths:
            self.input_path_edit.setText(';'.join(file_paths))

    def browseOutputFolder(self):
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, 'Open directory', '')
        if folder_path:
            self.output_folder_edit.setText(folder_path)

    def resizeVideos(self):
        input_paths = self.input_path_edit.text().split(';')
        output_folder = self.output_folder_edit.text()
        file_type = self.file_type_combo.currentText()

        for input_path in input_paths:
            try:
                video_clip = VideoFileClip(input_path)
                output_filename = os.path.basename(input_path).split('.')[0] + '.' + file_type
                output_path = os.path.join(output_folder, output_filename)
                #resized_clip = video_clip.resize(newsize=(640, 480))
                resized_clip = video_clip.resize(newsize=(video_clip.w,video_clip.h))
                resized_clip.write_videofile(output_path, codec='libx264')
                video_clip.close()
                resized_clip.close()
                print(f"Conversion of {input_path} successful!")
            except Exception as e:
                print(f"Conversion of {input_path} failed: {str(e)}")

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.downloader_tab = QWidget()
        self.downloader_layout = QVBoxLayout(self.downloader_tab)

        # YouTube Downloader
        self.youtube_label = QLabel("YouTube Video URL:")
        self.youtube_label.setStyleSheet("color:white;")
        self.youtube_url_edit = QLineEdit()
        self.youtube_url_edit.setStyleSheet("color:white;")
        self.download_button = QPushButton("Download")
        self.download_button.setStyleSheet("color:white;")
        self.download_button.clicked.connect(self.downloadYouTubeVideo)
        self.youtube_console_box = QTextEdit()
        self.youtube_console_box.setReadOnly(True)
        self.youtube_console_box.setStyleSheet("background-color: black; color: green;")

        self.Download_folder_button = QPushButton("Select Output Folder")
        self.Download_folder_button.setStyleSheet("color:white;")
        self.Download_folder_button.clicked.connect(self.browseDownloadFolder)

        self.resolution_label = QLabel("Resolution:")
        self.resolution_label.setStyleSheet("color:white;")
        self.resolution_combo = QComboBox()
        self.resolution_combo.setStyleSheet("color:white;")
        self.resolution_combo.addItems(["Highest", "720p", "480p", "360p"])  # Example resolution options

        self.custom_name_label = QLabel("Folder Name:")
        self.custom_name_label.setStyleSheet("color:white;")
        self.custom_name_edit = QLineEdit()
        self.custom_name_edit.setStyleSheet("color:white;")

        self.convert_mp3_checkbox = QCheckBox("Also Convert to MP3")

        self.downloader_layout.addWidget(self.youtube_label)
        self.downloader_layout.addWidget(self.youtube_url_edit)
        self.downloader_layout.addWidget(self.Download_folder_button)
        self.downloader_layout.addWidget(self.resolution_label)
        self.downloader_layout.addWidget(self.resolution_combo)
        self.downloader_layout.addWidget(self.custom_name_label)
        self.downloader_layout.addWidget(self.custom_name_edit)
        self.downloader_layout.addWidget(self.convert_mp3_checkbox)
        self.downloader_layout.addWidget(self.download_button)
        self.downloader_layout.addWidget(self.youtube_console_box)

        self.setLayout(self.downloader_layout)
    def downloadYouTubeVideo(self):
        url = self.youtube_url_edit.text()
        if not url:
            self.youtube_console_box.append("Please enter a valid YouTube URL.")
            return

        if not hasattr(self, 'output_folder'):
            self.youtube_console_box.append("Please select an output folder.")
            return

        resolution_text = self.resolution_combo.currentText()
        resolution_code = self.getResolutionCode(resolution_text)

        try:
            yt = YouTube(url)
            stream = yt.streams.get_by_resolution(resolution_code)
            if stream:
                output_name = self.custom_name_edit.text() or yt.title
                output_path = self.output_folder + "/" + output_name
                print("path = ",output_path)
                stream.download(output_path)
                output_path = output_path+"/"+yt.title+".mp4"
                self.youtube_console_box.append("Download successful!")

                if self.convert_mp3_checkbox.isChecked():
                    mp4_path = output_path + ".mp4"
                    if os.path.exists(mp4_path):
                        self.convertToMP3(mp4_path, output_path + ".mp3")
                        self.youtube_console_box.append("Conversion to MP3 successful!")
                    else:
                        self.youtube_console_box.append("MP4 file not found for conversion.")
            else:
                self.youtube_console_box.append("No stream available for the selected resolution.")
        except Exception as e:
            self.youtube_console_box.append(f"Download failed: {str(e)}")

    def getResolutionCode(self, resolution_text):
        if resolution_text == "Highest":
            return "highest"
        elif resolution_text == "720p":
            return "720p"
        elif resolution_text == "480p":
            return "480p"
        elif resolution_text == "360p":
            return "360p"
        else:
            return "highest"

    def browseDownloadFolder(self):
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, 'Select Output Folder', '')
        if folder_path:
            self.output_folder = folder_path

    def convertToMP3(self, input_path, output_path):
        try:
            if os.path.exists(input_path):
                video = VideoFileClip(input_path)
                video.audio.write_audiofile(output_path)
                self.youtube_console_box.append("Conversion to MP3 successful!")
            else:
                self.youtube_console_box.append("MP4 file not found for conversion.")
        except Exception as e:
            self.youtube_console_box.append(f"Conversion to MP3 failed: {str(e)}")



class VideoResizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Set application icon
        self.setWindowIcon(QIcon('D:/Projects/Converter/icon.ico'))  # Provide the path to your icon file

        # Set background color of elements
        element_background_color = "background-color: rgba(0, 0, 0, 0);"

        self.input_path_label = QLabel("Input Video Paths:")
        self.input_path_edit = QLineEdit()
        self.input_path_edit.setStyleSheet(element_background_color)
        self.input_path_button = QPushButton("Browse")
        self.input_path_button.clicked.connect(self.browseInputFiles)

        self.output_folder_label = QLabel("Output Folder:")
        self.output_folder_edit = QLineEdit()
        self.output_folder_edit.setStyleSheet(element_background_color)
        self.output_folder_button = QPushButton("Browse")
        self.output_folder_button.clicked.connect(self.browseOutputFolder)

        self.file_type_label = QLabel("File Type:")
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems(["mp4", "ogv", "avi", "webm"])
        self.file_type_combo.setStyleSheet(element_background_color)

        self.mp4_codec_label = QLabel("MP4 Video Codec:")
        self.mp4_video_codec_combo = QComboBox()
        self.mp4_video_codec_combo.addItems(["libx264", "mpeg4"])
        self.mp4_video_codec_combo.setStyleSheet(element_background_color)

        self.resolution_label = QLabel("Resolution:")
        self.width_edit = QLineEdit()
        self.width_edit.setStyleSheet(element_background_color)
        self.width_edit.setPlaceholderText("Width")
        self.height_edit = QLineEdit()
        self.height_edit.setStyleSheet(element_background_color)
        self.height_edit.setPlaceholderText("Height")

        self.fps_label = QLabel("FPS:")
        self.fps_edit = QLineEdit()
        self.fps_edit.setText("30")
        self.fps_edit.setStyleSheet(element_background_color)

        self.video_bitrate_label = QLabel("Video Bitrate:")
        self.video_bitrate_edit = QLineEdit()
        self.video_bitrate_edit.setStyleSheet(element_background_color)
        self.video_bitrate_edit.setText("2000k")

        self.total_bitrate_label = QLabel("Total Bitrate:")
        self.total_bitrate_edit = QLineEdit()
        self.total_bitrate_edit.setStyleSheet(element_background_color)
        self.total_bitrate_edit.setText("4000k")

        self.audio_bitrate_label = QLabel("Audio Bitrate:")
        self.audio_bitrate_edit = QLineEdit()
        self.audio_bitrate_edit.setStyleSheet(element_background_color)
        self.audio_bitrate_edit.setText("128k")

        self.audio_sample_rate_label = QLabel("Audio Sample Rate:")
        self.audio_sample_rate_edit = QLineEdit()
        self.audio_sample_rate_edit.setStyleSheet(element_background_color)
        self.audio_sample_rate_edit.setText("44100")

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.resizeVideos)
        self.convert_button.setStyleSheet(element_background_color)

        layout.addWidget(self.input_path_label)
        layout.addWidget(self.input_path_edit)
        layout.addWidget(self.input_path_button)

        layout.addWidget(self.output_folder_label)
        layout.addWidget(self.output_folder_edit)
        layout.addWidget(self.output_folder_button)

        layout.addWidget(self.file_type_label)
        layout.addWidget(self.file_type_combo)

        layout.addWidget(self.mp4_codec_label)
        layout.addWidget(self.mp4_video_codec_combo)

        layout.addWidget(self.resolution_label)
        layout.addWidget(self.width_edit)
        layout.addWidget(self.height_edit)

        layout.addWidget(self.fps_label)
        layout.addWidget(self.fps_edit)

        layout.addWidget(self.video_bitrate_label)
        layout.addWidget(self.video_bitrate_edit)

        layout.addWidget(self.total_bitrate_label)
        layout.addWidget(self.total_bitrate_edit)

        layout.addWidget(self.audio_bitrate_label)
        layout.addWidget(self.audio_bitrate_edit)

        layout.addWidget(self.audio_sample_rate_label)
        layout.addWidget(self.audio_sample_rate_edit)

        layout.addWidget(self.convert_button)

        self.setLayout(layout)
        self.setWindowTitle("General Video Convert")
        self.setFixedSize(500, 700)
        self.setStyleSheet("color:white;""background-color:qlineargradient(x1:0, y1:0, x2:1, y2:0,stop:0 #357482, stop:1 #2a1418);")

    def browseInputFiles(self):
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(self, 'Open files', '', 'Video files (*.mp4 *.avi *.mov *.ts)')
        if file_paths:
            self.input_path_edit.setText(';'.join(file_paths))

    def browseOutputFolder(self):
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, 'Open directory', '')
        if folder_path:
            self.output_folder_edit.setText(folder_path)

    def resizeVideos(self):
        input_paths = self.input_path_edit.text().split(';')
        output_folder = self.output_folder_edit.text()
        file_type = self.file_type_combo.currentText()
        width = int(self.width_edit.text())
        height = int(self.height_edit.text())
        fps = float(self.fps_edit.text())
        video_bitrate = self.video_bitrate_edit.text()
        total_bitrate = self.total_bitrate_edit.text()
        audio_bitrate = self.audio_bitrate_edit.text()
        audio_sample_rate = int(self.audio_sample_rate_edit.text())

        if file_type == "mp4":
            video_codec = self.mp4_video_codec_combo.currentText()
            audio_codec = "aac"
        elif file_type == "ogv":
            video_codec = "libvorbis"
            audio_codec = "aac"
        elif file_type == "avi":
            video_codec = "rawvideo"
            audio_codec = "aac"
        elif file_type == "webm":
            video_codec = "libvpx"
            audio_codec = "aac"

        for input_path in input_paths:
            try:
                video_clip = VideoFileClip(input_path)
                output_filename = os.path.basename(input_path).split('.')[0] + '.' + file_type
                output_path = os.path.join(output_folder, output_filename)
                resized_clip = video_clip.resize((width, height))
                resized_clip.write_videofile(output_path, codec=video_codec, fps=fps, bitrate=total_bitrate,
                                              audio_bitrate=audio_bitrate, audio_fps=audio_sample_rate,
                                              audio_codec=audio_codec)
                video_clip.close()
                resized_clip.close()
                print(f"Conversion of {input_path} successful!")
            except Exception as e:
                print(f"Conversion of {input_path} failed: {str(e)}")

class MainApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.video_converter_tab = VideoConverter()
        self.youtube_downloader_tab = YouTubeDownloader()
        self.video_resizer_tab = VideoResizer()

        self.tabs.addTab(self.video_converter_tab, "Video Converter")
        self.tabs.addTab(self.youtube_downloader_tab, "YouTube Downloader")
        self.tabs.addTab(self.video_resizer_tab, "Video Resizer")

        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.setWindowTitle("Video Toolbox")
        self.setWindowIcon(QIcon('D:/Projects/Converter/icon.ico'))
        #self.setFixedSize(500, 800)
        self.setStyleSheet("color:black; background-color:qlineargradient(x1:0, y1:0, x2:1, y2:0,stop:0 #357482, stop:1 #2a1418);")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec_())
