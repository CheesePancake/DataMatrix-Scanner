from pylibdmtx.pylibdmtx import encode
from PIL import Image, ImageTk
import tkinter as tk
import os
import shutil
import atexit

def split_input_into_chunks(input_str, chunk_size):
    # Split the input string into chunks of the specified size
    return [input_str[i:i + chunk_size] for i in range(0, len(input_str), chunk_size)]

def update_character_count(*args):
    # Update the character count label with the current input length
    current_length = len(input_entry.get())
    character_count_label.config(text=f"{current_length}/256")

def encode_and_display():
    global current_index

    # Get user input
    user_input = input_entry.get()

    # Split the input into chunks of maximum 12 characters
    chunks = split_input_into_chunks(user_input, 12)

    # Create an empty list to store the DataMatrix images
    data_matrix_images = []

    for chunk in chunks:
        # Encode each chunk and save as a separate DataMatrix image
        encoded = encode(chunk.encode('utf8'), size="16x16")
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)

        # Save the image to a directory with a unique name
        image_path = os.path.join("data_matrix_images", f"dmtx_{current_index}.png")
        img.save(image_path)

        # Increment the current image index
        current_index += 1

        # Append the image to the list
        data_matrix_images.append(img)

    # Display the first DataMatrix image initially
    display_data_matrix(0, data_matrix_images)

def display_data_matrix(index, data_matrix_images):
    # Open the specified DataMatrix image
    if index < len(data_matrix_images):
        image = data_matrix_images[index]
        photo = ImageTk.PhotoImage(image)

        # Update the label with the new image
        label.config(image=photo)
        label.image = photo

        # Schedule the next update after a delay of 2000 milliseconds (2 seconds)
        root.after(2000, display_data_matrix, (index + 1) % len(data_matrix_images), data_matrix_images)
    else:
        # If there are no more images, display an error message
        label.config(text="No more DataMatrix images available")

def remove_directory():
    # Remove the "data_matrix_images" directory and its contents
    if os.path.exists("data_matrix_images"):
        shutil.rmtree("data_matrix_images")

# Tkinter window
root = tk.Tk()
root.title("Data Matrix")

# DataMatrix display label
label = tk.Label(root)
label.pack(side=tk.LEFT)

# Frame for input and character count
input_frame = tk.Frame(root)
input_frame.pack(side=tk.RIGHT)

# User input medium
input_entry = tk.Entry(input_frame, width=50)  # Adjust the width as needed
input_entry.pack()

# Character count label
character_count_label = tk.Label(input_frame, text="0/256")
character_count_label.pack()

# Bind the input event to the update_character_count function
input_entry.bind("<KeyRelease>", update_character_count)

# Button to trigger encoding
encode_button = tk.Button(input_frame, text="Refresh", command=encode_and_display)
encode_button.pack()

# Create the directory if it doesn't exist
if not os.path.exists("data_matrix_images"):
    os.makedirs("data_matrix_images")

# Register the remove_directory function to be called on script exit
atexit.register(remove_directory)

# Global variable untuk image index tracker
current_index = 0

root.mainloop()
