import sys
import os
import datetime
import socket

from fs_base.const.app_constants import AppConstants


class CommonUtil:

    @staticmethod
    def get_resource_path(relative_path):
        """
        获取资源路径，处理打包后的路径问题（兼容Nuitka和PyInstaller）。
        """
        # 处理Nuitka单文件模式
        if "NUITKA_ONEFILE_PARENT" in os.environ:
            application_path = os.environ["NUITKA_ONEFILE_PARENT"]
        # 处理PyInstaller打包的情况
        elif getattr(sys, 'frozen', False):
            # PyInstaller的单文件模式使用_MEIPASS，多文件模式使用executable的目录
            application_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        # 非打包环境
        else:
            application_path = os.path.dirname(sys.argv[0])
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
        return CommonUtil.get_resource_path(AppConstants.APP_ICON_FULL_PATH)

    @staticmethod
    def get_mini_ico_full_path():
        return CommonUtil.get_resource_path(AppConstants.APP_MINI_ICON_FULL_PATH)

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
        app_ini_path = os.path.join(CommonUtil.get_external_path(), AppConstants.EXTERNAL_APP_INI_FILE)
        if os.path.exists(app_ini_path):
            return app_ini_path
        return CommonUtil.get_resource_path(AppConstants.APP_INI_FILE)

    @staticmethod
    def get_external_path() -> str:
        return AppConstants.SAVE_FILE_PATH_WIN if CommonUtil.check_win_os() else CommonUtil.get_mac_user_path()
