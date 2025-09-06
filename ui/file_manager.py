#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版文件管理器 
提供更丰富的文件管理功能和更好的用户体验
"""

import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict

from ui.qt_adapter import (
    Qt, QThread, Signal, QTimer, QIcon, QPixmap, QFont,
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox, QGroupBox,
    QFileDialog, QHeaderView, QAbstractItemView, QSplitter, QFrame,
    QProgressBar, QMessageBox, QMenu, QAction
)

from core.rename_engine import RenameEngine, FileItem


class EnhancedFileTableWidget(QTableWidget):
    """增强版文件表格组件 - 风格"""
    
    def __init__(self):
        super().__init__()
        self.setup_table()
        self.setup_context_menu()
        
    def setup_table(self):
        """设置表格"""
        # 设置列
        headers = ["状态", "原文件名", "新文件名", "类型", "大小", "修改时间", "路径"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # 设置表格属性
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSortingEnabled(True)
        self.setShowGrid(False)  # 隐藏网格线，更现代化
        
        # 设置列宽
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # 状态列固定宽度
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # 原文件名
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # 新文件名拉伸
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # 类型固定
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # 大小
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # 时间
        
        # 设置列宽度
        self.setColumnWidth(0, 60)   # 状态列
        self.setColumnWidth(3, 80)   # 类型列
        
        # 设置行高
        self.verticalHeader().setDefaultSectionSize(36)
        self.verticalHeader().setVisible(False)
        
    def setup_context_menu(self):
        """设置右键菜单"""
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def show_context_menu(self, position):
        """显示右键菜单"""
        if self.itemAt(position) is None:
            return
            
        menu = QMenu(self)
        
        # 复制文件名
        copy_action = QAction("复制文件名", self)
        copy_action.triggered.connect(self.copy_filename)
        menu.addAction(copy_action)
        
        # 复制路径
        copy_path_action = QAction("复制完整路径", self)
        copy_path_action.triggered.connect(self.copy_filepath)
        menu.addAction(copy_path_action)
        
        menu.addSeparator()
        
        # 在资源管理器中显示
        show_action = QAction("在资源管理器中显示", self)
        show_action.triggered.connect(self.show_in_explorer)
        menu.addAction(show_action)
        
        menu.exec(self.mapToGlobal(position))
    
    def copy_filename(self):
        """复制文件名到剪贴板"""
        current_row = self.currentRow()
        if current_row >= 0:
            filename = self.item(current_row, 1).text()
            from ui.qt_adapter import QApplication
            QApplication.clipboard().setText(filename)
    
    def copy_filepath(self):
        """复制完整路径到剪贴板"""
        current_row = self.currentRow()
        if current_row >= 0:
            path = self.item(current_row, 6).text()
            from ui.qt_adapter import QApplication
            QApplication.clipboard().setText(path)
    
    def show_in_explorer(self):
        """在资源管理器中显示文件"""
        current_row = self.currentRow()
        if current_row >= 0:
            path = self.item(current_row, 6).text()
            os.startfile(os.path.dirname(path))
    
    def load_files(self, files: List[FileItem]):
        """加载文件到表格"""
        self.setRowCount(len(files))
        
        for row, file_item in enumerate(files):
            # 状态图标
            status_item = QTableWidgetItem()
            status_item.setData(Qt.ItemDataRole.UserRole, file_item)
            status_item.setText(self._get_status_icon(file_item.status))
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 0, status_item)
            
            # 原文件名
            original_item = QTableWidgetItem(file_item.original_name)
            if file_item.is_directory:
                font = QFont()
                font.setBold(True)
                original_item.setFont(font)
                original_item.setIcon(self._get_folder_icon())
            else:
                original_item.setIcon(self._get_file_icon(file_item.extension))
            self.setItem(row, 1, original_item)
            
            # 新文件名
            new_name_item = QTableWidgetItem(file_item.new_name)
            if file_item.new_name != file_item.original_name:
                font = QFont()
                font.setBold(True)
                new_name_item.setFont(font)
                # 设置颜色表示有变化
                new_name_item.setForeground(self._get_change_color())
            self.setItem(row, 2, new_name_item)
            
            # 文件类型
            file_type = "文件夹" if file_item.is_directory else file_item.extension.upper().lstrip('.')
            type_item = QTableWidgetItem(file_type)
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 3, type_item)
            
            # 文件大小
            size_text = self._format_file_size(file_item.size) if not file_item.is_directory else "-"
            size_item = QTableWidgetItem(size_text)
            size_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.setItem(row, 4, size_item)
            
            # 修改时间
            time_text = file_item.modified_date.strftime("%Y/%m/%d %H:%M")
            time_item = QTableWidgetItem(time_text)
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 5, time_item)
            
            # 文件路径
            path_item = QTableWidgetItem(str(file_item.original_path))
            self.setItem(row, 6, path_item)
            
            # 设置状态背景色
            self._set_row_status_color(row, file_item.status)
    
    def _get_status_icon(self, status: str) -> str:
        """获取状态图标"""
        status_icons = {
            "ready": "●",
            "renamed": "✓",
            "error": "✗",
            "skipped": "○",
            "conflict": "⚠"
        }
        return status_icons.get(status, "●")
    
    def _get_change_color(self):
        """获取变更颜色"""
        from ui.qt_adapter import QColor
        return QColor("#1976d2")  # 蓝色表示有变化
    
    def _set_row_status_color(self, row: int, status: str):
        """设置行状态背景色"""
        from ui.qt_adapter import QColor
        
        color_map = {
            "ready": QColor(255, 255, 255, 0),      # 透明
            "renamed": QColor(76, 175, 80, 30),     # 浅绿色
            "error": QColor(244, 67, 54, 30),       # 浅红色
            "skipped": QColor(255, 193, 7, 30),     # 浅黄色
            "conflict": QColor(255, 152, 0, 30)     # 浅橙色
        }
        
        color = color_map.get(status, QColor(255, 255, 255, 0))
        
        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item:
                item.setBackground(color)
    
    def _get_file_icon(self, extension: str) -> QIcon:
        """根据文件扩展名获取图标"""
        # 可以根据扩展名返回不同的图标
        return QIcon()
    
    def _get_folder_icon(self) -> QIcon:
        """获取文件夹图标"""
        return QIcon()
    
    def _format_file_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"


class EnhancedFileFilterWidget(QWidget):
    """增强版文件筛选器 - 更多筛选选项"""
    
    filter_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 第一行：基本筛选
        basic_layout = QHBoxLayout()
        
        # 文件类型筛选
        self.type_label = QLabel("文件类型:")
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "所有文件",
            "图片文件 (*.jpg;*.png;*.gif;*.bmp;*.tiff)",
            "文档文件 (*.txt;*.doc;*.docx;*.pdf;*.rtf)",
            "音频文件 (*.mp3;*.wav;*.flac;*.aac;*.ogg)",
            "视频文件 (*.mp4;*.avi;*.mkv;*.mov;*.wmv)",
            "压缩文件 (*.zip;*.rar;*.7z;*.tar)",
            "可执行文件 (*.exe;*.msi;*.bat)",
            "自定义..."
        ])
        self.type_combo.currentTextChanged.connect(self.filter_changed.emit)
        
        # 包含选项
        self.include_subdirs_cb = QCheckBox("包含子目录")
        self.include_subdirs_cb.toggled.connect(self.filter_changed.emit)
        
        self.show_hidden_cb = QCheckBox("显示隐藏文件")
        self.show_hidden_cb.toggled.connect(self.filter_changed.emit)
        
        self.include_folders_cb = QCheckBox("包含文件夹")
        self.include_folders_cb.setChecked(True)
        self.include_folders_cb.toggled.connect(self.filter_changed.emit)
        
        basic_layout.addWidget(self.type_label)
        basic_layout.addWidget(self.type_combo)
        basic_layout.addWidget(self.include_subdirs_cb)
        basic_layout.addWidget(self.show_hidden_cb)
        basic_layout.addWidget(self.include_folders_cb)
        basic_layout.addStretch()
        
        # 第二行：高级筛选
        advanced_layout = QHBoxLayout()
        
        # 文件大小筛选
        self.size_label = QLabel("文件大小:")
        self.size_combo = QComboBox()
        self.size_combo.addItems([
            "不限制",
            "小于 1MB",
            "1MB - 10MB",
            "10MB - 100MB",
            "大于 100MB"
        ])
        self.size_combo.currentTextChanged.connect(self.filter_changed.emit)
        
        # 修改时间筛选
        self.time_label = QLabel("修改时间:")
        self.time_combo = QComboBox()
        self.time_combo.addItems([
            "不限制",
            "今天",
            "最近一周",
            "最近一月",
            "最近一年"
        ])
        self.time_combo.currentTextChanged.connect(self.filter_changed.emit)
        
        # 文件名筛选
        self.name_label = QLabel("文件名包含:")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("输入要筛选的文件名关键词...")
        self.name_edit.textChanged.connect(self.filter_changed.emit)
        
        advanced_layout.addWidget(self.size_label)
        advanced_layout.addWidget(self.size_combo)
        advanced_layout.addWidget(self.time_label)
        advanced_layout.addWidget(self.time_combo)
        advanced_layout.addWidget(self.name_label)
        advanced_layout.addWidget(self.name_edit)
        advanced_layout.addStretch()
        
        layout.addLayout(basic_layout)
        layout.addLayout(advanced_layout)
    
    def get_file_filters(self) -> List[str]:
        """获取当前文件筛选器"""
        current_text = self.type_combo.currentText()
        
        if "所有文件" in current_text:
            return None  # None表示不过滤，显示所有文件
        elif "图片文件" in current_text:
            return ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        elif "文档文件" in current_text:
            return ['.txt', '.doc', '.docx', '.pdf', '.rtf', '.odt', '.xls', '.xlsx']
        elif "音频文件" in current_text:
            return ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma']
        elif "视频文件" in current_text:
            return ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
        elif "压缩文件" in current_text:
            return ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2']
        elif "可执行文件" in current_text:
            return ['.exe', '.msi', '.bat', '.cmd', '.com']
        else:
            return None  # 默认不过滤
    
    def get_filter_options(self) -> Dict:
        """获取所有筛选选项"""
        return {
            'file_types': self.get_file_filters(),
            'include_subdirs': self.include_subdirs_cb.isChecked(),
            'show_hidden': self.show_hidden_cb.isChecked(),
            'include_folders': self.include_folders_cb.isChecked(),
            'size_filter': self.size_combo.currentText(),
            'time_filter': self.time_combo.currentText(),
            'name_filter': self.name_edit.text().strip()
        }


class EnhancedFileManagerWidget(QWidget):
    """增强版文件管理器主组件"""
    
    files_loaded = Signal(list)
    selection_changed = Signal(list)
    
    def __init__(self):
        super().__init__()
        self.current_directory = None
        self.files = []
        self.load_thread = None
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # 目录选择区域
        dir_group = QGroupBox("文件夹选择")
        dir_layout = QVBoxLayout(dir_group)
        
        # 路径输入行
        path_layout = QHBoxLayout()
        
        self.dir_edit = QLineEdit()
        self.dir_edit.setPlaceholderText("请选择要重命名的文件夹...")
        self.dir_edit.setReadOnly(True)
        
        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.clicked.connect(self.browse_directory)
        
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.refresh_files)
        self.refresh_btn.setEnabled(False)
        
        # 快捷路径按钮
        self.desktop_btn = QPushButton("桌面")
        self.desktop_btn.clicked.connect(lambda: self.load_quick_path("Desktop"))
        
        self.documents_btn = QPushButton("文档")
        self.documents_btn.clicked.connect(lambda: self.load_quick_path("Documents"))
        
        self.downloads_btn = QPushButton("下载")
        self.downloads_btn.clicked.connect(lambda: self.load_quick_path("Downloads"))
        
        path_layout.addWidget(self.dir_edit)
        path_layout.addWidget(self.browse_btn)
        path_layout.addWidget(self.refresh_btn)
        path_layout.addWidget(self.desktop_btn)
        path_layout.addWidget(self.documents_btn)
        path_layout.addWidget(self.downloads_btn)
        
        dir_layout.addLayout(path_layout)
        
        # 筛选器
        self.filter_widget = EnhancedFileFilterWidget()
        self.filter_widget.filter_changed.connect(self.refresh_files)
        
        # 文件列表区域
        list_group = QGroupBox("文件列表")
        list_layout = QVBoxLayout(list_group)
        
        # 统计信息和操作栏
        stats_layout = QHBoxLayout()
        
        self.stats_label = QLabel("未选择目录")
        
        # 操作按钮
        self.select_all_btn = QPushButton("全选")
        self.select_all_btn.clicked.connect(self.select_all_files)
        self.select_all_btn.setEnabled(False)
        
        self.select_none_btn = QPushButton("取消全选")
        self.select_none_btn.clicked.connect(self.select_no_files)
        self.select_none_btn.setEnabled(False)
        
        self.invert_selection_btn = QPushButton("反选")
        self.invert_selection_btn.clicked.connect(self.invert_selection)
        self.invert_selection_btn.setEnabled(False)
        
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.select_all_btn)
        stats_layout.addWidget(self.select_none_btn)
        stats_layout.addWidget(self.invert_selection_btn)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # 文件表格
        self.file_table = EnhancedFileTableWidget()
        self.file_table.itemSelectionChanged.connect(self.on_selection_changed)
        
        list_layout.addLayout(stats_layout)
        list_layout.addWidget(self.progress_bar)
        list_layout.addWidget(self.file_table)
        
        # 添加到主布局
        layout.addWidget(dir_group)
        layout.addWidget(self.filter_widget)
        layout.addWidget(list_group)
        
    def load_quick_path(self, folder_name: str):
        """加载快捷路径"""
        try:
            from pathlib import Path
            if folder_name == "Desktop":
                path = Path.home() / "Desktop"
            elif folder_name == "Documents":
                path = Path.home() / "Documents"
            elif folder_name == "Downloads":
                path = Path.home() / "Downloads"
            else:
                return
                
            if path.exists():
                self.load_directory(str(path))
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法访问{folder_name}文件夹: {str(e)}")
    
    def browse_directory(self):
        """浏览选择目录"""
        directory = QFileDialog.getExistingDirectory(
            self, "选择要重命名的文件夹", 
            str(Path.home())
        )
        
        if directory:
            self.load_directory(directory)
    
    def load_directory(self, directory_path: str):
        """加载目录"""
        self.current_directory = Path(directory_path)
        self.dir_edit.setText(directory_path)
        self.refresh_btn.setEnabled(True)
        
        # 启用选择按钮
        self.select_all_btn.setEnabled(True)
        self.select_none_btn.setEnabled(True)
        self.invert_selection_btn.setEnabled(True)
        
        # 开始加载文件
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        # 这里应该创建加载线程，简化版本直接加载
        self.load_files_sync()
    
    def load_files_sync(self):
        """同步加载文件（简化版本）"""
        try:
            engine = RenameEngine()
            filter_options = self.filter_widget.get_filter_options()
            
            files = engine.load_directory(
                str(self.current_directory),
                filter_options['include_subdirs'],
                filter_options['file_types']
            )
            
            # 应用其他筛选器
            filtered_files = self.apply_additional_filters(files, filter_options)
            
            self.on_files_loaded(filtered_files)
            
        except Exception as e:
            self.on_load_error(str(e))
    
    def apply_additional_filters(self, files: List[FileItem], options: Dict) -> List[FileItem]:
        """应用额外的筛选器"""
        filtered_files = []
        
        for file_item in files:
            # 文件夹筛选
            if file_item.is_directory and not options['include_folders']:
                continue
                
            # 隐藏文件筛选
            if file_item.original_name.startswith('.') and not options['show_hidden']:
                continue
                
            # 文件名筛选
            if options['name_filter'] and options['name_filter'].lower() not in file_item.original_name.lower():
                continue
                
            # 文件大小筛选
            if not self.check_size_filter(file_item, options['size_filter']):
                continue
                
            # 时间筛选
            if not self.check_time_filter(file_item, options['time_filter']):
                continue
                
            filtered_files.append(file_item)
        
        return filtered_files
    
    def check_size_filter(self, file_item: FileItem, size_filter: str) -> bool:
        """检查文件大小筛选"""
        if size_filter == "不限制" or file_item.is_directory:
            return True
            
        size_mb = file_item.size / (1024 * 1024)
        
        if size_filter == "小于 1MB":
            return size_mb < 1
        elif size_filter == "1MB - 10MB":
            return 1 <= size_mb <= 10
        elif size_filter == "10MB - 100MB":
            return 10 <= size_mb <= 100
        elif size_filter == "大于 100MB":
            return size_mb > 100
            
        return True
    
    def check_time_filter(self, file_item: FileItem, time_filter: str) -> bool:
        """检查时间筛选"""
        if time_filter == "不限制":
            return True
            
        from datetime import datetime, timedelta
        now = datetime.now()
        file_time = file_item.modified_date
        
        if time_filter == "今天":
            return file_time.date() == now.date()
        elif time_filter == "最近一周":
            return file_time >= now - timedelta(days=7)
        elif time_filter == "最近一月":
            return file_time >= now - timedelta(days=30)
        elif time_filter == "最近一年":
            return file_time >= now - timedelta(days=365)
            
        return True
    
    def refresh_files(self):
        """刷新文件列表"""
        if self.current_directory:
            self.load_files_sync()
    
    def select_all_files(self):
        """全选文件"""
        self.file_table.selectAll()
    
    def select_no_files(self):
        """取消全选"""
        self.file_table.clearSelection()
    
    def invert_selection(self):
        """反选"""
        selection_model = self.file_table.selectionModel()
        for row in range(self.file_table.rowCount()):
            index = self.file_table.model().index(row, 0)
            if selection_model.isRowSelected(row, index.parent()):
                selection_model.select(index, selection_model.SelectionFlag.Deselect | selection_model.SelectionFlag.Rows)
            else:
                selection_model.select(index, selection_model.SelectionFlag.Select | selection_model.SelectionFlag.Rows)
    
    def on_files_loaded(self, files: List[FileItem]):
        """文件加载完成处理"""
        self.progress_bar.setVisible(False)
        self.files = files
        
        # 更新表格
        self.file_table.load_files(files)
        
        # 更新统计信息
        total_files = len([f for f in files if not f.is_directory])
        total_dirs = len([f for f in files if f.is_directory])
        
        if total_dirs > 0:
            self.stats_label.setText(f"共 {len(files)} 项 ({total_files} 个文件, {total_dirs} 个文件夹)")
        else:
            self.stats_label.setText(f"共 {total_files} 个文件")
        
        # 发出信号
        self.files_loaded.emit(files)
    
    def on_load_error(self, error_message: str):
        """文件加载错误处理"""
        self.progress_bar.setVisible(False)
        QMessageBox.warning(self, "加载错误", f"加载文件时发生错误:\n{error_message}")
    
    def on_selection_changed(self):
        """选择变更处理"""
        selected_rows = set()
        for item in self.file_table.selectedItems():
            selected_rows.add(item.row())
        
        selected_files = []
        for row in selected_rows:
            item = self.file_table.item(row, 0)
            if item:
                file_item = item.data(Qt.ItemDataRole.UserRole)
                if file_item:
                    selected_files.append(file_item)
        
        self.selection_changed.emit(selected_files)
    
    def update_preview(self, files: List[FileItem]):
        """更新预览"""
        self.files = files
        self.file_table.load_files(files)
        
        # 更新统计信息
        will_rename = sum(1 for f in files if f.new_name != f.original_name and f.status != "conflict")
        conflicts = sum(1 for f in files if f.status == "conflict")
        
        status_text = f"共 {len(files)} 项"
        if will_rename > 0:
            status_text += f", ✅ {will_rename} 项将重命名"
        if conflicts > 0:
            status_text += f", ⚠️ {conflicts} 项冲突"
        
        self.stats_label.setText(status_text)
    
    def get_files(self) -> List[FileItem]:
        """获取当前文件列表"""
        return self.files
    
    def get_selected_files(self) -> List[FileItem]:
        """获取选中的文件列表"""
        selected_files = []
        for item in self.file_table.selectedItems():
            if item.column() == 0:
                file_item = item.data(Qt.ItemDataRole.UserRole)
                if file_item:
                    selected_files.append(file_item)
        return selected_files
    
    def refresh_preview(self):
        """刷新预览"""
        if self.files:
            self.file_table.load_files(self.files)
