# coding=utf-8

import subprocess

def get_audio(text):
    stat = subprocess.call(['./tts', text])
    if (stat == 0):
	return "Success"
    else:
	print "Failed"
