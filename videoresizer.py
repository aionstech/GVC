import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox,QSplashScreen,QMessageBox
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import QSize,Qt,QTimer
from moviepy.editor import VideoFileClip
import os
import time
import subprocess


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



class VideoResizer(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        if check_ffmpeg_installed():
            mes = QMessageBox(self)
            mes.setWindowTitle('FFMPEG Found')
            mes.setText("Try using the Tool.")
            mes.setStandardButtons(QMessageBox.Ok)
            timer = QTimer()
            timer.setSingleShot(True)  
            timer.timeout.connect(mes.accept)
            timer.start(1500)  

         # Show the message box
            mes.exec()
        else:
            QMessageBox.warning(self,'No FFMPEG Found', 'Try using the tool after installing FFMPEG via winget procedure.')
            print("Try using the tool after installing FFMPEG via winget procedure.")
            install_ffmpeg()
        layout = QVBoxLayout()

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

        self.convert_button = QPushButton(QIcon(r"D:\Projects\Converter\images\resize.png"),"Resize")
        self.convert_button.setIconSize(QSize(60,60))
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
        self.setWindowTitle("AIONS Video Resizer")
        self.setFixedSize(500, 750)
        self.setStyleSheet("color:white;""background-color:qlineargradient(x1:0, y1:0, x2:1, y2:0,stop:0 #357482, stop:1 #2a1418);")
        self.setWindowIcon(QIcon(r"D:\Projects\Converter\images\resize.png"))

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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    if check_ffmpeg_installed():
        print("Enjoy the Tool.")
        splash_pix = QPixmap('D:/Projects/Converter/images/ns-rm.png')
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        splash.show()
        time.sleep(2)
    else:
        install_ffmpeg()
        app.quit()
    converter = VideoResizer()
    converter.show()
    splash.finish(converter)
    sys.exit(app.exec_())
