import os
import subprocess
from sgtk.platform import SoftwareLauncher

class MayaLaunchWithRez(SoftwareLauncher):
    def launch(self, software_entity, context, file_to_open=None, args=None):
        """
        Maya를 Rez 환경에서 실행한다.
        """
        # 기본 마야 실행 경로
        maya_exe = software_entity.path

        # Rez 패키지 이름 (extra에 설정되어 있어야 함)
        rez_pkg = software_entity.extra.get("rez_package", "maya_object_plugin")

        # 실행 명령어 구성
        launch_cmd = [
            "rez", "env", rez_pkg, "--", maya_exe
        ]

        print(f"▶️ Launching: {' '.join(launch_cmd)}")

        # 실행
        subprocess.Popen(launch_cmd)

        print("🚀 launch hook 실행됨!")

