import tkinter as tk
import pyperclip

def generate_playfair_matrix(key):
    # Fungsi untuk menghasilkan matriks Playfair Cipher
    key = key.replace("J", "I")  # Ganti J dengan I
    key = "".join(dict.fromkeys(key))  # Hapus duplikat karakter
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

def playfair_encrypt(plaintext, key):
    # Fungsi untuk melakukan enkripsi Playfair Cipher
    matrix = generate_playfair_matrix(key)
    plaintext = plaintext.replace("J", "I")  # Ganti J dengan I
    plaintext = plaintext.replace(" ", "")  # Hapus spasi dari plaintext

    if len(plaintext) % 2 != 0:
        plaintext += 'X'

    ciphertext = ""

    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i + 1]
        row_a, col_a, row_b, col_b = 0, 0, 0, 0

        for row in range(5):
            if a in matrix[row]:
                row_a, col_a = row, matrix[row].index(a)
            if b in matrix[row]:
                row_b, col_b = row, matrix[row].index(b)

        if row_a == row_b:
            ciphertext += matrix[row_a][(col_a + 1) % 5]
            ciphertext += matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            ciphertext += matrix[(row_a + 1) % 5][col_a]
            ciphertext += matrix[(row_b + 1) % 5][col_b]
        else:
            ciphertext += matrix[row_a][col_b]
            ciphertext += matrix[row_b][col_a]

    return ciphertext

def copy_to_clipboard():
    # Fungsi untuk menyalin teks hasil cipher ke clipboard
    ciphertext = ciphertext_label.cget("text").replace("Ciphertext: ", "")
    pyperclip.copy(ciphertext)

def encrypt_button_click():
    # Fungsi yang dijalankan saat tombol "Encrypt" ditekan
    key = key_entry.get()
    plaintext = plaintext_entry.get()
    matrix = generate_playfair_matrix(key)
    ciphertext = playfair_encrypt(plaintext, key)
    
    # Tampilkan matriks Playfair
    playfair_text.config(state='normal')
    playfair_text.delete(1.0, tk.END)
    for row in matrix:
        playfair_text.insert(tk.END, ' '.join(row) + '\n')
    playfair_text.config(state='disabled')
    
    # Tampilkan hasil enkripsi
    ciphertext_label.config(text="Ciphertext: " + ciphertext)

app = tk.Tk()
app.title("Playfair Cipher")
app.geometry("800x600")  # Atur ukuran jendela GUI

key_label = tk.Label(app, text="Key(Huruf Besar) :")  # Label untuk kunci
key_label.pack()
key_entry = tk.Entry(app, width=40)  # Kotak inputan kunci yang lebih panjang
key_entry.pack()

plaintext_label = tk.Label(app, text="Plaintext(Huruf Besar) :")  # Label untuk plaintext
plaintext_label.pack()
plaintext_entry = tk.Entry(app, width=40)  # Kotak inputan plaintext yang lebih panjang
plaintext_entry.pack()

encrypt_button = tk.Button(app, text="Encrypt", command=encrypt_button_click)  # Tombol "Encrypt"
encrypt_button.pack()

playfair_label = tk.Label(app, text="Playfair Matrix:")  # Label untuk matriks Playfair
playfair_label.pack()
playfair_text = tk.Text(app, height=10, width=20)  # Kotak teks untuk matriks Playfair
playfair_text.pack()
playfair_text.config(state='disabled')

ciphertext_label = tk.Label(app, text="")  # Label untuk hasil ciphertext
ciphertext_label.pack()

copy_button = tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard)  # Tombol "Copy to Clipboard"
copy_button.pack()

app.mainloop()
