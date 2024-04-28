import base64
import os


def encrypt(text):
    encrypted_text = ""
    for char in text:
        encrypted_char = chr(ord(char) + 8)
        encrypted_text += encrypted_char
    encrypted_text = base64.b64encode(encrypted_text.encode()).decode()
    return encrypted_text


def decrypt(encrypted_text):
    decrypted_text = base64.b64decode(encrypted_text).decode()
    decrypted_result = ""
    for char in decrypted_text:
        decrypted_char = chr(ord(char) - 8)
        decrypted_result += decrypted_char
    return decrypted_result


def ncssourl():
    return decrypt("cHx8eEI3N8KBa212azbCgW1teGnCgTZrd3VCOzg8Ojo3woF9cWk1e216fnFrbTVqd3t7N2l9fHA3eHpxdmtxeGl0")


def innerssourl():
    return decrypt("cHx8eEI3N8KBfXFpNntten5xa202and7ezbCgXhCOzg8Ojo3woF9cWk1e216fnFrbTVqd3t7N2l9fHA3eHpxdmtxeGl0")


def ssourl():
    url = ncssourl() if os.getenv("DEPLOY_ENV") == "LOCAL" else innerssourl()
    return url

def enabledsso():
    return False if os.getenv("DEPLOY_ENV") == "LOCAL" else True



