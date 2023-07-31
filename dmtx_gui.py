from pylibdmtx.pylibdmtx import encode
from PIL import Image, ImageTk
import tkinter as tk

def encode_and_display():
    # get user input
    user_input = input_entry.get()

    # Encode the user input
    encoded = encode(user_input.encode('utf8'))
    img = Image.frombytes('RGB', (encoded.height, encoded.width), encoded.pixels)
    img.save('dmtx.png')

    # real time refresh update
    image = Image.open("dmtx.png")
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

#tkinter window
root = tk.Tk()
root.title("Data Matrix")

# user input medium
input_entry = tk.Entry(root)
input_entry.pack()

# button untuk trigger encoding
encode_button = tk.Button(root, text="Refresh", command=encode_and_display)
encode_button.pack()

# Label display
label = tk.Label(root)
label.pack()



root.mainloop()
