#!/usr/bin/env python3

import sys
import json
import os
from time import sleep

def parse_hex_signature(hex_str):
    clean = ""
    for line in hex_str.strip().splitlines():
       
        if '(' in line:
            line = line.split('(', 1)[0]
       
        clean += ''.join(ch for ch in line if ch.upper() in "0123456789ABCDEF")
   
    if len(clean) % 2 != 0:
        clean = clean[:-1]  
    return clean

def hex_to_bytes(hex_str):
    if not hex_str:
        return b""
    try:
        return bytes(int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2))
    except ValueError as e:
        raise ValueError(f"Invalid hex string: {hex_str}") from e

def parse_offset(offset_str):
    if not offset_str or offset_str.strip().lower() in ('any', ''):
        return 0
    try:
        return int(offset_str.strip())
    except ValueError:
        return 0  

def main():
    if len(sys.argv) != 2:
        print("Usage: main.py <filename>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print(f"Error: File '{filepath}' does not exist.", file=sys.stderr)
        sys.exit(1)

    
    with open(filepath, "rb") as f:
        file_start = f.read(32)  

    sig_file = "../assets/file_sigs.json"
    try:
        with open(sig_file, "r") as sf:
            signatures = json.load(sf)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading signatures: {e}", file=sys.stderr)
        sys.exit(1)

    detected_ext = [] 
    identified_magic_bytes = b''
    file_type = ''
    is_legit_file = False  # has file type - can it be identified?
    for entry in signatures:
        file_type = entry.get("Description", "Unknown")
        ext = entry.get("Extension", "unknown")
        hex_sig_raw = entry.get("Hex signature", "")
        offset_str = entry.get("Offset", "0")

        offset = parse_offset(offset_str)
        
        hex_clean = parse_hex_signature(hex_sig_raw)
        if not hex_clean:
            continue

        magic_bytes = hex_to_bytes(hex_clean)
       
        end = offset + len(magic_bytes)
        if end > len(file_start):
            continue  

        if file_start[offset:end] == magic_bytes:
            detected_ext = ext
            identified_magic_bytes = magic_bytes
            is_legit_file = True
            break 

    file_ext = os.path.splitext(filepath)[1].lstrip('.').lower()
    file_name = os.path.basename(filepath)

    print(f"""
File Type Analysis
    Name: {file_name}
    Extension: {file_ext}
    Type: {file_type}
    Identified Header Hex: {identified_magic_bytes.hex()}
    """)

    print("\nChecking if file matches what it claims to be...\n")
    sleep(1)

    if file_ext in detected_ext:
        print("Legit file! The file extension matches the actual file type.")
    else:
        if "unknown" not in detected_ext and is_legit_file:
            print(f"Mismatch in extensions! File claims '.{file_ext}', but content suggests one of these: '.{' .'.join(detected_ext)}'")
        else:
            print("Unknown File Type! Maybe ASCII text or a raw data?!")

if __name__ == "__main__":
    main()
