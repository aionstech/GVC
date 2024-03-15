# GVC
# General Video Converter
<img src="icon.jpg" width="200" height="200">
This Python script utilizes PyQt5, a set of Python bindings for the Qt application framework, to create a simple video converter application with a graphical user interface (GUI). The application allows users to select input video files, specify output settings such as file type, resolution, frame rate, and bitrate, and convert the videos accordingly.

Here's a breakdown of the key components and functionalities:

User Interface: The GUI is constructed using PyQt5 widgets such as QLineEdit, QPushButton, QLabel, QComboBox, and QVBoxLayout. These widgets are arranged vertically using a QVBoxLayout to create a clean and organized layout.

Styling: The application's styling is customized using Qt stylesheets. The main window's background color is set to '#357482', while the background color of the individual elements (input fields, buttons, labels) is set to transparent to achieve a seamless integration with the main window's background.

Input and Output Handling: Users can browse and select input video files using the "Browse" button associated with the input path field. Similarly, they can specify the output folder by browsing through the directory structure. The selected input files and output folder paths are then used for video conversion.

Video Conversion: Upon clicking the "Convert" button, the application reads the input video files, resizes them based on the specified resolution, and converts them to the selected output file format. The conversion process utilizes the moviepy library, specifically the VideoFileClip class, to handle video processing tasks such as resizing and encoding.

Error Handling: The application includes error handling mechanisms to handle exceptions that may occur during the conversion process. If a conversion fails, the application prints an error message indicating the cause of the failure.

Overall, this video converter application provides a user-friendly interface for converting videos with customizable output settings. It demonstrates the capabilities of PyQt5 for creating GUI applications and integrates seamlessly with external libraries like moviepy for multimedia processing tasks.

# Python 3.10.x: Ensure that Python 3.10.x is installed on the system.
# PyQt5: The application uses PyQt5 for the graphical user interface. You can install it via pip:
<code>pip install PyQt5 </code>
