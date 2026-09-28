SMART REPAIR EDITION BY ALI GAMES - FIX 2

This build removes the stale card_informasi reference that caused:
AttributeError: App object has no attribute card_informasi

IMPORTANT: Build this ZIP from a fresh GitHub Actions run. Do not reuse an old artifact.
The workflow verifies main.py contains no card_informasi reference before PyInstaller.

The current application is a UI/prototype shell. Native WETOOL operations remain in the original wetool.exe.
