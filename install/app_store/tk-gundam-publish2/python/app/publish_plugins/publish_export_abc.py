import os
import sgtk
import maya.cmds as cmds

HookBaseClass = sgtk.get_hook_baseclass()

class ExportAlembicPlugin(HookBaseClass):
    """
    마야 Alembic (.abc) export 플러그인
    """

    def accept(self, settings, item):
        return {"accepted": True, "checked": True}

    def validate(self, settings, item):
        return True

    def publish(self, settings, item):
        if not item.properties.get("register_in_shotgun", True):
            self.logger.info("❎ Alembic: ShotGrid 등록 체크 안 됨 → 퍼블리시 제외")
            return

        # 필수 정보
        export_dir = os.path.dirname(item.parent.properties["path"])
        export_name = "geometry.abc"
        export_path = os.path.join(export_dir, export_name)

        start = item.parent.properties.get("start_frame", 100)
        end = item.parent.properties.get("end_frame", 200)

        # export 대상 루트 노드 (지금은 임의로 설정: 필요 시 UI에서 지정 가능)
        root_node = "|group1"
        if not cmds.objExists(root_node):
            self.logger.warning(f"Alembic export 실패: '{root_node}' 노드가 존재하지 않습니다.")
            return

        # Alembic export 명령어
        abc_args = f"-frameRange {start} {end} -root {root_node} -file \"{export_path}\""
        self.logger.info(f"🚀 Alembic Export 실행: {abc_args}")
        cmds.AbcExport(j=abc_args)

        # 퍼블리시 경로 등록
        item.properties["publish_path"] = export_path
        self.logger.info(f"✅ Alembic export 완료 → {export_path}")

    def finalize(self, settings, item):
        self.logger.info("🟢 finalize 완료 (Alembic)")
