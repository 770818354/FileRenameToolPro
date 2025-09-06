#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版主题系统 - 软件风格
提供更现代化和专业的界面样式
"""

import os
import sys
from ui.qt_adapter import QApplication, Signal, QPalette, QColor
from ui.qt_adapter import QWidget as QObject
from enum import Enum


def get_resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发环境和打包环境"""
    try:
        # PyInstaller打包后的临时目录
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境
        base_path = os.path.abspath(".")
    
    full_path = os.path.join(base_path, relative_path)
    # 转换为Qt兼容的路径格式
    return full_path.replace("\\", "/")


class ThemeMode(Enum):
    """主题模式枚举"""
    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"  # 新增蓝色专业主题


class EnhancedThemeManager(QObject):
    """增强版主题管理器"""
    
    theme_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.current_theme = ThemeMode.LIGHT
        
    def set_theme(self, theme_mode: ThemeMode):
        """设置主题"""
        self.current_theme = theme_mode
        
        if theme_mode == ThemeMode.BLUE:
            self._apply_blue_theme()
        else:
            self._apply_light_theme()  # 默认使用亮色主题
        
        self.theme_changed.emit(theme_mode.value)
    
    def toggle_theme(self):
        """循环切换主题"""
        themes = [ThemeMode.LIGHT, ThemeMode.BLUE]  # 移除DARK主题
        current_index = themes.index(self.current_theme)
        next_index = (current_index + 1) % len(themes)
        self.set_theme(themes[next_index])
    
    def _apply_light_theme(self):
        """应用亮色主题"""
        app = QApplication.instance()
        if app:
            checkmark_path = get_resource_path("static/对勾1.png")
            stylesheet = self.get_light_stylesheet().replace("{checkmark_path}", checkmark_path)
            app.setStyleSheet(stylesheet)
    
    def _apply_dark_theme(self):
        """应用暗色主题"""
        app = QApplication.instance()
        if app:
            checkmark_path = get_resource_path("static/对勾1.png")
            stylesheet = self.get_dark_stylesheet().replace("{checkmark_path}", checkmark_path)
            app.setStyleSheet(stylesheet)
            
    def _apply_blue_theme(self):
        """应用蓝色专业主题"""
        app = QApplication.instance()
        if app:
            checkmark_path = get_resource_path("static/对勾1.png")
            stylesheet = self.get_blue_stylesheet().replace("{checkmark_path}", checkmark_path)
            app.setStyleSheet(stylesheet)
    
    def get_light_stylesheet(self) -> str:
        """获取亮色主题样式表"""
        return """
        /* 亮色主题 - 风格 */
        QMainWindow {
            background-color: #f8f9fa;
            color: #2c3e50;
            font-family: "Microsoft YaHei UI", "Segoe UI", Arial, sans-serif;
        }
        
        /* 工具栏样式 */
        QToolBar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f0f0f0);
            border: none;
            border-bottom: 1px solid #d0d0d0;
            padding: 6px;
            spacing: 4px;
        }
        
        QToolButton {
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 6px;
            padding: 8px 16px;
            margin: 2px;
            font-weight: 500;
            font-size: 13px;
            min-width: 80px;
        }
        
        QToolButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #e3f2fd, stop:1 #bbdefb);
            border-color: #2196f3;
            color: #1976d2;
        }
        
        QToolButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #bbdefb, stop:1 #90caf9);
        }
        
        QToolButton:checked {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2196f3, stop:1 #1976d2);
            color: white;
            border-color: #fff;
        }
        
        /* 按钮样式 - 风格 */
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4fc3f7, stop:1 #29b6f6);
            color: white;
            border: 1px solid #0288d1;
            border-radius: 6px;
            padding: 10px 24px;
            font-weight: 500;
            font-size: 13px;
            min-width: 100px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #29b6f6, stop:1 #0288d1);
            border-color: #0277bd;
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0288d1, stop:1 #0277bd);
        }
        
        QPushButton:disabled {
            background: #bdbdbd;
            color: #757575;
            border-color: #9e9e9e;
        }
        
        QPushButton.secondary {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f5f5f5);
            color: #424242;
            border: 1px solid #d0d0d0;
        }
        
        QPushButton.secondary:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f5f5f5, stop:1 #eeeeee);
            border-color: #bdbdbd;
        }
        
        QPushButton.danger {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f44336, stop:1 #d32f2f);
            border-color: #c62828;
        }
        
        QPushButton.danger:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #d32f2f, stop:1 #c62828);
        }
        
        QPushButton.success {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4caf50, stop:1 #388e3c);
            border-color: #2e7d32;
        }
        
        /* 表格样式 - 增强版 */
        QTableWidget {
            background-color: white;
            alternate-background-color: #f8f9fa;
            gridline-color: #e0e0e0;
            border: 1px solid #d0d0d0;
            border-radius: 8px;
            selection-background-color: #e3f2fd;
            font-size: 13px;
        }
        
        QTableWidget::item {
            padding: 12px 8px;
            border: none;
            border-bottom: 1px solid #f0f0f0;
        }
        
        QTableWidget::item:selected {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #e3f2fd, stop:1 #bbdefb);
            color: #1976d2;
        }
        
        QTableWidget::item:hover {
            background-color: #f5f5f5;
        }
        
        QHeaderView::section {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #fafafa, stop:1 #f0f0f0);
            color: #424242;
            padding: 12px 8px;
            border: none;
            border-right: 1px solid #e0e0e0;
            border-bottom: 1px solid #d0d0d0;
            font-weight: 600;
            font-size: 13px;
        }
        
        QHeaderView::section:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f0f0f0, stop:1 #e8e8e8);
        }
        
        /* 输入框样式 - 现代化 */
        QLineEdit {
            background-color: white;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            padding: 10px 12px;
            font-size: 13px;
            selection-background-color: #2196f3;
        }
        
        QLineEdit:focus {
            border-color: #2196f3;
            outline: none;
            box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
        }
        
        QLineEdit:hover {
            border-color: #bdbdbd;
        }
        
        QTextEdit {
            background-color: white;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            padding: 8px;
            font-family: "Consolas", "Monaco", "Courier New", monospace;
            font-size: 13px;
            selection-background-color: #2196f3;
        }
        
        QTextEdit:focus {
            border-color: #2196f3;
            box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
        }
        
        /* 组合框样式 */
        QComboBox {
            background-color: white;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
            min-width: 120px;
        }
        
        QComboBox:focus {
            border-color: #2196f3;
        }
        
        QComboBox:hover {
            border-color: #bdbdbd;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 30px;
        }
        
        QComboBox::down-arrow {
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iIzQyNDI0MiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
            width: 12px;
            height: 8px;
        }
        
        QComboBox QAbstractItemView {
            background-color: white;
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 4px;
            selection-background-color: #e3f2fd;
        }
        
        QComboBox QAbstractItemView::item {
            padding: 8px 12px;
            border-radius: 4px;
            min-height: 20px;
        }
        
        QComboBox QAbstractItemView::item:hover {
            background-color: #f5f5f5;
        }
        
        QComboBox QAbstractItemView::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        
        /* 复选框样式 */
        QCheckBox {
            spacing: 8px;
            font-size: 13px;
            color: #424242;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 1px solid #bdbdbd;
            border-radius: 18px;
            background-color: white;
        }
        
        QCheckBox::indicator:hover {
            border-color: #2196f3;
            background-color: #f8f9fa;
        }
        
        QCheckBox::indicator:checked {
            background-color: #fff;
            border-color: #fff;
            image: url({checkmark_path});
        }
        
        /* 单选框样式 */
        QRadioButton {
            spacing: 8px;
            font-size: 13px;
            color: #424242;
        }
        
        QRadioButton::indicator {
            width: 18px;
            height: 18px;
            border: 1px solid #bdbdbd;
            border-radius: 18px;
            background-color: white;
        }
        
        QRadioButton::indicator:hover {
            border-color: #2196f3;
            background-color: #f8f9fa;
        }
        
        QRadioButton::indicator:checked {
            background-color: #fff;
            border-color: #fff;
            image: url({checkmark_path});
        }
        
        /* 分组框样式 - 卡片风格 */
        QGroupBox {
            font-weight: 600;
            font-size: 14px;
            color: #424242;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-top: 16px;
            padding-top: 16px;
            background-color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 16px;
            padding: 0 8px;
            background-color: white;
            color: #1976d2;
        }
        
        /* 滚动条样式 */
        QScrollBar:vertical {
            background-color: #f5f5f5;
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }
        
        QScrollBar::handle:vertical {
            background-color: #bdbdbd;
            border-radius: 6px;
            min-height: 30px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #9e9e9e;
        }
        
        QScrollBar::handle:vertical:pressed {
            background-color: #757575;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
            height: 0;
        }
        
        /* 状态栏样式 */
        QStatusBar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f8f9fa);
            border-top: 1px solid #e0e0e0;
            color: #666666;
            font-size: 12px;
        }
        
        /* 进度条样式 */
        QProgressBar {
            border: none;
            border-radius: 8px;
            background-color: #e0e0e0;
            text-align: center;
            font-weight: 500;
            font-size: 12px;
            height: 20px;
        }
        
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4fc3f7, stop:1 #29b6f6);
            border-radius: 8px;
        }
        
        /* 菜单样式 */
        QMenuBar {
            background-color: #ffffff;
            border-bottom: 1px solid #e0e0e0;
            font-size: 13px;
        }
        
        QMenuBar::item {
            padding: 8px 16px;
            background-color: transparent;
            color: #424242;
        }
        
        QMenuBar::item:hover {
            background-color: #f5f5f5;
            color: #1976d2;
        }
        
        QMenu {
            background-color: white;
            border: 1px solid #d0d0d0;
            border-radius: 8px;
            padding: 6px;
        }
        
        QMenu::item {
            padding: 8px 20px;
            border-radius: 4px;
            font-size: 13px;
        }
        
        QMenu::item:hover {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        
        QMenu::separator {
            height: 1px;
            background-color: #e0e0e0;
            margin: 4px 0;
        }
        """
    
    def get_blue_stylesheet(self) -> str:
        """获取蓝色专业主题样式表"""
        return """
        /* 蓝色专业主题 - 我很会养猪丶开发版 */
        QMainWindow {
            background-color: #f0f4f8;
            color: #1a365d;
            font-family: "Microsoft YaHei UI", "Segoe UI", Arial, sans-serif;
        }
        
        /* 工具栏 - 我很会养猪丶开发蓝色风格 */
        QToolBar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3182ce, stop:1 #2c5282);
            border: none;
            padding: 8px;
            spacing: 6px;
        }
        
        QToolButton {
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 6px;
            padding: 10px 18px;
            margin: 2px;
            font-weight: 500;
            font-size: 13px;
            color: white;
            min-width: 90px;
        }
        
        QToolButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4299e1, stop:1 #3182ce);
            border-color: #63b3ed;
        }
        
        QToolButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2c5282, stop:1 #2a4365);
        }
        
        QToolButton:checked {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #63b3ed, stop:1 #4299e1);
            border-color: #90cdf4;
        }
        
        /* 按钮 - 专业蓝色系 */
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4299e1, stop:1 #3182ce);
            color: white;
            border: 1px solid #2c5282;
            border-radius: 6px;
            padding: 12px 28px;
            font-weight: 600;
            font-size: 13px;
            min-width: 110px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3182ce, stop:1 #2c5282);
            border-color: #2a4365;
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2c5282, stop:1 #2a4365);
        }
        
        QPushButton.secondary {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #edf2f7, stop:1 #e2e8f0);
            color: #2d3748;
            border: 1px solid #cbd5e0;
        }
        
        QPushButton.secondary:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #e2e8f0, stop:1 #cbd5e0);
        }
        
        /* 表格 - 专业风格 */
        QTableWidget {
            background-color: white;
            alternate-background-color: #f7fafc;
            gridline-color: #e2e8f0;
            border: 2px solid #cbd5e0;
            border-radius: 8px;
            selection-background-color: #bee3f8;
            font-size: 13px;
        }
        
        QTableWidget::item {
            padding: 14px 10px;
            border: none;
            border-bottom: 1px solid #f1f5f9;
        }
        
        QTableWidget::item:selected {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #bee3f8, stop:1 #90cdf4);
            color: #1a365d;
        }
        
        QHeaderView::section {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4a5568, stop:1 #2d3748);
            color: white;
            padding: 14px 10px;
            border: none;
            border-right: 1px solid #718096;
            font-weight: 600;
            font-size: 13px;
        }
        
        QHeaderView::section:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #718096, stop:1 #4a5568);
        }
        
        /* 输入框 - 专业样式 */
        QLineEdit {
            background-color: white;
            border: 2px solid #e2e8f0;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 13px;
            selection-background-color: #3182ce;
        }
        
        QLineEdit:focus {
            border-color: #3182ce;
            box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1);
        }
        
        /* 复选框样式 - 专业蓝色 */
        QCheckBox {
            spacing: 8px;
            font-size: 13px;
            color: #2d3748;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #cbd5e0;
            border-radius: 4px;
            background-color: white;
        }
        
        QCheckBox::indicator:hover {
            border-color: #FFF;
            background-color: #f7fafc;
        }
        
        QCheckBox::indicator:checked {
            background-color: #FFF;
            border-color: #FFF;
            image: url({checkmark_path});
        }
        
        /* 单选框样式 - 专业蓝色 */
        QRadioButton {
            spacing: 8px;
            font-size: 13px;
            color: #2d3748;
        }
        
        QRadioButton::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #cbd5e0;
            border-radius: 9px;
            background-color: white;
        }
        
        QRadioButton::indicator:hover {
            border-color: #3182ce;
            background-color: #f7fafc;
        }
        
        QRadioButton::indicator:checked {
            background-color: #fff;
            border-color: #fff;
            image: url({checkmark_path});
        }
        
        /* 分组框 - 专业卡片 */
        QGroupBox {
            font-weight: 600;
            font-size: 14px;
            color: #2d3748;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            margin-top: 18px;
            padding-top: 18px;
            background-color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 20px;
            padding: 0 12px;
            background-color: white;
            color: #3182ce;
            font-weight: 700;
        }
        
        /* 状态栏 */
        QStatusBar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #edf2f7, stop:1 #e2e8f0);
            border-top: 2px solid #cbd5e0;
            color: #4a5568;
            font-size: 12px;
            font-weight: 500;
        }
        """
    
    def get_dark_stylesheet(self) -> str:
        """获取暗色主题样式表"""
        return """
        /* 暗色主题 - 现代化风格 */
        QMainWindow {
            background-color: #1a1a1a;
            color: #ffffff;
            font-family: "Microsoft YaHei UI", "Segoe UI", Arial, sans-serif;
        }
        
        /* 工具栏 - 暗色风格 */
        QToolBar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2d2d2d, stop:1 #1e1e1e);
            border: none;
            border-bottom: 1px solid #404040;
            padding: 8px;
            spacing: 6px;
        }
        
        QToolButton {
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 6px;
            padding: 10px 18px;
            margin: 2px;
            font-weight: 500;
            font-size: 13px;
            color: #ffffff;
            min-width: 90px;
        }
        
        QToolButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #404040, stop:1 #353535);
            border-color: #555555;
            color: #64b5f6;
        }
        
        QToolButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #353535, stop:1 #2a2a2a);
        }
        
        QToolButton:checked {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1976d2, stop:1 #1565c0);
            border-color: ##94c86c;
        }
        
        /* 按钮 - 暗色系 */
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1976d2, stop:1 #1565c0);
            color: white;
            border: 1px solid #1565c0;
            border-radius: 6px;
            padding: 12px 28px;
            font-weight: 600;
            font-size: 13px;
            min-width: 110px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1565c0, stop:1 #0d47a1);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0d47a1, stop:1 #0a3d62);
        }
        
        QPushButton.secondary {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2d2d2d, stop:1 #1e1e1e);
            color: #ffffff;
            border: 1px solid #404040;
        }
        
        QPushButton.secondary:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #404040, stop:1 #2d2d2d);
        }
        
        /* 表格 - 暗色风格 */
        QTableWidget {
            background-color: #2d2d2d;
            alternate-background-color: #353535;
            gridline-color: #404040;
            border: 2px solid #404040;
            border-radius: 8px;
            selection-background-color: #1e3a5f;
            color: #ffffff;
            font-size: 13px;
        }
        
        QTableWidget::item {
            padding: 14px 10px;
            border: none;
            border-bottom: 1px solid #404040;
        }
        
        QTableWidget::item:selected {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1e3a5f, stop:1 #1a2f4a);
            color: #64b5f6;
        }
        
        QHeaderView::section {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #404040, stop:1 #2d2d2d);
            color: #ffffff;
            padding: 14px 10px;
            border: none;
            border-right: 1px solid #555555;
            font-weight: 600;
            font-size: 13px;
        }
        
        QHeaderView::section:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #555555, stop:1 #404040);
        }
        
        /* 输入框 - 暗色样式 */
        QLineEdit {
            background-color: #2d2d2d;
            border: 2px solid #404040;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 13px;
            color: #ffffff;
            selection-background-color: #1976d2;
        }
        
        QLineEdit:focus {
            border-color: #1976d2;
            box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.2);
        }
        
        /* 复选框样式 - 暗色 */
        QCheckBox {
            spacing: 8px;
            font-size: 13px;
            color: #ffffff;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #666666;
            border-radius: 4px;
            background-color: #2d2d2d;
        }
        
        QCheckBox::indicator:hover {
            border-color: #64b5f6;
            background-color: #404040;
        }
        
        QCheckBox::indicator:checked {
            background-color: #1976d2;
            border-color: #1976d2;
            image: url({checkmark_path});
        }
        
        /* 单选框样式 - 暗色 */
        QRadioButton {
            spacing: 8px;
            font-size: 13px;
            color: #ffffff;
        }
        
        QRadioButton::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #666666;
            border-radius: 9px;
            background-color: #2d2d2d;
        }
        
        QRadioButton::indicator:hover {
            border-color: #64b5f6;
            background-color: #404040;
        }
        
        QRadioButton::indicator:checked {
            background-color: #1976d2;
            border-color: #1976d2;
            image: url({checkmark_path});
        }
        
        /* 分组框 - 暗色卡片 */
        QGroupBox {
            font-weight: 600;
            font-size: 14px;
            color: #ffffff;
            border: 2px solid #404040;
            border-radius: 10px;
            margin-top: 18px;
            padding-top: 18px;
            background-color: #2d2d2d;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 20px;
            padding: 0 12px;
            background-color: #2d2d2d;
            color: #64b5f6;
            font-weight: 700;
        }
        
        /* 状态栏 */
        QStatusBar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2d2d2d, stop:1 #1e1e1e);
            border-top: 2px solid #404040;
            color: #b0b0b0;
            font-size: 12px;
            font-weight: 500;
        }
        """


# 全局增强主题管理器实例（延迟初始化）
enhanced_theme_manager = None

def get_enhanced_theme_manager():
    """获取增强主题管理器实例（延迟初始化）"""
    global enhanced_theme_manager
    if enhanced_theme_manager is None:
        enhanced_theme_manager = EnhancedThemeManager()
    return enhanced_theme_manager
