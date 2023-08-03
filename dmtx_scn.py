import cv2
from pylibdmtx.pylibdmtx import decode
import textwrap

# List kosong untuk barcode
combined_barcodes = []

def wrappingText(frame, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255, 255, 255), thickness=2):
    # Membungkus teks menjadi beberapa baris dengan lebar maksimum 40 karakter menggunakan textwrap
    wrapped_text = textwrap.fill(text, width=40)

    # Menghitung tinggi teks yang sudah dibungkus
    (text_width, text_height), _ = cv2.getTextSize(wrapped_text, font, font_scale, thickness)

    # Menampilkan teks di area frame yang sudah dihitung
    for line in wrapped_text.split('\n'):
        cv2.putText(frame, line, position, font, font_scale, color, thickness, cv2.LINE_AA)
        position = (position[0], position[1] + text_height)

def decoder(image):
    global combined_barcodes
    
    code = decode(image, timeout=100, max_count=1)
    
    for obj in code:
        barcodeData = obj.data.decode("utf-8")
        barcodeType = "Data Matrix"  # Tipe barcode selalu Data Matrix untuk pylibdmtx

        if barcodeData not in combined_barcodes:
            # masukkan data kedalam list
            combined_barcodes.append(barcodeData)
            print("New Barcode: " + barcodeData + " | Type: " + barcodeType)
        else:
            # Data yang sudah pernah masuk list akan "Data sudah terbaca" di console
            print("Data sudah terbaca")

        output = "".join(combined_barcodes)
        wrapped_output = textwrap.fill(output, width=40)

        # Tampilkan teks berjalan di atas gambar
        wrappingText(image, wrapped_output, (0, 30), font_scale=0.8, color=(255, 0, 0), thickness=2)

# Inisialisasi objek kamera
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    
    decoder(frame)

    cv2.imshow('Data Matrix Scanner', frame)

    code = cv2.waitKey(1)
    
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
