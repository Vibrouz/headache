# Headache 

A simple Python tool for analyzing file types by scanning their magic bytes (file headers) and detecting mismatches between file extensions and actual file content.This tool is built for learning how file type detection works. 

## Summary

Headache reads the first 32 bytes of a file and compares them against a database of known file signatures (magic bytes). It tells you what type of file it actually is, and optionally flags suspicious extension mismatches (e.g., a `.jpg` file that's actually a `.exe`).

## Motivation
I and my friend (@Barok-y) built this mini project together to understand how file type detection works at the binary level (magic bytes), parsing and matching binary signatures from a CSV database, how attackers might disguise malicious files by changing extensions, Basic CLI argument parsing and colored terminal output in Python

This is a learning tool, not a production security system.

## Features

- **Magic byte detection**: Reads the first 32 bytes of a file and matches them against 100+ known file signatures
- **Extension validation**: Compares the claimed file extension against the detected file type
- **Mismatch alerts**: Flags suspicious cases where extension doesn't match the real file type (e.g., `.jpg` file with `.exe` magic bytes)
- **Colorized output**: Color-coded CLI output for easy reading (green for legit, red for suspicious, yellow for unknown)
- **CSV-to-JSON conversion**: Converts a CSV signature database to JSON for efficient lookups

## Quick start

1. **Clone and navigate**:
   ```bash
   git clone https://github.com/Vibrouz/headache.git
   cd headache

2. **Run a basic scan**:
   ```bash
   python main.py sample.pdf
   ```
3. **Check for extension mismatches**:
   ```bash 
   python main.py suspicious_file.jpg --check 
   ```


