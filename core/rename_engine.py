#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量文件重命名工具 - 核心重命名引擎
提供各种重命名规则的实现和文件操作功能
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class RenameMode(Enum):
    """重命名模式枚举"""
    REPLACE = "replace"          # 替换模式
    ADD_PREFIX = "add_prefix"    # 添加前缀
    ADD_SUFFIX = "add_suffix"    # 添加后缀
    ADD_INDEX = "add_index"      # 添加序号
    DELETE_CHARS = "delete_chars" # 删除字符
    REGEX = "regex"              # 正则表达式
    CASE_CHANGE = "case_change"  # 大小写转换
    EXTENSION = "extension"      # 扩展名修改
    DATE_TIME = "date_time"      # 日期时间


class CaseMode(Enum):
    """大小写转换模式"""
    UPPER = "upper"              # 全大写
    LOWER = "lower"              # 全小写
    TITLE = "title"              # 首字母大写
    SENTENCE = "sentence"        # 句首大写


@dataclass
class RenameRule:
    """重命名规则数据类"""
    mode: RenameMode
    enabled: bool = True
    # 通用参数
    search_text: str = ""
    replace_text: str = ""
    case_sensitive: bool = True
    # 序号相关
    start_number: int = 1
    step: int = 1
    padding: int = 3
    # 删除相关
    delete_start: int = 0
    delete_end: int = 0
    # 大小写相关
    case_mode: CaseMode = CaseMode.LOWER
    # 正则表达式
    regex_pattern: str = ""
    regex_flags: int = 0
    # 日期时间
    date_format: str = "%Y%m%d"
    use_create_date: bool = True


@dataclass
class FileItem:
    """文件项数据类"""
    original_path: Path
    original_name: str
    new_name: str
    extension: str
    size: int
    modified_date: datetime
    created_date: datetime
    is_directory: bool = False
    status: str = "ready"  # ready, renamed, error, skipped


