from pylibdmtx.pylibdmtx import encode, decode
from PIL import Image
encoded = encode('hello world'.encode('utf8'))
img = Image.frombytes('RGB', (100, 100), 16)
img.save('dmtx.png')
print(decode(Image.open('dmtx.png')))