import configparser
import os
from loguru import logger

from fs_base.base_util import BaseUtil
from fs_base.const.app_constants import AppConstants


class AppIniUtil:
    # 调试模式
    DEBUG_MODE = True

    @staticmethod
    def get_ini_config():
        """
        获取 INI 文件的配置对象，如果文件不存在或为空则初始化默认配置。
        """
        ini_path = BaseUtil.get_app_ini_path()
        config = configparser.ConfigParser(allow_no_value=True)

        if not os.path.exists(ini_path):
            logger.warning(f"INI 文件不存在，创建默认配置文件：{ini_path}")
            AppIniUtil.initialize_default_config(ini_path)
        else:
            try:
                config.read(ini_path, encoding="utf-8")
                if not config.sections():
                    logger.warning(f"INI 文件为空或无效，初始化默认配置：{ini_path}")
                    AppIniUtil.initialize_default_config(ini_path)
            except Exception as e:
                logger.error(f"加载 INI 文件失败：{e}")
                AppIniUtil.initialize_default_config(ini_path)

        return config, ini_path

    @staticmethod
    def initialize_default_config(ini_path):
        """
        初始化默认配置文件。
        """
        config = configparser.ConfigParser()
        config[AppConstants.SETTINGS_SECTION] = {
            key: str(value) for key, value in AppConstants.DEFAULT_CONFIG.items()
        }
        with open(ini_path, "w", encoding="utf-8") as f:
            config.write(f)

    @staticmethod
    def get_config_param(section: str, key: str, fallback=None, as_type: any = str):
        """
        通用方法，从 INI 文件中读取指定的配置项。
        """
        config, _ = AppIniUtil.get_ini_config()
        try:
            if as_type == bool:
                return config.getboolean(section, key, fallback=fallback)
            elif as_type == int:
                return config.getint(section, key, fallback=fallback)
            elif as_type == float:
                return config.getfloat(section, key, fallback=fallback)
            elif as_type == str or as_type is None:
                return config.get(section, key, fallback=fallback)
            else:
                raise ValueError(f"不支持的类型：{as_type}")
        except Exception as e:
            if AppIniUtil.DEBUG_MODE:
                logger.error(f"读取配置失败：[Section: {section}] [Key: {key}] - 错误：{e}")
            return fallback

    @staticmethod
    def set_config_param(section: str, key: str, value: any):
        """
        通用方法，更新 INI 文件中的指定配置项。
        """
        config, ini_path = AppIniUtil.get_ini_config()
        AppIniUtil.update_ini_line(ini_path, section, key, value)
        if AppIniUtil.DEBUG_MODE:
            logger.info(f"更新配置：[Section: {section}] [Key: {key}] = {value}")

    @staticmethod
    def get_ini_app_param(key: str):
        """
        获取应用程序配置项的值。
        """
        if key in AppConstants.DEFAULT_CONFIG:
            return AppIniUtil.get_config_param(
                AppConstants.SETTINGS_SECTION,
                key,
                fallback=AppConstants.DEFAULT_CONFIG[key],
                as_type=AppConstants.CONFIG_TYPES[key]
            )
        else:
            logger.warning(f"未注册的配置项: {key}")
            return None

    @staticmethod
    def set_ini_app_param(key: str, value: any):
        """
        设置应用程序配置项的值。
        """
        if key in AppConstants.DEFAULT_CONFIG:
            if AppConstants.CONFIG_TYPES[key] == bool:
                value = "true" if value else "false"
            AppIniUtil.set_config_param(AppConstants.SETTINGS_SECTION, key, str(value))
        else:
            logger.warning(f"未注册的配置项: {key}")

    @staticmethod
    def update_ini_line(ini_path, section, key, value):
        """
        修改 INI 文件中的指定配置项，仅修改目标行，保留注释和空行。
        """
        if not os.path.exists(ini_path):
            raise FileNotFoundError(f"配置文件 {ini_path} 不存在！")

        with open(ini_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        updated = False
        in_section = False
        section_header = f"[{section}]"
        new_line = f"{key} = {value}\n"

        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line == section_header:
                in_section = True
                continue

            if in_section:
                # 更新目标键
                if stripped_line.startswith(f"{key} =") or stripped_line.startswith(f"{key}\t"):
                    lines[i] = new_line
                    updated = True
                    break

                # 检测到新节，停止更新
                if stripped_line.startswith("[") and stripped_line != section_header:
                    break

        # 如果没有更新目标键，则添加新键值
        if not updated:
            if in_section:
                lines.append(new_line)
            else:
                lines.append(f"\n{section_header}\n{new_line}")

        with open(ini_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    @staticmethod
    def reset_config():
        """
        重置配置为默认值。
        """
        _, ini_path = AppIniUtil.get_ini_config()
        AppIniUtil.initialize_default_config(ini_path)
        if AppIniUtil.DEBUG_MODE:
            logger.info("配置已重置为默认值。")