#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
我很会养猪丶开发版主窗口 - 软件风格
提供更丰富的功能和更好的用户体验
"""

import sys
from pathlib import Path
from typing import List

from ui.qt_adapter import (
    Qt, QTimer, Signal, QIcon, QAction, QFont, QPixmap,
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QToolBar, QStatusBar, QPushButton, QLabel, QMessageBox,
    QProgressDialog, QDialog, QDialogButtonBox, QTextEdit, QGroupBox,
    QApplication, QTabWidget, QFrame
)

from core.rename_engine import RenameEngine, FileItem
from ui.file_manager import EnhancedFileManagerWidget
from ui.rule_panels import RulePanelsWidget, ClearFilenamePanel
from ui.themes import get_enhanced_theme_manager, ThemeMode


class WelcomeWidget(QWidget):
    """欢迎界面组件"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """设置欢迎界面"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 标题
        title_label = QLabel("🚀 批量文件重命名工具")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #1976d2; margin: 20px;")
        
        # 副标题
        subtitle_label = QLabel("我很会养猪丶开发版-我很会养猪丶")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #666; margin: 20px;")
        
        # 功能介绍
        features_label = QLabel("""
        9种重命名模式，实时预览效果，支持一键撤销，支持大量文件的快速处理
        """)
        subtitle_font.setPointSize(8)
        features_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        features_label.setStyleSheet("color: #424242; line-height: 1.8; margin: 20px;")
        
        # 开始使用提示
        start_label = QLabel("点击左上角的\"主工作区\"按钮开始使用")
        start_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        start_font = QFont()
        start_font.setPointSize(12)
        start_font.setBold(True)
        start_label.setFont(start_font)
        start_label.setStyleSheet("color: #1976d2; margin: 20px;")
        
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(features_label)
        layout.addWidget(start_label)


class EnhancedPreviewDialog(QDialog):
    """增强版预览对话框"""
    
    def __init__(self, parent=None, summary=None, files=None):
        super().__init__(parent)
        self.summary = summary or {}
        self.files = files or []
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        self.setWindowTitle("重命名预览")
        self.setModal(True)
        self.resize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # 摘要信息
        summary_group = QGroupBox("操作摘要")
        summary_layout = QVBoxLayout(summary_group)
        
        total = self.summary.get('total_files', 0)
        will_rename = self.summary.get('will_rename', 0)
        conflicts = self.summary.get('conflicts', 0)
        unchanged = self.summary.get('unchanged', 0)
        
        summary_text = f"""
        总文件数: {total}
        将被重命名: {will_rename}
        名称冲突: {conflicts}
        ⏸保持不变: {unchanged}
        """
        
        summary_label = QLabel(summary_text)
        summary_font = QFont()
        summary_font.setPointSize(12)
        summary_label.setFont(summary_font)
        summary_layout.addWidget(summary_label)
        
        if conflicts > 0:
            warning_label = QLabel("⚠️ 检测到名称冲突，冲突的文件将被跳过")
            warning_label.setStyleSheet("color: #ff9800; font-weight: bold; font-size: 14px;")
            summary_layout.addWidget(warning_label)
        
        layout.addWidget(summary_group)
        
        # 详细预览列表（如果有文件信息）
        if self.files:
            preview_group = QGroupBox("详细预览")
            preview_layout = QVBoxLayout(preview_group)
            
            preview_text = QTextEdit()
            preview_text.setReadOnly(True)
            preview_text.setMaximumHeight(200)
            
            preview_content = ""
            for file_item in self.files[:50]:  # 只显示前50个
                if file_item.new_name != file_item.original_name:
                    status_icon = "⚠️" if file_item.status == "conflict" else "✅"
                    preview_content += f"{status_icon} {file_item.original_name} → {file_item.new_name}\n"
            
            if len(self.files) > 50:
                preview_content += f"\n... 还有 {len(self.files) - 50} 个文件"
            
            preview_text.setText(preview_content)
            preview_layout.addWidget(preview_text)
            layout.addWidget(preview_group)
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setText("执行重命名")
        ok_button.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setText("取消")
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)


