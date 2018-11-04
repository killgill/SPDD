import time
import os
import wave
class audioSystem():
	# Put audio filenames string here
	ready2pour = "ready2pour.wav"
	# Functional stuff
	cmd_string = "omxplayer -o local "

	def playAudio(filename):
		fs = wave_read.getframerate(filename)
		samps = wave_read.getframes(filename)
		os.system(cmd_string + filename)
		time.sleep(samps/fs) #pause for audio



		


