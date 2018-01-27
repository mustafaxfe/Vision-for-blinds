import argparse
from enum import Enum
import io

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
def dec_ocr(PATH):
	"""Returns document bounds given an image."""
	client = vision.ImageAnnotatorClient()

	words = []

	with io.open(PATH, 'rb') as image_file:
		content = image_file.read()

	image = types.Image(content=content)
	response = client.document_text_detection(image=image)
	document = response.full_text_annotation()
	print(document[0])

# Collect specified feature bounds by enumerating all document features


# The list `bounds` contains the coordinates of the bounding boxes.
if __name__ == '__main__':
	dec_ocr('/home/connecticals/gcf_ocr/4.jpg')
