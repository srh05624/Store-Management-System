from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from scripts import in_out_put
from ui.engine import Engine

class ExportPrompt(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.text_color = (255, 255, 255, 255)
        self.window_size = (400, 300)
        self.export_list = set()
        
        self.setStyleSheet("background-color: rgba(40, 40, 40, 200); border-radius: 10px;")
        self.setFixedSize(self.window_size[0], self.window_size[1])
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Exportar Datos")
        
        self.export_prompt_title = Engine.create_text(
            text="¿Qué datos desea exportar?",
            size=16,
            position=(100, 20),
            color=self.text_color,
            background_color=(0, 0, 0, 0),
            font="Arial",
            window=self
        )

        if self.export_prompt_title:
            self.export_prompt_title.show()

        # ================================================================
        # Backgrounds
        # ================================================================
        self.selection_background = Engine.create_rectangle(
            size=(170, 180),
            position=(20, 60),
            color=(60, 60, 60, 255),
            border_color=(200, 200, 200, 255),
            border_width=1,
            border_radius=5,
            window=self
        )

        self.format_background = Engine.create_rectangle(
            size=(170, 180),
            position=(210, 60),
            color=(60, 60, 60, 255),
            border_color=(200, 200, 200, 255),
            border_width=1,
            border_radius=5,
            window=self
        )

        # ================================================================
        # Export Checkboxes
        # ================================================================
        self.export_all_checkbox = Engine.create_checkbox(
            text="Exportar Todo",
            size=(160, 20),
            position=(35, 70),
            color=self.text_color,
            background_color=(0, 0, 0, 0),
            click_color=(0, 0, 0, 0),
            hover_color=(0, 0, 0, 0),
            border_width=0,
            checked_color=(0, 255, 0, 255),
            unchecked_color=(255, 0, 0, 255),
            indicator_color=(255, 255, 255, 255),
            indicator_size=(12, 12),
            indicator_width=1,
            indicator_border_radius=2,
            font="Arial",
            font_size=12,
            padding=1,
            window=self
        )

        if self.export_all_checkbox:
            self.export_all_checkbox.show()
            self.export_all_checkbox.clicked.connect(self.toggle_export_all)

        # ================================================================

        self.export_stores_checkbox = Engine.create_checkbox(
            text="Exportar Tiendas",
            size=(160, 20),
            position=(35, 105),
            color=self.text_color,
            background_color=(0, 0, 0, 0),
            click_color=(0, 0, 0, 0),
            hover_color=(0, 0, 0, 0),
            border_width=0,
            checked_color=(0, 255, 0, 255),
            unchecked_color=(255, 0, 0, 255),
            indicator_color=(255, 255, 255, 255),
            indicator_size=(12, 12),
            indicator_width=1,
            indicator_border_radius=2,
            font="Arial",
            font_size=12,
            padding=1,
            window=self
        )

        if self.export_stores_checkbox:
            self.export_stores_checkbox.show()
            self.export_stores_checkbox.clicked.connect(self.toggle_export_stores)

        # ================================================================

        self.export_services_checkbox = Engine.create_checkbox(
            text="Exportar Servicios",
            size=(160, 20),
            position=(35, 140),
            color=self.text_color,
            background_color=(0, 0, 0, 0),
            click_color=(0, 0, 0, 0),
            hover_color=(0, 0, 0, 0),
            border_width=0,
            checked_color=(0, 255, 0, 255),
            unchecked_color=(255, 0, 0, 255),
            indicator_color=(255, 255, 255, 255),
            indicator_size=(12, 12),
            indicator_width=1,
            indicator_border_radius=2,
            font="Arial",
            font_size=12,
            padding=1,
            window=self
        )

        if self.export_services_checkbox:
            self.export_services_checkbox.show()
            self.export_services_checkbox.clicked.connect(self.toggle_export_services)

        # ================================================================

        self.export_service_records_checkbox = Engine.create_checkbox(
            text="Exportar Registros",
            size=(160, 20),
            position=(35, 175),
            color=self.text_color,
            background_color=(0, 0, 0, 0),
            click_color=(0, 0, 0, 0),
            hover_color=(0, 0, 0, 0),
            border_width=0,
            checked_color=(0, 255, 0, 255),
            unchecked_color=(255, 0, 0, 255),
            indicator_color=(255, 255, 255, 255),
            indicator_size=(12, 12),
            indicator_width=1,
            indicator_border_radius=2,
            font="Arial",
            font_size=12,
            padding=1,
            window=self
        )

        if self.export_service_records_checkbox:
            self.export_service_records_checkbox.show()
            self.export_service_records_checkbox.clicked.connect(self.toggle_export_service_records)

        # ================================================================

        self.export_service_history_checkbox = Engine.create_checkbox(
            text="Exportar Historial",
            size=(160, 20),
            position=(35, 210),
            color=self.text_color,
            background_color=(0, 0, 0, 0),
            click_color=(0, 0, 0, 0),
            hover_color=(0, 0, 0, 0),
            border_width=0,
            checked_color=(0, 255, 0, 255),
            unchecked_color=(255, 0, 0, 255),
            indicator_color=(255, 255, 255, 255),
            indicator_size=(12, 12),
            indicator_width=1,
            indicator_border_radius=2,
            font="Arial",
            font_size=12,
            padding=1,
            window=self
        )

        if self.export_service_history_checkbox:
            self.export_service_history_checkbox.show()
            self.export_service_history_checkbox.clicked.connect(self.toggle_export_service_history)

        # ================================================================
        # Action Buttons
        # ================================================================
        self.cancel_button = Engine.create_button(
            text="Cancelar",
            size=(100, 20),
            position=(20 , self.window_size[1] - 50),
            color=self.text_color,
            background_color=(51, 51, 51, 255),
            hover_color=(57, 57, 57, 255),
            click_color=(85, 85, 85, 255),
            font="Arial",
            font_size=12,
            padding=1,
            window=self
        )

        if self.cancel_button:
            self.cancel_button.show()
            self.cancel_button.clicked.connect(self.close)

        # ================================================================

        self.export_button = Engine.create_button(
            text="Exportar",
            size=(100, 20),
            position=(self.window_size[0] - 120 , self.window_size[1] - 50),
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
            self.export_button.clicked.connect(self.export_data)

    def toggle_export_stores(self, state):
        if self.export_all_checkbox and self.export_all_checkbox.isChecked():
            self.export_all_checkbox.setChecked(False)

        if self.export_stores_checkbox:
            if state:
                self.export_list.add("stores")
            else:
                self.export_list.discard("stores")

    def toggle_export_services(self, state):
        if self.export_all_checkbox and self.export_all_checkbox.isChecked():
            self.export_all_checkbox.setChecked(False)

        if self.export_services_checkbox:
            if state:
                self.export_list.add("services")
            else:
                self.export_list.discard("services")

    def toggle_export_service_records(self, state):
        if self.export_all_checkbox and self.export_all_checkbox.isChecked():
            self.export_all_checkbox.setChecked(False)

        if self.export_service_records_checkbox:
            if state:
                self.export_list.add("service_records")
            else:
                self.export_list.discard("service_records")

    def toggle_export_service_history(self, state):
        if self.export_all_checkbox and self.export_all_checkbox.isChecked():
            self.export_all_checkbox.setChecked(False)

        if self.export_service_history_checkbox:
            if state:
                self.export_list.add("service_history")
            else:
                self.export_list.discard("service_history")

    def toggle_export_all(self, state):
        if state:
            self.export_list = {"stores", "services", "service_records", "service_history"}

            if self.export_stores_checkbox and not self.export_stores_checkbox.isChecked():
                self.export_stores_checkbox.setChecked(True)
            if self.export_services_checkbox and not self.export_services_checkbox.isChecked():
                self.export_services_checkbox.setChecked(True)
            if self.export_service_records_checkbox and not self.export_service_records_checkbox.isChecked():
                self.export_service_records_checkbox.setChecked(True)
            if self.export_service_history_checkbox and not self.export_service_history_checkbox.isChecked():
                self.export_service_history_checkbox.setChecked(True)
        else:
            self.export_list.clear()

    def export_data(self):
        in_out_put.export_all_data(self.export_list)
        self.close()
