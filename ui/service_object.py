from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QEvent, QSize
from scripts import utils, database
from ui.engine import Engine

class ServiceWidget(QWidget):
    def __init__(
            self,
        service_id=None,
        service_name="",
        price=0.00,
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
        
        self.language = utils.current_language

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
            text=f"${self.price:.2f}" if self.price else "",
            placeholder="Precio" if self.language == "es"
                else "Price",
            size=(60, 20),
            position=(135, 5),
            color=self.TEXT,
            background_color=self.TRANSPARENT,
            font="Arial",
            window=self
        )

        if self.price_label:
            self.price_label.installEventFilter(self)

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
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusOut:
            if obj == self.price_label:
                self.update_price()
        return super().eventFilter(obj, event)

    # =====================================================
    # Utility functions
    # =====================================================
    def update_price(self):
        if self.price_label:
            price = self.price_label.text().replace("$", "")

            try:
                n = float(self.price_label.text().replace("$", "").strip())
                n = f"{n:.2f}"
                price = "$" + n
                self.price_label.setText(str(price))
                self.update_service()
            except ValueError:
                utils.log_error(f"Invalid price input: '{self.price_label.text()}' is not a valid number")
            except Exception as e:
                utils.log_error(f"Error updating price: {e}")

    def update_service(self):
        if self.name and self.price_label:
            new_name = self.name.text()
            new_price = self.price_label.text().replace("$", "")

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