from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize, QEvent
from PySide6.QtGui import QImage, QPixmap
from scripts import utils, database
from ui.engine import Engine
from ui.image_object import ImageObject

class ServiceHistoryWidget(QWidget):
    def __init__(
            self,
            history_id=None,
            store_id=None,
            service_id=None,
            completed_date=None,
            worker_name=None,
            status=None,
            amount_charged=None,
            notes=None,
            created_at=None,
            parent=None,
            refresh=None
        ):
        super().__init__(parent)

        self.history_id = history_id
        self.store_id = store_id
        self.service_id = service_id
        self.completed_date = completed_date
        self.worker_name = worker_name
        self.status = status
        self.amount_charged = amount_charged
        self.notes = notes
        self.created_at = created_at

        self.refresh = refresh

        self.size_hint = QSize(600, 125)
        self.TEXT = (240, 240, 240, 255)
        self.TRANSPARENT = (0, 0, 0, 0)
        self.BACKGROUND = (40, 40, 40, 255)

        self.default_service = database.get_service(self.service_id) if self.service_id else None

        # =====================================================
        self.background = Engine.create_rectangle(
            size=(621, 120),
            position=(0, 0),
            color=(55, 55, 55, 255),
            border_color=self.TRANSPARENT,
            border_radius=0,
            window=self
        )

        # =====================================================
        # Service Details
        # =====================================================
        self.service_text = Engine.create_text(
            text=f"Servicio: {self.default_service.get('name', 'N/A') if self.default_service else 'N/A'}",
            size=14,
            position=(10, 5),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )

        if self.service_text:
            self.service_text.setToolTip("El servicio realizado")

        # =====================================================

        self.completed_date_text = Engine.create_text(
            text=f"Fecha:",
            size=14,
            position=(10, 35),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )

        if self.completed_date_text:
            self.completed_date_text.setToolTip("Fecha que se completó el servicio")

        # =====================================================

        self.completed_date_textbox = Engine.create_input(
            text=self.completed_date if self.completed_date else "",
            placeholder="Fecha",
            size=(80, 20),
            position=(60, 33),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )

        if self.completed_date_textbox:
            self.completed_date_textbox.installEventFilter(self)

        # =====================================================

        self.worker_name_text = Engine.create_text(
            text="Trabajador:",
            size=14,
            position=(145, 35),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )

        if self.worker_name_text:
            self.worker_name_text.setToolTip("Trabajador asignado al servicio")

        # =====================================================

        self.worker_textbox = Engine.create_input(
            text=self.worker_name if self.worker_name else "",
            placeholder="Nombre del trabajador",
            size=(100, 20),
            position=(220, 33),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )

        if self.worker_textbox:
            self.worker_textbox.installEventFilter(self)

        # =====================================================

        self.amount_charged_textbox = Engine.create_input(
            text=self.amount_charged if self.amount_charged is not None else self.default_service.get("default_price", "") if self.default_service else "",
            placeholder="Cantidad cobrada",
            size=(50, 20),
            position=(220, 3),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )

        if self.amount_charged_textbox:
            self.amount_charged_textbox.installEventFilter(self)

        # =====================================================

        self.notes_textbox = Engine.create_text_area(
            text=self.notes if self.notes is not None else "",
            placeholder="Notas adicionales",
            size=(335, 55),
            position=(10, 60),
            color=self.TEXT,
            background_color=self.BACKGROUND,
            font="Arial",
            window=self
        )

        if self.notes_textbox:
            self.notes_textbox.installEventFilter(self)

        # =====================================================

        self.photos_text = Engine.create_text(
            text="Imagenes:",
            size=14,
            position=(280, 5),
            color=self.TEXT,
            background_color=self.TRANSPARENT,
            font="Arial",
            window=self
        )

        if self.photos_text:
            self.photos_text.setToolTip("Fotos del servicio realizado")

        # =====================================================

        self.image_list = Engine.create_image_list(
            images=[],
            size=(250, 80),
            image_size=(30, 30),
            spacing=5,
            position=(360, 5),
            background_color=self.BACKGROUND,
            window=self
        )

        if self.image_list:
            self.refresh_images()

        # =====================================================

        self.import_image_button = Engine.create_button(
            text="Añadir Imagen",
            size=(120, 25),
            position=(360, 90),
            color=(255, 255, 255, 255),
            background_color=(90, 90, 90, 255),
            font="Arial",
            font_size=12,
            padding=0,
            window=self
        )

        if self.import_image_button:
            self.import_image_button.clicked.connect(self.add_photo)

        # =====================================================

        self.delete_button = Engine.create_button(
            text="Eliminar Historial",
            size=(120, 25),
            position=(490, 90),
            color=(255, 255, 255, 255),
            background_color=(90, 90, 90, 255),
            font="Arial",
            font_size=12,
            padding=0,
            window=self
        )

        if self.delete_button:
            self.delete_button.clicked.connect(self.delete_history)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusOut:
            if obj == self.amount_charged_textbox:
                self.update_price()
            if obj == self.notes_textbox or obj == self.worker_textbox or obj == self.completed_date_textbox:
                    self.update_data()
        return super().eventFilter(obj, event)

    def update_price(self):
        if self.amount_charged_textbox:
            try:
                n = float(self.amount_charged_textbox.text().replace("$", "").strip())
                n = f"{n:.2f}"
                price = "$" + n
                self.amount_charged_textbox.setText(str(price))
                self.update_data()
            except ValueError:
                utils.log_error(f"Invalid price input: '{self.amount_charged_textbox.text()}' is not a valid number")
            except Exception as e:
                utils.log_error(f"Error updating price: {e}")


    def refresh_images(self):
        if self.image_list:
            self.image_list.clear()

            for image in database.get_images_by_history_id(self.history_id):
                if image:
                    item = Engine.create_list_item(self.image_list)
                    if item:
                        qimage = QImage.fromData(image.get("file"))
                        pixmap = QPixmap.fromImage(qimage)
                        row = ImageObject(image.get("id"), pixmap, image_size=(50,50), refresh=self.refresh_images)

                        item.setSizeHint(row.sizeHint())
                        self.image_list.addItem(item)
                        self.image_list.setItemWidget(item, row)

    def add_photo(self):
        new_photo_path = utils.request_image_file()

        if self.image_list and new_photo_path:
            database.add_image(self.history_id, new_photo_path)
            self.refresh_images()
            utils.log_debug(f"Added image for history ID {self.history_id}: {new_photo_path}")

    def delete_history(self):
        if self.history_id:
            database.delete_service_history(self.history_id)
            utils.log_debug(f"Deleted service history record with id: {self.history_id}")

            if self.refresh:
                self.refresh()

    # =====================================================
    # UI Update functions
    # =====================================================
    def sizeHint(self):
        return self.size_hint

    def update_data(self, ):
        database.update_service_history(
            self.history_id,
            {
                "date_completed": self.completed_date_textbox.text() if self.completed_date_textbox else self.completed_date,
                "worker_name": self.worker_textbox.text() if self.worker_textbox else self.worker_name,
                "status": self.status if self.status else "Completed",
                "amount_charged": self.amount_charged_textbox.text() if self.amount_charged_textbox else self.amount_charged,
                "notes": self.notes_textbox.toPlainText() if self.notes_textbox else self.notes,
            }
        )

        utils.log_debug(f"Updated service history record with id: {self.history_id}")

        if self.refresh:
            self.refresh()

