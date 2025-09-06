#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qt适配器模块 - 支持PyQt6和PySide6
"""

import sys

# 尝试导入PyQt6，如果失败则使用PySide6
try:
    from PyQt6.QtCore import Qt, QThread, pyqtSignal as Signal, QTimer
    from PyQt6.QtGui import QIcon, QAction, QFont, QPixmap, QPalette, QColor
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
        QFormLayout, QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox, QGroupBox,
        QSpinBox, QTextEdit, QTabWidget, QScrollArea, QFrame, QSplitter,
        QMessageBox, QButtonGroup, QRadioButton, QTableWidget, QTableWidgetItem,
        QFileDialog, QHeaderView, QAbstractItemView, QProgressBar, QProgressDialog,
        QDialog, QDialogButtonBox, QMenuBar, QToolBar, QStatusBar, QMenu
    )
    
    QT_BACKEND = "PyQt6"
    print(f"使用GUI后端: {QT_BACKEND}")
    
except ImportError:
    try:
        from PySide6.QtCore import Qt, QThread, Signal, QTimer
        from PySide6.QtGui import QIcon, QAction, QFont, QPixmap, QPalette, QColor
        from PySide6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
            QFormLayout, QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox, QGroupBox,
            QSpinBox, QTextEdit, QTabWidget, QScrollArea, QFrame, QSplitter,
            QMessageBox, QButtonGroup, QRadioButton, QTableWidget, QTableWidgetItem,
            QFileDialog, QHeaderView, QAbstractItemView, QProgressBar, QProgressDialog,
            QDialog, QDialogButtonBox, QMenuBar, QToolBar, QStatusBar, QMenu
        )
        
        QT_BACKEND = "PySide6"
        print(f"使用GUI后端: {QT_BACKEND}")
        
    except ImportError:
        print("错误：无法导入PyQt6或PySide6")
        print("请安装其中一个GUI框架:")
        print("pip install PyQt6")
        print("或")
        print("pip install PySide6")
        sys.exit(1)


# 导出所有需要的类和常量
__all__ = [
    'Qt', 'QThread', 'Signal', 'QTimer',
    'QIcon', 'QAction', 'QFont', 'QPixmap', 'QPalette', 'QColor',
    'QApplication', 'QMainWindow', 'QWidget', 
    'QVBoxLayout', 'QHBoxLayout', 'QGridLayout', 'QFormLayout',
    'QPushButton', 'QLabel', 'QLineEdit', 'QComboBox', 'QCheckBox', 'QGroupBox',
    'QSpinBox', 'QTextEdit', 'QTabWidget', 'QScrollArea', 'QFrame', 'QSplitter',
    'QMessageBox', 'QButtonGroup', 'QRadioButton', 'QTableWidget', 'QTableWidgetItem',
    'QFileDialog', 'QHeaderView', 'QAbstractItemView', 'QProgressBar', 'QProgressDialog',
    'QDialog', 'QDialogButtonBox', 'QMenuBar', 'QToolBar', 'QStatusBar', 'QMenu',
    'QT_BACKEND'
]
