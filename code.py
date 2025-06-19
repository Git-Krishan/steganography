import cv2, base64, os, platform
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Create a secret key from a password
def get_key(password):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                     salt=b'stego_salt', iterations=100000,
                     backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Convert text to binary (0s and 1s)
def text_to_bin(text): return ''.join(f'{ord(c):08b}' for c in text)

# Convert binary back to text
def bin_to_text(bin_data): return ''.join(chr(int(bin_data[i:i+8], 2)) for i in range(0, len(bin_data), 8))

# Open image in default viewer (Windows/Mac/Linux)
def open_image(path):
    cmd = 'start' if platform.system() == 'Windows' else 'open' if platform.system() == 'Darwin' else 'xdg-open'
    os.system(f'{cmd} {path}')

# Hide a secret message inside an image
def encode(image_in, image_out, message, password):
    img = cv2.imread(image_in)
    if img is None: return print("❌ Image not found.")

    # Encrypt and encode message
    key = get_key(password)
    encrypted = Fernet(key).encrypt(message.encode())
    encoded = base64.b64encode(encrypted).decode()
    length = f"{len(encoded):08d}"  # store 8-digit length
    data = text_to_bin(length + encoded)

    flat = img.flatten()
    if len(data) > len(flat):
        return print("❌ Message too long for this image.")

    # Hide bits in image pixels
    for i, bit in enumerate(data): flat[i] = (flat[i] & ~1) | int(bit)
    cv2.imwrite(image_out, flat.reshape(img.shape))
    print(f"✅ Message hidden in '{image_out}'")
    open_image(image_out)

# Extract hidden message from image
def decode(image_path, password):
    img = cv2.imread(image_path)
    if img is None: return print("❌ Image not found.")

    flat = img.flatten()
    bits = ''.join(str(flat[i] & 1) for i in range(4096))  # read first 512 bytes
    length = int(bin_to_text(bits[:64]))  # first 8 chars = message length
    total = (8 + length) * 8

    if total > len(flat):
        return print("❌ Message is incomplete or image is corrupted.")

    data_bits = ''.join(str(flat[i] & 1) for i in range(total))
    encoded = bin_to_text(data_bits[64:])

    try:
        key = get_key(password)
        decrypted = Fernet(key).decrypt(base64.b64decode(encoded)).decode()
        print("✅ Secret message:", decrypted)
    except:
        print("❌ Wrong password or message damaged.")

# ----------- Main Menu -----------

def main():
    in_img = "mypic.png"
    out_img = "hidden.png"
    choice = input("(E)ncode or (D)ecode? ").strip().lower()

    if choice == 'e':
        msg = input("Enter your secret message: ")
        pwd = input("Create a password: ")
        encode(in_img, out_img, msg, pwd)
    elif choice == 'd':
        pwd = input("Enter password to decrypt: ")
        decode(out_img, pwd)
    else:
        print("❌ Choose E to encode or D to decode.")

if __name__ == "__main__":
    main()
