from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPalette, QColor
from scripts import utils, database, in_out_put
from ui.engine import Engine
from ui.store_object import StoreWidget
from ui.export_prompt import ExportPrompt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user = utils.get_username()
        self.window_size = (800, 600)
        self.screen_size = (self.screen().size().width(), self.screen().size().height())

        # ================================================================
        # UI Appearance
        # ================================================================
        self.text_color = (189, 189, 189, 255)
        self.background_color = (34, 34, 34, 255)

        self.setWindowTitle("Lawn Service Manager")
        self.resize(self.window_size[0], self.window_size[1])

        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(*self.background_color))
        self.setPalette(palette)

        # List widget style
        self.search_background_color = (56, 56, 56, 255)
        self.item_background_color = (0, 0, 0, 0)
        self.item_text_color = (189, 189, 189, 255)

        self.store_total = 0
        self.service_types_offered = 0
        self.active_services = 0
        self.services_completed = 0
        self.services_completed_month = 0
        self.services_completed_year = 0
        
        # ================================================================
        # Welcome message
        # ================================================================
        self.welcome_label = Engine.create_text(
            text=f"Bienvenido al administrador de Lawn Service Manager, {self.user}!",
            size=24,
            position=(50, 50),
            color=self.text_color,
            background_color=self.background_color,
            window=self
        )

        if self.welcome_label:
            self.welcome_label.show()

        # ================================================================
        # Store totals
        # ================================================================
        self.store_total_label = Engine.create_text(
            text=f"Total de tiendas: {self.store_total}",
            size=18,
            position=(50, 100),
            color=self.text_color,
            background_color=self.background_color,
            font="Arial",
            window=self
        )

        if self.store_total_label:
            self.store_total_label.show()
        
        # ================================================================

        self.service_types_offered_label = Engine.create_text(
            text=f"Tipos de servicios ofrecidos: {self.service_types_offered}",
            size=18,
            position=(50, 130),
            color=self.text_color,
            background_color=self.background_color,
            font="Arial",
            window=self
        )
        if self.service_types_offered_label:
            self.service_types_offered_label.show()
        
        # ================================================================

        self.service_total_label = Engine.create_text(
            text=f"Servicios activos programados: {self.active_services}",
            size=18,
            position=(50, 160),
            color=self.text_color,
            background_color=self.background_color,
            font="Arial",
            window=self
        )

        if self.service_total_label:
            self.service_total_label.show()

        # ================================================================
        # Service completion stats
        # ================================================================
        self.services_completed_label = Engine.create_text(
            text=f"Servicios completados: {self.services_completed}",
            size=18,
            position=(350, 100),
            color=self.text_color,
            background_color=self.background_color,
            font="Arial",
            window=self
        )

        if self.services_completed_label:
            self.services_completed_label.show()

        # ================================================================
        
        self.services_completed_month_label = Engine.create_text(
            text=f"Servicios completados este mes: {self.services_completed_month}",
            size=18,
            position=(350, 130),
            color=self.text_color,
            background_color=self.background_color,
            font="Arial",
            window=self
        )

        if self.services_completed_month_label:
            self.services_completed_month_label.show()

        # ================================================================

        self.services_completed_year_label = Engine.create_text(
            text=f"Servicios completados este año: {self.services_completed_year}",
            size=18,
            position=(350, 160),
            color=self.text_color,
            background_color=self.background_color,
            font="Arial",
            window=self
        )
    
        if self.services_completed_year_label:
            self.services_completed_year_label.show()

        # ================================================================
        # Store search
        # ================================================================
        self.search_bar = Engine.create_input(
            placeholder="Buscar tiendas...",
            size=(self.window_size[0] - 100, 30),
            position=(50, 200),
            color=self.text_color,
            background_color=self.search_background_color,
            hover_color=(72, 72, 72, 255),
            focus_color=(88, 88, 88, 255),
            window=self
        )
        if self.search_bar:
            self.search_bar.show()
            self.search_bar.textEdited.connect(self.refresh_stores)
        
        # ================================================================

        self.search_results = Engine.create_list(
            items=[],
            size=(self.window_size[0] - 100, self.window_size[1] - 300),
            position=(50, 275),
            color=self.text_color,
            background_color=self.search_background_color,
            hover_color=(72, 72, 72, 255),
            click_color=(88, 88, 88, 255),
            window=self
        )
        if self.search_results:
            self.search_results.show()
            self.refresh_stores()
            self.search_results.itemDoubleClicked.connect(self.item_clicked)

        # ================================================================
        self.categories = Engine.create_text(
            text="Compañía | Tienda # | Dirección | Próximo Servicio | Estado:",
            size=18,
            position=(50, 250),
            color=self.text_color,
            background_color=self.background_color,
            font="Arial",
            window=self
            )

        if self.categories:
            self.categories.show()
        
        # ================================================================
        # Add store button
        # ================================================================
        self.add_store_button = Engine.create_button(
            text="+",
            size=(25, 25),
            position=(self.window_size[0] - 50, 245),
            color=self.text_color,
            background_color=(51, 51, 51, 255),
            hover_color=(57, 57, 57, 255),
            click_color=(85, 85, 85, 255),
            font="Arial",
            font_size=32,
            padding=1,
            window=self
        )

        if self.add_store_button:
            self.add_store_button.show()
            self.add_store_button.clicked.connect(self.add_store)

        # ================================================================
        # Export data button
        # ================================================================
        self.export_button = Engine.create_button(
            text="Exportar",
            size=(80, 25),
            position=(self.window_size[0] - 160, 245),
            color=self.text_color,
            background_color=(51, 51, 51, 255),
            hover_color=(57, 57, 57, 255),
            click_color=(85, 85, 85, 255),
            font="Arial",
            font_size=12,
            padding=1,
            window=self
        )

        if self.export_button:
            self.export_button.show()
            self.export_button.clicked.connect(self.export_list)

        # ================================================================
        # Refresh stores button
        # ================================================================
        self.refresh_button = Engine.create_button(
            text="Refrescar",
            size=(80, 25),
            position=(self.window_size[0] - 250, 245),
            color=self.text_color,
            background_color=(51, 51, 51, 255),
            hover_color=(57, 57, 57, 255),
            click_color=(85, 85, 85, 255),
            font="Arial",
            font_size=12,
            padding=1,
            window=self
        )

        if self.refresh_button:
            self.refresh_button.show()
            self.refresh_button.clicked.connect(self.refresh_stores)

        # ================================================================
        # Backup data button
        # ================================================================
        self.backup_button = Engine.create_button(
            text="Respaldar",
            size=(80, 25),
            position=(self.window_size[0] - 340, 245),
            color=self.text_color,
            background_color=(51, 51, 51, 255),
            hover_color=(57, 57, 57, 255),
            click_color=(85, 85, 85, 255),
            font="Arial",
            font_size=12,
            padding=1,
            window=self
        )

        if self.backup_button:
            self.backup_button.show()
            self.backup_button.clicked.connect(self.backup_database)

        # ================================================================
        # Import data button
        # ================================================================
        self.restore_button = Engine.create_button(
            text="Restaurar",
            size=(80, 25),
            position=(self.window_size[0] - 340, 245),
            color=self.text_color,
            background_color=(51, 51, 51, 255),
            hover_color=(57, 57, 57, 255),
            click_color=(85, 85, 85, 255),
            font="Arial",
            font_size=12,
            padding=1,
            window=self
        )

        if self.restore_button:
            self.restore_button.show()
            self.restore_button.clicked.connect(self.restore_backup)

        # ================================================================
        # Finish UI setup and move to fullscreen
        # ================================================================
        self.showFullScreen()
        
    def resizeEvent(self, event):
        self.update_ui()
        super().resizeEvent(event)

    # ================================================================
    # Search functionality
    # ================================================================
    def add_store(self):
        database.add_store({
            "company_name": "Nombre de la Compañía",
            "store_number": "123456",
            "address": "123 Calle Principal",
            "city": "Ciudad",
            "state": "Estado",
            "zip": "12345",
            "coordinates": "0,0",
            "contact_name": "Juan Pérez",
            "contact_phone": "123-456-7890",
            "contact_email": "juanperez@example.com",
            "notes": "Notas sobre la tienda",
            "active": 1
        })

        self.refresh_stores()

    def export_list(self):
        self.export_prompt = ExportPrompt()
        self.export_prompt.show()

    def refresh_stores(self):
        if self.search_results:
            self.search_results.clear()

            stores = database.get_all_stores()
            utils.log_debug(f"Loaded {len(stores)} stores from database.")

            if stores != []: # If no stores are found, show a message in the list
                for store in stores:
                    latest_service = database.get_next_service_date(store['id'])
                    if latest_service:
                        latest_service = utils.format_datetime(latest_service)
                    else:
                        latest_service = "Ningún servicio programado"

                    item = Engine.create_list_item(self.search_results)
                    if item:
                        row = StoreWidget(
                            store_id=store['id'],
                            company_name=store['company_name'],
                            store_number=store['store_number'],
                            address=store['address'],
                            city=store['city'],
                            state=store['state'],
                            zip=store['zip'],
                            coordinates=store['coordinates'],
                            next_service_date=latest_service,
                            status=store["active"],
                            refresh=self.refresh_stores,
                            item=item,
                            list_widget=self.search_results
                            )
                        item.setSizeHint(row.sizeHint())
                        self.search_results.addItem(item)
                        self.search_results.setItemWidget(item, row)
            
            self.update_store_totals()

    def item_clicked(self, item):
        if self.search_results:
            widget = self.search_results.itemWidget(item)
            
            if widget and isinstance(widget, StoreWidget):
                widget.toggle_advanced_display()
                widget.screen_size = self.screen_size
                widget.window_size = self.window_size
                self.search_results.update()

    def restore_backup(self):
        in_out_put.import_database()
        database.initialize_database(database.get_database_path())
        self.refresh_stores()

    def backup_database(self):
        in_out_put.backup_database()
        self.refresh_stores()

    # ================================================================
    # Update UI element positions and sizes based on current window size
    # ================================================================
    def update_ui(self):
        new_size = self.size()
        self.window_size = (new_size.width(), new_size.height())

        if self.search_bar: # Update search bar size
            x_size = utils.clamp(self.window_size[0] - 100, 505, self.screen_size[0] - 100)
            self.search_bar.setFixedSize(x_size, 30)

        if self.search_results: # Update search results size
            x_size = utils.clamp(self.window_size[0] - 100, 505, self.screen_size[0] - 100)
            y_size = utils.clamp(self.window_size[1] - 300, 200, self.screen_size[1] - 300)
            self.search_results.setFixedSize(x_size, y_size)

        if self.add_store_button: # Update add store button position
            x_pos = utils.clamp(self.window_size[0] - 75, 475, self.screen_size[0] - 75)
            self.add_store_button.move(x_pos, 245)

        if self.export_button: # Update export button position
            x_pos = utils.clamp(self.window_size[0] - 160, 390, self.screen_size[0] - 160)
            self.export_button.move(x_pos, 245)

        if self.refresh_button: # Update refresh button position
            x_pos = utils.clamp(self.window_size[0] - 250, 300, self.screen_size[0] - 250)
            self.refresh_button.move(x_pos, 245)
        
        if self.backup_button: # Update backup button position
            x_pos = utils.clamp(self.window_size[0] - 340, 300, self.screen_size[0] - 310)
            self.backup_button.move(x_pos, 245)

        if self.restore_button: # Update import button position
            x_pos = utils.clamp(self.window_size[0] - 430, 210, self.screen_size[0] - 400)
            self.restore_button.move(x_pos, 245)

    def update_store_totals(self):
        self.store_total = database.get_store_count()
        self.service_types_offered = database.get_service_count()
        self.active_services = database.get_active_services()
        self.services_completed = database.get_services_completed()
        self.services_completed_month = database.get_services_completed_month()
        self.services_completed_year = database.get_services_completed_year()

        if self.store_total_label:
            self.store_total_label.setText(f"Total de tiendas: {self.store_total}")
        
        if self.service_total_label:
            self.service_total_label.setText(f"Servicios activos programados: {self.active_services}")

        if self.service_types_offered_label:
            self.service_types_offered_label.setText(f"Tipos de servicios ofrecidos: {self.service_types_offered}")
        
        if self.services_completed_label:
            self.services_completed_label.setText(f"Servicios completados: {self.services_completed}")

        if self.services_completed_month_label:
            self.services_completed_month_label.setText(f"Servicios completados este mes: {self.services_completed_month}")

        if self.services_completed_year_label:
            self.services_completed_year_label.setText(f"Servicios completados este año: {self.services_completed_year}")
        


    # ================================================================
    # Overrides the key press event to handle fullscreen toggle
    # ================================================================
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif event.key() == Qt.Key_Escape:
            self.showNormal()
