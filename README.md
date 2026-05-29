# WeChat Auto Lock

离开电脑后自动锁定电脑版微信，保护隐私。检测系统空闲（无键鼠操作）超过设定时间后，自动发送锁定热键给微信窗口。**零依赖，纯 Python 标准库。**

## 快速开始

```bash
# 默认：空闲 5 分钟后锁定
python wechat_auto_lock.py

# 自定义空闲时长（秒）
python wechat_auto_lock.py -t 180     # 3 分钟
python wechat_auto_lock.py -t 600     # 10 分钟
```

或者双击 `start_wechat_lock.bat` 启动。

## 前提条件

- Windows 系统
- Python 3.x
- 电脑版微信正在运行
- 微信锁定快捷键为默认 `Ctrl+L`

## 开机自启

将 `start_wechat_lock.bat` 的快捷方式放到 `shell:startup` 文件夹即可。

## 适配不同微信版本

按以下优先级查找微信窗口：

1. Qt 版微信：`Qt51514QWindowIcon` 窗口类名
2. 旧版微信：`WeChatMainWndForPC` 窗口类名
3. 按窗口标题 `微信` 搜索

如果你的版本未被检测到，请提 Issue 附上微信版本和窗口信息。

## 注意事项

- 仅支持 Windows
- 如果修改过微信的锁定快捷键，需编辑 `lock_wechat()` 中的按键码
- 空闲检测基于系统全局键鼠输入，播放视频等不会阻止空闲判定

## License

MIT
