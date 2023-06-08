import random

SYMBOLS_UNIVERSE = [chr(ord('a')+i) for i in range(26)]
SYMBOLS_UNIVERSE.extend([chr(ord('A')+i) for i in range(26)])
SYMBOLS_UNIVERSE.extend([chr(ord('0')+i) for i in range(10)])
SYMBOLS_UNIVERSE.extend(['-'])
IMAGE_EXTENSION = ('png', 'jpg', 'jpeg')

def create_random_name(length):
    name = ""
    for _ in range(length):
        name += random.choice(SYMBOLS_UNIVERSE)
    return name

def isAllowedExtension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSION