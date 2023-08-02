import cv2
from pylibdmtx.pylibdmtx import decode

# List kosong untuk barcode
combined_barcodes = []

def decoder(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    code = decode(gray_img)
    
    for obj in code:
        (x, y, w, h) = obj.rect
        
        barcodeData = obj.data.decode("utf-8")
        barcodeType = "Data Matrix"  # Tipe barcode selalu Data Matrix untuk pylibdmtx

        
        if barcodeData not in combined_barcodes:
            # masukkan data kedalam list
            combined_barcodes.append(barcodeData)
            print("New Barcode: " + barcodeData + " | Type: " + barcodeType)
        else:
            # Data yang sudah pernah masuk list akan "Data sudah terbaca" di console
            print("Data sudah terbaca")

        cv2.putText(image, barcodeData.strip(), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        # strip() untuk hilangkan escape character dari gambar
# open kamera
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    decoder(frame)
    cv2.imshow('Data Matrix Scanner', frame)
    code = cv2.waitKey(10)
    # tutup dengan tombol q
    if code == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
output = "".join(combined_barcodes)

# simpan kedalam file.txt
with open("barcode_data.txt", "w") as file:
    file.write(output)

# notifikasi tersimpan
print("Data Barcode telah tersimpan di barcode_data.txt")
print(output)
