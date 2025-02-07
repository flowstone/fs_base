import sys
import os
import datetime
import socket

from fs_base.const.app_constants import AppConstants
from importlib.resources import files  # Python 3.9+


class BaseUtil:

    @staticmethod
    def get_resource_path(relative_path):
        """
        获取资源（如图片等）的实际路径，处理打包后资源路径的问题
        """
        # PyInstaller、Nuitka打包单文件 写入的参数
        if "NUITKA_ONEFILE_PARENT" in os.environ or getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # 如果是冻结状态（例如使用 PyInstaller、Nuitka 等打包后的状态）
            # sys.executable 当前程序运行的目录，仅支持Win系统
            # sys._MEIPASS 是一个存储了程序资源的临时目录
            # 当程序被打包时，资源会被解压到该目录中
            # 此路径和打包的应用有关系，目前pyinstaller打macOS端，Nuitka打Win端
            if BaseUtil.check_win_os():
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = sys._MEIPASS
            # logger.info("[冻结状态]打包后的资源路径:{}".format(application_path))
        else:
            # 如果不是冻结状态，使用当前脚本所在的目录
            #application_path = os.path.dirname(os.path.abspath(__file__))
            application_path = os.path.dirname(sys.argv[0])
            # logger.info("[非冻结状态]打包后的资源路径:{}".format(application_path))
        return os.path.join(application_path, relative_path)

    @staticmethod
    def check_win_os():
        return sys.platform.startswith('win')

    @staticmethod
    def check_mac_os():
        return sys.platform.startswith("darwin")

    @staticmethod
    def check_linux_os():
        return sys.platform.startswith('linux')

    @staticmethod
    def get_ico_full_path():
        return BaseUtil.get_resource_path(AppConstants.APP_ICON_FULL_PATH)

    @staticmethod
    def get_mini_ico_full_path():
        return BaseUtil.get_resource_path(AppConstants.APP_MINI_ICON_FULL_PATH)

    @staticmethod
    def get_mac_user_path():
        return os.path.expanduser(AppConstants.SAVE_FILE_PATH_MAC)

    @staticmethod
    def get_today():
        current_date = datetime.date.today()
        return current_date.strftime('%Y-%m-%d')

    @staticmethod
    def get_current_time(format: str = '%Y-%m-%d %H:%M:%S'):
        current_datetime = datetime.datetime.now()
        return current_datetime.strftime(format)

    @staticmethod
    def count_files_in_directory_tree(folder_path: str):
        count = 0
        for root, dirs, files in os.walk(folder_path):
            count += len(files)
        return count

    @staticmethod
    def count_files_in_current_folder(folder_path: str):
        file_count = 0
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                file_count += 1
        return file_count

    @staticmethod
    def count_folders_in_current_folder(folder_path: str):
        folder_count = 0
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                folder_count += 1
        return folder_count

    @staticmethod
    def format_time(current_datetime):
        format: str = '%Y-%m-%d %H:%M:%S'
        dt_object = datetime.datetime.fromtimestamp(current_datetime)
        return dt_object.strftime(format)

    @staticmethod
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    @staticmethod
    def get_app_ini_path():
        app_ini_path = os.path.join(BaseUtil.get_external_path(), AppConstants.EXTERNAL_APP_INI_FILE)
        if os.path.exists(app_ini_path):
            return app_ini_path
        return BaseUtil.get_resource_path(AppConstants.APP_INI_FILE)

    @staticmethod
    def get_external_path() -> str:
        return AppConstants.SAVE_FILE_PATH_WIN if BaseUtil.check_win_os() else BaseUtil.get_mac_user_path()
