from base64 import b64decode
def decodeAuth(string):
    data = b64decode(string.split(" ")[1].encode("ascii")).decode("ascii").split(":")
    return (data[0], data[1])