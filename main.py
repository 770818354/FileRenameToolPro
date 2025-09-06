#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量文件重命名工具 - 开发版主程序入口
我很会养猪丶开发版本
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui.qt_adapter import QApplication, QMessageBox, Qt, QIcon
from ui.main_window import EnhancedMainWindow


def setup_application():
    """设置应用程序"""
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName("批量文件重命名工具 - 我很会养猪丶开发版")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("File Rename Tool Pro")
    
    # 设置应用程序图标（如果有的话）
    icon_path = project_root / "resources" / "icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # 启用高DPI支持（移除废弃的属性）
    try:
        # 新版本Qt的高DPI设置
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    except AttributeError:
        # 兼容旧版本
        pass
    
    return app


def main():
    """主函数"""
    try:
        # 设置应用程序
        app = setup_application()
        
        # 创建增强版主窗口
        main_window = EnhancedMainWindow()
        main_window.show()
        
        # 运行应用程序
        sys.exit(app.exec())
        
    except ImportError as e:
        # 处理依赖包缺失的情况
        error_msg = f"""
        缺少必要的依赖包: {str(e)}
        
        请安装所需的依赖包:
        pip install PySide6
        
        或者运行:
        pip install -r requirements.txt
        """
        
        # 尝试显示图形化错误对话框
        try:
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "依赖错误", error_msg)
        except:
            # 如果无法显示图形化对话框，则打印到控制台
            print(error_msg)
        
        sys.exit(1)
        
    except Exception as e:
        # 处理其他未预期的错误
        error_msg = f"程序启动时发生未知错误: {str(e)}"
        
        try:
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "启动错误", error_msg)
        except:
            print(error_msg)
        
        sys.exit(1)


if __name__ == "__main__":
    main()
