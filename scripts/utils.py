import os, sys, json, logging
from datetime import datetime
from scripts import installer
from PySide6.QtWidgets import QFileDialog

# ===============================================================
# Utility functions
# ===============================================================
def get_username():
    try:
        return os.getlogin()
    except Exception as e:
        logging.error(f"Error getting username: {e}")
        return "User"

def create_directory(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            logging.info(f"Created directory: {path}")
        else:
            logging.info(f"Directory already exists: {path}")
    except Exception as e:
        logging.error(f"Error creating directory {path}: {e}")

def exit(code=0):
    print("Exiting application.")
    sys.exit(code)

# ===============================================================
# File dialog functions
# ===============================================================
def request_dir():
    try:
        log_info("Requesting directory for export...")
        directory = QFileDialog.getExistingDirectory(
            None, 
            "Seleccionar Directorio para Exportar Datos", 
            ""
        )

        log_info(f"Directory selected for export: {directory}")
        return directory
    except Exception as e:
        log_error(f"Error requesting directory: {e}")
        return None
    
def request_file():
    try:
        log_info("Requesting file for import...")
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("DB Files (*.db)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            log_info(f"File selected for import: {file_path}")
            return file_path
        else:
            log_info("File selection cancelled.")
            return None
    except Exception as e:
        log_error(f"Error requesting file: {e}")
        return None
    
def request_image_file():
    try:
        log_info("Requesting image file...")
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            log_info(f"Image file selected: {file_path}")
            return file_path
        else:
            log_info("Image file selection cancelled.")
            return None
    except Exception as e:
        log_error(f"Error requesting image file: {e}")
        return None

# ===============================================================
# Math functions
# ===============================================================
def clamp(n, min_val=0, max_val=1):
    return max(min_val, min(n, max_val))

# ===============================================================
# Time and date functions
# ===============================================================
def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_datetime(date=get_current_date(), time=get_current_time()):
    try:
        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%m-%d-%Y %I:%M:%S %p")
    except Exception as e:
        logging.error(f"Error formatting datetime: {e}")
        return "unknown_datetime"

def formated_time():
    try:
        time_now = datetime.now()
        time_final = time_now.strftime("%m-%d-%Y@")
        if time_now.hour > 12:
            time_final += f"{time_now.hour - 12:02d}-{time_now.minute:02d}-{time_now.second:02d}PM"
        else:
            time_final += f"{time_now.hour:02d}-{time_now.minute:02d}-{time_now.second:02d}AM"
        
        return time_final
    except Exception as e:
        logging.error(f"Error formatting time: {e}")
        return "unknown_time"

# ===============================================================
# Logging functions
# ===============================================================
def setup_logging(log_dir, debug=False):
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, f"LawnServiceManager_{formated_time()}.log")
        
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG if debug else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        log_info("Logging setup complete.")
    except Exception as e:
        print(f"Error setting up logging: {e}")

def log_debug(message):
    logging.debug(message)

def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message):
    logging.error(message)

# ===============================================================
# Config functions
# ===============================================================
def load_config(config_path):
    try:
        if not os.path.exists(config_path):
            print(f"Config file {config_path} not found. Using default configuration.")
            return installer.default_config
        
        with open(config_path, 'r') as f:
            config = json.load(f)
            return {**installer.default_config, **config}
    except Exception as e:
        print(f"Error loading config: {e}")
        return installer.default_config
    
def save_config(config, config_path):
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")