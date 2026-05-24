from scripts import installer, utils, database
from ui.engine import Engine
from ui.main_window import MainWindow
import PySide6.QtWidgets

def main():
    print("Starting Lawn Service Manager...")

    # Run installation and setup
    install_results = installer.verify_all()
    for message in install_results["messages"]:
        print(" > ", message)

    if not install_results["success"]:
        input("Installation failed.\n > Press Enter to exit...")
        utils.exit(1)

    # Load configuration and setup logging
    config = utils.load_config(installer.config_path)
    utils.setup_logging(installer.default_config["logging"]["directory"], debug=config["logging"]["debug"])
    utils.log_info("Application started.")

    # Initialize database
    if not database.initialize_database(config["paths"]["database_path"]):
        input(" > Database initialization failed.\n > Press Enter to exit...")
        utils.exit(1)
    print(" > Database initialized successfully.")

    # Initialize and launch the UI
    utils.log_info("Launching UI.")
    print("Launching UI...")
    app = PySide6.QtWidgets.QApplication([])
    window = MainWindow()
    Engine.change_window(window)
    app.exec()

    utils.log_info("Application exiting...")
    Engine.close_window()
    app.quit()
    
if __name__ == "__main__":
    main()