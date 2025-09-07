@echo off
title 批量文件重命名工具 - 我很会养猪丶开发版
echo.
echo ================================================
echo     批量文件重命名工具 - 我很会养猪丶开发版
echo     功能更强大
echo ================================================
echo.
echo 正在启动程序，请稍候...
echo 首次运行可能需要较长时间加载
echo.
"FileRenameToolPro.exe"
if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查系统环境
    pause
)
