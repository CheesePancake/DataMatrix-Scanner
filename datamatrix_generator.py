from pylibdmtx.pylibdmtx import encode, decode
from PIL import Image
encoded = encode('hello world'.encode('utf8'))
img = Image.frombytes('RGB', (encoded.height, encoded.width), encoded.pixels)
img.save('dmtx.png')
print(decode(Image.open('dmtx.png')))
