@echo off
REM 微信自动上锁 - 后台静默启动（无窗口）
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
start "" /b pythonw "%~dp0wechat_auto_lock.py" %*
