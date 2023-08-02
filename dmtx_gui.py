from pylibdmtx.pylibdmtx import encode
from PIL import Image, ImageTk
import tkinter as tk
import os
import shutil
import atexit

def split_input_into_chunks(input_str, chunk_size):
    return [input_str[i:i + chunk_size] for i in range(0, len(input_str), chunk_size)]

def update_character_count(*args):
    current_length = len(input_entry.get("1.0", tk.END))
    character_count_label.config(text=f"{current_length}/256")

def encode_and_display():
    global current_index

    # Reset the index to 0
    current_index = 0

    user_input = input_entry.get("1.0", tk.END)
    chunks = split_input_into_chunks(user_input, 12)
    data_matrix_images = []

    for chunk in chunks:
        encoded = encode(chunk.encode('utf8'), size="16x16")
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
        img = img.resize((700, 700), resample=Image.NEAREST)

        image_path = os.path.join("data_matrix_images", f"dmtx_{current_index}.png")
        img.save(image_path)

        current_index += 1
        data_matrix_images.append(img)

    # Reset padx to 0 before displaying the first image
    label.pack_forget()
    label.pack(side=tk.LEFT, padx=(0, 0))

    display_data_matrix(0, data_matrix_images)
    for chunk in chunks:
        encoded = encode(chunk.encode('utf8'), size="16x16")
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
        img = img.resize((700, 700), resample=Image.NEAREST)

        image_path = os.path.join("data_matrix_images", f"dmtx_{current_index}.png")
        img.save(image_path)

        current_index += 1
        data_matrix_images.append(img)

    display_data_matrix(0, data_matrix_images)

def display_data_matrix(index, data_matrix_images):
    if index < len(data_matrix_images):
        image = data_matrix_images[index]
        photo = ImageTk.PhotoImage(image)

        label.config(image=photo)
        label.image = photo

        root.after(2000, display_data_matrix, (index + 1) % len(data_matrix_images), data_matrix_images)
    else:
        label.config(text="No more DataMatrix images available")

def remove_directory():
    if os.path.exists("data_matrix_images"):
        shutil.rmtree("data_matrix_images")

root = tk.Tk()
root.title("Data Matrix")
root.geometry("1366x768")  # Set the window size to 1366x768

label = tk.Label(root, text="Barcode akan muncul disini", font=("Arial", 16))
label.pack(side=tk.LEFT, padx=(200, 0))

input_frame = tk.Frame(root)
input_frame.pack(side=tk.RIGHT)

user_input_text = tk.Label(input_frame, text="User Input:")
user_input_text.pack(anchor=tk.NW, padx=5, pady=5)

input_entry = tk.Text(input_frame, width=70, height=35)
input_entry.pack()

character_count_label = tk.Label(input_frame, text="0/256")
character_count_label.pack()

input_entry.bind("<KeyRelease>", update_character_count)

encode_button = tk.Button(input_frame, text="Encode", command=encode_and_display)
encode_button.pack()

if not os.path.exists("data_matrix_images"):
    os.makedirs("data_matrix_images")

atexit.register(remove_directory)

current_index = 0

root.mainloop()
