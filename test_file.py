# /test_file.py
# Copyright (C) 2025 H.-C. Knolle
# Licensed under the MIT License
# PasswordManagerAPI Test File

###########
# Imports #
###########
import os
import time
from src.package.PWM_ApiBase import PasswordManagerAPI

###########
# Globals #
###########
def log_test(message: str) -> None:
    print(f"[TEST] {message}")
    time.sleep(1)

###########
# Testing #
###########
def run_tests() -> None:
    """Runs a series of tests on the PasswordManagerAPI."""
    test_dir: str = "test_json"
    os.makedirs(os.path.join(test_dir, "data"), exist_ok=True)
    api: PasswordManagerAPI = PasswordManagerAPI(data_dir=test_dir)
    
    log_test("Testing user registration...")
    try:
        api.register_user("testuser", "test@example.com", "securepass")
        log_test("User registration successful.")
    except Exception as e:
        log_test(f"User registration failed: {e}")
    
    log_test("Testing duplicate user registration...")
    try:
        api.register_user("testuser", "test@example.com", "anotherpass")
        log_test("Error: Duplicate user registration did not raise an error!")
    except ValueError:
        log_test("Duplicate user registration correctly prevented.")
    
    log_test("Testing login...")
    try:
        api.login("testuser", "securepass")
        if api.get_active_user() == "testuser":
            log_test("Login successful.")
        api.logout()
        if api.get_active_user() is None:
            log_test("Logout successful.")
    except Exception as e:
        log_test(f"Login test failed: {e}")
    
    log_test("Testing add and retrieve entry...")
    try:
        api.login("testuser", "securepass")
        api.add_entry("GitHub", "testuser_github", "password123")
        entry: dict = api.get_entry("GitHub")
        if entry["username"] == "testuser_github" and entry["password"] == "password123":
            log_test("Entry addition and retrieval successful.")
    except Exception as e:
        log_test(f"Entry test failed: {e}")
    
    log_test("Testing entry removal...")
    try:
        api.remove_entry("GitHub")
        try:
            api.get_entry("GitHub")
            log_test("Error: Entry was not removed correctly!")
        except ValueError:
            log_test("Entry removal successful.")
    except Exception as e:
        log_test(f"Entry removal test failed: {e}")
    
    log_test("Testing user deletion...")
    try:
        api.delete_user("testuser")
        if "testuser" not in api.users:
            log_test("User deletion successful.")
    except Exception as e:
        log_test(f"User deletion test failed: {e}")

###############
# Entry Point #
###############
if __name__ == "__main__":
    run_tests()
