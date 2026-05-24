from PySide6.QtWidgets import (QWidget, QHBoxLayout, QLabel, QPushButton)
from PySide6.QtCore import QSize
from ui.engine import Engine
from scripts import utils, database

class ServiceWidget(QWidget):
    def __init__(
            self,
        service_id=None,
        service_name="",
        price="$0",
        description="",
        parent=None,
        refresh=None,
        item=None,
        list_widget=None
        ):
        super().__init__(parent)
        self.service_id = service_id
        self.service_name = service_name
        self.price = price
        self.description = description

        self.refresh = refresh
        self.item = item
        self.list_widget = list_widget

        self.size_hint = QSize(180, 30)
        self.window_size = (800, 600)
        self.screen_size = (1920, 1080)
        self.advanced_size = QSize(self.screen_size[0] - 125, 290)
        
        self.TEXT = (240, 240, 240, 255)
        self.TRANSPARENT = (0, 0, 0, 0)

        self.name = Engine.create_text(
            text=self.service_name,
            size=14,
            position=(5, 5),
            color=self.TEXT,
            background_color=self.TRANSPARENT,
            font="Arial",
            window=self
        )

        if self.name:
            self.name.show()

        self.price_label = Engine.create_input(
            text=str(self.price),
            placeholder="Precio",
            size=(60, 20),
            position=(135, 5),
            color=self.TEXT,
            background_color=self.TRANSPARENT,
            font="Arial",
            window=self
        )

        if self.price_label:
            self.price_label.returnPressed.connect(self.update_price)

        self.delete_button = Engine.create_button(
            text="-",
            size=(20, 20),
            position=(200, 5),
            color=self.TEXT,
            background_color=(45, 45, 45, 255),
            hover_color=(51, 51, 51, 255),
            click_color=(79, 79, 79, 255),
            font="Arial",
            font_size=10,
            padding=3,
            window=self
        )

        if self.delete_button:
            self.delete_button.clicked.connect(self.delete_service)
    
    # =====================================================
    # Utility functions
    # =====================================================
    def update_price(self):
        if self.price_label:
            price = self.price_label.text()
            self.price_label.setText(f"{price}" if price.startswith("$") else f"${price}")

            self.update_service()

    def update_service(self):
        if self.name and self.price_label:
            new_name = self.name.text()
            new_price = self.price_label.text()

            if self.service_id:
                database.update_service(self.service_id,{
                    "name": new_name,
                    "default_price": new_price
                })
                utils.log_info(f"Updated service ID {self.service_id} with name '{new_name}' and price {new_price}")
                if self.refresh:
                    self.refresh()
            else:
                utils.log_error("Service ID is None, cannot update service.")
        

    # =====================================================
    # UI Update functions
    # =====================================================
    def sizeHint(self):
        return self.size_hint
    
    def delete_service(self):
        if self.service_id:
            database.delete_service(self.service_id)
            utils.log_info(f"Deleted service with ID {self.service_id}")
            if self.refresh:
                self.refresh()
        else:
            utils.log_error("Service ID is None, cannot delete service.")