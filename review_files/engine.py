import PySide6.QtWidgets
from PySide6.QtCore import Qt
from scripts import utils

class Engine:
    window = None

    # ================================================================
    # UI element creation and management functions
    # ================================================================
    @classmethod
    def create_rectangle(cls, size=(100, 100), position=(0, 0), color=(255, 255, 255, 255), border_color=(0, 0, 0, 255), border_width=1, border_radius=5, window=None):
        try:
            rectangle = PySide6.QtWidgets.QLabel(window)
            rectangle.setStyleSheet(f"""
                QLabel {{
                    background-color: rgba{color};
                    border: {border_width}px solid rgba{border_color};
                    border-radius: {border_radius}px;
                }}
            """)
            rectangle.setFixedSize(size[0], size[1])
            if position:
                rectangle.move(position[0], position[1])
            return rectangle
        except Exception as e:
            utils.log_error(f"Error creating rectangle: {e}")
            return None

    @classmethod
    def create_text(cls, text="Text Label", size=12, position=(0,0), color=(0,0,0,255), background_color=(255,255,255,255), font="Arial", window=None):
        try:
            label = PySide6.QtWidgets.QLabel(text, window)
            label.setStyleSheet(f"""
                QLabel {{
                    color: rgba{color};
                    background-color: rgba{background_color};
                    font-family: {font};
                    font-size: {size}px;
                }}
            """)
            if position:
                label.move(position[0], position[1])
            return label
        except Exception as e:
            utils.log_error(f"Error creating label: {e}")
            return None

    @classmethod
    def create_list(cls,
            items=[],
            size=(100,25),
            position=(0,0),
            color=(0,0,0,0),
            background_color=(255,255,255,255),
            hover_color=(187,187,187,255),
            click_color=(119,119,119,255),
            font="Arial",
            window=None
        ):
        try:
            list_widget = PySide6.QtWidgets.QListWidget(window)
            list_widget.setStyleSheet(f"""
                QListWidget {{
                    color: rgba{color};
                    background-color: rgba{background_color};
                    font-family: {font};
                }}
                QListWidget::item {{
                    outline: none;
                    margin: 0px;
                    padding: 0px;
                }}
                QListWidget::item:hover {{
                    background-color: rgba{hover_color};
                    color: rgba{color};
                    }}
                QListWidget::item:selected {{
                    background-color: rgba{click_color};
                    color: rgba{color};
                    }}
            """)
            list_widget.setFixedSize(size[0], size[1])
            for item in items:
                list_widget.addItem(item)
            if position:
                list_widget.move(position[0], position[1])
            return list_widget
        except Exception as e:
            utils.log_error(f"Error creating list widget: {e}")
            return None

    @classmethod
    def create_image_list(cls,
            images=[],
            size=(100,25),
            image_size=(80, 80),
            spacing=10,
            position=(0,0),
            color=(0,0,0,0),
            background_color=(255,255,255,255),
            hover_color=(187,187,187,255),
            click_color=(119,119,119,255),
            font="Arial",
            window=None
        ):
        try:
            list_widget = cls.create_list(images, size, position, color, background_color, hover_color, click_color, font, window)
            list_widget.setViewMode(PySide6.QtWidgets.QListView.IconMode)
            list_widget.setFlow(PySide6.QtWidgets.QListView.LeftToRight)
            list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            list_widget.setResizeMode(PySide6.QtWidgets.QListView.Adjust)
            list_widget.setIconSize(PySide6.QtCore.QSize(image_size[0]-10, image_size[1]-10))
            list_widget.setSpacing(spacing)
            list_widget.setWrapping(False) 
            return list_widget
        except Exception as e:
            utils.log_error(f"Error creating horizontal list widget: {e}")
            return None

    @classmethod
    def create_list_item(cls, parent):
        try:
            return PySide6.QtWidgets.QListWidgetItem(parent)
        except Exception as e:
            utils.log_error(f"Error creating list item: {e}")
            return None

    @classmethod
    def create_input(cls,
            text="",
            placeholder="Text Input",
            size=(100,25),
            position=(0,0),
            color=(0,0,0,255),
            background_color=(255,255,255,255),
            hover_color=(187,187,187,255),
            focus_color=(119,119,119,255),
            font="Arial",
            padding=5,
            window=None
        ):
        try:
            input_field = PySide6.QtWidgets.QLineEdit(window)
            input_field.setText(text)
            input_field.setPlaceholderText(placeholder)
            input_field.setStyleSheet(f"""
                QLineEdit {{
                    color: rgba{color};
                    background-color: rgba{background_color};
                    font-family: {font};
                    padding: {padding}px;
                    border-radius: 5px;
                }}
                QLineEdit:hover {{
                    background-color: rgba{hover_color};
                }}
                QLineEdit:focus {{
                    background-color: rgba{focus_color};
                }}
            """)
            input_field.setFixedSize(size[0], size[1])
            if position:
                input_field.move(position[0], position[1])
            return input_field
        except Exception as e:
            print(f"Error creating input field: {text}, {placeholder}, {size}, {position}, {color}, {background_color}, {hover_color}, {focus_color}, {font}, {padding}")
            utils.log_error(f"Error creating input field: {e}")
            return None
    
    @classmethod
    def create_text_area(cls, text="", placeholder="Text Area", size=(100,25), position=(0,0), color=(0,0,0,255), background_color=(255,255,255,255), hover_color=(187,187,187,255), focus_color=(119,119,119,255), font="Arial", padding=5, window=None):
        try:
            text_area = PySide6.QtWidgets.QTextEdit(window)
            text_area.setText(text)
            text_area.setPlaceholderText(placeholder)
            text_area.setStyleSheet(f"""
                QTextEdit {{
                    color: rgba{color};
                    background-color: rgba{background_color};
                    font-family: {font};
                    padding: {padding}px;
                    border-radius: 5px;
                }}
                QTextEdit:hover {{
                    background-color: rgba{hover_color};
                }}
                QTextEdit:focus {{
                    background-color: rgba{focus_color};
                }}
            """)
            text_area.setFixedSize(size[0], size[1])
            if position:
                text_area.move(position[0], position[1])
            return text_area
        except Exception as e:
            print(f"Error creating text area: {text}, {placeholder}, {size}, {position}, {color}, {background_color}, {hover_color}, {focus_color}, {font}, {padding}")
            utils.log_error(f"Error creating text area: {e}")
            return None

    @classmethod
    def create_checkbox(
            cls,
            text="Checkbox",
            size=(30, 30),
            position=(0, 0),
            color=(255, 255, 255, 255),
            background_color=(51, 51, 51, 255),
            border_color=(255, 255, 255, 255),
            border_width=2,
            border_radius=5,
            hover_color=(57, 57, 57, 255),
            click_color=(85, 85, 85, 255),
            indicator_size=(20, 20),
            indicator_width=2,
            indicator_border_radius=3,
            indicator_color=(255, 255, 255, 255),
            indicator_background_color=(51, 51, 51, 255),
            checked_color=(255, 255, 255, 255),
            unchecked_color=(51, 51, 51, 255),
            font="Arial",
            font_size=12,
            padding=1,
            window=None
        ):
        try:
            checkbox = PySide6.QtWidgets.QCheckBox(text, window)
            checkbox.setStyleSheet(f"""
                QCheckBox {{
                    color: rgba{color};
                    background-color: rgba{background_color};
                    font-family: {font};
                    font-size: {font_size}px;
                    padding: {padding}px;
                    border-radius: {border_radius}px;
                    border: {border_width}px solid rgba{border_color};
                }}
                QCheckBox::indicator {{
                    width: {indicator_size[0]}px;
                    height: {indicator_size[1]}px;
                    border: {indicator_width}px solid rgba{indicator_color};
                    border-radius: {indicator_border_radius}px;
                    background-color: rgba{indicator_background_color};
                }}
                QCheckBox::indicator:checked {{
                    background-color: rgba{checked_color};
                }}
                QCheckBox::indicator:unchecked {{
                    background-color: rgba{unchecked_color};
                }}
                QCheckBox:hover {{
                    background-color: rgba{hover_color};
                }}
                QCheckBox:pressed {{
                    background-color: rgba{click_color};
                }}
            """)
            checkbox.setFixedSize(size[0], size[1])
            if position:
                checkbox.move(position[0], position[1])
            return checkbox
        except Exception as e:
            utils.log_error(f"Error creating checkbox: {e}")
            return None

    @classmethod
    def create_button(
            cls,
            text="Button",
            size=(100,25),
            position=(0,0),
            color=(0,0,0,255),
            background_color=(255,255,255,255),
            hover_color=(187,187,187,255),
            click_color=(119,119,119,255),
            font="Arial",
            font_size=10,
            padding=10,
            window=None
        ):
        try:
            button = PySide6.QtWidgets.QPushButton(text, window)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba{background_color};
                    color: rgba{color};
                    font-family: {font};
                    font-size: {font_size}px;
                    padding: {padding}px;
                    border-radius: 5px;
                }}
                QPushButton:hover {{
                    background-color: rgba{hover_color};
                }}
                QPushButton:pressed {{
                    background-color: rgba{click_color};
                }}
            """)
            button.setFixedSize(size[0], size[1])
            if position:
                button.move(position[0], position[1])
            return button
        except Exception as e:
            utils.log_error(f"Error creating button: {e}")
            return None

    # ================================================================
    # UI element management functions
    # ================================================================
    @classmethod
    def update_button(cls, button, text=None, size=None, position=None, color=None, text_color=None, font=None, padding=None):
        try:
            if text:
                button.setText(text)
            if size:
                button.setFixedSize(size[0], size[1])
            if color or text_color or font or padding:
                current_style = button.styleSheet()
                new_style = f"""background-color: rgba{color if color else (76, 175, 80, 255)}; color: rgba{text_color if text_color else (255, 255, 255, 255)}; font-family: {font if font else 'Arial'}; padding: {padding if padding else 10}px; border-radius: 5px;"""
                button.setStyleSheet(current_style + new_style)
            if position:
                button.move(position[0], position[1])
        except Exception as e:
            utils.log_error(f"Error updating button: {e}")

    # ================================================================
    # Window management functions
    # ================================================================
    @classmethod
    def change_window(cls, new_window):
        try:
            if cls.window:
                cls.window.close()
            cls.window = new_window
            cls.window.show()
        except Exception as e:
            utils.log_error(f"Error changing window: {e}")

    @classmethod
    def close_window(cls):
        try:
            if cls.window:
                cls.window.close()
                cls.window = None
        except Exception as e:
            utils.log_error(f"Error closing window: {e}")