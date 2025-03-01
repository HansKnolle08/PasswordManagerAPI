# /src/packages/log.py
# Copyright (C) 2025 H.-C. Knolle
# Licensed under the MIT License
# Simple logging message module

def log(message: str) -> None:
    """Returns a log Message."""
    print(f"[LOG] {message}")