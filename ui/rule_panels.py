#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量文件重命名工具 - 重命名规则设置面板
提供各种重命名规则的设置界面
"""

import re
from typing import List, Optional

from ui.qt_adapter import (
    Qt, Signal, QFont,
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox, QGroupBox,
    QSpinBox, QTextEdit, QTabWidget, QScrollArea, QFrame, QSplitter,
    QMessageBox, QButtonGroup, QRadioButton
)

from core.rename_engine import RenameRule, RenameMode, CaseMode


class BaseRulePanel(QWidget):
    """基础规则面板"""
    
    rule_changed = Signal()  # 规则变更信号
    
    def __init__(self, title: str, mode: RenameMode):
        super().__init__()
        self.mode = mode
        self.enabled = True
        self.setup_ui(title)
        
    def setup_ui(self, title: str):
        """设置界面"""
        layout = QVBoxLayout(self)
        
        # 标题和启用复选框
        header_layout = QHBoxLayout()
        
        self.enable_cb = QCheckBox(title)
        self.enable_cb.setChecked(True)
        self.enable_cb.setFont(QFont("", 10, QFont.Weight.Bold))
        self.enable_cb.toggled.connect(self.on_enabled_changed)
        
        header_layout.addWidget(self.enable_cb)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # 内容区域
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.setup_content()
        
        layout.addWidget(self.content_widget)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
    
    def setup_content(self):
        """设置内容区域 - 子类重写"""
        pass
    
    def on_enabled_changed(self, enabled: bool):
        """启用状态变更"""
        self.enabled = enabled
        self.content_widget.setEnabled(enabled)
        self.emit_rule_changed()
    
    def emit_rule_changed(self):
        """发射规则变更信号"""
        self.rule_changed.emit()
    
    def get_rule(self) -> Optional[RenameRule]:
        """获取规则 - 子类重写"""
        return None
    
    def set_rule(self, rule: RenameRule):
        """设置规则 - 子类重写"""
        pass


class ReplaceRulePanel(BaseRulePanel):
    """替换规则面板"""
    
    def __init__(self):
        super().__init__("文本替换", RenameMode.REPLACE)
        
    def setup_content(self):
        """设置内容区域"""
        form_layout = QFormLayout()
        self.content_layout.addLayout(form_layout)
        
        # 查找文本
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("要替换的文本...")
        self.search_edit.textChanged.connect(self.emit_rule_changed)
        form_layout.addRow("查找:", self.search_edit)
        
        # 替换文本
        self.replace_edit = QLineEdit()
        self.replace_edit.setPlaceholderText("替换为...")
        self.replace_edit.textChanged.connect(self.emit_rule_changed)
        form_layout.addRow("替换为:", self.replace_edit)
        
        # 区分大小写
        self.case_sensitive_cb = QCheckBox("区分大小写")
        self.case_sensitive_cb.setChecked(True)
        self.case_sensitive_cb.toggled.connect(self.emit_rule_changed)
        form_layout.addRow("", self.case_sensitive_cb)
    
    def get_rule(self) -> Optional[RenameRule]:
        """获取替换规则"""
        if not self.enabled or not self.search_edit.text():
            return None
            
        return RenameRule(
            mode=self.mode,
            enabled=self.enabled,
            search_text=self.search_edit.text(),
            replace_text=self.replace_edit.text(),
            case_sensitive=self.case_sensitive_cb.isChecked()
        )
    
    def set_rule(self, rule: RenameRule):
        """设置替换规则"""
        self.search_edit.setText(rule.search_text)
        self.replace_edit.setText(rule.replace_text)
        self.case_sensitive_cb.setChecked(rule.case_sensitive)
        self.enable_cb.setChecked(rule.enabled)


class AddTextRulePanel(BaseRulePanel):
    """添加文本规则面板"""
    
    def __init__(self):
        super().__init__("添加文本", RenameMode.ADD_PREFIX)
        
    def setup_content(self):
        """设置内容区域"""
        layout = QVBoxLayout()
        self.content_layout.addLayout(layout)
        
        # 位置选择
        position_group = QGroupBox("添加位置")
        position_layout = QVBoxLayout(position_group)
        
        self.position_group = QButtonGroup()
        
        self.prefix_rb = QRadioButton("文件名前")
        self.prefix_rb.setChecked(True)
        self.prefix_rb.toggled.connect(self.on_position_changed)
        
        self.suffix_rb = QRadioButton("文件名后")
        self.suffix_rb.toggled.connect(self.on_position_changed)
        
        self.position_group.addButton(self.prefix_rb, 0)
        self.position_group.addButton(self.suffix_rb, 1)
        
        position_layout.addWidget(self.prefix_rb)
        position_layout.addWidget(self.suffix_rb)
        
        # 添加文本
        form_layout = QFormLayout()
        
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("要添加的文本...")
        self.text_edit.textChanged.connect(self.emit_rule_changed)
        form_layout.addRow("文本:", self.text_edit)
        
        layout.addWidget(position_group)
        layout.addLayout(form_layout)
    
    def on_position_changed(self):
        """位置变更处理"""
        if self.prefix_rb.isChecked():
            self.mode = RenameMode.ADD_PREFIX
        else:
            self.mode = RenameMode.ADD_SUFFIX
        self.emit_rule_changed()
    
    def get_rule(self) -> Optional[RenameRule]:
        """获取添加文本规则"""
        if not self.enabled or not self.text_edit.text():
            return None
            
        return RenameRule(
            mode=self.mode,
            enabled=self.enabled,
            replace_text=self.text_edit.text()
        )
    
    def set_rule(self, rule: RenameRule):
        """设置添加文本规则"""
        self.text_edit.setText(rule.replace_text)
        if rule.mode == RenameMode.ADD_PREFIX:
            self.prefix_rb.setChecked(True)
        else:
            self.suffix_rb.setChecked(True)
        self.enable_cb.setChecked(rule.enabled)


class IndexRulePanel(BaseRulePanel):
    """序号规则面板"""
    
    def __init__(self):
        super().__init__("添加序号", RenameMode.ADD_INDEX)
        
    def setup_content(self):
        """设置内容区域"""
        form_layout = QFormLayout()
        self.content_layout.addLayout(form_layout)
        
        # 序号模板
        self.template_edit = QLineEdit()
        self.template_edit.setText("{index}")
        self.template_edit.setPlaceholderText("序号模板 (使用 {index} 作为占位符)")
        self.template_edit.textChanged.connect(self.emit_rule_changed)
        form_layout.addRow("模板:", self.template_edit)
        
        # 起始数字
        self.start_spin = QSpinBox()
        self.start_spin.setRange(0, 99999)
        self.start_spin.setValue(1)
        self.start_spin.valueChanged.connect(self.emit_rule_changed)
        form_layout.addRow("起始数字:", self.start_spin)
        
        # 步长
        self.step_spin = QSpinBox()
        self.step_spin.setRange(1, 1000)
        self.step_spin.setValue(1)
        self.step_spin.valueChanged.connect(self.emit_rule_changed)
        form_layout.addRow("步长:", self.step_spin)
        
        # 位数
        self.padding_spin = QSpinBox()
        self.padding_spin.setRange(1, 10)
        self.padding_spin.setValue(3)
        self.padding_spin.valueChanged.connect(self.emit_rule_changed)
        form_layout.addRow("位数:", self.padding_spin)
        
        # 示例
        self.example_label = QLabel()
        self.update_example()
        form_layout.addRow("示例:", self.example_label)
        
    def update_example(self):
        """更新示例"""
        try:
            template = self.template_edit.text() or "{index}"
            start = self.start_spin.value()
            padding = self.padding_spin.value()
            
            index_str = str(start).zfill(padding)
            if "{index}" in template:
                example = template.replace("{index}", index_str)
            else:
                example = template + index_str
                
            self.example_label.setText(f"photo_{example}.jpg")
        except:
            self.example_label.setText("无效模板")
    
    def get_rule(self) -> Optional[RenameRule]:
        """获取序号规则"""
        if not self.enabled:
            return None
            
        return RenameRule(
            mode=self.mode,
            enabled=self.enabled,
            replace_text=self.template_edit.text(),
            start_number=self.start_spin.value(),
            step=self.step_spin.value(),
            padding=self.padding_spin.value()
        )
    
    def set_rule(self, rule: RenameRule):
        """设置序号规则"""
        self.template_edit.setText(rule.replace_text)
        self.start_spin.setValue(rule.start_number)
        self.step_spin.setValue(rule.step)
        self.padding_spin.setValue(rule.padding)
        self.enable_cb.setChecked(rule.enabled)


class DeleteCharsRulePanel(BaseRulePanel):
    """删除字符规则面板"""
    
    def __init__(self):
        super().__init__("删除字符", RenameMode.DELETE_CHARS)
        
    def setup_content(self):
        """设置内容区域"""
        form_layout = QFormLayout()
        self.content_layout.addLayout(form_layout)
        
        # 删除位置
        self.start_spin = QSpinBox()
        self.start_spin.setRange(0, 1000)
        self.start_spin.setValue(0)
        self.start_spin.valueChanged.connect(self.emit_rule_changed)
        form_layout.addRow("开始位置:", self.start_spin)
        
        self.end_spin = QSpinBox()
        self.end_spin.setRange(1, 1000)
        self.end_spin.setValue(1)
        self.end_spin.valueChanged.connect(self.emit_rule_changed)
        form_layout.addRow("结束位置:", self.end_spin)
        
        # 说明
        info_label = QLabel("删除从开始位置到结束位置之间的字符")
        info_label.setStyleSheet("color: #666; font-size: 12px;")
        form_layout.addRow("", info_label)
    
    def get_rule(self) -> Optional[RenameRule]:
        """获取删除字符规则"""
        if not self.enabled:
            return None
            
        return RenameRule(
            mode=self.mode,
            enabled=self.enabled,
            delete_start=self.start_spin.value(),
            delete_end=self.end_spin.value()
        )
    
    def set_rule(self, rule: RenameRule):
        """设置删除字符规则"""
        self.start_spin.setValue(rule.delete_start)
        self.end_spin.setValue(rule.delete_end)
        self.enable_cb.setChecked(rule.enabled)


class CaseChangeRulePanel(BaseRulePanel):
    """大小写转换规则面板"""
    
    def __init__(self):
        super().__init__("大小写转换", RenameMode.CASE_CHANGE)
        
    def setup_content(self):
        """设置内容区域"""
        form_layout = QFormLayout()
        self.content_layout.addLayout(form_layout)
        
        # 转换模式
        self.case_combo = QComboBox()
        self.case_combo.addItems([
            "全部小写",
            "全部大写", 
            "首字母大写",
            "句首大写"
        ])
        self.case_combo.currentTextChanged.connect(self.emit_rule_changed)
        form_layout.addRow("转换模式:", self.case_combo)
    
    def get_rule(self) -> Optional[RenameRule]:
        """获取大小写转换规则"""
        if not self.enabled:
            return None
            
        case_modes = {
            "全部小写": CaseMode.LOWER,
            "全部大写": CaseMode.UPPER,
            "首字母大写": CaseMode.TITLE,
            "句首大写": CaseMode.SENTENCE
        }
        
        return RenameRule(
            mode=self.mode,
            enabled=self.enabled,
            case_mode=case_modes[self.case_combo.currentText()]
        )
    
    def set_rule(self, rule: RenameRule):
        """设置大小写转换规则"""
        case_texts = {
            CaseMode.LOWER: "全部小写",
            CaseMode.UPPER: "全部大写",
            CaseMode.TITLE: "首字母大写",
            CaseMode.SENTENCE: "句首大写"
        }
        self.case_combo.setCurrentText(case_texts[rule.case_mode])
        self.enable_cb.setChecked(rule.enabled)


class RegexRulePanel(BaseRulePanel):
    """正则表达式规则面板"""
    
    def __init__(self):
        super().__init__("正则表达式", RenameMode.REGEX)
        
    def setup_content(self):
        """设置内容区域"""
        layout = QVBoxLayout()
        self.content_layout.addLayout(layout)
        
        # 正则表达式
        form_layout = QFormLayout()
        
        self.pattern_edit = QLineEdit()
        self.pattern_edit.setPlaceholderText("正则表达式模式...")
        self.pattern_edit.textChanged.connect(self.on_pattern_changed)
        form_layout.addRow("模式:", self.pattern_edit)
        
        self.replace_edit = QLineEdit()
        self.replace_edit.setPlaceholderText("替换为...")
        self.replace_edit.textChanged.connect(self.emit_rule_changed)
        form_layout.addRow("替换为:", self.replace_edit)
        
        # 标志
        flags_layout = QHBoxLayout()
        
        self.ignore_case_cb = QCheckBox("忽略大小写")
        self.ignore_case_cb.toggled.connect(self.emit_rule_changed)
        
        self.multiline_cb = QCheckBox("多行模式")
        self.multiline_cb.toggled.connect(self.emit_rule_changed)
        
        flags_layout.addWidget(self.ignore_case_cb)
        flags_layout.addWidget(self.multiline_cb)
        flags_layout.addStretch()
        
        # 状态标签
        self.status_label = QLabel()
        
        layout.addLayout(form_layout)
        layout.addLayout(flags_layout)
        layout.addWidget(self.status_label)
        
        # 常用模式按钮
        patterns_group = QGroupBox("常用模式")
        patterns_layout = QVBoxLayout(patterns_group)
        
        common_patterns = [
            ("删除数字", r"\d+", ""),
            ("删除括号内容", r"\([^)]*\)", ""),
            ("删除方括号内容", r"\[[^\]]*\]", ""),
            ("替换空格为下划线", r"\s+", "_"),
            ("删除特殊字符", r"[^\w\s\.]", "")
        ]
        
        for name, pattern, replacement in common_patterns:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, p=pattern, r=replacement: self.set_pattern(p, r))
            patterns_layout.addWidget(btn)
        
        layout.addWidget(patterns_group)
    
    def set_pattern(self, pattern: str, replacement: str):
        """设置模式"""
        self.pattern_edit.setText(pattern)
        self.replace_edit.setText(replacement)
    
    def on_pattern_changed(self):
        """模式变更处理"""
        pattern = self.pattern_edit.text()
        
        if not pattern:
            self.status_label.setText("")
            self.emit_rule_changed()
            return
            
        try:
            re.compile(pattern)
            self.status_label.setText("✓ 正则表达式有效")
            self.status_label.setStyleSheet("color: green;")
        except re.error as e:
            self.status_label.setText(f"✗ 正则表达式错误: {e}")
            self.status_label.setStyleSheet("color: red;")
        
        self.emit_rule_changed()
    
    def get_rule(self) -> Optional[RenameRule]:
        """获取正则表达式规则"""
        if not self.enabled or not self.pattern_edit.text():
            return None
            
        flags = 0
        if self.ignore_case_cb.isChecked():
            flags |= re.IGNORECASE
        if self.multiline_cb.isChecked():
            flags |= re.MULTILINE
            
        return RenameRule(
            mode=self.mode,
            enabled=self.enabled,
            regex_pattern=self.pattern_edit.text(),
            replace_text=self.replace_edit.text(),
            regex_flags=flags
        )
    
    def set_rule(self, rule: RenameRule):
        """设置正则表达式规则"""
        self.pattern_edit.setText(rule.regex_pattern)
        self.replace_edit.setText(rule.replace_text)
        self.ignore_case_cb.setChecked(bool(rule.regex_flags & re.IGNORECASE))
        self.multiline_cb.setChecked(bool(rule.regex_flags & re.MULTILINE))
        self.enable_cb.setChecked(rule.enabled)


class ExtensionRulePanel(BaseRulePanel):
    """扩展名规则面板"""
    
    def __init__(self):
        super().__init__("修改扩展名", RenameMode.EXTENSION)
        
    def setup_content(self):
        """设置内容区域"""
        form_layout = QFormLayout()
        self.content_layout.addLayout(form_layout)
        
        # 新扩展名
        self.extension_edit = QLineEdit()
        self.extension_edit.setPlaceholderText("新扩展名 (如: .txt)")
        self.extension_edit.textChanged.connect(self.emit_rule_changed)
        form_layout.addRow("新扩展名:", self.extension_edit)
        
        # 警告
        warning_label = QLabel("⚠️ 修改扩展名可能影响文件的打开方式")
        warning_label.setStyleSheet("color: #ff9800; font-size: 12px;")
        form_layout.addRow("", warning_label)
    
    def get_rule(self) -> Optional[RenameRule]:
        """获取扩展名规则"""
        if not self.enabled or not self.extension_edit.text():
            return None
            
        return RenameRule(
            mode=self.mode,
            enabled=self.enabled,
            replace_text=self.extension_edit.text()
        )
    
    def set_rule(self, rule: RenameRule):
        """设置扩展名规则"""
        self.extension_edit.setText(rule.replace_text)
        self.enable_cb.setChecked(rule.enabled)


class DateTimeRulePanel(BaseRulePanel):
    """日期时间规则面板"""
    
    def __init__(self):
        super().__init__("添加日期时间", RenameMode.DATE_TIME)
        
    def setup_content(self):
        """设置内容区域"""
        layout = QVBoxLayout()
        self.content_layout.addLayout(layout)
        
        # 日期来源
        source_group = QGroupBox("日期来源")
        source_layout = QVBoxLayout(source_group)
        
        self.create_date_rb = QRadioButton("文件创建日期")
        self.create_date_rb.setChecked(True)
        self.create_date_rb.toggled.connect(self.emit_rule_changed)
        
        self.modify_date_rb = QRadioButton("文件修改日期")
        self.modify_date_rb.toggled.connect(self.emit_rule_changed)
        
        source_layout.addWidget(self.create_date_rb)
        source_layout.addWidget(self.modify_date_rb)
        
        # 日期格式
        form_layout = QFormLayout()
        
        self.format_combo = QComboBox()
        self.format_combo.addItems([
            "%Y%m%d - 20240101",
            "%Y-%m-%d - 2024-01-01", 
            "%Y%m%d_%H%M%S - 20240101_120000",
            "%Y-%m-%d_%H-%M-%S - 2024-01-01_12-00-00"
        ])
        self.format_combo.currentTextChanged.connect(self.emit_rule_changed)
        form_layout.addRow("格式:", self.format_combo)
        
        # 模板
        self.template_edit = QLineEdit()
        self.template_edit.setText("{date}")
        self.template_edit.setPlaceholderText("模板 (使用 {date} 作为占位符)")
        self.template_edit.textChanged.connect(self.emit_rule_changed)
        form_layout.addRow("模板:", self.template_edit)
        
        layout.addWidget(source_group)
        layout.addLayout(form_layout)
    
    def get_rule(self) -> Optional[RenameRule]:
        """获取日期时间规则"""
        if not self.enabled:
            return None
            
        # 提取日期格式
        format_text = self.format_combo.currentText()
        date_format = format_text.split(" - ")[0]
        
        return RenameRule(
            mode=self.mode,
            enabled=self.enabled,
            replace_text=self.template_edit.text(),
            date_format=date_format,
            use_create_date=self.create_date_rb.isChecked()
        )
    
    def set_rule(self, rule: RenameRule):
        """设置日期时间规则"""
        self.template_edit.setText(rule.replace_text)
        
        # 设置日期格式
        for i in range(self.format_combo.count()):
            if rule.date_format in self.format_combo.itemText(i):
                self.format_combo.setCurrentIndex(i)
                break
        
        if rule.use_create_date:
            self.create_date_rb.setChecked(True)
        else:
            self.modify_date_rb.setChecked(True)
            
        self.enable_cb.setChecked(rule.enabled)


class RulePanelsWidget(QWidget):
    """规则面板容器组件"""
    
    rules_changed = Signal()  # 规则变更信号
    
    def __init__(self):
        super().__init__()
        self.rule_panels = []
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("重命名规则")
        title_label.setFont(QFont("", 12, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # 规则容器
        rules_widget = QWidget()
        rules_layout = QVBoxLayout(rules_widget)
        rules_layout.setSpacing(10)
        
        # 创建规则面板
        self.rule_panels = [
            ReplaceRulePanel(),
            AddTextRulePanel(),
            IndexRulePanel(),
            DeleteCharsRulePanel(),
            CaseChangeRulePanel(),
            RegexRulePanel(),
            ExtensionRulePanel(),
            DateTimeRulePanel()
        ]
        
        # 连接信号
        for panel in self.rule_panels:
            panel.rule_changed.connect(self.rules_changed.emit)
            rules_layout.addWidget(panel)
        
        rules_layout.addStretch()
        
        scroll_area.setWidget(rules_widget)
        layout.addWidget(scroll_area)
        
        # 操作按钮
        buttons_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("清空规则")
        self.clear_btn.clicked.connect(self.clear_rules)
        
        self.preview_btn = QPushButton("预览效果")
        self.preview_btn.clicked.connect(self.rules_changed.emit)
        
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.preview_btn)
        
        layout.addLayout(buttons_layout)
    
    def get_rules(self) -> List[RenameRule]:
        """获取所有规则"""
        rules = []
        for panel in self.rule_panels:
            rule = panel.get_rule()
            if rule:
                rules.append(rule)
        return rules
    
    def set_rules(self, rules: List[RenameRule]):
        """设置规则"""
        # 重置所有面板
        for panel in self.rule_panels:
            panel.enable_cb.setChecked(False)
        
        # 应用规则
        for rule in rules:
            for panel in self.rule_panels:
                if panel.mode == rule.mode:
                    panel.set_rule(rule)
                    break
    
    def clear_rules(self):
        """清空所有规则"""
        for panel in self.rule_panels:
            panel.enable_cb.setChecked(False)
        self.rules_changed.emit()
    
    def get_enabled_rules_count(self) -> int:
        """获取启用的规则数量"""
        return sum(1 for panel in self.rule_panels if panel.enabled)


class ClearFilenamePanel(QWidget):
    """清空文件名面板"""
    
    clear_requested = Signal()  # 清空请求信号
    generate_requested = Signal(str, int, int, int)  # 生成请求信号 (template, start, step, padding)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # 标题
        title_label = QLabel("清空文件名")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 说明文本
        desc_label = QLabel("清空所有文件名，然后根据模板生成新的文件名")
        desc_label.setStyleSheet("color: #666; font-size: 12px; margin-bottom: 10px;")
        layout.addWidget(desc_label)
        
        # 清空按钮
        clear_group = QGroupBox("清空操作")
        clear_layout = QVBoxLayout(clear_group)
        
        self.clear_btn = QPushButton("清空所有文件名")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6b6b, stop:1 #ee5a52);
                color: white;
                border: 1px solid #e74c3c;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ee5a52, stop:1 #e74c3c);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
            }
        """)
        self.clear_btn.clicked.connect(self.clear_requested.emit)
        clear_layout.addWidget(self.clear_btn)
        
        layout.addWidget(clear_group)
        
        # 生成新文件名
        generate_group = QGroupBox("生成新文件名")
        generate_layout = QFormLayout(generate_group)
        
        # 文件名模板
        self.template_edit = QLineEdit()
        self.template_edit.setPlaceholderText("例如: 新文件_{n}{ext} 或 图片_{n:03d}{ext}")
        self.template_edit.setText("新文件_{n}{ext}")
        generate_layout.addRow("文件名模板:", self.template_edit)
        
        # 模板说明
        template_help = QLabel("占位符: {n}=序号, {ext}=扩展名, {name}=原文件名, {dir}=文件夹名")
        template_help.setStyleSheet("color: #666; font-size: 11px; margin-top: 2px;")
        template_help.setWordWrap(True)  # 启用自动换行
        generate_layout.addRow("", template_help)
        
        # 序号设置
        number_layout = QHBoxLayout()
        
        self.start_spin = QSpinBox()
        self.start_spin.setRange(1, 99999)
        self.start_spin.setValue(1)
        self.start_spin.setSuffix(" 开始")
        number_layout.addWidget(QLabel("起始序号:"))
        number_layout.addWidget(self.start_spin)
        
        self.step_spin = QSpinBox()
        self.step_spin.setRange(1, 100)
        self.step_spin.setValue(1)
        self.step_spin.setSuffix(" 步长")
        number_layout.addWidget(QLabel("步长:"))
        number_layout.addWidget(self.step_spin)
        
        self.padding_spin = QSpinBox()
        self.padding_spin.setRange(1, 10)
        self.padding_spin.setValue(3)
        self.padding_spin.setSuffix(" 位数")
        number_layout.addWidget(QLabel("位数:"))
        number_layout.addWidget(self.padding_spin)
        
        number_layout.addStretch()
        generate_layout.addRow("序号设置:", number_layout)
        
        # 生成按钮
        self.generate_btn = QPushButton("生成新文件名")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4ecdc4, stop:1 #44a08d);
                color: white;
                border: 1px solid #26a69a;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #44a08d, stop:1 #26a69a);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #26a69a, stop:1 #00695c);
            }
        """)
        self.generate_btn.clicked.connect(self.on_generate_clicked)
        generate_layout.addRow("", self.generate_btn)
        
        layout.addWidget(generate_group)
        
        # 预览区域
        preview_group = QGroupBox("预览")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_text = QTextEdit()
        self.preview_text.setMaximumHeight(100)
        self.preview_text.setReadOnly(True)
        self.preview_text.setPlaceholderText("输入模板后点击生成按钮查看预览...")
        preview_layout.addWidget(self.preview_text)
        
        layout.addWidget(preview_group)
        
        # 连接信号
        self.template_edit.textChanged.connect(self.update_preview)
        self.start_spin.valueChanged.connect(self.update_preview)
        self.step_spin.valueChanged.connect(self.update_preview)
        self.padding_spin.valueChanged.connect(self.update_preview)
        
    def on_generate_clicked(self):
        """生成按钮点击事件"""
        template = self.template_edit.text().strip()
        if not template:
            QMessageBox.warning(self, "警告", "请输入文件名模板！")
            return
        
        self.generate_requested.emit(
            template,
            self.start_spin.value(),
            self.step_spin.value(),
            self.padding_spin.value()
        )
    
    def update_preview(self):
        """更新预览"""
        template = self.template_edit.text().strip()
        if not template:
            self.preview_text.clear()
            return
        
        try:
            # 生成预览示例
            start = self.start_spin.value()
            step = self.step_spin.value()
            padding = self.padding_spin.value()
            
            preview_lines = []
            for i in range(3):  # 显示3个示例
                number = start + i * step
                example_name = template.format(
                    n=str(number).zfill(padding),
                    ext=".txt",
                    name="原文件名",
                    dir="文件夹"
                )
                preview_lines.append(f"示例 {i+1}: {example_name}")
            
            self.preview_text.setText("\n".join(preview_lines))
        except Exception as e:
            self.preview_text.setText(f"模板错误: {str(e)}")
    
    def set_template(self, template: str):
        """设置模板"""
        self.template_edit.setText(template)
    
    def get_template(self) -> str:
        """获取模板"""
        return self.template_edit.text().strip()
