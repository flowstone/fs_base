from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu
from loguru import logger


class BaseMenuBar:
    def __init__(self, parent):
        self.parent = parent
        self.menu_bar = QMenuBar(self.parent)
        self._menus = {}
        self._create_default_menus()
        self._extend_menus()  # 子类扩展菜单
        self._setup_menu_bar()

    def _create_default_menus(self):
        """创建默认的菜单"""
        # 创建帮助菜单
        help_menu = QMenu("帮助", self.parent)

        # 首选项菜单项
        option_action = QAction("首选项", self.parent)
        option_action.triggered.connect(self.show_option_tab)

        # 日志菜单项
        log_action = QAction("日志", self.parent)
        log_action.triggered.connect(self.show_log_window)

        # 关于菜单项
        about_action = QAction("关于", self.parent)
        about_action.triggered.connect(self.show_about_window)

        # 添加到帮助菜单
        help_menu.addAction(option_action)
        help_menu.addAction(log_action)
        help_menu.addAction(about_action)

        # 保存到菜单字典
        self._menus['help'] = help_menu

    def _extend_menus(self):
        """子类可重写此方法以添加更多菜单"""
        pass

    def _setup_menu_bar(self):
        """将所有菜单添加到菜单栏"""
        for menu_name, menu in self._menus.items():
            self.menu_bar.addMenu(menu)
        self.parent.setMenuBar(self.menu_bar)

    def show_option_tab(self):
        """显示首选项窗口，子类可重写"""
        logger.info("展示首选项窗口")

    def show_log_window(self):
        """显示日志窗口，子类可重写"""
        logger.info("展示日志窗口")

    def show_about_window(self):
        """显示关于窗口，子类可重写"""
        logger.info("展示关于窗口")
