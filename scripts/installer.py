import os, json
from scripts import database

local_path = str(os.getenv('APPDATA') or os.path.expanduser('~'))
install_path = os.path.join(local_path, "Lawn Service Manager")
log_directory = os.path.join(install_path, "logs")
reports_path = os.path.join(install_path, "reports")
config_path = os.path.join(install_path, "config.json")
database_path = os.path.join(install_path, "data", "lawn_services.db")

default_config = {
    "paths": {
        "install_directory": install_path,
        "log_directory": log_directory,
        "reports_directory": reports_path,
        "database_path": database_path,
    },
    "logging": {
        "directory": log_directory,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "debug": False
    },
    "alerts": {
        "enabled": True,
        "interval": 3600,
        "desktop": {
            "enabled": True,
            "icon_path": ".\\assets\\icon.ico"
        },
        "email": {
            "enabled": False,
            "smtp_server": "GMAIL_SMTP_SERVER",
            "smtp_port": "GMAIL_SMTP_PORT",
            "sender": "",
            "recipients": []
        }
    },
    "import": {
        "enabled": False,
        "directory": os.path.join(install_path, "imports")
    },
    "export": {
        "enabled": False,
        "directory": os.path.join(install_path, "exports")
    },
    "app_name": "Lawn Service Manager",
    "report": True
}

# =====================================================
# Installation and Setup Functions
# =====================================================
def verify_install_directory():
    try:
        if not os.path.exists(install_path):
            os.makedirs(install_path, exist_ok=True)
            return f"Installation directory created at: {install_path}", True
        return f"Installation directory already exists at: {install_path}", True
    except Exception as e:
        return f"Error creating installation directory: {str(e)}", False

def verify_log_directory():
    try:
        if not os.path.exists(log_directory):
            os.makedirs(log_directory, exist_ok=True)
            return f"Log directory created at: {log_directory}", True
        return f"Log directory already exists at: {log_directory}", True
    except Exception as e:
        return f"Error creating log directory: {str(e)}", False

def verify_reports_directory():
    try:
        if not os.path.exists(reports_path):
            os.makedirs(reports_path, exist_ok=True)
            return f"Reports directory created at: {reports_path}", True
        return f"Reports directory already exists at: {reports_path}", True
    except Exception as e:
        return f"Error creating reports directory: {str(e)}", False

def verify_config_file():
    try:
        if not os.path.exists(config_path):
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            return f"Config file created at: {config_path}", True
        return f"Config file already exists at: {config_path}", True
    except Exception as e:
        return f"Error creating config file: {str(e)}", False
    
def verify_database_directory(db_path):
    try:
        if not os.path.exists(db_path):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            database.initialize_database(db_path)
            return f"Database created at: {db_path}", True
        return f"Database already exists at: {db_path}", True
    except Exception as e:
        return f"Error creating database: {str(e)}", False

def results(msg, success, data=None):
    if data is None:
        data = {"success": True, "messages": []}
    if not success:
        data["success"] = False
    data["messages"].append(msg)
    return data

def verify_all():
    data = {"success": True, "messages": []}
    results(*verify_install_directory(), data)
    results(*verify_log_directory(), data)
    results(*verify_reports_directory(), data)
    results(*verify_config_file(), data)
    results(*verify_database_directory(default_config["paths"]["database_path"]), data)

    return data