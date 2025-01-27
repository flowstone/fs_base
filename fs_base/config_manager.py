from PySide6.QtCore import QObject, Signal

from loguru import logger

from fs_base.app_ini_util import AppIniUtil
from fs_base.const.app_constants import AppConstants


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
    # 配置更新信号
    config_updated = Signal(str, object)

    def __init__(self):
        super().__init__()
        logger.info("Config Manager初始化")
        # 初始化配置，可以动态扩展
        self.default_config = AppConstants.DEFAULT_CONFIG.copy()

    def load_config(self):
        """
        加载配置文件，返回字典形式的配置
        """
        config = {}
        for key in self.default_config.keys():
            config[key] = AppIniUtil.get_ini_app_param(key)
        return config

    def save_config(self, key, value):
        """
        保存配置，并发出配置更新信号
        """
        if key in self.default_config:
            logger.info(f"保存配置：{key} = {value}")
            AppIniUtil.set_ini_app_param(key, value)
            self.config_updated.emit(key, value)
        else:
            logger.warning(f"尝试保存未注册的配置项: {key}")

    def get_config(self, key):
        """
        根据键获取配置
        """
        if key in self.default_config:
            return AppIniUtil.get_ini_app_param(key)
        else:
            logger.warning(f"未注册的配置项: {key}")
            return None

    def set_config(self, key, value):
        """
        设置配置值，并保存
        """
        self.save_config(key, value)