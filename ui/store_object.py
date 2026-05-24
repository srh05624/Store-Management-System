from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget
from scripts import utils, database
from ui.engine import Engine
from ui.service_object import ServiceWidget
from ui.service_record_object import ServiceRecordWidget
from ui.service_history_object import ServiceHistoryWidget

class StoreWidget(QWidget):
    def __init__(
            self,
        store_id=None,
        company_name="",
        store_number="",
        address="",
        city="",
        state="",
        zip="",
        coordinates="0,0",
        next_service_date="",
        status="",
        parent=None,
        refresh=None,
        item=None,
        list_widget=None
        ):
        super().__init__(parent)

        self.store_id = store_id
        self.company_name = company_name
        self.store_number = store_number
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.coordinates = str(coordinates).split(",")
        self.next_service_date = next_service_date
        self.status = status

        self.refresh = refresh
        self.item = item
        self.list_widget = list_widget

        self.size_hint = QSize(0, 30)
        self.screen_size = (1920, 1080)
        self.advanced_size = QSize(self.screen_size[0] - 125, 290)
        self.advanced_view = False

        self.language = utils.current_language

        self.TEXT = (240, 240, 240, 255)
        self.TRANSPARENT = (0, 0, 0, 0)

        # ================================================
        # Store information
        # ================================================
        self.company_text = Engine.create_text(
            text=company_name,
            size=14,
            position=(10, 0),
            color=self.TEXT,
            background_color=self.TRANSPARENT,
            font="Arial",
            window=self
        )
        if self.company_text:
            if store_id:
                self.company_text.setFixedSize(200, 30)
            self.company_text.show()

        if store_id:
            self.main_number_text = Engine.create_text(
                text=f"Tienda #: {store_number}" if self.language == "es"
                    else
                    f"Store #: {store_number}",
                size=14,
                position=(205, 0),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            if self.main_number_text:
                self.main_number_text.setFixedSize(190, 30)
                self.main_number_text.show()

            # ================================================================

            self.store_address = Engine.create_text(
                text=f"Dirección: {address}, {city}, {state} {zip}" if self.language == "es"
                    else
                    f"Address: {address}, {city}, {state} {zip}",
                size=14,
                position=(400, 0),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            if self.store_address:
                self.store_address.setFixedSize(445, 30)
                self.store_address.show()

            # ================================================================

            self.active_services = Engine.create_text(
                text=f"Servicios activos: {database.get_active_store_services(self.store_id) if self.store_id else 0}" if self.language == "es"
                    else
                    f"Active Services: {database.get_active_store_services(self.store_id) if self.store_id else 0}",
                size=14,
                position=(850, 0),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            if self.active_services:
                self.active_services.setFixedSize(395, 30)
                self.active_services.show()

            # ================================================================

            self.status_text = Engine.create_text(
                text=f"Estado: {'Activo' if self.status == 1 else 'Inactivo'}" if self.language == "es"
                    else
                    f"Status: {'Active' if self.status == 1 else 'Inactive'}",
                size=14,
                position=(1250, 0),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            if self.status_text:
                self.status_text.setFixedSize(200, 30)
                self.status_text.show()

            # ================================================================
            # Store actions
            # ================================================================
            self.delete_button = Engine.create_button(
                text="Borrar" if self.language == "es"
                    else
                    "Delete",
                size=(80, 20),
                position=(1550, 5),
                color=self.TEXT,
                background_color=(45, 45, 45, 255),
                hover_color=(51, 51, 51, 255),
                click_color=(79, 79, 79, 255),
                font="Arial",
                padding=3,
                window=self
            )
            if self.delete_button:
                self.delete_button.show()
                self.delete_button.clicked.connect(self.delete)

            # ================================================================

            self.toggle_active_button = Engine.create_button(
                text="Desactivar" if self.status == 1 else "Activar" if self.language == "es"
                    else
                    "Deactivate" if self.status == 1 else "Activate",
                size=(100, 20),
                position=(1640, 5),
                color=self.TEXT,
                background_color=(45, 45, 45, 255),
                hover_color=(51, 51, 51, 255),
                click_color=(79, 79, 79, 255),
                font="Arial",
                padding=3,
                window=self
            )

            if self.toggle_active_button:
                self.toggle_active_button.show()
                self.toggle_active_button.clicked.connect(self.toggle_active)

            # ================================================================
            # Advanced display
            # ================================================================
            self.advanced_background = Engine.create_rectangle(
                size=(self.screen_size[0] - 125, 248),
                position=(10, 30),
                color=(70, 70, 70, 255),
                window=self
            )

            # ================================================================

            self.company_name_text = Engine.create_text(
                text=f"Nombre:" if self.language == "es"
                    else
                    "Name:",
                size=14,
                position=(20, 35),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            # ================================================================

            self.company_name_textbox = Engine.create_input(
                text=company_name,
                placeholder="Nombre de la Compañía" if self.language == "es"
                    else
                    "Company Name",
                size=(200, 30),
                position=(20, 55),
                color=(0,0,0,255),
                background_color=(255, 255, 255, 255),
                font="Arial",
                window=self
            )

            if self.company_name_textbox:
                self.company_name_textbox.textEdited.connect(self.update_info)

            # ================================================================

            self.store_number_text = Engine.create_text(
                text=f"Número de Tienda:" if self.language == "es"
                    else
                    "Store Number:",
                size=14,
                position=(240, 35),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            # ================================================================

            self.store_number_textbox = Engine.create_input(
                text=str(store_number) if store_number is not None else "",
                placeholder="Número de Tienda" if self.language == "es"
                    else
                    "Store Number",
                size=(200, 30),
                position=(240, 55),
                color=(0,0,0,255),
                background_color=(255, 255, 255, 255),
                font="Arial",
                window=self
            )

            if self.store_number_textbox:
                self.store_number_textbox.textEdited.connect(self.update_info)

            # ================================================================
            
            self.address_text = Engine.create_text(
                text=f"Dirección:" if self.language == "es"
                    else
                    "Address:",
                size=14,
                position=(20, 100),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            # ================================================================

            self.address_textbox = Engine.create_input(
                text=str(address) if address is not None else "",
                placeholder="Dirección" if self.language == "es"
                    else
                    "Address",
                size=(420, 30),
                position=(20, 120),
                color=(0,0,0,255),
                background_color=(255, 255, 255, 255),
                font="Arial",
                window=self
            )

            if self.address_textbox:
                self.address_textbox.textEdited.connect(self.update_info)

            # ================================================================

            self.city_text = Engine.create_text(
                text=f"Ciudad:" if self.language == "es"
                    else
                    "City:",
                size=14,
                position=(20, 160),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            # ================================================================

            self.city_textbox = Engine.create_input(
                text=str(city) if city is not None else "",
                placeholder="Ciudad" if self.language == "es"
                    else
                    "City",
                size=(160, 30),
                position=(20, 180),
                color=(0, 0, 0, 255),
                background_color=(255, 255, 255, 255),
                font="Arial",
                window=self
            )

            if self.city_textbox:
                self.city_textbox.textEdited.connect(self.update_info)

            # ================================================================

            self.state_text = Engine.create_text(
                text=f"Estado:" if self.language == "es"
                    else
                    "State:",
                size=14,
                position=(200, 160),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            # ================================================================

            self.state_textbox = Engine.create_input(
                text=str(state) if state is not None else "",
                placeholder="Estado" if self.language == "es"
                    else
                    "State",
                size=(120, 30),
                position=(200, 180),
                color=(0, 0, 0, 255),
                background_color=(255, 255, 255, 255),
                font="Arial",
                window=self
            )

            if self.state_textbox:
                self.state_textbox.textEdited.connect(self.update_info)

            # ================================================================

            self.zip_text = Engine.create_text(
                text=f"Código Postal:" if self.language == "es"
                    else
                    "Zip Code:",
                size=14,
                position=(300, 160),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            # ================================================================

            self.zip_textbox = Engine.create_input(
                text=str(zip) if zip is not None else "",
                placeholder="Código Postal" if self.language == "es"
                    else
                    "Zip Code",
                size=(100, 30),
                position=(340, 180),
                color=(0, 0, 0, 255),
                background_color=(255, 255, 255, 255),
                font="Arial",
                window=self
            )

            if self.zip_textbox:
                self.zip_textbox.textEdited.connect(self.update_info)
            
            # ================================================================

            self.coordinates_text = Engine.create_text(
                text=f"Coordenadas:" if self.language == "es"
                    else
                    "Coordinates:",
                size=14,
                position=(20, 220),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            # ================================================================

            self.coordinates_textbox_x = Engine.create_input(
                text=str(self.coordinates[0]) if len(self.coordinates) > 0 else "",
                placeholder="Latitud" if self.language == "es"
                    else
                    "Latitude",
                size=(200, 30),
                position=(20, 240),
                color=(0, 0, 0, 255),
                background_color=(255, 255, 255, 255),
                font="Arial",
                window=self
            )

            if self.coordinates_textbox_x:
                self.coordinates_textbox_x.textEdited.connect(self.update_info)

            # ================================================================

            self.coordinates_textbox_y = Engine.create_input(
                text=str(self.coordinates[1]) if len(self.coordinates) > 1 else "",
                placeholder="Longitud" if self.language == "es"
                    else
                    "Longitude",
                size=(200, 30),
                position=(240, 240),
                color=(0, 0, 0, 255),
                background_color=(255, 255, 255, 255),
                font="Arial",
                window=self
            )

            if self.coordinates_textbox_y:
                self.coordinates_textbox_y.textEdited.connect(self.update_info)

            # ================================================================
            # Service information
            # ================================================================
            self.services_text = Engine.create_text(
                text=f"Servicios: Nombre - Precio - Frecuencia - Fecha de Inicio - Fecha de Fin - Notas" if self.language == "es"
                    else
                    "Services: Name - Price - Frequency - Start Date - End Date - Notes",
                size=14,
                position=(480, 35),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            self.services_list = Engine.create_list(
                items=[],
                size=(625, 215),
                position=(480, 55),
                color=(0, 0, 0, 255),
                background_color=(35, 35, 35, 255),
                hover_color=(72, 72, 72, 255),
                click_color=(88, 88, 88, 255),
                window=self
            )

            # ================================================================
            
            self.add_service_button = Engine.create_button(
                text="+",
                size=(19, 19),
                position=(1086, 34),
                color=self.TEXT,
                background_color=(51, 51, 51, 255),
                hover_color=(57, 57, 57, 255),
                click_color=(85, 85, 85, 255),
                font="Arial",
                font_size=20,
                padding=0,
                window=self
            )

            if self.add_service_button:
                self.add_service_button.clicked.connect(self.show_service_list)

            # ================================================================

            self.service_history_text = Engine.create_text(
                text=f"Historial de Servicios:" if self.language == "es"
                    else
                    "Service History:",
                size=14,
                position=(1145, 35),
                color=self.TEXT,
                background_color=self.TRANSPARENT,
                font="Arial",
                window=self
            )

            self.service_history_list = Engine.create_list(
                items=[],
                size=(625, 215),
                position=(1145, 55),
                color=(0, 0, 0, 0),
                background_color=(35, 35, 35, 255),
                hover_color=(72, 72, 72, 255),
                click_color=(88, 88, 88, 255),
                window=self
            )

            # ================================================================

            self.service_choice_list = Engine.create_list(
                items=[],
                size=(240, 100),
                position=(1094, 50),
                color=(0, 0, 0, 0),
                background_color=(30, 30, 30, 255),
                hover_color=(72, 72, 72, 255),
                click_color=(88, 88, 88, 255),
                window=self
            )

            if self.service_choice_list:
                self.service_choice_list.hide()
                self.service_choice_list.itemDoubleClicked.connect(self.add_service_record)
            
            # ================================================================

            self.service_choice_list_box = Engine.create_input(
                text="",
                placeholder="Nuevo Servicio..." if self.language == "es"
                    else
                    "New Service...",
                size=(240, 30),
                position=(1094, 146),
                color=self.TEXT,
                background_color=(30, 30, 30, 255),
                hover_color=(72, 72, 72, 255),
                focus_color=(88, 88, 88, 255),
                font="Arial",
                window=self
            )

            if self.service_choice_list_box:
                self.service_choice_list_box.hide()
                self.service_choice_list_box.returnPressed.connect(self.add_service)

           
    def add_service(self):
        database.add_service({
            "name": self.service_choice_list_box.text(),
            "default_price": "0.00",
            "description": "",
        })

        self.service_choice_list_box.setText("")
        self.show_service_list()

    def show_service_list(self):
        if self.service_choice_list and self.service_choice_list_box:
            self.service_choice_list.clear()

            if self.service_choice_list.isVisible():
                self.service_choice_list.hide()
                self.service_choice_list_box.hide()
            else:
                self.service_choice_list.show()
                self.service_choice_list_box.show()

            services = database.get_all_services()

            for service in services:
                item = Engine.create_list_item(self.service_choice_list)

                if item:
                    row = ServiceWidget(
                        service_id=service.get("id"),
                        service_name=service.get("name"),
                        price=service.get("default_price"),
                        description=service.get("description"),
                        refresh=self.show_service_list,
                        item=item,
                        list_widget=self.service_choice_list
                    )
                    item.setSizeHint(row.sizeHint())
                    self.service_choice_list.addItem(item)
                    self.service_choice_list.setItemWidget(item, row)

    def add_service_record(self, item):
        if self.service_choice_list:
            widget = self.service_choice_list.itemWidget(item)

            if widget and isinstance(widget, ServiceWidget):
                database.add_service_record({
                    "store_id": self.store_id,
                    "service_id": widget.service_id,
                    "price": widget.price,
                    "frequency": "",
                    "start_date": utils.get_current_date(),
                    "end_date": utils.get_current_date(),
                    "notes": "",
                })

                self.show_service_list()
                self.refresh_service_records()

    def refresh_service_records(self):
        if self.services_list:
            self.services_list.clear()

            services = database.get_all_service_records(self.store_id)
            utils.log_debug(f"Loaded {len(services)} services from database for store_id: {self.store_id}")

            if services != []:
                for service in services:
                    item = Engine.create_list_item(self.services_list)
                    if item:
                        row = ServiceRecordWidget(
                            record_id=service.get("id"),
                            store_id=service.get("store_id"),
                            service_id=service.get("service_id"),
                            service_name=database.get_service(service.get("service_id")).get("name") if database.get_service(service.get("service_id")) else "",
                            price=service.get("price"),
                            frequency=service.get("frequency"),
                            start_date=service.get("start_date"),
                            end_date=service.get("end_date"),
                            notes=service.get("notes"),
                            created_at=service.get("created_at"),
                            refresh=self.refresh_service_records,
                            history_refresh=self.refresh_service_history,
                            item=item,
                            list_widget=self.services_list
                        )

                        item.setSizeHint(row.sizeHint())
                        self.services_list.addItem(item)
                        self.services_list.setItemWidget(item, row)

    def refresh_service_history(self):
        if self.service_history_list:
            self.service_history_list.clear()

            history = database.get_all_service_history(self.store_id)
            utils.log_debug(f"Loaded {len(history)} service history records from database for store_id: {self.store_id}")

            if history != []:
                for record in history:
                    item = Engine.create_list_item(self.service_history_list)
                    if item:
                        row = ServiceHistoryWidget(
                            history_id=record.get("id"),
                            store_id=record.get("store_id"),
                            service_id=record.get("service_id"),
                            completed_date=record.get("date_completed"),
                            worker_name=record.get("worker_name"),
                            status=record.get("status"),
                            amount_charged=record.get("amount_charged"),
                            notes=record.get("notes"),
                            created_at=record.get("created_at"),
                            refresh=self.refresh_service_history
                        )
                        
                        item.setSizeHint(row.sizeHint())
                        self.service_history_list.addItem(item)
                        self.service_history_list.setItemWidget(item, row)

    def update_info(self):
        if self.company_text:
            self.company_name = self.company_name_textbox.text()

            self.company_text.setText(
                self.company_name
            )
            

        if self.main_number_text:
            self.store_number = self.store_number_textbox.text()

            self.main_number_text.setText(
                f"Tienda #: {self.store_number}" if self.language == "es"
                else 
                f"Store #: {self.store_number}"
            )
            
            
        if self.store_address:
            self.address = self.address_textbox.text()
            self.city = self.city_textbox.text()
            self.state = self.state_textbox.text()
            self.zip = self.zip_textbox.text()

            self.store_address.setText(
                f"Dirección: {self.address}, {self.city}, {self.state} {self.zip}" if self.language == "es"
                else
                f"Address: {self.address}, {self.city}, {self.state} {self.zip}"
            )
            

        if self.coordinates_textbox_x and self.coordinates_textbox_y:
            self.coordinates = f"{self.coordinates_textbox_x.text()},{self.coordinates_textbox_y.text()}"

        if self.status_text and self.toggle_active_button:
            self.status_text.setText(
                f"Estado: {'Activo' if self.status == 1 else 'Inactivo'}" if self.language == "es"
                else
                f"Status: {'Active' if self.status == 1 else 'Inactive'}"
                )
            
            self.toggle_active_button.setText(
                f"Desactivar" if self.status == 1 else f"Activar" if self.language == "es"
                else
                f"Deactivate" if self.status == 1 else f"Activate"
                )

        updates = {
            "company_name": self.company_name,
            "store_number": self.store_number,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "coordinates": self.coordinates,
            "active": self.status
        }

        database.update_store(self.store_id, updates)

    # =====================================================
    # UI Update functions
    # =====================================================
    def sizeHint(self):
        return self.size_hint

    def toggle_advanced_display(self):
        if self.item:
            if self.advanced_view == False:
                self.item.setSizeHint(self.advanced_size)
                if self.list_widget:
                    self.list_widget.doItemsLayout()
                self.refresh_service_records()
                self.refresh_service_history()
                self.advanced_view = True
            else:
                self.item.setSizeHint(self.sizeHint())
                if self.list_widget:
                    self.list_widget.doItemsLayout()
                self.advanced_view = False

    def delete(self):
        database.delete_store(self.store_id)
        self.setParent(None)
        self.deleteLater()
        if self.refresh:
            self.refresh()

    def toggle_active(self):
        database.update_store(self.store_id, {"active": 0 if self.status == 1 else 1})
        if self.refresh:
            self.refresh()
        if self.list_widget:
            self.list_widget.doItemsLayout()