from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize, QEvent
from ui.engine import Engine
from scripts import utils, database

class ServiceRecordWidget(QWidget):
    def __init__(
            self,
            record_id=None,
            store_id=None,
            service_id=None,
            service_name="",
            price=None,
            frequency=None,
            start_date=None,
            end_date=None,
            notes=None,
            created_at=None,
            parent=None,
            refresh=None,
            history_refresh=None,
            item=None,
            list_widget=None
        ):
        super().__init__(parent)

        self.store_id = store_id
        self.record_id = record_id
        self.service_id = service_id
        self.service_name = service_name
        self.price = price
        self.frequency = frequency
        self.start_date = start_date
        self.end_date = end_date
        self.notes = notes
        self.created_at = created_at

        self.refresh = refresh
        self.history_refresh = history_refresh
        self.item = item
        self.list_widget = list_widget

        self.window_size = (800, 600)
        self.screen_size = (1920, 1080)
        self.size_hint = QSize(600, 105)
        
        self.TEXT = (240, 240, 240, 255)
        self.TRANSPARENT = (0, 0, 0, 0)
        self.BACKGROUND = (40, 40, 40, 255)

        # ================================================================
        self.background = Engine.create_rectangle(
            size=(621, 100),
            position=(0, 0),
            color=(55, 55, 55, 255),
            border_color=self.TRANSPARENT,
            border_radius=0,
            window=self
        )

        # ================================================================
        # Service information
        # ================================================================
        self.service_textbox = Engine.create_input(
            text=self.service_name,
            placeholder="Servicio",
            size=(200, 20),
            position=(10, 5),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )
        
        if self.service_textbox:
            self.service_textbox.returnPressed.connect(self.update_record)

        # ================================================================

        self.price_textbox = Engine.create_input(
            text=str(self.price) if self.price is not None else "",
            placeholder="Precio",
            size=(60, 20),
            position=(220, 5),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )

        if self.price_textbox:
            self.price_textbox.returnPressed.connect(self.update_price)

        # ================================================================

        self.frequency_textbox = Engine.create_input(
            text=str(self.frequency) if self.frequency is not None else "",
            placeholder="Frecuencia",
            size=(80, 20),
            position=(290, 5),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )

        if self.frequency_textbox:
            self.frequency_textbox.returnPressed.connect(self.update_record)

        # ================================================================

        self.start_date_textbox = Engine.create_input(
            text=str(self.start_date) if self.start_date is not None else "",
            placeholder="YYYYMMDD",
            size=(80, 20),
            position=(380, 5),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )

        if self.start_date_textbox:
            self.start_date_textbox.returnPressed.connect(self.update_record)

        # ================================================================
        self.date_connector = Engine.create_text(
            text="-",
            size=14,
            position=(462, 7),
            color=self.TEXT,
            background_color=self.TRANSPARENT,
            font="Arial",
            window=self
        )

        # ================================================================
        
        self.end_date_textbox = Engine.create_input(
            text=str(self.end_date) if self.end_date is not None else "",
            placeholder="YYYYMMDD",
            size=(80, 20),
            position=(470, 5),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )

        if self.end_date_textbox:
            self.end_date_textbox.returnPressed.connect(self.update_record)

        # ================================================================

        self.delete_button = Engine.create_button(
            text="-",
            size=(20, 20),
            position=(585, 5),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            hover_color=(51, 51, 51, 255),
            click_color=(79, 79, 79, 255),
            font="Arial",
            font_size=10,
            padding=3,
            window=self
        )

        if self.delete_button:
            self.delete_button.clicked.connect(self.delete_record)

        # ================================================================

        self.add_service_history_button = Engine.create_button(
            text="->",
            size=(20, 20),
            position=(560, 5),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            hover_color=(51, 51, 51, 255),
            click_color=(79, 79, 79, 255),
            font="Arial",
            font_size=10,
            padding=3,
            window=self
        )

        if self.add_service_history_button:
            self.add_service_history_button.clicked.connect(self.add_service_history)

        # ================================================================

        self.notes_textbox = Engine.create_text_area(
            text=str(self.notes) if self.notes is not None else "",
            placeholder="Notas",
            size=(595, 50),
            position=(10, 30),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )

        if self.notes_textbox:
            self.notes_textbox.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.notes_textbox and event.type() == QEvent.FocusOut:
            self.update_record()
        return super().eventFilter(obj, event)

    # =====================================================
    # Utility functions
    # =====================================================
    def delete_record(self):
        if self.store_id and self.record_id:
            database.delete_service_record(self.record_id)
            utils.log_info(f"Deleted service record ID {self.record_id} for store ID {self.store_id}")
            if self.refresh:
                self.refresh()
        else:
            utils.log_error("Cannot delete service record: missing store_id or record_id")

    def update_price(self):
        if self.price_textbox:
            try:
                n = float(self.price_textbox.text().replace("$", "").strip())
                n = f"{n:.2f}"
                price = "$" + n
                self.price_textbox.setText(str(price))
                self.update_record()
            except ValueError:
                utils.log_error(f"Invalid price input: '{self.price_textbox.text()}' is not a valid number")
            except Exception as e:
                utils.log_error(f"Error updating price: {e}")

    def update_record(self):
        if self.store_id and self.record_id:
            if self.service_textbox:
                service = database.get_services_by_name(self.service_textbox.text())
                if self.service_id and service and service[0]["id"] == int(self.service_id):
                    updated_data = {
                        "price": self.price_textbox.text() if self.price_textbox and self.price_textbox.text() else "",
                        "frequency": self.frequency_textbox.text() if self.frequency_textbox and self.frequency_textbox.text() else "",
                        "start_date": self.start_date_textbox.text() if self.start_date_textbox else "",
                        "end_date": self.end_date_textbox.text() if self.end_date_textbox else "",
                        "notes": self.notes_textbox.toPlainText() if self.notes_textbox else ""
                    }
                    database.update_service_record(self.record_id, updated_data)
                else:
                    new_service_id = database.add_service({
                        "name": self.service_textbox.text(),
                        "default_price": self.price_textbox.text() if self.price_textbox and self.price_textbox.text() else "$0",
                        "description": "",
                    })
                    if new_service_id:
                        updated_data = {
                            "store_id": self.store_id,
                            "service_id": new_service_id,
                            "price": self.price_textbox.text().replace("$", "") if self.price_textbox and self.price_textbox.text() else None,
                            "frequency": int(self.frequency_textbox.text()) if self.frequency_textbox and self.frequency_textbox.text() else None,
                            "start_date": self.start_date_textbox.text() if self.start_date_textbox else None,
                            "end_date": self.end_date_textbox.text() if self.end_date_textbox else None,
                            "notes": self.notes_textbox.toPlainText() if self.notes_textbox else None
                        }
                        database.update_service_record(self.record_id, updated_data)
                
                if self.refresh:
                    self.refresh()
        else:
            utils.log_error("Cannot update service record: missing store_id or record_id")

    def add_service_history(self):
        if self.store_id and self.history_refresh:
            database.add_service_history({
                "store_id": self.store_id,
                "service_id": self.service_id,
                "date_completed": str(utils.get_current_date()),
                "worker_name": None,
                "status": "Activo",
                "amount_charged": self.price_textbox.text() if self.price_textbox and self.price_textbox.text() else "",
                "notes": self.notes_textbox.toPlainText() if self.notes_textbox else ""
            })
            
            self.history_refresh()

    # =====================================================
    # UI Update functions
    # =====================================================
    def sizeHint(self):
        return self.size_hint

