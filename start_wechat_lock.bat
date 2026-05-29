@echo off
REM 微信自动上锁 - 快捷启动脚本
REM 双击此文件即可后台运行

chcp 65001 >nul
set PYTHONIOENCODING=utf-8
python wechat_auto_lock.py %*
pause
