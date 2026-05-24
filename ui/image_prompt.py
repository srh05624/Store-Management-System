from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel
from scripts import in_out_put, database
from ui.engine import Engine

class ImagePrompt(QDialog):
    def __init__(
            self,
            image_id,
            pixmap,
            parent=None,
            refresh=None
        ):
        super().__init__(parent)

        self.image_id = image_id
        self.pixmap = pixmap
        self.refresh = refresh

        self.setWindowTitle("Seleccionar imagen")
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("""
            QDialog {
                background-color: rgba(40, 40, 40, 200);
            }
        """)

        self.setModal(True)
        self.max_size = 900
        self.image_label = QLabel(self)

        self.image_label.setPixmap(self.pixmap.scaled(self.max_size, self.max_size, Qt.KeepAspectRatio))
        self.resize(self.image_label.pixmap().width() + 40, self.image_label.pixmap().height() + 100)
        self.image_label.move(20, 20)

        # ================================================================
        # Action Button definitions
        # ================================================================
        self.save_button = Engine.create_button(
            text="Salvar Imagen",
            size=(120, 40),
            position=(self.width() - 380, self.height() - 60),
            color=(240, 240, 240, 255),
            background_color=(60, 60, 60, 255),
            font="Arial",
            font_size=14,
            window=self
            )
        
        if self.save_button:
            self.save_button.clicked.connect(self.save_image)
        
        # ================================================================
        
        self.delete_button = Engine.create_button(
            text="Eliminar",
            size=(100, 40),
            position=(self.width() - 240, self.height() - 60),
            color=(240, 240, 240, 255),
            background_color=(60, 60, 60, 255),
            font="Arial",
            font_size=14,
            window=self
            )
        
        if self.delete_button:
            self.delete_button.clicked.connect(self.delete_image)

        # ================================================================

        self.cancel_button = Engine.create_button(
            text="Cancelar",
            size=(100, 40),
            position=(self.width() - 120, self.height() - 60),
            color=(240, 240, 240, 255),
            background_color=(60, 60, 60, 255),
            font="Arial",
            font_size=14,
            window=self
            )
    
        if self.cancel_button:
            self.cancel_button.clicked.connect(self.reject)

        # ================================================================

    def delete_image(self):
        if self.image_id:
            database.delete_image(self.image_id)
            if self.refresh:
                self.refresh()
            self.accept()

    def save_image(self):
        if self.image_id:
            in_out_put.export_image(self.image_id)
            self.accept()