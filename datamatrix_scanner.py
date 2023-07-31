import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode

def decoder(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    code = decode(gray_img)
    
    for obj in code:
        (x, y, w, h) = obj.rect
        
        barcodeData = obj.data.decode("utf-8")
        barcodeType = "Data Matrix"  # Tipe barcode selalu Data Matrix untuk pylibdmtx
        string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
        
        cv2.putText(image, barcodeData, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        print("Barcode: " + barcodeData + " | Type: " + barcodeType)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
