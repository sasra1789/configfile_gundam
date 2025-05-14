import os
import sgtk
import maya.cmds as cmds

HookBaseClass = sgtk.get_hook_baseclass()

class ExportMoviePlugin(HookBaseClass):
    """
    Viewport Playblast → mov export 플러그인
    """

    def accept(self, settings, item):
        return {"accepted": True, "checked": True}

    def validate(self, settings, item):
        return True

    def publish(self, settings, item):
        if not item.properties.get("register_in_shotgun", True):
            self.logger.info("❎ Movie: ShotGrid 등록 체크 안 됨 → 퍼블리시 제외")
            return

        # 출력 위치
        export_dir = os.path.dirname(item.parent.properties["path"])
        export_name = "playblast.mov"
        export_path = os.path.join(export_dir, export_name)

        start = item.parent.properties.get("start_frame", 100)
        end = item.parent.properties.get("end_frame", 200)

        try:
            cmds.playblast(
                startTime=start,
                endTime=end,
                format="qt",  # quicktime
                filename=export_path,
                forceOverwrite=True,
                showOrnaments=False,
                percent=100,
                compression="H.264",
                widthHeight=(1920, 1080)
            )
        except Exception as e:
            self.logger.error(f"Playblast 실패: {e}")
            return

        item.properties["publish_path"] = export_path
        self.logger.info(f"✅ Playblast export 완료 → {export_path}")

    def finalize(self, settings, item):
        self.logger.info("🟢 finalize 완료 (MOV)")
