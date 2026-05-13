from random import *
from cryptography.fernet import Fernet
import base64
import os
import json

# ---------------------------- CRYPT GENERATOR ------------------------------- #
def get_key():
    if not open('key.key', 'rb').read():
        key = Fernet.generate_key()
        with open('key.key', 'wb') as key_file:
            key_file.write(key)
    else:
        with open('key.key', 'rb') as key_file:
            key = key_file.read()
    
    return Fernet(key)

def encrypt_json(data,fernet):
    json_bytes = json.dumps(data).encode('utf-8')
    encrypted_data = fernet.encrypt(json_bytes)
    return encrypted_data

def decrypt_json(encrypted_data, fernet):
    decrypted_bytes = fernet.decrypt(encrypted_data)
    json_string = decrypted_bytes.decode('utf-8')
    return json.loads(json_string)

# ---------------------------- CODE GENERATOR PASSWORD ------------------------------- #

def Generate_random_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    return password_list