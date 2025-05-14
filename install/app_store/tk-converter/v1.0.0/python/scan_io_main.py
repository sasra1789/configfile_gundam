def launch_scan_io_manager(app_instance):
    from PySide6 import QtWidgets
    import sys

    from controller import Controller
    from main_window import MainWindow

    ui = MainWindow()
    controller = Controller(ui)
    ui.show()