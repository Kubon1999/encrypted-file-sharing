import crypto
import sys
sys.modules['Crypto'] = crypto

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA as rsa2
from Crypto.Util.Padding import pad, unpad
import hashlib
import rsa
import secrets
from base64 import b64decode, b64encode

def stringToKey(str):
    return rsa2.importKey(str)

def getHash(password):
    return hashlib.sha256(password).digest()

def encryptRSA(hashed_Pass, data, mode):
    if mode == AES.MODE_CBC:
        cipher = AES.new(hashed_Pass, mode) # mode = AES.MODE_CBC or AES.MODE_ECB
        return b64encode(cipher.iv + cipher.encrypt(pad(data, AES.block_size)))
    else:
        cipher = AES.new(hashed_Pass, mode) # mode = AES.MODE_CBC or AES.MODE_ECB
        return b64encode( cipher.encrypt(pad(data, AES.block_size)))       

def decryptRSA(hashed_Pass,data, mode):
    string = '=' * (-len(data) % 4)
    if string:
        data = data + string.encode()
    raw = b64decode(data)
    if mode == AES.MODE_CBC:
        cipher = AES.new(hashed_Pass, mode, raw[:AES.block_size])
        return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size)
    else:
        cipher = AES.new(hashed_Pass, mode)
        return unpad(cipher.decrypt(raw), AES.block_size)

def writeRSAKey(hashed_Pass, path, key):
    f = open(path, 'wb')
    f.write(encryptRSA(hashed_Pass, key.save_pkcs1('PEM')))
    f.close()

def readRSAKey(hashed_Pass, path, mode):
    f = open(path, 'rb')
    key = f.read()
    return decryptRSA(hashed_Pass, key, mode)

def encryptWithPublicKey(public_key, data):
    return b64encode(rsa.encrypt(data.encode('UTF-8'), public_key))

def decryptWithPrivateKey(private_key, data):
    string = '=' * (-len(data) % 4)
    if string:
        data = data + string.encode()
    return rsa.decrypt(b64decode(data), private_key).decode()

def createSessionKey(len):
    return secrets.token_hex(len)