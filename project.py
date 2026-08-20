from PIL import Image
import os
from cryptography.fernet import Fernet

def validate_image(image):
    if not os.path.exists(image):
        raise FileNotFoundError(f"File not found: {image}")
    if not image.lower().endswith(".png"):
        raise ValueError(f"File must be a PNG: {image}")
    return True

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

def encode_message(image_path, message, output_path):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    binary_message = ''.join(f"{ord(char):08b}" for char in message + '\x00')

    for i, bit in enumerate(binary_message):
        pixel_index = i // 3
        channel_index = i % 3

        x = pixel_index % width
        y = pixel_index // width

        r, g, b = pixels[x, y]
        channels = [r, g, b]

        if bit == '1':
            channels[channel_index] = channels[channel_index] | 0b00000001
        else:
            channels[channel_index] = channels[channel_index] & 0b11111110

        pixels[x, y] = tuple(channels)

    img.save(output_path)

def decode_message(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    binary_message = ""
    message = ""

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            for channel in [r, g, b]:
                binary_message += str(channel & 1)  

                if len(binary_message) == 8:
                    char = chr(int(binary_message, 2))
                    if char == '\x00':      
                        return message
                    message += char
                    binary_message = ""    

    return message  

def decrypt_message(ciphertext_str, key):
    f = Fernet(key)
    return f.decrypt(ciphertext_str.encode()).decode()

def main():
    print("=== Steganography Tool ===")
    print("1. Encode a message")
    print("2. Decode a message")
    
    choice = input("Choose (1 or 2): ").strip()
    
    if choice == "1":
        key = None
        generate_key_choice = input("Do you want to generate a new encryption key? (y/n): ").strip().lower()
        if generate_key_choice == 'y':
            key = generate_key()
            print(f"Your encryption key: {key.decode()}")
        elif generate_key_choice == 'n':
            existing = input("Enter your existing key (or press Enter to skip encryption): ").strip()
            if existing:
                key = existing.encode()
        
        image_path = input("Enter image path: ").strip()
        message = input("Enter message to hide: ").strip()
        output_path = input("Enter output path: ").strip()
        
        encrypted = encrypt_message(message, key) if key else message
        encode_message(image_path, encrypted, output_path)
        print("Message encoded successfully!")
        
    elif choice == "2":
        generated_key = input("Enter the encryption key (leave blank if not encrypted): ").strip()
        if generated_key:
            key = generated_key.encode()
            image_path = input("Enter image path: ").strip()
            encrypted_message = decode_message(image_path)
            decrypted = decrypt_message(encrypted_message, key) if key else encrypted_message
            print(f"Decoded message: {decrypted}")
        
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()