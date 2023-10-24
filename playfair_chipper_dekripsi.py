import tkinter as tk
import pyperclip

def generate_playfair_matrix(key):
    key = key.replace("J", "I")
    key = "".join(dict.fromkeys(key))
    key = key.replace(" ", "")  # Hapus spasi dari kunci
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = [[0] * 5 for _ in range(5)]

    key_position = 0
    for row in range(5):
        for col in range(5):
            if key_position < len(key):
                matrix[row][col] = key[key_position]
                key_position += 1
            else:
                while True:
                    letter = alphabet[0]
                    alphabet = alphabet[1:] + letter
                    if letter not in key:
                        matrix[row][col] = letter
                        break

    return matrix

def playfair_decrypt(ciphertext, key):
    matrix = generate_playfair_matrix(key)
    ciphertext = ciphertext.replace("J", "I")  # Ganti J dengan I
    ciphertext = ciphertext.replace(" ", "")  # Hapus spasi dari ciphertext

    if len(ciphertext) % 2 != 0:
        ciphertext += 'X'

    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        row_a, col_a, row_b, col_b = 0, 0, 0, 0

        for row in range(5):
            if a in matrix[row]:
                row_a, col_a = row, matrix[row].index(a)
            if b in matrix[row]:
                row_b, col_b = row, matrix[row].index(b)

        if row_a == row_b:
            plaintext += matrix[row_a][(col_a - 1) % 5]
            plaintext += matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            plaintext += matrix[(row_a - 1) % 5][col_a]
            plaintext += matrix[(row_b - 1) % 5][col_b]
        else:
            plaintext += matrix[row_a][col_b]
            plaintext += matrix[row_b][col_a]

    return plaintext

def copy_to_clipboard():
    plaintext = plaintext_label.cget("text").replace("Plaintext: ", "")
    pyperclip.copy(plaintext)

def decrypt_button_click():
    key = key_entry.get()
    ciphertext = ciphertext_entry.get()
    matrix = generate_playfair_matrix(key)
    plaintext = playfair_decrypt(ciphertext, key)
    
    playfair_text.config(state='normal')
    playfair_text.delete(1.0, tk.END)
    for row in matrix:
        playfair_text.insert(tk.END, ' '.join(row) + '\n')
    playfair_text.config(state='disabled')
    
    plaintext_label.config(text="Plaintext: " + plaintext)

app = tk.Tk()
app.title("Playfair Cipher Decryption")
app.geometry("800x600")

key_label = tk.Label(app, text="Key(Huruf Besar) :")  # Label untuk kunci
key_label.pack()
key_entry = tk.Entry(app, width=40)  # Kotak inputan kunci yang lebih panjang
key_entry.pack()

ciphertext_label = tk.Label(app, text="Ciphertext(Huruf Besar) :")  # Label untuk ciphertext
ciphertext_label.pack()
ciphertext_entry = tk.Entry(app, width=40)  # Kotak inputan ciphertext yang lebih panjang
ciphertext_entry.pack()

decrypt_button = tk.Button(app, text="Decrypt", command=decrypt_button_click)  # Tombol "Decrypt"
decrypt_button.pack()

playfair_label = tk.Label(app, text="Playfair Matrix:")  # Label untuk matriks Playfair
playfair_label.pack()
playfair_text = tk.Text(app, height=10, width=20)  # Kotak teks untuk matriks Playfair
playfair_text.pack()
playfair_text.config(state='disabled')

plaintext_label = tk.Label(app, text="")  # Label untuk hasil plaintext
plaintext_label.pack()

copy_button = tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard)  # Tombol "Copy to Clipboard"
copy_button.pack()

app.mainloop()
