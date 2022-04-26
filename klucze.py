from typing import KeysView
from Crypto import Random
from Crypto.PublicKey import RSA
import os

path_private = "private"
path_public = "public"
if not os.path.exists(path_private):
    os.makedirs(path_private)
if not os.path.exists(path_public):
    os.makedirs(path_public)

key_len = 2048

key = RSA.generate(key_len)
f = open('private/mykey.pem','wb')
f.write(key.exportKey('PEM'))
f.close()

f = open('public/mykey_public.pem', 'wb')
f.write(key.publickey().exportKey('PEM'))
f.close()

f = open('private/mykey.pem','rb')
key1 = RSA.import_key(f.read())
f.close()
print(key1.exportKey().decode())

f = open('public/mykey_public.pem','rb')
key2 = RSA.import_key(f.read())
f.close()
print(key2.exportKey().decode())


"""
key manager:

1. generowanie kluczy jesli nie istnieja
1.1 zabezpieczenie ich haslem
1.2 haslo to hash (SHA) z hasla "user friendly" wpisanego przez uzytkownika
2. odszyfrowanie kluczy za pomoca hashu hasla




"""
