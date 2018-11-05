import time
import os
import wave

class AudioSystem():
	def __init__(self):
		# Put audio filenames string here
		self.swipeDetected = "swipeDetected.wav"
		self.whatIsObject = ["whatIsObject0.wav", "whatIsObject1.wav"]
		self.readyToPour = 'readyToPour.wav'
		self.timeOut = 'timeOut.wav'
		self.enjoy = ['enjoy0.wav', 'enjoy1.wav']
		self.welcome = ['welcome0.wav', 'welcome1.wav']
		self.master = ['master0.wav', 'master1.wav']

		# Functional stuff
		self.cmd_string = "omxplayer -o local "

	def playAudio(self, filename):
		wav = wave.open(filename)
		fs = wav.getframerate()
		samps = wav.getnframes()
		os.system(self.cmd_string + filename)
		time.sleep(samps/fs) #pause for audio
