class FsConstants:
    """
    ---------------------
    宽度为0 高度为0,则表示窗口【宽高】由组件们决定
    ---------------------
    """
    # 主窗口相关常量
    APP_WINDOW_TITLE = "FSBase"
    VERSION = "0.1.0"
    COPYRIGHT_INFO = f"© 2025 {APP_WINDOW_TITLE}"

    # 悬浮球相关常量
    APP_MINI_SIZE = 80
    APP_MINI_WINDOW_TITLE = ""

    # 共用的常量，应用图标
    APP_ICON_FULL_PATH = "resources/images/app.ico"
    APP_MINI_ICON_FULL_PATH = "resources/images/app_mini.ico"
    APP_BAR_ICON_FULL_PATH = "resources/images/app_bar.ico"
    AUTHOR_MAIL = "xueyao.me@gmail.com"
    AUTHOR_BLOG = "https://blog.xueyao.tech"
    AUTHOR_GITHUB = "https://github.com/flowstone"
    PROJECT_ADDRESS = "https://github.com/flowstone/FSBase"
    BASE_QSS_PATH = "resources/qss/base.qss"

    # 保存文件路径
    SAVE_FILE_PATH_WIN = "C:\\FSBase\\"
    SAVE_FILE_PATH_MAC = "~/FSBase/"
    EXTERNAL_APP_INI_FILE = "app.ini"

    APP_INI_FILE = "app.ini"
    FONT_FILE_PATH = "resources/fonts/AlimamaFangYuanTiVF-Thin.ttf"


    ################### INI设置 #####################

    # INI 文件配置节名称
    SETTINGS_SECTION = "Settings"

    # 配置键名
    APP_MINI_MASK_CHECKED_KEY = "mini.mask_checked"
    APP_MINI_BREATHING_LIGHT_CHECKED_KEY = "mini.breathing_light_checked"
    APP_MINI_CHECKED_KEY = "mini.checked"
    APP_MINI_SIZE_KEY = "mini.size"
    APP_MINI_IMAGE_KEY = "mini.image"
    APP_TRAY_MENU_CHECKED_KEY = "tray_menu.checked"
    APP_TRAY_MENU_IMAGE_KEY = "tray_menu.image"

    # 默认值
    DEFAULT_CONFIG = {
        APP_MINI_MASK_CHECKED_KEY: True,
        APP_MINI_BREATHING_LIGHT_CHECKED_KEY: True,
        APP_MINI_CHECKED_KEY: False,
        APP_MINI_SIZE_KEY: 80,
        APP_MINI_IMAGE_KEY: "",
        APP_TRAY_MENU_CHECKED_KEY: False,
        APP_TRAY_MENU_IMAGE_KEY: "",
    }

    # 类型映射
    CONFIG_TYPES = {
        APP_MINI_MASK_CHECKED_KEY: bool,
        APP_MINI_BREATHING_LIGHT_CHECKED_KEY: bool,
        APP_MINI_CHECKED_KEY: bool,
        APP_MINI_SIZE_KEY: int,
        APP_MINI_IMAGE_KEY: str,
        APP_TRAY_MENU_CHECKED_KEY: bool,
        APP_TRAY_MENU_IMAGE_KEY: str,
    }
    ################### INI设置 #####################
