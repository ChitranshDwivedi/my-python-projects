# Pixel Secrets — A Steganography Tool
#### Video Demo: <URL HERE>
#### Description:

## What if you could hide a message inside a Pikachu?

No, seriously. That's what this project does.

**Pixel Secrets** is a command-line steganography tool written in Python. It lets you embed a secret text message inside a PNG image — invisibly — by flipping the least significant bit of each color channel in the image's pixels. To anyone looking at the image, it's just... a Pikachu. But if you know the tool exists, you can pull the hidden message right back out. Optionally, you can also encrypt the message with Fernet symmetric encryption before hiding it, so even if someone finds the tool, they still can't read your secret without the key.

This is my final project for Harvard's CS50P — Introduction to Programming with Python.

---

## The Big Idea: How Does Steganography Actually Work?

Every pixel in a PNG image is made up of three color channels: Red, Green, and Blue. Each channel is a number from 0 to 255. In binary, that's 8 bits — for example, the number 36 in binary is `00100100`.

The *last* bit — the Least Significant Bit, or LSB — has almost no effect on the color. Flipping it changes the color value by exactly 1 out of 255. Human eyes cannot detect that. Monitors cannot render that. It's invisible.

So: if you take a message, convert every character to its 8-bit binary representation, and overwrite the LSBs of the image's color channels with those bits — you've hidden the message inside the image. To decode it, you just read those LSBs back out and reconstruct the characters.

That's the whole trick. Simple in concept, genuinely cool in practice.

---

## Project Files

### `project.py`

This is the main file — the whole program lives here. It contains five functions:

**`validate_image(image)`**
The bouncer. Before anything touches an image file, this function checks that the file actually exists (`os.path.exists()`) and that it ends with `.png` (case-insensitive, so `.PNG` works too). If either check fails, it raises an appropriate exception — `FileNotFoundError` or `ValueError`. It returns `True` if the image passes both checks. The reason this is a standalone function rather than inline logic inside `encode_message` and `decode_message` is reusability and testability — pytest can test this independently, and both encode and decode can call it without duplicating the checks.

**`encode_message(image, message)`**
The hider. This function opens the image with Pillow, converts the message to a binary string using `f"{ord(char):08b}"` for each character (which gives you the 8-bit binary representation of the character's ASCII code), then appends a null byte `\x00` as a delimiter so the decoder knows where the message ends. Then it loops through the binary string bit by bit, maps each bit position to a pixel and channel (`pixel_index = i // 3`, `channel_index = i % 3`), and flips the LSB of that channel to match the current bit using bitwise AND and OR operations. The modified image is saved with `_encoded` appended to the filename so the original is never overwritten.

**`decode_message(image)`**
The revealer. This does `encode_message` in reverse — reads LSBs from each channel, one bit at a time, assembles them into 8-bit chunks, converts each chunk back to a character with `chr(int(bits, 2))`, and stops the moment it hits the `\x00` delimiter. The reconstructed string is returned.

**`encrypt_message(message, key)` and `decrypt_message(ciphertext, key)`**
The optional security layer. These wrap the `cryptography` library's Fernet implementation. `encrypt_message` takes a plaintext string and a Fernet key (bytes), encrypts it, and returns the ciphertext as a string (`.decode()` to bridge bytes → string). `decrypt_message` reverses this — takes the ciphertext string, re-encodes it to bytes, decrypts with the key, and returns the original plaintext. Fernet is symmetric-key authenticated encryption — fast, safe, and built for exactly this kind of use case.

**`generate_key()`**
A one-liner wrapper around `Fernet.generate_key()`. Having it as a named function makes it testable in pytest and keeps `main()` clean.

**`main()`**
The user-facing CLI. It asks whether you want to encode or decode, takes the image path and message (or just image path for decode), optionally handles encryption/decryption, and runs the appropriate pipeline. The encode path always generates a fresh key and displays it — the user must save it, because it's never stored anywhere. The decode path asks for the key if the message was encrypted, or lets you skip if it wasn't. The `if key else message` pattern handles the optional encryption cleanly without nested conditionals everywhere.

---

### `test_project.py`

Seven pytest tests, all passing:

- `test_generate_key()` — verifies `generate_key()` returns valid bytes that Fernet can accept without exploding
- `test_encrypt_message()` — checks that the output is a string and is not just the plaintext sitting there unencrypted
- `test_encrypt_wrong_key()` — verifies that using the wrong key during decryption raises an exception (Fernet is authenticated, so it won't silently return garbage)
- `test_decrypt_message()` — full roundtrip: encrypt then decrypt, assert the output matches the original
- `test_validate_image_valid()` — creates a real PNG in memory using `Image.new()` and checks that `validate_image()` returns `True`
- `test_validate_image_invalid()` — checks that a `.jpg` extension raises `ValueError`
- `test_validate_image_not_found()` — checks that a nonexistent file raises `FileNotFoundError`

Test images are generated programmatically with `Image.new()` rather than shipping an actual image file with the project. This keeps the repo clean and the tests fully self-contained.

---

### `requirements.txt`

```
Pillow
cryptography
```

Two libraries. That's it.

---

## Design Decisions Worth Explaining

**Why PNG and not JPEG?**
JPEG uses lossy compression — it slightly modifies pixel values when saving to reduce file size. That would destroy the hidden bits. PNG is lossless, so what you write is exactly what you get back. This is non-negotiable for steganography.

**Why a null byte `\x00` as delimiter?**
The decoder needs to know when the message ends. The null byte is a clean sentinel — it's not a printable character, so it won't appear in any normal message, and it's the standard string terminator in C (which is where CS50 started, so it felt fitting). An alternative would be prepending the message length, but that requires storing and reading a fixed-width header — more code, more surface area for bugs.

**Why keep encryption and encoding as separate functions instead of combining them?**
Clean separation of concerns. `encode_message` doesn't care whether the message was encrypted or not — it just hides bits. `encrypt_message` doesn't care about images. Keeping them separate makes each function independently testable, independently reusable, and much easier to reason about. The boundary conversion (`.encode()` / `.decode()` to move between bytes and strings) happens in `main()` where the two pipelines connect.

**Why not store the key in the image?**
Because then what's the point? The whole threat model assumes someone might find the image. If the key is in the image, it's game over. The key lives with the person who encoded the message — that's the security model.

---

## How to Run It

```bash
pip install Pillow cryptography
python project.py
```

Follow the prompts. If you're encoding, save the key it gives you — there's no recovery if you lose it.

---

Built with Python, Pillow, and an unhealthy obsession with binary arithmetic.
