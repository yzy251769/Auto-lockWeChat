$script_dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$startup = [Environment]::GetFolderPath('Startup')
$shortcut_path = Join-Path $startup 'WeChatAutoLock.lnk'
$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut($shortcut_path)
$sc.TargetPath = 'pythonw'
$sc.Arguments = """$script_dir\wechat_auto_lock.py"""
$sc.WorkingDirectory = $script_dir
$sc.WindowStyle = 7
$sc.Description = 'WeChat Auto Lock'
$sc.Save()
Write-Output "Done: $shortcut_path"