class RenameEngine:
    """核心重命名引擎"""
    
    def __init__(self):
        self.files: List[FileItem] = []
        self.rules: List[RenameRule] = []
        self.history: List[Dict] = []  # 操作历史记录
        self.current_directory: Optional[Path] = None
        
    def load_directory(self, directory_path: str, include_subdirs: bool = False, 
                      file_filters: List[str] = None) -> List[FileItem]:
        """
        加载目录中的文件
        
        Args:
            directory_path: 目录路径
            include_subdirs: 是否包含子目录
            file_filters: 文件扩展名筛选器 (如 ['.jpg', '.png'])
        
        Returns:
            文件列表
        """
        self.current_directory = Path(directory_path)
        self.files = []
        
        if not self.current_directory.exists():
            raise FileNotFoundError(f"目录不存在: {directory_path}")
        
        # 获取文件列表
        if include_subdirs:
            pattern = "**/*"
        else:
            pattern = "*"
            
        for item_path in self.current_directory.glob(pattern):
            if item_path.is_file() or item_path.is_dir():
                # 应用文件筛选器
                if file_filters is not None and item_path.is_file():
                    if item_path.suffix.lower() not in [f.lower() for f in file_filters]:
                        continue
                
                try:
                    stat = item_path.stat()
                    file_item = FileItem(
                        original_path=item_path,
                        original_name=item_path.name,
                        new_name=item_path.name,
                        extension=item_path.suffix,
                        size=stat.st_size if item_path.is_file() else 0,
                        modified_date=datetime.fromtimestamp(stat.st_mtime),
                        created_date=datetime.fromtimestamp(stat.st_ctime),
                        is_directory=item_path.is_dir()
                    )
                    self.files.append(file_item)
                except (OSError, PermissionError) as e:
                    print(f"无法访问文件: {item_path}, 错误: {e}")
                    continue
        
        # 按名称排序
        self.files.sort(key=lambda x: x.original_name.lower())
        return self.files
    
    def add_rule(self, rule: RenameRule):
        """添加重命名规则"""
        self.rules.append(rule)
    
    def remove_rule(self, index: int):
        """移除重命名规则"""
        if 0 <= index < len(self.rules):
            self.rules.pop(index)
    
    def clear_rules(self):
        """清空所有规则"""
        self.rules.clear()
    
    def preview_rename(self) -> List[FileItem]:
        """
        预览重命名结果，不实际执行重命名
        
        Returns:
            预览后的文件列表
        """
        # 重置所有文件的新名称
        for file_item in self.files:
            file_item.new_name = file_item.original_name
            file_item.status = "ready"
        
        # 按顺序应用所有启用的规则
        for rule in self.rules:
            if rule.enabled:
                self._apply_rule_to_files(rule)
        
        # 检查名称冲突
        self._check_name_conflicts()
        
        return self.files
    
    def _apply_rule_to_files(self, rule: RenameRule):
        """将规则应用到所有文件"""
        if rule.mode == RenameMode.REPLACE:
            self._apply_replace_rule(rule)
        elif rule.mode == RenameMode.ADD_PREFIX:
            self._apply_add_prefix_rule(rule)
        elif rule.mode == RenameMode.ADD_SUFFIX:
            self._apply_add_suffix_rule(rule)
        elif rule.mode == RenameMode.ADD_INDEX:
            self._apply_add_index_rule(rule)
        elif rule.mode == RenameMode.DELETE_CHARS:
            self._apply_delete_chars_rule(rule)
        elif rule.mode == RenameMode.REGEX:
            self._apply_regex_rule(rule)
        elif rule.mode == RenameMode.CASE_CHANGE:
            self._apply_case_change_rule(rule)
        elif rule.mode == RenameMode.EXTENSION:
            self._apply_extension_rule(rule)
        elif rule.mode == RenameMode.DATE_TIME:
            self._apply_date_time_rule(rule)
    
    def _apply_replace_rule(self, rule: RenameRule):
        """应用替换规则"""
        for file_item in self.files:
            name_without_ext = Path(file_item.new_name).stem
            extension = Path(file_item.new_name).suffix
            
            if rule.case_sensitive:
                new_name = name_without_ext.replace(rule.search_text, rule.replace_text)
            else:
                # 不区分大小写的替换
                pattern = re.escape(rule.search_text)
                new_name = re.sub(pattern, rule.replace_text, name_without_ext, flags=re.IGNORECASE)
            
            file_item.new_name = new_name + extension
    
    def _apply_add_prefix_rule(self, rule: RenameRule):
        """应用添加前缀规则"""
        for file_item in self.files:
            name_without_ext = Path(file_item.new_name).stem
            extension = Path(file_item.new_name).suffix
            file_item.new_name = rule.replace_text + name_without_ext + extension
    
    def _apply_add_suffix_rule(self, rule: RenameRule):
        """应用添加后缀规则"""
        for file_item in self.files:
            name_without_ext = Path(file_item.new_name).stem
            extension = Path(file_item.new_name).suffix
            file_item.new_name = name_without_ext + rule.replace_text + extension
    
    def _apply_add_index_rule(self, rule: RenameRule):
        """应用添加序号规则"""
        current_number = rule.start_number
        for file_item in self.files:
            name_without_ext = Path(file_item.new_name).stem
            extension = Path(file_item.new_name).suffix
            
            # 格式化序号
            index_str = str(current_number).zfill(rule.padding)
            
            if rule.replace_text:  # 如果有模板文本
                if "{index}" in rule.replace_text:
                    formatted_text = rule.replace_text.replace("{index}", index_str)
                else:
                    formatted_text = rule.replace_text + index_str
            else:
                formatted_text = index_str
            
            file_item.new_name = name_without_ext + "_" + formatted_text + extension
            current_number += rule.step
    
    def _apply_delete_chars_rule(self, rule: RenameRule):
        """应用删除字符规则"""
        for file_item in self.files:
            name_without_ext = Path(file_item.new_name).stem
            extension = Path(file_item.new_name).suffix
            
            # 删除指定位置的字符
            if rule.delete_start >= 0 and rule.delete_end > rule.delete_start:
                new_name = name_without_ext[:rule.delete_start] + name_without_ext[rule.delete_end:]
            else:
                new_name = name_without_ext
            
            file_item.new_name = new_name + extension
    
    def _apply_regex_rule(self, rule: RenameRule):
        """应用正则表达式规则"""
        try:
            pattern = re.compile(rule.regex_pattern, rule.regex_flags)
            for file_item in self.files:
                name_without_ext = Path(file_item.new_name).stem
                extension = Path(file_item.new_name).suffix
                
                new_name = pattern.sub(rule.replace_text, name_without_ext)
                file_item.new_name = new_name + extension
        except re.error as e:
            print(f"正则表达式错误: {e}")
    
    def _apply_case_change_rule(self, rule: RenameRule):
        """应用大小写转换规则"""
        for file_item in self.files:
            name_without_ext = Path(file_item.new_name).stem
            extension = Path(file_item.new_name).suffix
            
            if rule.case_mode == CaseMode.UPPER:
                new_name = name_without_ext.upper()
            elif rule.case_mode == CaseMode.LOWER:
                new_name = name_without_ext.lower()
            elif rule.case_mode == CaseMode.TITLE:
                new_name = name_without_ext.title()
            elif rule.case_mode == CaseMode.SENTENCE:
                new_name = name_without_ext.capitalize()
            else:
                new_name = name_without_ext
            
            file_item.new_name = new_name + extension
    
    def _apply_extension_rule(self, rule: RenameRule):
        """应用扩展名修改规则"""
        for file_item in self.files:
            if not file_item.is_directory:
                name_without_ext = Path(file_item.new_name).stem
                new_extension = rule.replace_text
                if not new_extension.startswith('.'):
                    new_extension = '.' + new_extension
                file_item.new_name = name_without_ext + new_extension
    
    def _apply_date_time_rule(self, rule: RenameRule):
        """应用日期时间规则"""
        for file_item in self.files:
            name_without_ext = Path(file_item.new_name).stem
            extension = Path(file_item.new_name).suffix
            
            # 选择使用创建日期还是修改日期
            target_date = file_item.created_date if rule.use_create_date else file_item.modified_date
            date_str = target_date.strftime(rule.date_format)
            
            if rule.replace_text:
                if "{date}" in rule.replace_text:
                    formatted_text = rule.replace_text.replace("{date}", date_str)
                else:
                    formatted_text = date_str + "_" + rule.replace_text
            else:
                formatted_text = date_str
            
            file_item.new_name = formatted_text + "_" + name_without_ext + extension
    
    def _check_name_conflicts(self):
        """检查文件名冲突"""
        name_counts = {}
        for file_item in self.files:
            lower_name = file_item.new_name.lower()
            if lower_name in name_counts:
                name_counts[lower_name] += 1
                file_item.status = "conflict"
            else:
                name_counts[lower_name] = 1
        
        # 标记所有冲突的文件
        for file_item in self.files:
            if name_counts.get(file_item.new_name.lower(), 0) > 1:
                file_item.status = "conflict"
    
    def execute_rename(self) -> Tuple[int, int, List[str]]:
        """
        执行重命名操作
        
        Returns:
            成功数量, 失败数量, 错误信息列表
        """
        success_count = 0
        error_count = 0
        error_messages = []
        rename_operations = []  # 用于撤销操作
        
        for file_item in self.files:
            if file_item.status == "conflict":
                error_messages.append(f"跳过冲突文件: {file_item.original_name}")
                file_item.status = "skipped"
                continue
            
            if file_item.new_name == file_item.original_name:
                continue  # 名称未改变，跳过
            
            try:
                old_path = file_item.original_path
                new_path = old_path.parent / file_item.new_name
                
                # 检查目标文件是否已存在
                if new_path.exists() and new_path != old_path:
                    error_messages.append(f"目标文件已存在: {file_item.new_name}")
                    file_item.status = "error"
                    error_count += 1
                    continue
                
                # 执行重命名
                old_path.rename(new_path)
                
                # 记录操作用于撤销
                rename_operations.append({
                    'old_path': new_path,
                    'new_path': old_path,
                    'original_name': file_item.original_name,
                    'new_name': file_item.new_name
                })
                
                file_item.status = "renamed"
                file_item.original_path = new_path
                file_item.original_name = file_item.new_name
                file_item.new_name = file_item.new_name  # 保持一致性
                success_count += 1
                
            except (OSError, PermissionError) as e:
                error_messages.append(f"重命名失败 {file_item.original_name}: {str(e)}")
                file_item.status = "error"
                error_count += 1
        
        # 保存到历史记录
        if rename_operations:
            self.history.append({
                'timestamp': datetime.now(),
                'operations': rename_operations,
                'success_count': success_count,
                'error_count': error_count
            })
        
        return success_count, error_count, error_messages
    
    def undo_last_rename(self) -> Tuple[bool, str]:
        """
        撤销上一次重命名操作
        
        Returns:
            成功标志, 消息
        """
        if not self.history:
            return False, "没有可撤销的操作"
        
        last_operation = self.history[-1]
        operations = last_operation['operations']
        
        success_count = 0
        error_count = 0
        
        # 逆向执行重命名操作
        for op in reversed(operations):
            try:
                if op['old_path'].exists():
                    op['old_path'].rename(op['new_path'])
                    success_count += 1
            except (OSError, PermissionError) as e:
                error_count += 1
        
        # 从历史记录中移除
        self.history.pop()
        
        # 刷新文件列表
        if self.current_directory:
            self.load_directory(str(self.current_directory))
        
        if error_count == 0:
            return True, f"成功撤销 {success_count} 个文件的重命名"
        else:
            return False, f"撤销完成，但有 {error_count} 个文件撤销失败"
    
    def get_rename_preview_summary(self) -> Dict:
        """获取重命名预览摘要"""
        total = len(self.files)
        will_rename = sum(1 for f in self.files if f.new_name != f.original_name and f.status != "conflict")
        conflicts = sum(1 for f in self.files if f.status == "conflict")
        
        return {
            'total_files': total,
            'will_rename': will_rename,
            'conflicts': conflicts,
            'unchanged': total - will_rename - conflicts
        }
    
    def clear_all_filenames(self):
        """清空所有文件名（保留扩展名）"""
        for file_item in self.files:
            if not file_item.is_directory:
                # 保留扩展名，清空文件名部分
                file_item.new_name = file_item.extension
            else:
                # 文件夹清空名称
                file_item.new_name = ""
            file_item.status = "ready"
    
    def generate_new_filenames(self, template: str, start_number: int = 1, step: int = 1, padding: int = 3):
        """
        根据模板生成新的文件名
        
        Args:
            template: 文件名模板，支持以下占位符：
                - {n}: 序号（从start_number开始）
                - {ext}: 原文件扩展名
                - {name}: 原文件名（不含扩展名）
                - {dir}: 文件夹名称
            start_number: 起始序号
            step: 序号步长
            padding: 序号位数（不足时前面补0）
        """
        if not template.strip():
            return
        
        current_number = start_number
        
        for file_item in self.files:
            if file_item.is_directory:
                # 文件夹处理
                new_name = template.format(
                    n=current_number,
                    ext="",
                    name=file_item.original_name,
                    dir=file_item.original_path.parent.name
                )
                file_item.new_name = new_name
            else:
                # 文件处理
                original_name_without_ext = file_item.original_path.stem
                new_name = template.format(
                    n=str(current_number).zfill(padding),
                    ext=file_item.extension,
                    name=original_name_without_ext,
                    dir=file_item.original_path.parent.name
                )
                file_item.new_name = new_name
            
            file_item.status = "ready"
            current_number += step
        
        # 检查重名冲突
        self._check_name_conflicts()
    
    def refresh_file_list(self):
        """刷新文件列表，确保与实际文件系统同步"""
        if not self.current_directory:
            return
        
        # 重新扫描目录
        for file_item in self.files:
            if file_item.original_path.exists():
                # 更新文件信息
                try:
                    stat = file_item.original_path.stat()
                    file_item.size = stat.st_size if file_item.original_path.is_file() else 0
                    file_item.modified_date = datetime.fromtimestamp(stat.st_mtime)
                    file_item.created_date = datetime.fromtimestamp(stat.st_ctime)
                    
                    # 如果文件路径或名称发生变化，更新相关信息
                    current_name = file_item.original_path.name
                    if current_name != file_item.original_name:
                        file_item.original_name = current_name
                        file_item.new_name = current_name
                        file_item.extension = file_item.original_path.suffix
                        file_item.status = "ready"
                except (OSError, PermissionError):
                    # 文件可能已被删除或无法访问
                    file_item.status = "error"
            else:
                # 文件不存在
                file_item.status = "error"
