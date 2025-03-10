import tkinter as tk
from tkinter import *
from tkinter import ttk

def caesar_decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - shift_base - shift) % 26 + shift_base)
            decrypted_text += new_char
        else:
            decrypted_text += char
    return decrypted_text

def decrypt_message():
    shift = int(shift_var.get())
    encrypted_text = input_text.get("1.0", tk.END).strip()  # Get text from Text widget
    decrypted_text = caesar_decrypt(encrypted_text, shift)
    output_label.config(text=f"Decrypted Text:\n{decrypted_text}")

# Create the main window
root = tk.Tk()
root.title("Caesar Cipher Decryptor")
root.geometry("400x300")

# Input Text Widget
tk.Label(root, text="Enter Encrypted Text:").pack(pady=5)
input_text = tk.Text(root, height=5, width=40)
input_text.pack()

# Shift Selector
tk.Label(root, text="Select Shift Value:").pack(pady=5)
shift_var = tk.StringVar(value="3")
shift_spinner = ttk.Spinbox(root, from_=1, to=25, textvariable=shift_var, width=5)
shift_spinner.pack()

# Decrypt Button
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_message)
decrypt_button.pack(pady=10)

# Output Label
output_label = tk.Label(root, text="Decrypted Text:", wraplength=350, justify="center")
output_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
