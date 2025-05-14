import os
import json
import sgtk

HookBaseClass = sgtk.get_hook_baseclass()

class ExportSceneInfoPlugin(HookBaseClass):
    def accept(self, settings, item):
        return {"accepted": True, "checked": True}

    def validate(self, settings, item):
        return True

    def publish(self, settings, item):
        if not item.properties.get("register_in_shotgun", True):
            self.logger.info("✔ ShotGrid 퍼블리시 제외됨 (체크 해제 상태)")
            return

        context = item.context
        export_data = {
            "project": context.project["name"],
            "entity": context.entity["name"] if context.entity else None,
            "step": context.step["name"] if context.step else None,
            "user": context.user["name"] if context.user else None,
            "description": item.properties.get("description", "")
        }

        output_path = os.path.join(item.properties["path"], "scene_info.json")
        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=4)

        self.logger.info(f"scene_info.json 저장 완료 → {output_path}")
