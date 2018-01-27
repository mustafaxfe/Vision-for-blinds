from google.cloud import vision
from google.cloud.vision import types
import io, os
def ocr_test(PATH):
	""" 
	Detects text in image using Google Cloud Vision OCR Api
	"""
	# Load Api's client function
	client = vision.ImageAnnotatorClient()
	# Read image
	with io.open(PATH, 'rb') as image_file:
		content = image_file.read()
	image = types.Image(content=content)
	response = client.document_text_detection(image=image)
	# Start a loop for detecting words and symbols that is in image
	for page in response.full_text_annotation.pages:
		for block in page.blocks:
			block_words = []
			for paragraph in block.paragraphs:
				block_words.extend(paragraph.words)
			block_text = '' # Create a block_text string to 
							# store words and symbols of image
			block_symbols = []
			for word in block_words:
				block_symbols.extend(word.symbols)
				word_text = ''
				for symbol in word.symbols:
					word_text = word_text + symbol.text
				block_text += ' ' + word_text
	print('block: %s' % block_text)
	os.system('espeak -l tr "%s"' % block_text)
if __name__ == '__main__': ocr_test('/home/connecticals/gcf_ocr/4.jpg')
