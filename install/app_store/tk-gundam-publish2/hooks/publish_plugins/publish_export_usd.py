import os
import sgtk
import maya.cmds as cmds

HookBaseClass = sgtk.get_hook_baseclass()

class ExportUSDPlugin(HookBaseClass):
    """
    USD Export 플러그인
    """

    def accept(self, settings, item):
        return {"accepted": True, "checked": True}

    def validate(self, settings, item):
        return True

    def publish(self, settings, item):
        if not item.properties.get("register_in_shotgun", True):
            self.logger.info("❎ USD: ShotGrid 등록 체크 안 됨 → 퍼블리시 제외")
            return

        # USD Export 위치
        export_dir = os.path.dirname(item.parent.properties["path"])
        export_name = "scene.usda"
        export_path = os.path.join(export_dir, export_name)

        # 프레임 범위
        start = item.parent.properties.get("start_frame", 100)
        end = item.parent.properties.get("end_frame", 200)

        # USD Export 실행
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")

        try:
            cmds.mayaUSDExport(
                file=export_path,
                frameRange=(start, end),
                shadingMode="useRegistry",
                mergeTransformAndShape=True,
                exportInstances=True,
                renderableOnly=True
            )
        except Exception as e:
            self.logger.error(f"USD Export 실패: {e}")
            return

        item.properties["publish_path"] = export_path
        self.logger.info(f"✅ USD export 완료 → {export_path}")

    def finalize(self, settings, item):
        self.logger.info("🟢 finalize 완료 (USD)")
