import random
import string
import pyperclip

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$^&*"
    return "".join(random.choice(chars) for _ in range(length))

def copy_clipboard(text):
    pyperclip.copy(text)

def l1ne():
    print("===========================")