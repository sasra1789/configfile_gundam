import os
import json
import sgtk

HookBaseClass = sgtk.get_hook_baseclass()

class ExportSceneInfoPlugin(HookBaseClass):
    """
    현재 씬의 컨텍스트 정보를 JSON으로 저장하는 퍼블리시 플러그인
    """

    def accept(self, settings, item):
        return {"accepted": True, "checked": True}

    def validate(self, settings, item):
        return True

    def publish(self, settings, item):
        # 등록 여부 확인
        if not item.properties.get("register_in_shotgun", True):
            self.logger.info("❎ ShotGrid 등록 체크 해제됨: 퍼블리시 생략")
            return

        context = item.context
        export_data = {
            "project": context.project["name"],
            "entity": context.entity["name"] if context.entity else None,
            "step": context.step["name"] if context.step else None,
            "task": context.task["name"] if context.task else None,
            "user": context.user["name"] if context.user else None,
            "description": item.properties.get("description", ""),
            "start_frame": item.properties.get("start_frame"),
            "end_frame": item.properties.get("end_frame"),
        }

        # 저장 위치
        export_path = os.path.join(
            os.path.dirname(item.properties["path"]),
            "scene_info.json"
        )
        with open(export_path, "w") as f:
            json.dump(export_data, f, indent=4)

        self.logger.info(f"scene_info.json export 완료 → {export_path}")
        # 퍼블리시 경로 등록 (ShotGrid에 등록하려면 필요)
        item.properties["publish_path"] = export_path

    def finalize(self, settings, item):
        self.logger.info("🟢 finalize 완료 (scene_info)")
