#!/usr/bin/env python3

import sys
import json
import os

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

    detected_ext = "Unknown"
    for entry in signatures:
        ext = entry.get("Extension", "Unknown")
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
            break 

    given_ext = os.path.splitext(filepath)[1].lstrip('.').lower()
    detected_ext = detected_ext.lower()

    if given_ext == detected_ext:
        print("The file extension matches the actual file type.")
    else:
        print(f"Mismatch in extensions! File claims '.{given_ext}', but content suggests '.{detected_ext}'.")

if __name__ == "__main__":
    main()