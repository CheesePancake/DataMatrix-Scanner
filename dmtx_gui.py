from pylibdmtx.pylibdmtx import encode
from PIL import Image, ImageTk
import tkinter as tk
import os
import shutil
import atexit

def split_input_into_chunks(input_str, chunk_size):
    # membagi input string ke beberapa bagian
    return [input_str[i:i + chunk_size] for i in range(0, len(input_str), chunk_size)]

def update_character_count(*args):
    # character counter 
    current_length = len(input_entry.get())
    character_count_label.config(text=f"{current_length}/256")

def encode_and_display():
    global current_index

    # Get user input
    user_input = input_entry.get()

    # bagi inputan per 12 karakter
    chunks = split_input_into_chunks(user_input, 12)

    # list kosong untung menyimpan datamatrix
    data_matrix_images = []

    for chunk in chunks:
        # encode setiap bagian dan simpan di datamatrix terpisah
        encoded = encode(chunk.encode('utf8'), size="16x16")
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)

        # file unique name
        image_path = os.path.join("data_matrix_images", f"dmtx_{current_index}.png")
        img.save(image_path)

        # index gambar
        current_index += 1

        # memasukkan gambar kedalam list
        data_matrix_images.append(img)

    # menampilkan dmtx_0.png dulu, lalu berurutan
    display_data_matrix(0, data_matrix_images)

def display_data_matrix(index, data_matrix_images):
    # data matrix opener 
    if index < len(data_matrix_images):
        image = data_matrix_images[index]
        photo = ImageTk.PhotoImage(image)

        # Update the label with the new image
        label.config(image=photo)
        label.image = photo

        # secara dynamics berubah selama 2 detik
        root.after(2000, display_data_matrix, (index + 1) % len(data_matrix_images), data_matrix_images)
    else:
        # error handling, mungkin, hehe
        label.config(text="No more DataMatrix images available")

def remove_directory():
    # hapus folder penyimpan datamatrix ketika program ditutup
    # solusi sementara buat bug
    if os.path.exists("data_matrix_images"):
        shutil.rmtree("data_matrix_images")

# Tkinter window
root = tk.Tk()
root.title("Data Matrix")

# DataMatrix display label
label = tk.Label(root)
label.pack(side=tk.LEFT)

# frame input dan char counter
input_frame = tk.Frame(root)
input_frame.pack(side=tk.RIGHT)

# User input medium
input_entry = tk.Entry(input_frame, width=50)  # Adjust the width as needed
input_entry.pack()

# char counter label
character_count_label = tk.Label(input_frame, text="0/256")
character_count_label.pack()

# update_character_count event bind
input_entry.bind("<KeyRelease>", update_character_count)

# Button to trigger encoding
encode_button = tk.Button(input_frame, text="Refresh", command=encode_and_display)
encode_button.pack()

# buat folder penyimpan data matrix 
if not os.path.exists("data_matrix_images"):
    os.makedirs("data_matrix_images")

# Hapus directory at exit
atexit.register(remove_directory)

# Global variable untuk image index tracker
current_index = 0

root.mainloop()
