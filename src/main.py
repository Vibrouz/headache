import sys
import json
if len(sys.argv) < 2:
    print("The file format should be main.py <filename>")

with open(sys.argv[1],"rb") as file:
    file.seek(0)
    magic_string=file.read(32)

with open("../assets/file_sigs.json","r") as file_sig:
    data=json.load(file_sig)
    extension=""
    for entity in data:
        for sig_line in entity["Hex signature"].split("\n"):
            hex_sign=""
            for ch in sig_line:
                if ch =="(": break
                if ch.upper() in "1234567890ABCDEF":
                    hex_sign+=ch
        magic_bytes=bytes(int(hex_sign[i:i+2],16)%256 for i in range(0,len(hex_sign),2))
        offset= entity.get("offset",0)
        if magic_string[offset:offset+len(magic_bytes)] == magic_bytes:
            print("ENtity Extension: ", entity.get("Extension","Unknown"))
            extension = entity.get("Extension","Unknown")
            break;
ext=sys.argv[1].split(".")[1]
print(ext)
print(extension)
if ext == extension:
    print("The file extension and the extension written on the back of your file are similar ")
else:
    print("Mismatch in Extensions")

