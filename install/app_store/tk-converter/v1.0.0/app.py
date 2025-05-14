import sgtk

class App(sgtk.platform.Application):
    def init_app(self):
        self.engine.register_command(
            "ScanData Converter",
            self.launch_ui,
            {"type": "studio"}
        )

    def launch_ui(self):
        # from python.scan_io_main import launch_scan_io_manager # 왜 밖으로 빼면 안되는지 귀신이 곡할노릇
        # launch_scan_io_manager(self)
        import python.main
        python.main.main(self)