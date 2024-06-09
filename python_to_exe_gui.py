import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QProgressBar, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QPainter, QColor, QMouseEvent
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPoint


class ConverterThread(QThread):
    conversion_progress = pyqtSignal(int)
    conversion_finished = pyqtSignal(str)

    def __init__(self, filename, icon_path, name, bind_file):
        super().__init__()
        self.filename = filename
        self.icon_path = icon_path
        self.name = name
        self.bind_file = bind_file

    def run(self):
        pyinstaller_cmd = ["pyinstaller", "--onefile", "--clean", self.filename]

        if self.icon_path:
            pyinstaller_cmd.extend(["--icon", self.icon_path])

        if self.name:
            pyinstaller_cmd.extend(["--name", self.name])

        if self.bind_file:
            pyinstaller_cmd.extend(["--add-data", f"{self.bind_file};."])

        process = subprocess.Popen(pyinstaller_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                self.conversion_progress.emit(1)  # Increase progress bar
        self.conversion_finished.emit("Conversion completed.")


class GuideWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Guide - Python to EXE Converter")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setGeometry(100, 100, 600, 400)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)  # Remove window frame
        self.setAttribute(Qt.WA_TranslucentBackground)  # Set window background to be translucent

        self.oldPos = self.pos()

        layout = QVBoxLayout()

        # Apply glassy style
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 150);
                color: black;
                border: 1px solid rgba(255, 255, 255, 200);
                border-radius: 10px;
            }
            QPushButton {
                background: rgba(0, 0, 0, 100);
                color: white;
                border: 1px solid rgba(255, 255, 255, 200);
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 150);
            }
            QLabel {
                background: transparent;
                padding: 5px;
            }
        """)

        # Title bar layout
        title_bar = QHBoxLayout()
        title_bar.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Guide - Python to EXE Converter")
        title.setStyleSheet("padding: 10px; font-size: 16px;")

        close_button = QPushButton("X")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: black;
                border: 1px solid black;
                border-radius: 2px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: rgba(255, 0, 0, 150);
                color: white;
            }
        """)
        close_button.clicked.connect(self.close)

        title_bar.addWidget(title)
        title_bar.addStretch()
        title_bar.addWidget(close_button)

        layout.addLayout(title_bar)

        instructions = QLabel("""
        <h2>How to Use Python to EXE Converter</h2>
        <ol>
            <li>Select the Python (.py) file you want to convert by clicking the 'Browse' button next to 'Select .py file'.</li>
            <li>(Optional) Select an icon (.ico) file for your executable by clicking the 'Browse' button next to 'Select .ico file'.</li>
            <li>Enter the desired name for your executable in the 'Program Name' field.</li>
            <li>(Optional) If you want to bind another file to your executable, select it by clicking the 'Browse' button next to 'Bind to another file'.</li>
            <li>Click the 'Convert to .exe' button to start the conversion process. You can track the progress using the progress bar.</li>
            <li>Once the conversion is complete, the .exe file will be available in the 'dist' directory.</li>
        </ol>
        """)
        instructions.setStyleSheet("font-size: 14px;")

        layout.addWidget(instructions)

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255, 180))
        painter.setPen(QColor(255, 255, 255, 200))
        rect = self.rect()
        rect.setWidth(rect.width() - 1)
        rect.setHeight(rect.height() - 1)
        painter.drawRoundedRect(rect, 10, 10)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
            event.accept()


class ExeConverterUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python to EXE Converter")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setGeometry(100, 100, 600, 400)  # Larger window

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)  # Remove window frame
        self.setAttribute(Qt.WA_TranslucentBackground)  # Set window background to be translucent

        self.oldPos = self.pos()

        layout = QVBoxLayout()

        # Apply glassy style
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 150);
                color: black;
                border: 1px solid rgba(255, 255, 255, 200);
                border-radius: 10px;
            }
            QPushButton {
                background: rgba(0, 0, 0, 100);
                color: white;
                border: 1px solid rgba(255, 255, 255, 200);
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 150);
            }
            QLineEdit, QLabel {
                background: rgba(255, 255, 255, 100);
                padding: 5px;
                border: 1px solid rgba(255, 255, 255, 200);
                border-radius: 5px;
            }
            QProgressBar {
                background: rgba(0, 0, 0, 50);
                color: black;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: rgba(0, 0, 255, 150);
                border-radius: 5px;
            }
        """)

        # Title bar layout
        title_bar = QHBoxLayout()
        title_bar.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Python to EXE Converter")
        title.setStyleSheet("padding: 10px; font-size: 16px;")

        close_button = QPushButton("X")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: black;
                border: 1px solid black;
                border-radius: 2px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: rgba(255, 0, 0, 150);
                color: white;
            }
        """)
        close_button.clicked.connect(self.close)

        title_bar.addWidget(title)
        title_bar.addStretch()
        title_bar.addWidget(close_button)

        layout.addLayout(title_bar)

        self.file_label = QLabel("Select .py file:")
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Select .py file")
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.get_file)

        self.icon_label = QLabel("Select .ico file (optional):")
        self.icon_path = QLineEdit()
        self.icon_path.setPlaceholderText("Select .ico file")
        self.icon_button = QPushButton("Browse")
        self.icon_button.clicked.connect(self.get_icon)

        self.name_label = QLabel("Enter the name of the program:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Program Name")

        self.bind_label = QLabel("Bind to another file (optional):")
        self.bind_path = QLineEdit()
        self.bind_path.setPlaceholderText("Select file to bind")
        self.bind_button = QPushButton("Browse")
        self.bind_button.clicked.connect(self.get_bind_file)

        self.convert_button = QPushButton("Convert to .exe")
        self.convert_button.clicked.connect(self.convert_to_exe)

        self.progress_label = QLabel("Conversion progress:")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        layout.addWidget(self.file_label)
        layout.addWidget(self.file_path)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.icon_path)
        layout.addWidget(self.icon_button)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.bind_label)
        layout.addWidget(self.bind_path)
        layout.addWidget(self.bind_button)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        self.converter_thread = ConverterThread("", "", "", "")
        self.converter_thread.conversion_progress.connect(self.update_progress)
        self.converter_thread.conversion_finished.connect(self.show_message)

    def get_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select .py file", "", "Python Files (*.py)")
        self.file_path.setText(file_path)

    def get_icon(self):
        icon_path, _ = QFileDialog.getOpenFileName(self, "Select .ico file", "", "Icon Files (*.ico)")
        self.icon_path.setText(icon_path)

    def get_bind_file(self):
        bind_file, _ = QFileDialog.getOpenFileName(self, "Select file to bind", "", "All Files (*)")
        self.bind_path.setText(bind_file)

    def convert_to_exe(self):
        filename = self.file_path.text().strip()

        if not filename.endswith('.py') or not os.path.exists(filename):
            self.show_error("Error", "Please select an existing Python (.py) file.")
            return

        output_dir = "dist"
        os.makedirs(output_dir, exist_ok=True)

        icon_path = self.icon_path.text().strip()
        name = self.name_input.text().strip()
        bind_file = self.bind_path.text().strip()

        self.progress_bar.setValue(0)  # Reset progress bar

        self.converter_thread = ConverterThread(filename, icon_path, name, bind_file)
        self.converter_thread.conversion_progress.connect(self.update_progress)
        self.converter_thread.conversion_finished.connect(self.show_message)
        self.converter_thread.conversion_finished.connect(lambda: self.progress_bar.setValue(100))  # Set progress to 100 when conversion finishes
        self.converter_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(self.progress_bar.value() + value)

    def show_message(self, message):
        self.show_info("Info", message)

    def show_info(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def show_error(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.exec_()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255, 180))
        painter.setPen(QColor(255, 255, 255, 200))
        rect = self.rect()
        rect.setWidth(rect.width() - 1)
        rect.setHeight(rect.height() - 1)
        painter.drawRoundedRect(rect, 10, 10)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
            event.accept()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    guide_window = GuideWindow()
    guide_window.show()

    window = ExeConverterUI()
    window.show()

    sys.exit(app.exec_())

