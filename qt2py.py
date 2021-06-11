import os
import platform
import sys
from pathlib import Path, PurePath


# pyuic
class FindPyuic:
    KW_PYTHON = "app"
    PYTHON_EXT = PurePath("python_ext").joinpath("py.pth")
    KW_LIB = ".wood"
    PYUIC = {
        "Windows": "pyside2-uic.exe",
        "Mac": "pyside2-uic",
    }
    PYRRC = {
        "Windows": "pyside2-rrc.exe",
        "Mac": "pyside2-rrc",
    }

    def __init__(self, ):
        # 初始化设置
        self.init_set()

    def init_set(self):
        # find pyuic path
        self.pyuic_path = None
        # find python path
        self.python_path = sys.executable
        # get system type
        self.get_sys_type()

        wood_bin = None
        pyuic_path = None
        # read py.pth
        pos = self.python_path.rfind(self.KW_PYTHON)
        pyth = Path(self.python_path[:pos + len(self.KW_PYTHON)]).joinpath(
            self.PYTHON_EXT)
        with open(pyth) as f:
            context = f.readlines()
        # get .wood/libs path
        for txt in context:
            if self.KW_LIB in txt:
                wood_bin = Path(txt.strip()).joinpath("bin")
                break
        # 判断是否存在 .wood/libs/bin/uic
        if wood_bin:
            pyuic_path = Path(wood_bin).joinpath(self.PYUIC[self.sys_type])
            if Path(pyuic_path).exists():
                self.pyuic_path = str(pyuic_path)
        # 打印执行结果
        print("wood_bin:", wood_bin)
        print("pyuic_path:", pyuic_path)
        print("self.pyuic_path:", self.pyuic_path)

    def get_sys_type(self):
        sys_str = platform.system()
        if sys_str == "Windows":
            self.sys_type = "Windows"
        elif sys_str == "Darwin":
            self.sys_type = "Mac"

    def pyuic(self, ui_path):
        # 获取文件名
        ui_pre = Path(ui_path).stem
        ui_path_pre = str(Path(ui_path).parents[0])
        ui_py_name = Path(ui_path_pre).joinpath("ui_{}.py".format(ui_pre))

        order = None

        # 优化对路径中包含空格的处理，使其可以执行带空格的路径
        ui_path = "".join(['"', str(ui_path), '"'])
        ui_py_name = "".join(['"', str(ui_py_name), '"'])

        # execute pyuic5
        if self.pyuic_path:
            # pyuic5 bin
            order = "{} {} -o {}".format(self.pyuic_path, ui_path,
                                         str(ui_py_name))
        else:
            # uic.pyuic model
            order = "{} -m PySide2.scripts.uic {} -o {}".format(
                self.python_path, ui_path, str(ui_py_name))
        print(order)
        os.system(order)


# ui
from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Qt2Py(object):
    def setupUi(self, Qt2Py):
        Qt2Py.setObjectName("Qt2Py")
        Qt2Py.resize(500, 350)
        self.centralwidget = QtWidgets.QWidget(Qt2Py)
        self.centralwidget.setObjectName("centralwidget")
        self.lb_title = QtWidgets.QLabel(self.centralwidget)
        self.lb_title.setGeometry(QtCore.QRect(60, 20, 381, 27))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.lb_title.setFont(font)
        self.lb_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_title.setObjectName("lb_title")
        self.lb_info = QtWidgets.QLabel(self.centralwidget)
        self.lb_info.setGeometry(QtCore.QRect(48, 175, 391, 46))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lb_info.setFont(font)
        self.lb_info.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lb_info.setWordWrap(False)
        self.lb_info.setIndent(6)
        self.lb_info.setObjectName("lb_info")
        self.pbtn_file = QtWidgets.QPushButton(self.centralwidget)
        self.pbtn_file.setGeometry(QtCore.QRect(48, 110, 151, 41))
        self.pbtn_file.setStyleSheet("")
        self.pbtn_file.setObjectName("pbtn_file")
        self.pbtn_switch = QtWidgets.QPushButton(self.centralwidget)
        self.pbtn_switch.setGeometry(QtCore.QRect(290, 110, 151, 41))
        self.pbtn_switch.setMinimumSize(QtCore.QSize(0, 0))
        self.pbtn_switch.setStyleSheet("")
        self.pbtn_switch.setObjectName("pbtn_switch")
        Qt2Py.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 22))
        self.menubar.setObjectName("menubar")
        Qt2Py.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Qt2Py)
        self.statusbar.setObjectName("statusbar")
        Qt2Py.setStatusBar(self.statusbar)

        self.retranslateUi(Qt2Py)
        QtCore.QMetaObject.connectSlotsByName(Qt2Py)

    def retranslateUi(self, Qt2Py):
        Qt2Py.setWindowTitle(QtWidgets.QApplication.translate("Qt2Py", "Qt Creator转换器", None, -1))
        self.lb_title.setText(QtWidgets.QApplication.translate("Qt2Py", "Qt Creator转换器", None, -1))
        self.lb_info.setText(QtWidgets.QApplication.translate("Qt2Py", "请选择需要转换的 ui 文件...", None, -1))
        self.pbtn_file.setText(QtWidgets.QApplication.translate("Qt2Py", "选择 ui 文件", None, -1))
        self.pbtn_switch.setText(QtWidgets.QApplication.translate("Qt2Py", "开始转换", None, -1))


# Work: ExcutePyuic
from PySide2.QtCore import QThread, Signal


class ExcutePyuic(QThread):
    trigger = Signal(str)

    def __init__(self, ui_file):
        super().__init__()
        self.ui_file = ui_file

    def run(self):
        if not self.ui_file:
            self.trigger.emit("null")
            return
        self.trigger.emit("start")
        caller = FindPyuic()
        caller.pyuic(self.ui_file)
        self.trigger.emit("end")

    def __del__(self):
        self.wait()
        self.quit()
        print("ExcutePyuic Finish~")


# logic
from PySide2.QtWidgets import *


class Qt2Py(QMainWindow, Ui_Qt2Py):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)
        self.init_set()

        # ui 路径和文件名
        self.ui_path = None
        # 提示信息
        self.info = None
        # 状态配置
        self.status = {
            "start": {
                "msg": "正在努力转换中...请稍后...",
                "btn_enable": False
            },
            "end": {
                "msg": "转换完成！",
                "btn_enable": True
            },
            "null": {
                "msg": "请先选择 ui 文件...",
                "btn_enable": True
            },
        }

        # Connect up the buttons.
        self.pbtn_file.clicked.connect(self.select_file)
        self.pbtn_switch.clicked.connect(self.start_switch)

        self.show()

    def init_set(self):
        self.lb_info.adjustSize()

    def select_file(self):
        filename = QFileDialog.getOpenFileName(caption="选择文件", filter="(*.ui)")
        self.ui_path = filename[0]
        try:
            if filename[0]:
                pos = filename[0].rfind(os.path.sep)
                self.info = filename[0][pos + 1:]
        except Exception:
            print("getOpenFileName Error!")

        self.lb_info.setText(self.info)

    def set_info(self, info):
        self.lb_info.setText(self.status[info]["msg"])
        self.pbtn_file.setEnabled(self.status[info]["btn_enable"])
        self.pbtn_switch.setEnabled(self.status[info]["btn_enable"])

    def start_switch(self):
        # switch
        working_pyuic = ExcutePyuic(self.ui_path)
        working_pyuic.trigger.connect(self.set_info)
        working_pyuic.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Qt2Py()
    sys.exit(app.exec_())
