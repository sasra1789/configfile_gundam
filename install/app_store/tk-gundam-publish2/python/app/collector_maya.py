import sgtk
import maya.cmds as cmds
import os

HookBaseClass = sgtk.get_hook_baseclass()

class CollectorPlugin(HookBaseClass):
    def process_current_session(self, settings, parent_item):
        """
        퍼블리셔 실행 시 호출되는 Collector 진입점
        - 현재 마야 씬을 대표하는 session item 생성
        - 글로벌 설정 필드 정의
        - export 대상 수집
        """
        # 1. 현재 씬 경로 추출
        current_path = cmds.file(q=True, sn=True) or "untitled"

        # 2. session 아이템 생성
        session_item = parent_item.create_item(
            "maya.session",
            "Maya Session",
            os.path.basename(current_path)
        )
        session_item.properties["path"] = current_path

        # 3. 글로벌 설정 필드 (Start/End Frame, Description)
        session_item.properties["extra_fields"] = {
            "start_frame": {
                "type": "int",
                "default": int(cmds.playbackOptions(q=True, min=True)),
                "label": "Start Frame"
            },
            "end_frame": {
                "type": "int",
                "default": int(cmds.playbackOptions(q=True, max=True)),
                "label": "End Frame"
            },
            "description": {
                "type": "text",
                "default": "",
                "label": "Description"
            }
        }

        # 4. export 대상 생성
        self._collect_abc(session_item)
        self._collect_usd(session_item)
        self._collect_json(session_item)

        return session_item

    def _collect_abc(self, parent_item):
        item = parent_item.create_item("maya.abc", "Alembic Export", "export.abc")
        item.properties.update({
            "output_type": "abc",
            "register_in_shotgun": True,
            "extra_fields": {
                "register_in_shotgun": {
                    "type": "bool",
                    "default": True,
                    "label": "Publish to ShotGrid?"
                }
            }
        })

    def _collect_usd(self, parent_item):
        item = parent_item.create_item("maya.usd", "USD Export", "export.usd")
        item.properties.update({
            "output_type": "usd",
            "register_in_shotgun": True,
            "extra_fields": {
                "register_in_shotgun": {
                    "type": "bool",
                    "default": True,
                    "label": "Publish to ShotGrid?"
                }
            }
        })

    def _collect_json(self, parent_item):
        item = parent_item.create_item("maya.json", "Scene Info (.json)", "scene_info.json")
        item.properties.update({
            "output_type": "json",
            "register_in_shotgun": True,
            "extra_fields": {
                "register_in_shotgun": {
                    "type": "bool",
                    "default": True,
                    "label": "Publish to ShotGrid?"
                }
            }
        })
