from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from ui.image_prompt import ImagePrompt

class ImageObject(QWidget):
    def __init__(
            self,
            image_id,
            pixmap,
            image_size=(30,30),
            parent=None,
            refresh=None,
            ):
        super().__init__(parent)
        self.image_id = image_id
        self.size_hint = QSize(image_size[0], image_size[1])
        self.pixmap = pixmap
        self.refresh = refresh
        self.image_label = QLabel(self)
        self.image_label.setPixmap(self.pixmap.scaled(self.size_hint, Qt.KeepAspectRatio))

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.image_label)

        self.setLayout(self.layout)
        
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            ImagePrompt(self.image_id, self.pixmap, parent=self, refresh=self.refresh).exec()
        
    def sizeHint(self):
        return self.size_hint