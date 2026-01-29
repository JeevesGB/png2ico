import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QMessageBox, QVBoxLayout, QHBoxLayout, QListWidget,
    QCheckBox, QDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PIL import Image


# ===== THEME =====
BG = "#1e1e1e"
FG = "#ffffff"
ACCENT = "#2d89ef"
BTN = "#2d2d2d"
BTN_HOVER = "#404040"


# ===== Size selection dialog =====
class SizeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Icon Sizes")
        self.setFixedSize(250, 200)

        self.sizes = [16, 32, 48, 64, 128, 256]
        self.checks = {}

        layout = QVBoxLayout()

        for s in self.sizes:
            cb = QCheckBox(f"{s}x{s}")
            cb.setChecked(True)
            self.checks[s] = cb
            layout.addWidget(cb)

        btn = QPushButton("Convert")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

        self.setLayout(layout)

    def selected_sizes(self):
        return [(s, s) for s, cb in self.checks.items() if cb.isChecked()]


# ===== Main Window =====
class IconConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Img2Ico")
        self.setFixedSize(450, 450)
        self.setAcceptDrops(True)

        self.images = []
        self.init_ui()
        self.apply_style()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # ===== Toolbar =====
        toolbar = QHBoxLayout()

        open_btn = QPushButton("Open")
        open_btn.clicked.connect(self.open_files)

        convert_btn = QPushButton("Convert")
        convert_btn.clicked.connect(self.convert)

        toolbar.addWidget(open_btn)
        toolbar.addWidget(convert_btn)
        toolbar.addStretch()

        main_layout.addLayout(toolbar)

        # ===== Content =====
        content = QHBoxLayout()

        self.file_list = QListWidget()
        content.addWidget(self.file_list, 2)

        self.preview = QLabel("Drop Images Here")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.addWidget(self.preview, 5)

        main_layout.addLayout(content)

    def apply_style(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BG};
                color: {FG};
                font-family: Segoe UI;
            }}

            QPushButton {{
                background-color: {BTN};
                padding: 6px 12px;
                border: none;
            }}

            QPushButton:hover {{
                background-color: {BTN_HOVER};
            }}

            QListWidget {{
                background-color: #111;
            }}
        """)

    # ===== Drag & Drop =====
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                self.add_image(path)

    def add_image(self, path):
        if path not in self.images:
            self.images.append(path)
            self.file_list.addItem(os.path.basename(path))

            pix = QPixmap(path).scaled(
                300, 300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.preview.setPixmap(pix)

    # ===== Open Files =====
    def open_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        for f in files:
            self.add_image(f)

    # ===== Convert =====
    def convert(self):
        if not self.images:
            QMessageBox.warning(self, "Error", "No images loaded")
            return

        dlg = SizeDialog()
        if not dlg.exec():
            return

        sizes = dlg.selected_sizes()
        if not sizes:
            QMessageBox.warning(self, "Error", "No sizes selected")
            return

        out_root = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if not out_root:
            return

        for img_path in self.images:
            name = os.path.splitext(os.path.basename(img_path))[0]
            out_dir = os.path.join(out_root, name)
            os.makedirs(out_dir, exist_ok=True)

            img = Image.open(img_path)
            ico_path = os.path.join(out_dir, f"{name}.ico")
            img.save(ico_path, format="ICO", sizes=sizes)

        QMessageBox.information(self, "Done", "Icons created successfully!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IconConverter()
    window.show()
    sys.exit(app.exec())
