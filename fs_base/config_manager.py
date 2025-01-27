from PySide6.QtCore import QObject, Signal

from loguru import logger

from fs_base.common_util import CommonUtil
from fs_base.const.fs_constants import FsConstants
from fs_base.ini_util import IniUtil


def singleton(cls):
    """
    单例装饰器，确保一个类只有一个实例
    """
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)  # 第一次调用时实例化
        return instances[cls]

    wrapper.__name__ = cls.__name__
    wrapper.__doc__ = cls.__doc__
    wrapper.__dict__.update(cls.__dict__)  # 保留类的原有属性和方法
    return wrapper


@singleton
class ConfigManager(QObject):
    """
    管理应用程序的配置，包括加载、保存、发出信号等
    """
    # 配置键常量
    APP_MINI_MASK_CHECKED_KEY = "mini_mask_checked"
    APP_MINI_BREATHING_LIGHT_CHECKED_KEY = "mini_breathing_light_checked"
    APP_MINI_CHECKED_KEY = "mini_checked"
    APP_MINI_SIZE_KEY = "mini_size"
    APP_MINI_IMAGE_KEY = "mini_image"

    APP_TRAY_MENU_CHECKED_KEY = "tray_menu_checked"
    APP_TRAY_MENU_IMAGE_KEY = "tray_menu_image"

    # 配置更新信号
    config_updated = Signal(str, object)

    def __init__(self):
        super().__init__()
        logger.info("Config Manager初始化")

    @staticmethod
    def load_config():
        """
        加载配置文件，返回字典形式的配置
        """
        ini_mini_size = IniUtil.get_ini_app_param(IniUtil.APP_MINI_SIZE_KEY)
        ini_mini_image = IniUtil.get_ini_app_param(IniUtil.APP_MINI_IMAGE_KEY)
        mini_size = ini_mini_size if IniUtil.get_ini_app_param(
            IniUtil.APP_MINI_CHECKED_KEY) else FsConstants.APP_MINI_SIZE
        mini_image = ini_mini_image if IniUtil.get_ini_app_param(
            IniUtil.APP_MINI_CHECKED_KEY) else CommonUtil.get_resource_path(FsConstants.APP_MINI_ICON_FULL_PATH)

        ini_tray_menu_image = IniUtil.get_ini_app_param(IniUtil.APP_TRAY_MENU_IMAGE_KEY)
        tray_menu_image = ini_tray_menu_image if IniUtil.get_ini_app_param(
            IniUtil.APP_TRAY_MENU_CHECKED_KEY) else CommonUtil.get_resource_path(FsConstants.APP_BAR_ICON_FULL_PATH)

        return {
            ConfigManager.APP_MINI_MASK_CHECKED_KEY: IniUtil.get_ini_app_param(IniUtil.APP_MINI_MASK_CHECKED_KEY),
            ConfigManager.APP_MINI_BREATHING_LIGHT_CHECKED_KEY: IniUtil.get_ini_app_param(
                IniUtil.APP_MINI_BREATHING_LIGHT_CHECKED_KEY),
            ConfigManager.APP_MINI_CHECKED_KEY: IniUtil.get_ini_app_param(IniUtil.APP_MINI_CHECKED_KEY),
            ConfigManager.APP_MINI_SIZE_KEY: mini_size,
            ConfigManager.APP_MINI_IMAGE_KEY: mini_image,
            ConfigManager.APP_TRAY_MENU_CHECKED_KEY: IniUtil.get_ini_app_param(IniUtil.APP_TRAY_MENU_CHECKED_KEY),
            ConfigManager.APP_TRAY_MENU_IMAGE_KEY: tray_menu_image
        }

    def save_config(self, key, value):
        """
        保存配置，并发出配置更新信号
        """
        logger.info(f"保存配置：{key} = {value}")

        # 处理不同键的保存逻辑
        key_mapping = {
            ConfigManager.APP_MINI_MASK_CHECKED_KEY: IniUtil.APP_MINI_MASK_CHECKED_KEY,
            ConfigManager.APP_MINI_BREATHING_LIGHT_CHECKED_KEY: IniUtil.APP_MINI_BREATHING_LIGHT_CHECKED_KEY,
            ConfigManager.APP_MINI_CHECKED_KEY: IniUtil.APP_MINI_CHECKED_KEY,
            ConfigManager.APP_MINI_SIZE_KEY: IniUtil.APP_MINI_SIZE_KEY,
            ConfigManager.APP_MINI_IMAGE_KEY: IniUtil.APP_MINI_IMAGE_KEY,
            ConfigManager.APP_TRAY_MENU_CHECKED_KEY: IniUtil.APP_TRAY_MENU_CHECKED_KEY,
            ConfigManager.APP_TRAY_MENU_IMAGE_KEY: IniUtil.APP_TRAY_MENU_IMAGE_KEY,
        }

        if key in key_mapping:
            IniUtil.set_ini_app_param(key_mapping[key], value)

        # 发出信号
        self.config_updated.emit(key, value)

    def get_config(self, key):
        """
        根据键获取配置
        """
        config = self.load_config()
        return config.get(key)

    def set_config(self, key, value):
        """
        设置配置值，并保存
        """
        self.save_config(key, value)
