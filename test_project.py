from project import generate_key, encrypt_message, decrypt_message, validate_image
from cryptography.fernet import Fernet
import pytest

def test_encrypt_message():
    key = generate_key()
    ciphertext = encrypt_message("hello", key)
    assert ciphertext != "hello"  # actually encrypted
    assert isinstance(ciphertext, str)  # returns a string

def test_encrypt_wrong_key():
    key1 = generate_key()
    key2 = generate_key()
    ciphertext = encrypt_message("hello", key1)
    with pytest.raises(Exception):
        decrypt_message(ciphertext, key2)  # wrong key should fail

def test_generate_key():
    key = generate_key()
    assert isinstance(key, bytes)
    Fernet(key)  # if the key is invalid, this line throws an error

def test_decrypt_message():
    key = generate_key()
    message = "hello"
    assert decrypt_message(encrypt_message(message, key), key) == message

def test_validate_image_valid():
    assert validate_image("Pikachu.png") == True

def test_validate_image_invalid():
    with pytest.raises(FileNotFoundError):
        validate_image("image.jpg")

def test_validate_image_not_found():
    with pytest.raises(FileNotFoundError):
        validate_image("ghost.png")