class EnhancedAboutDialog(QDialog):
    """增强版关于对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        self.setWindowTitle("关于")
        self.setModal(True)
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # 应用图标和标题
        header_layout = QHBoxLayout()
        
        # 这里可以添加应用图标
        icon_label = QLabel("🚀")
        icon_label.setStyleSheet("font-size: 48px;")
        
        title_layout = QVBoxLayout()
        app_label = QLabel("批量文件重命名工具")
        app_label.setFont(QFont("", 18, QFont.Weight.Bold))
        
        version_label = QLabel("版本 1.0.0 (我很会养猪丶开发版)")
        version_label.setStyleSheet("color: #666;")
        
        title_layout.addWidget(app_label)
        title_layout.addWidget(version_label)
        
        header_layout.addWidget(icon_label)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # 详细信息
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setHtml("""
        <div style="font-family: 'Microsoft YaHei UI'; line-height: 1.6;">
        <h3 style="color: #1976d2;">产品特性</h3>
        <ul>
            <li><strong>多种重命名模式</strong>：文本替换、添加序号、正则表达式等9种模式</li>
            <li><strong>实时预览功能</strong>：所见即所得，重命名前即可看到效果</li>
            <li><strong>安全操作保障</strong>：支持一键撤销，避免误操作风险</li>
            <li><strong>智能文件筛选</strong>：按类型、大小、时间等多维度筛选</li>
            <li><strong>现代化界面</strong>：支持多主题，界面美观易用</li>
            <li><strong>高性能处理</strong>：支持大量文件的快速处理</li>
        </ul>
        
        <h3 style="color: #1976d2;">🛠️ 技术架构</h3>
        <ul>
            <li><strong>开发语言</strong>：Python 3.8+</li>
            <li><strong>GUI框架</strong>：PySide6 / PyQt6</li>
            <li><strong>架构模式</strong>：MVC 分层架构</li>
            <li><strong>支持平台</strong>：Windows, macOS, Linux</li>
        </ul>
        
        <h3 style="color: #1976d2;">📞 技术支持</h3>
        <p>如遇问题请联系技术支持或查看帮助文档</p>
        
        <hr style="margin: 20px 0; border: 1px solid #eee;">
        <p style="text-align: center; color: #666; font-size: 12px;">
            © 2025 批量文件重命名工具 | MIT License
        </p>
        </div>
        """)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        
        layout.addLayout(header_layout)
        layout.addWidget(info_text)
        layout.addWidget(button_box)


class EnhancedMainWindow(QMainWindow):
    """增强版主窗口"""
    
    def __init__(self):
        super().__init__()
        self.rename_engine = RenameEngine()
        self.current_files = []
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """设置界面"""
        self.setWindowTitle("🚀 批量文件重命名工具 - 我很会养猪丶开发版")
        self.setMinimumSize(1400, 900)
        
        # 应用增强主题
        get_enhanced_theme_manager().set_theme(ThemeMode.LIGHT)
        
        # 先创建中央组件
        self.create_central_widget()
        
        # 创建菜单栏和工具栏
        self.create_menu_bar()
        self.create_toolbar()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 居中显示
        self.center_window()
        
        # 连接信号
        self.connect_signals()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")
        
        open_action = QAction("打开文件夹(&O)", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.file_manager.browse_directory)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # 导入导出功能
        import_action = QAction("导入规则(&I)", self)
        import_action.triggered.connect(self.import_rules)
        file_menu.addAction(import_action)
        
        export_action = QAction("导出规则(&E)", self)
        export_action.triggered.connect(self.export_rules)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("编辑(&E)")
        
        self.undo_action = QAction("撤销重命名(&U)", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.setEnabled(False)
        self.undo_action.triggered.connect(self.undo_rename)
        edit_menu.addAction(self.undo_action)
        
        edit_menu.addSeparator()
        
        clear_rules_action = QAction("清空规则(&C)", self)
        clear_rules_action.triggered.connect(self.rule_panels.clear_rules)
        edit_menu.addAction(clear_rules_action)
        
        # 视图菜单
        view_menu = menubar.addMenu("视图(&V)")
        
        self.theme_action = QAction("切换主题(&T)", self)
        self.theme_action.setShortcut("Ctrl+T")
        self.theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(self.theme_action)
        
        # 工具菜单
        tools_menu = menubar.addMenu("工具(&T)")
        
        batch_action = QAction("批处理模式(&B)", self)
        batch_action.triggered.connect(self.show_batch_mode)
        tools_menu.addAction(batch_action)
        
        settings_action = QAction("设置(&S)", self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")
        
        help_action = QAction("使用帮助(&H)", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = self.addToolBar("主工具栏")
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        
        # 文件操作
        open_action = QAction("打开文件夹", self)
        open_action.triggered.connect(self.file_manager.browse_directory)
        toolbar.addAction(open_action)
        
        refresh_action = QAction("刷新文件列表", self)
        refresh_action.triggered.connect(self.refresh_file_list)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        # 预览和执行
        self.preview_action = QAction("预览效果", self)
        self.preview_action.setEnabled(False)
        self.preview_action.triggered.connect(self.preview_rename)
        toolbar.addAction(self.preview_action)
        
        self.execute_action = QAction("执行重命名", self)
        self.execute_action.setEnabled(False)
        self.execute_action.triggered.connect(self.execute_rename)
        toolbar.addAction(self.execute_action)
        
        toolbar.addSeparator()
        
        # 撤销
        self.undo_toolbar_action = QAction("撤销", self)
        self.undo_toolbar_action.setEnabled(False)
        self.undo_toolbar_action.triggered.connect(self.undo_rename)
        toolbar.addAction(self.undo_toolbar_action)
        
        toolbar.addSeparator()
        
        # 工具
        theme_action = QAction("主题", self)
        theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(theme_action)
        
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)
    
    def create_central_widget(self):
        """创建中央组件"""
        # 创建标签页容器
        self.tab_widget = QTabWidget()
        
        # 主工作区标签页
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：文件管理器
        self.file_manager = EnhancedFileManagerWidget()
        self.file_manager.setMinimumWidth(700)
        
        # 右侧：规则面板标签页
        self.right_tab_widget = QTabWidget()
        self.right_tab_widget.setMinimumWidth(400)
        self.right_tab_widget.setMaximumWidth(500)
        
        # 规则面板
        self.rule_panels = RulePanelsWidget()
        self.right_tab_widget.addTab(self.rule_panels, "重命名规则")
        
        # 清空文件名面板
        self.clear_filename_panel = ClearFilenamePanel()
        self.right_tab_widget.addTab(self.clear_filename_panel, "清空文件名")
        
        splitter.addWidget(self.file_manager)
        splitter.addWidget(self.right_tab_widget)
        
        # 设置分割器比例
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        
        # 添加标签页
        self.tab_widget.addTab(main_widget, "主工作区")
        
        # 欢迎页面
        welcome_widget = WelcomeWidget()
        self.tab_widget.addTab(welcome_widget, "欢迎")
        
        # 设置中央组件
        self.setCentralWidget(self.tab_widget)
        
        # 默认显示欢迎页面
        self.tab_widget.setCurrentIndex(1)
    
    def create_status_bar(self):
        """创建状态栏"""
        status_bar = self.statusBar()
        
        # 状态标签
        self.status_label = QLabel("🎉 欢迎使用批量文件重命名工具")
        status_bar.addWidget(self.status_label)
        
        # 文件计数标签
        self.file_count_label = QLabel("")
        status_bar.addPermanentWidget(self.file_count_label)
        
        # 主题标签
        self.theme_label = QLabel("亮色主题")
        status_bar.addPermanentWidget(self.theme_label)
        
        # 版本标签
        version_label = QLabel("v1.0.0")
        status_bar.addPermanentWidget(version_label)
    
    def setup_connections(self):
        """设置信号连接"""
        # 文件管理器信号
        self.file_manager.files_loaded.connect(self.on_files_loaded)
        self.file_manager.selection_changed.connect(self.on_selection_changed)
        
        # 规则面板信号
        self.rule_panels.rules_changed.connect(self.on_rules_changed)
        
        # 主题管理器信号
        get_enhanced_theme_manager().theme_changed.connect(self.on_theme_changed)
    
    def center_window(self):
        """窗口居中"""
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            window_geometry = self.frameGeometry()
            center_point = screen_geometry.center()
            window_geometry.moveCenter(center_point)
            self.move(window_geometry.topLeft())
    
    def on_files_loaded(self, files: List[FileItem]):
        """文件加载完成处理"""
        self.current_files = files
        self.rename_engine.files = files
        
        # 切换到主工作区
        self.tab_widget.setCurrentIndex(0)
        
        # 更新界面状态
        has_files = len(files) > 0
        self.preview_action.setEnabled(has_files)
        self.execute_action.setEnabled(False)
        
        # 更新状态栏
        self.file_count_label.setText(f"{len(files)} 个文件")
        self.status_label.setText(f"✅ 已加载 {len(files)} 个文件")
        
        # 清空规则引擎
        self.rename_engine.clear_rules()
    
    def on_selection_changed(self, selected_files: List[FileItem]):
        """选择变更处理"""
        count = len(selected_files)
        if count > 0:
            self.status_label.setText(f"已选择 {count} 个文件")
        else:
            self.status_label.setText("准备就绪")
    
    def on_rules_changed(self):
        """规则变更处理"""
        if not self.rename_engine.files:
            return
        
        rules = self.rule_panels.get_rules()
        
        if not rules:
            # 重置文件名
            for file_item in self.rename_engine.files:
                file_item.new_name = file_item.original_name
                file_item.status = "ready"
            self.file_manager.update_preview(self.rename_engine.files)
            self.update_execute_button_state()
            return
        
        # 应用规则
        self.rename_engine.clear_rules()
        for rule in rules:
            self.rename_engine.add_rule(rule)
        
        try:
            preview_files = self.rename_engine.preview_rename()
            self.file_manager.update_preview(preview_files)
            
            # 更新按钮状态
            self.update_execute_button_state()
            
            # 更新状态
            summary = self.rename_engine.get_rename_preview_summary()
            if summary['conflicts'] > 0:
                self.status_label.setText(f"⚠️ 预览完成 - {summary['conflicts']} 个冲突")
            elif summary['will_rename'] > 0:
                self.status_label.setText(f"✅ 预览完成 - {summary['will_rename']} 个文件将重命名")
            else:
                self.status_label.setText("预览完成 - 无文件需要重命名")
                
        except Exception as e:
            QMessageBox.warning(self, "规则错误", f"应用规则时出错：{str(e)}")
            self.update_execute_button_state()
            self.status_label.setText("❌ 预览失败")
    
    def preview_rename(self):
        """预览重命名"""
        if not self.current_files:
            QMessageBox.information(self, "提示", "请先选择要重命名的文件夹")
            return
        
        rules = self.rule_panels.get_rules()
        if not rules:
            QMessageBox.information(self, "提示", "请先设置重命名规则")
            return
        
        summary = self.rename_engine.get_rename_preview_summary()
        dialog = EnhancedPreviewDialog(self, summary, self.current_files)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.execute_rename()
    
    def execute_rename(self):
        """执行重命名"""
        if not self.rename_engine.files:
            QMessageBox.information(self, "提示", "请先选择文件夹！")
            return
        
        summary = self.rename_engine.get_rename_preview_summary()
        
        if summary['will_rename'] == 0:
            QMessageBox.information(self, "提示", "没有文件需要重命名")
            return
        
        # 确认对话框
        reply = QMessageBox.question(
            self, "确认重命名",
            f"确定要重命名 {summary['will_rename']} 个文件吗？\n\n"
            f"此操作将修改文件名，建议先备份重要文件。\n"
            f"程序支持一步撤销功能。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # 进度对话框
        progress = QProgressDialog("正在重命名文件...", "取消", 0, 0, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.show()
        
        try:
            success_count, error_count, error_messages = self.rename_engine.execute_rename()
            progress.close()
            
            # 刷新文件列表以确保与实际文件系统同步
            self.rename_engine.refresh_file_list()
            
            # 更新界面
            self.file_manager.update_preview(self.rename_engine.files)
            
            # 更新按钮状态
            self.update_execute_button_state()
            
            # 启用撤销
            self.undo_action.setEnabled(True)
            self.undo_toolbar_action.setEnabled(True)
            
            # 显示结果
            if error_count == 0:
                QMessageBox.information(
                    self, "🎉 重命名完成",
                    f"成功重命名了 {success_count} 个文件！\n\n"
                    f"如需撤销，可使用撤销功能。"
                )
                self.status_label.setText(f"🎉 重命名完成 - {success_count} 个文件")
            else:
                error_text = "\n".join(error_messages[:10])
                if len(error_messages) > 10:
                    error_text += f"\n... 还有 {len(error_messages) - 10} 个错误"
                
                QMessageBox.warning(
                    self, "⚠️ 重命名完成（有错误）",
                    f"✅ 成功重命名: {success_count} 个文件\n"
                    f"❌ 失败: {error_count} 个文件\n\n"
                    f"错误详情:\n{error_text}"
                )
                self.status_label.setText(f"⚠️ 重命名完成 - {success_count} 成功, {error_count} 失败")
        
        except Exception as e:
            progress.close()
            QMessageBox.critical(self, "❌ 重命名错误", f"重命名过程中发生错误:\n{str(e)}")
            self.status_label.setText("❌ 重命名失败")
    
    def undo_rename(self):
        """撤销重命名"""
        if not self.rename_engine.history:
            QMessageBox.information(self, "提示", "没有可撤销的操作")
            return
        
        reply = QMessageBox.question(
            self, "确认撤销",
            "确定要撤销上一次重命名操作吗？\n\n"
            "这将恢复所有文件的原始名称。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        try:
            success, message = self.rename_engine.undo_last_rename()
            
            if success:
                QMessageBox.information(self, "✅ 撤销成功", message)
                self.status_label.setText("✅ 撤销完成")
                self.file_manager.refresh_files()
                
                if not self.rename_engine.history:
                    self.undo_action.setEnabled(False)
                    self.undo_toolbar_action.setEnabled(False)
            else:
                QMessageBox.warning(self, "⚠️ 撤销失败", message)
                self.status_label.setText("⚠️ 撤销失败")
                
        except Exception as e:
            QMessageBox.critical(self, "❌ 撤销错误", f"撤销过程中发生错误:\n{str(e)}")
    
    def toggle_theme(self):
        """切换主题"""
        get_enhanced_theme_manager().toggle_theme()
    
    def on_theme_changed(self, theme_name: str):
        """主题变更处理"""
        theme_names = {
            "light": "亮色主题",
            "blue": "专业主题"
        }
        self.theme_label.setText(theme_names.get(theme_name, "亮色主题"))
    
    def import_rules(self):
        """导入规则"""
        QMessageBox.information(self, "功能开发中", "规则导入功能正在开发中，敬请期待！")
    
    def export_rules(self):
        """导出规则"""
        QMessageBox.information(self, "功能开发中", "规则导出功能正在开发中，敬请期待！")
    
    def show_batch_mode(self):
        """显示批处理模式"""
        QMessageBox.information(self, "功能开发中", "批处理模式正在开发中，敬请期待！")
    
    def show_settings(self):
        """显示设置"""
        QMessageBox.information(self, "功能开发中", "设置功能正在开发中，敬请期待！")
    
    def show_help(self):
        """显示帮助"""
        QMessageBox.information(self, "使用帮助", 
                               "详细使用说明请参考项目文档中的《快速开始.md》文件。\n\n"
                               "主要步骤：\n"
                               "1. 选择文件夹\n"
                               "2. 设置重命名规则\n"
                               "3. 预览效果\n"
                               "4. 执行重命名")
    
    def show_about(self):
        """显示关于对话框"""
        dialog = EnhancedAboutDialog(self)
        dialog.exec()
    
    def connect_signals(self):
        """连接信号"""
        # 连接清空文件名面板的信号
        self.clear_filename_panel.clear_requested.connect(self.on_clear_filenames)
        self.clear_filename_panel.generate_requested.connect(self.on_generate_filenames)
        
        # 连接文件管理器的信号
        self.file_manager.files_loaded.connect(self.on_files_loaded)
        self.file_manager.selection_changed.connect(self.on_selection_changed)
        
    
    def on_clear_filenames(self):
        """清空文件名"""
        if not self.rename_engine.files:
            QMessageBox.information(self, "提示", "请先选择文件夹！")
            return
        
        reply = QMessageBox.question(
            self, "确认清空", 
            f"确定要清空 {len(self.rename_engine.files)} 个文件的文件名吗？\n\n此操作将保留文件扩展名。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.rename_engine.clear_all_filenames()
            self.file_manager.refresh_preview()
            self.update_status("已清空所有文件名")
            # 更新执行按钮状态
            self.update_execute_button_state()
    
    def on_generate_filenames(self, template: str, start_number: int, step: int, padding: int):
        """生成新文件名"""
        if not self.rename_engine.files:
            QMessageBox.information(self, "提示", "请先选择文件夹！")
            return
        
        try:
            self.rename_engine.generate_new_filenames(template, start_number, step, padding)
            self.file_manager.refresh_preview()
            self.update_status(f"已根据模板生成新文件名: {template}")
            # 更新执行按钮状态
            self.update_execute_button_state()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成文件名时出错：{str(e)}")
    
    def on_files_loaded(self, files: List[FileItem]):
        """文件加载完成"""
        self.current_files = files
        self.rename_engine.files = files
        self.update_status(f"已加载 {len(files)} 个文件")
        # 更新执行按钮状态
        self.update_execute_button_state()
    
    def on_selection_changed(self, selected_files: List[FileItem]):
        """选择改变"""
        self.update_status(f"已选择 {len(selected_files)} 个文件")
    
    
    def update_status(self, message: str):
        """更新状态栏"""
        if hasattr(self, 'status_bar'):
            self.status_bar.showMessage(message, 3000)  # 显示3秒
    
    def update_execute_button_state(self):
        """更新执行重命名按钮状态"""
        if not hasattr(self, 'execute_action') or not self.rename_engine.files:
            return
        
        # 检查是否有文件需要重命名
        has_changes = any(
            f.new_name != f.original_name and f.status != "conflict" 
            for f in self.rename_engine.files
        )
        
        self.execute_action.setEnabled(has_changes)
        
        # 同时更新预览按钮状态
        if hasattr(self, 'preview_action'):
            self.preview_action.setEnabled(has_changes)
    
    def refresh_file_list(self):
        """刷新文件列表"""
        if not self.rename_engine.files:
            QMessageBox.information(self, "提示", "请先选择文件夹！")
            return
        
        # 刷新文件列表
        self.rename_engine.refresh_file_list()
        
        # 更新界面显示
        self.file_manager.refresh_preview()
        
        # 更新按钮状态
        self.update_execute_button_state()
        
        # 更新状态栏
        self.update_status("文件列表已刷新")
    
    def closeEvent(self, event):
        """关闭事件"""
        reply = QMessageBox.question(
            self, "确认退出",
            "确定要退出批量文件重命名工具吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
