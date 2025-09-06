#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版构建脚本 - 我很会养猪丶开发版本
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def main():
    """主函数"""
    print("=" * 60)
    print("构建批量文件重命名工具 - 我很会养猪丶开发版")
    print("=" * 60)
    
    # 清理构建文件
    print("清理构建文件...")
    cleanup_items = ['build', 'dist', '__pycache__']
    
    for item in cleanup_items:
        item_path = Path(item)
        if item_path.exists():
            if item_path.is_dir():
                shutil.rmtree(item_path)
                print(f"  ✅ 删除: {item_path}")
    
    # 删除所有.spec文件
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"  ✅ 删除: {spec_file}")
    
    print("✅ 清理完成")
    
    # 构建命令
    build_command = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                           # 单文件打包
        '--windowed',                          # 无控制台窗口
        '--name=FileRenameToolPro',           # 专业版名称
        '--exclude-module=PyQt6',              # 排除PyQt6
        '--exclude-module=PyQt6.QtCore',
        '--exclude-module=PyQt6.QtGui',
        '--exclude-module=PyQt6.QtWidgets',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui', 
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=ui.qt_adapter',
        '--hidden-import=ui.enhanced_main_window',
        '--hidden-import=ui.enhanced_file_manager',
        '--hidden-import=ui.enhanced_themes',
        '--hidden-import=ui.main_window',
        '--hidden-import=ui.file_manager',
        '--hidden-import=ui.rule_panels',
        '--hidden-import=ui.themes',
        '--hidden-import=core.rename_engine',
        '--add-data=static;static',             # 添加静态资源文件
        'main.py'                              # 主程序入口
    ]
    
    try:
        print("\n开始构建我很会养猪丶开发版...")
        print("📋 构建配置:")
        print("  - 目标文件: FileRenameToolPro.exe")
        print("  - 界面风格: 我很会养猪丶开发版")
        print("  - GUI框架: PySide6")
        print("  - 打包模式: 单文件 + 无控制台")
        print()
        
        # 直接运行，显示所有输出
        result = subprocess.run(build_command, check=True)
        
        print("✅ 构建成功完成")
        
        # 检查生成的文件
        exe_path = Path('dist') / 'FileRenameToolPro.exe'
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"✅ 可执行文件已生成: {exe_path}")
            print(f"  文件大小: {size_mb:.1f} MB")
            
            # 创建我很会养猪丶开发版启动脚本
            pro_launcher = exe_path.parent / '启动我很会养猪丶开发版重命名工具.bat'
            pro_launcher.write_text(
                '@echo off\n'
                'title 批量文件重命名工具 - 我很会养猪丶开发版\n'
                'echo.\n'
                'echo ================================================\n'
                'echo     批量文件重命名工具 - 我很会养猪丶开发版\n'
                'echo     仿金舟软件风格，功能更强大\n'
                'echo ================================================\n'
                'echo.\n'
                'echo 正在启动程序，请稍候...\n'
                'echo 首次运行可能需要较长时间加载\n'
                'echo.\n'
                '"FileRenameToolPro.exe"\n'
                'if errorlevel 1 (\n'
                '    echo.\n'
                '    echo 程序运行出错，请检查系统环境\n'
                '    pause\n'
                ')\n',
                encoding='gbk'
            )
            print(f"✅ 创建启动脚本: {pro_launcher}")
            
            # 创建readme文件
            readme_file = exe_path.parent / '使用说明.txt'
            readme_file.write_text(
                '批量文件重命名工具 - 我很会养猪丶开发版\n'
                '================================\n\n'
                '版本信息：\n'
                '- 版本号：1.0.0 我很会养猪丶开发版\n'
                '- 界面风格：我很会养猪丶\n'
                '- 技术架构：PySide6 + Python\n\n'
                '主要特性：\n'
                '9种重命名模式，功能强大\n'
                '实时预览效果，所见即所得\n'
                '安全操作保障，支持撤销\n'
                '现代化界面，多主题支持\n'
                '高性能处理，支持大量文件\n'
                '智能筛选，多维度过滤\n\n'
                '使用方法：\n'
                '1. 双击"FileRenameToolPro.exe"启动程序\n'
                '2. 或使用"启动我很会养猪丶开发版重命名工具.bat"启动\n'
                '3. 按照界面提示操作即可\n\n'
                '技术支持：\n'
                '- 遇到问题请查看项目文档\n'
                '- 或联系技术支持团队\n\n'
                '版权信息：\n'
                '© 2025 批量文件重命名工具\n'
                'MIT License\n',
                encoding='utf-8'
            )
            print(f"✅ 创建说明文档: {readme_file}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: 返回码 {e.returncode}")
        return False
    
    except Exception as e:
        print(f"❌ 构建过程中发生错误: {e}")
        return False


if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n" + "=" * 60)
        print("我很会养猪丶开发版构建成功完成！")
        print("=" * 60)
        print("输出目录: dist/")
        print("主程序: FileRenameToolPro.exe")
        print("启动脚本: 启动我很会养猪丶开发版重命名工具.bat")
        print("使用说明: 使用说明.txt")
        print("\n特色功能:")
        print("  我很会养猪丶界面风格")
        print("  2种主题模式（亮色/专业）")
        print("  增强的文件管理和筛选功能")
        print("  更多专业级操作选项")
        print("  适合专业用户和企业使用")
        print("\n立即体验我很会养猪丶开发版的强大功能！")
        sys.exit(0)
    else:
        print("\n构建失败，请检查错误信息")
        sys.exit(1)
