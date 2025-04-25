from cryptography.fernet import Fernet
import os

class Crypto:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

    def encrypt_file(self, filepath):
        with open(filepath, "rb") as f:
            data = f.read()
        encrypted = self.fernet.encrypt(data)
        
        enc_path = filepath + ".enc"
        with open(enc_path, "wb") as f:
            f.write(encrypted)
        return enc_path

    def decrypt_file(self, enc_file):
        try:
            with open(enc_file.name, "rb") as f:
                encrypted = f.read()
            decrypted = self.fernet.decrypt(encrypted).decode("utf-8")
            return decrypted
        except Exception as e:
            return f"❌ Error decrypting file: {str(e)}"
