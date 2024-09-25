from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os


def caesar_encrypt(plaintext: str, shift: int):
    result = []
    for char in plaintext:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            shifted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            result.append(shifted_char)
        else:
            result.append(char)
    return "".join(result)


def caesar_decrypt(ciphertext: str, shift: int):
    return caesar_encrypt(ciphertext, -shift)


def validate_vigenere_key(key: str) -> str:
    if not key or not key.isalpha():
        raise ValueError(
            "Key must be a non-empty string containing only alphabetic characters"
        )
    return key.upper()


def vigenere_encrypt(plaintext: str, key: str):
    key = validate_vigenere_key(key)
    if not plaintext:
        return ""

    result = []
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            shift = ord(key[i % len(key)].upper()) - ord("A")
            result.append(caesar_encrypt(plaintext[i], shift))
        else:
            result.append(plaintext[i])
    return "".join(result)


def vigenere_decrypt(ciphertext: str, key: str):
    key = validate_vigenere_key(key)
    if not ciphertext:
        return ""

    result = []
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            shift = ord(key[i % len(key)].upper()) - ord("A")
            result.append(caesar_encrypt(ciphertext[i], -shift))
        else:
            result.append(ciphertext[i])
    return "".join(result)


def generate_key(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt


def aes_encrypt(plaintext: str, password: str) -> tuple[str, str]:
    key, salt = generate_key(password)
    f = Fernet(key)
    encrypted = f.encrypt(plaintext.encode())
    return (
        base64.urlsafe_b64encode(encrypted).decode(),
        base64.urlsafe_b64encode(salt).decode(),
    )


def aes_decrypt(ciphertext: str, password: str, salt: str) -> str:
    key, _ = generate_key(password, base64.urlsafe_b64decode(salt))
    f = Fernet(key)
    decrypted = f.decrypt(base64.urlsafe_b64decode(ciphertext))
    return decrypted.decode()


def main():
    while True:
        print("\nEncryption/Decryption Tool")
        print("1. Caesar Cipher Encrypt")
        print("2. Caesar Cipher Decrypt")
        print("3. Vigenère Cipher Encrypt")
        print("4. Vigenère Cipher Decrypt")
        print("5. AES Encrypt")
        print("6. AES Decrypt")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            plaintext = input("Enter the plaintext: ")
            shift = int(input("Enter the shift value: "))
            result = caesar_encrypt(plaintext, shift)
            print(f"Encrypted text: {result}")

        elif choice == "2":
            ciphertext = input("Enter the ciphertext: ")
            shift = int(input("Enter the shift value: "))
            result = caesar_decrypt(ciphertext, shift)
            print(f"Decrypted text: {result}")

        elif choice == "3":
            plaintext = input("Enter the plaintext: ")
            key = input("Enter the key: ")
            result = vigenere_encrypt(plaintext, key)
            print(f"Encrypted text: {result}")

        elif choice == "4":
            ciphertext = input("Enter the ciphertext: ")
            key = input("Enter the key: ")
            result = vigenere_decrypt(plaintext, key)
            print(f"Decrypted text: {result}")

        elif choice == "5":
            plaintext = input("Enter the plaintext: ")
            password = input("Enter the password: ")
            ciphertext, salt = aes_encrypt(plaintext, password)
            print(f"Encrypted text: {ciphertext}")
            print(f"Salt: {salt}")

        elif choice == "6":
            ciphertext = input("Enter the ciphertext: ")
            password = input("Enter the password: ")
            salt = input("Enter the salt: ")
            result = aes_decrypt(ciphertext, password, salt)
            print(f"Encrypted text: {result}")

        elif choice == "7":
            print("Thank you for using the Encryption/Decryption Tool. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
