"""
微信自动上锁程序
检测系统空闲（无键鼠操作），超过设定时间后自动给电脑微信上锁。
离开电脑后自动保护微信隐私，回来动一下鼠标即重置状态。

用法：
    python wechat_auto_lock.py              # 默认5分钟空闲后上锁
    python wechat_auto_lock.py --timeout 120  # 2分钟空闲后上锁
    python wechat_auto_lock.py --check 10   # 每10秒检测一次
"""

import ctypes
from ctypes import wintypes
import time
import argparse
import sys


# ── Windows API 定义 ──────────────────────────────────────────

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("dwTime", wintypes.DWORD),
    ]


def get_idle_seconds() -> float:
    """获取系统空闲时间（秒），自上次键盘/鼠标操作以来。"""
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        return 0.0
    return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0


def find_wechat_window() -> int | None:
    """查找微信主窗口，返回窗口句柄，未找到返回 None。
    优先匹配 Qt 版微信类名，再尝试旧版类名，最后按标题搜索。
    """
    # 新版 Qt 微信
    hwnd = ctypes.windll.user32.FindWindowW("Qt51514QWindowIcon", None)
    if hwnd:
        return hwnd
    # 旧版 Windows 微信
    hwnd = ctypes.windll.user32.FindWindowW("WeChatMainWndForPC", None)
    if hwnd:
        return hwnd
    # 兜底：按窗口标题 "微信" 搜索
    hwnd = ctypes.windll.user32.FindWindowW(None, "微信")
    return hwnd if hwnd else None


def lock_wechat(hwnd: int) -> bool:
    """激活微信窗口并发送 Ctrl+L 锁定热键。"""
    VK_MENU = 0x12    # Alt
    VK_CONTROL = 0x11
    VK_L = 0x4C
    KEYEVENTF_KEYUP = 0x0002

    # 恢复窗口（如果最小化了）
    SW_RESTORE = 9
    ctypes.windll.user32.ShowWindow(hwnd, SW_RESTORE)
    time.sleep(0.3)

    # Alt 键技巧：让系统认为我们有前台权限
    ctypes.windll.user32.keybd_event(VK_MENU, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)

    # 尝试将微信带到前台（如果失败也不影响热键发送）
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.2)

    # 发送 Ctrl+L
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_L, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_L, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)

    return True


def format_time(seconds: float) -> str:
    """格式化秒数为可读时间。"""
    m, s = divmod(int(seconds), 60)
    if m > 0:
        return f"{m}分{s}秒"
    return f"{s}秒"


# ── 主循环 ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="微信自动上锁 - 离开电脑时自动锁定微信"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=300,
        help="空闲多少秒后锁定微信（默认 300 秒 = 5 分钟）",
    )
    parser.add_argument(
        "--check", "-c",
        type=int,
        default=5,
        help="检测间隔秒数（默认 5 秒）",
    )
    args = parser.parse_args()

    print(f"[启动] 微信自动上锁程序已运行")
    print(f"   空闲阈值: {format_time(args.timeout)}")
    print(f"   检测间隔: {args.check}秒")
    print(f"   按 Ctrl+C 退出\n")

    locked = False  # 是否已发送锁定信号

    try:
        while True:
            idle = get_idle_seconds()

            if idle >= args.timeout:
                if not locked:
                    hwnd = find_wechat_window()
                    if hwnd:
                        print(f"[{time.strftime('%H:%M:%S')}] 空闲 {format_time(idle)}，正在锁定微信...")
                        if lock_wechat(hwnd):
                            print(f"[{time.strftime('%H:%M:%S')}] [OK] 微信已锁定")
                            locked = True
                    else:
                        print(f"[{time.strftime('%H:%M:%S')}] [WARN] 空闲超时但未找到微信窗口，请确保微信正在运行")
            else:
                if locked:
                    # 用户回来了，重置锁定状态
                    print(f"[{time.strftime('%H:%M:%S')}] [USER] 检测到用户活动，重置监控状态")
                    locked = False

            time.sleep(args.check)

    except KeyboardInterrupt:
        print("\n[BYE] 微信自动上锁已退出")
        sys.exit(0)


if __name__ == "__main__":
    main()
