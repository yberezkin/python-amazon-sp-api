from Crypto.Util.Padding import pad

import base64
from Crypto.Cipher import AES

def fill_query_params(query, *args):
    return query.format(*args)


def sp_endpoint(path, method='GET'):
    def decorator(function):
        def wrapper(*args, **kwargs):
            kwargs.update({
                'path': path,
                'method': method
            })
            return function(*args, **kwargs)
        wrapper.__doc__ = function.__doc__
        return wrapper
    return decorator


def encrypt_aes(file_or_bytes_io, key, iv):
    key = base64.b64decode(key)
    iv = base64.b64decode(iv)
    aes = AES.new(key, AES.MODE_CBC, iv)
    try:
        return aes.encrypt(pad(bytes(file_or_bytes_io.read(), encoding='iso-8859-1'), 16))
    except UnicodeEncodeError:
        return aes.encrypt(pad(bytes(file_or_bytes_io.read(), encoding='utf-8'), 16))
    except TypeError:
        return aes.encrypt(pad(file_or_bytes_io.read(), 16))


def decrypt_aes(content, key, iv):
    key = base64.b64decode(key)
    iv = base64.b64decode(iv)
    decrypter = AES.new(key, AES.MODE_CBC, iv)
    decrypted = decrypter.decrypt(content)
    padding_bytes = decrypted[-1]
    return decrypted[:-padding_bytes]

