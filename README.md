# AFKJ-Metadatadecrypt

## Script Description
This script extracts decrypted global-metadata.dat from AFK Journey by utilizing debug strings of NEP2.

## Requirements
1. Python
2. Required Modules:
   - Elevate
   - Windbgmon
   - Pymem

## How to Use
1. Run the `Decrypt.py` and launch AFK Journey.
2. If you want the dumped metadata to be compatible with Il2CPPDumper, Bepinex, etc., enter `0` when prompted.
3. The `decrypted-global-metadata.dat` file will be created in the directory where you ran the Python script.

### Note
The underlying logic is not owned by me; I've only made minor adjustments for personal use.
