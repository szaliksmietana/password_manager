import subprocess

GPG_FILE="password.gpg"


def encrypt_data(data):
    process = subprocess.Popen(
        ["gpg", "--yes", "-o", GPG_FILE, "--symmetric", "--cipher-algo", "AES256"],
        stdin=subprocess.PIPE
    )
    process.communicate(input=data.encode()) 

def decrypt_data():
    process = subprocess.Popen(
        ["gpg", "-d", GPG_FILE],
        stdout=subprocess.PIPE
    )
    output, _ = process.communicate()
    return output.decode()
    