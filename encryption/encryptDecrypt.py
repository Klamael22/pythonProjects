import binascii
from Crypto.Cipher import AES 

# function to encrypt plaintext
def encrypt(key, plaintext):
    # creating the cipher object, takes the key and uses electronic codebook mode of AES
    cipher = AES.new(key, AES.MODE_ECB)
    # padding the plaintext with null bytes to ensure it is a multiple of 16 bytes
    padding = (16 - len(plaintext) % 16)
    padded_plaintext = plaintext.ljust(len(plaintext) + padding, b'\0')

    # encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)

    return ciphertext
   
# function to decrypt ciphertext
def decrypt(key, ciphertext):
    # creating the AES cipher object with the key and electronic codebook mode
    cipher = AES.new(key, AES.MODE_ECB)

    # decrypt the cyphertext
    plaintext = cipher.decrypt(ciphertext)

    # strip off any null bytes and return the plaintext
    return plaintext.rstrip(b'\0')

# encrypt or decrypt the message
def action(selection):
    if selection == 0:
        key = input("Enter the encryption key (16, 24, or 32 bytes): ").encode()
        message = input("Enter the message to ecrypt: ").encode()
        encrypted_message = encrypt(key, message)
        print("Encypted Message (in bytes): ", encrypted_message)
        encrypted_hex = binascii.hexlify(encrypted_message).decode()
        print("Encrypted Message (in hex): ", encrypted_hex)
    else:
        key = input("Enter the encryption key (16, 24, or 32 bytes): ").encode()
        message = input("Enter the message to decrypt (in hex): ").encode()
        ciphertext = binascii.unhexlify(message)
        decrypted_message = decrypt(key, ciphertext)
        print("Decrypted Message: ", decrypted_message.decode())

# get user input 
encrypt_or_decrypt = input("Encrypt(0) or decrypt(1)? ")

action(int(encrypt_or_decrypt))
