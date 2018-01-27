import argparse
from enum import Enum
import io

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)
                print(u'Paragraph Confidence: {}\n'.format(
                    paragraph.confidence))

            block_text = ''
            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)
                word_text = ''
                for symbol in word.symbols:
                    word_text = word_text + symbol.text
                    print(u'\tSymbol text: {} (confidence: {})'.format(
                        symbol.text, symbol.confidence))
                print(u'Word text: {} (confidence: {})\n'.format(
                    word_text, word.confidence))

                block_text += ' ' + word_text

            print(u'Block Content: {}\n'.format(block_text))
            print(u'Block Confidence:\n {}\n'.format(block.confidence))
if __name__ == '__main__':
	detect_document('/home/connecticals/gcf_ocr/4.jpg')
