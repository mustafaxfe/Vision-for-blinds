#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.cloud import translate
from picamera import PiCamera
from time import sleep
from gpiozero import Button
from google.cloud import speech
import io
import time
import picamera
import six
import os
import pyaudio
import wave
button = Button(17)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
TARGET_LANG = "tr"
def get_ocr():
	get_im()
	os.system("test.sh")
	text_to_speech(out.txt)
def rec_audio():
	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	print("* done recording")

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
def get_im():
	with picamera.PiCamera() as camera:
		#camera.resolution = (1024, 768)
		camera.start_preview()
		# Camera warm-up time
		time.sleep(2)
		camera.capture('/home/pi/scripts/im_source.jpg')
def get_im2txt():
	get_im()
	os.system("/home/pi/scripts/cloud_tf.sh")
#def get_ocr():
	
	
def get_text():
	get_im2txt()
	with open('/home/pi/im2txt_out/im2txt.txt', 'r') as infile:
		data = infile.read()
		data_begin = data.find("0)")
		data_end = data.find("(p")
		data = data[data_begin+3:data_end]
		print data
		return data
def transcribe_file(speech_file):
	rec_audio()
	speech_client = speech.Client()

	with io.open(speech_file, 'rb') as audio_file:
		content = audio_file.read()
		audio_sample = speech_client.sample(
            content=content,
            source_uri=None,
            encoding='LINEAR16',
            sample_rate_hertz=16000)
	alternatives = audio_sample.recognize('tr-TR')
	for alternative in alternatives:
		speech_out = alternative.transcript.encode('utf-8')
		print('Transcript: {}'.format(speech_out))#alternative.transcript))
		return speech_out

def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()
    print(target)
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target)

    #print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    translated_text = result['translatedText']
    return translated_text
#print trresult
#get_text()
def text_to_speech(tts_file):
	print(tts_file)
	#os.system('./home/pi/scripts/simple_google_tts tr %s' % (tts_file.encode('utf-8')))
if __name__ == "__main__":
	while True:
		#button = Button(17)
		button.wait_for_press()
		choice = transcribe_file("output.wav")
		if choice == "Neye bakıyorum":
			enTxt = get_text()
			trTxt = translate_text("tr", enTxt)
			text_to_speech(trTxt)
		elif (choice == "ne yazıyor"):
			get_ocr()
		else:
			os.system("/home/pi/scripts/err.sh")
			#os.system("/home/pi/scripts/simple_google_tts tr {}".format(tts_file))
