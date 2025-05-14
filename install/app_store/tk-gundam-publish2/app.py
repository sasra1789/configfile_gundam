import sgtk

class App(sgtk.platform.Application):
    def init_app(self):
        self.logger.info("✅ tk-gundam-publish2 초기화됨")

        self.engine.register_command(
            "Gundam Publish",
            self.launch_app,
            {"type": "menu"}
        )

    # def launch_app(self):
    #     self.logger.info("🚀 tk-multi-publish2 위장 실행 시도")

    #     try:
    #         publish_app = self.engine.apps.get("tk-multi-publish2")
    #         if not publish_app:
    #             raise RuntimeError("tk-multi-publish2 앱이 현재 환경에 설치되어 있지 않습니다.")

    #         publish_app.show_publish_dlg()
    #         self.logger.info(" tk-multi-publish2 UI 실행 완료")

    #     except Exception as e:
    #         self.logger.error(f"❌ 퍼블리셔 실행 실패: {e}")
    def launch_app(self):
        self.logger.info("🚀 tk-multi-publish2 위장 실행 시도")

        try:
            publish_app = self.engine.apps.get("tk-multi-publish2")
            if not publish_app:
                raise RuntimeError("tk-multi-publish2 앱이 현재 환경에 설치되어 있지 않습니다.")

            # api 모듈 import 우선 시도
            try:
                publish_api = publish_app.import_module("tk_multi_publish2.api")
                publish_api.show_dialog(publish_app)
            except ImportError:
                # fallback: __init__.py에 있을 경우
                self.logger.info("🔁 api.py 없음, __init__.py에서 show_dialog 실행 시도")
                publish_api = publish_app.import_module("tk_multi_publish2")
                publish_api.show_dialog(publish_app)

            self.logger.info("✅ 퍼블리셔 UI 실행 완료")

        except Exception as e:
            self.logger.error(f"❌ 퍼블리셔 실행 실패: {e}")