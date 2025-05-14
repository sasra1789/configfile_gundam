# tk-gundam-publish2/python/tk_gundam_publish2/app_dialog.py

from sgtk.platform.qt import QtWidgets
from sgtk.platform import Application

class AppDialog(QtWidgets.QDialog):
    def __init__(self, app_instance: Application):
        super(AppDialog, self).__init__()
        self.setWindowTitle("Gundam Publisher")
        self.setLayout(QtWidgets.QVBoxLayout())

        label = QtWidgets.QLabel("여기에 커스텀 UI 넣기 or tk-multi-publish2 dialog 연결 가능")
        self.layout().addWidget(label)


