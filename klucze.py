from typing import KeysView
from Crypto.PublicKey import RSA
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib

#making dirs for keys if not exists
path_private = "private"
path_public = "public"
if not os.path.exists(path_private):
    os.makedirs(path_private)
if not os.path.exists(path_public):
    os.makedirs(path_public)

#length of RSA key
key_len = 2048

#generating RSA key
key = RSA.generate(key_len)

#temp password for debug
password = b'ultraStronglyStrongPassword1234556333---xdxd'

#making SHA hash of password
p1 = hashlib.sha256(password).digest()

#making a cipher from hash of password
cipher = AES.new(p1,AES.MODE_CBC)

#getting RSA keys
encrypted_RSA_Priv = key.exportKey()
encrypted_RSA_Pub = key.publickey().exportKey()

#ENCRYPT
encrypted_RSA_Priv = cipher.iv + cipher.encrypt(pad(encrypted_RSA_Priv,AES.block_size))
encrypted_RSA_Pub = cipher.iv + cipher.encrypt(pad(encrypted_RSA_Pub,AES.block_size))

#writing private key to file
f = open('private/mykey.pem','wb')
f.write(encrypted_RSA_Priv)
f.close()

#writing public key to file
f = open('public/mykey_public.pem', 'wb')
f.write(encrypted_RSA_Pub)
f.close()
