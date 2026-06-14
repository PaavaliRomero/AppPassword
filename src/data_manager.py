from pathlib import Path
from random import *
from cryptography.fernet import Fernet
import json
import sys
# ---------------------------- CODE GENERATOR PASSWORD ------------------------------- #
if getattr(sys, 'frozen', False):
    DATA_DIR = Path(sys.executable).parent   # key.key junto al .exe
else:
    DATA_DIR = Path(__file__).parent.parent

KEY_FILE = DATA_DIR / "key.key"

if KEY_FILE.exists():
    key = KEY_FILE.read_bytes()
else:
    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
fernet = Fernet(key)


def Encrypted_Message(data):
    bytes_text = json.dumps(data).encode('utf-8')
    encrypted = fernet.encrypt(bytes_text)
    return encrypted

def Decrypted_Message(encrypted):
    decrypted = fernet.decrypt(encrypted)
    return json.loads(decrypted.decode('utf-8'))
    

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
