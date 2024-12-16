from cryptography.fernet import Fernet

# Use a key generation process or a fixed secret key for simplicity
SECRET_KEY = Fernet.generate_key()
cipher_suite = Fernet(SECRET_KEY)

def encrypt_message(message: str) -> str:
    encrypted = cipher_suite.encrypt(message.encode())
    return encrypted.decode()

def decrypt_message(encrypted_message: str) -> str:
    decrypted = cipher_suite.decrypt(encrypted_message.encode())
    return decrypted.decode()
