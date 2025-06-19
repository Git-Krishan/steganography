# Simple Image Steganography Tool

This is a simple Python tool to **hide secret messages inside PNG images** using **password-protected encryption** and **least significant bit (LSB) steganography**.

---

## Features

- Encrypts your message with a password before hiding it
- Hides message bits inside image pixels (PNG only — lossless format)
- Supports hiding and recovering messages of variable length
- Simple command-line interface (CLI)
- Cross-platform (Windows, macOS, Linux)
- Automatically opens the encoded image after hiding a message

---

## Requirements

- Python 3.6 or higher
- [cryptography](https://cryptography.io/en/latest/) Python package

Install dependencies with:

```bash
pip install cryptography opencv-python
