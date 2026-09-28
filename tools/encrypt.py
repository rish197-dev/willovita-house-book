"""Encrypt the Willovita Roots app into index.html.

Usage:
    pip install cryptography
    python3 tools/encrypt.py app.html "your-pass-phrase"

app.html is the readable app. Keep it out of the repo (it is in .gitignore).
The script swaps the encrypted payload inside index.html and leaves the login page as is.
"""
import base64, json, re, secrets, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 600_000

def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, pw = sys.argv[1], sys.argv[2]
    plain = open(src, encoding="utf-8").read().encode()
    salt, iv = secrets.token_bytes(16), secrets.token_bytes(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(pw.encode())
    ct = AESGCM(key).encrypt(iv, plain, None)
    payload = json.dumps({"s": base64.b64encode(salt).decode(), "i": base64.b64encode(iv).decode(),
                          "n": ITER, "c": base64.b64encode(ct).decode()})
    page = open("index.html", encoding="utf-8").read()
    page, n = re.subn(r"var P=\{.*?\};", lambda m: "var P=" + payload + ";", page, count=1, flags=re.S)
    if n != 1:
        sys.exit("Could not find the payload line in index.html")
    open("index.html", "w", encoding="utf-8").write(page)
    print("index.html updated")

if __name__ == "__main__":
    main()
