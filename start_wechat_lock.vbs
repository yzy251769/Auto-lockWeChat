' 微信自动上锁 - 后台静默启动
' 脚本会自动隐藏窗口，无需额外配置
Dim pythonPath, scriptPath
pythonPath = "C:\msys64\ucrt64\bin\python.exe"
scriptPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\wechat_auto_lock.py"
CreateObject("WScript.Shell").Run """" & pythonPath & """ """ & scriptPath & """", 0, False
