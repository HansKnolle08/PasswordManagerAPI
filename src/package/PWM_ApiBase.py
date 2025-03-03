# /src/PWM_ApiBase.py
# Copyright (C) 2025 H.-C. Knolle
# Licensed under the MIT License
# PasswordManagerAPI Base Source Code

"""Base source code for the Password Manager API."""

###########
# Imports #
###########
import json
import os
import hashlib
from time import sleep

###########
# Globals #
###########
def log(message: str) -> None:
    """Returns a log Message."""
    print(f"[LOG] {message}")

json_base_dir: str = os.path.join(os.path.dirname(__file__), "json")

#################################
# PasswordManagerAPI Main-Class #
#################################
class PasswordManagerAPI:
    """Main class for the Password Manager API."""
    def __init__(self: 'PasswordManagerAPI', data_dir: str = json_base_dir) -> None:
        self.data_dir: str = data_dir
        self.users_file: str = os.path.join(self.data_dir, "users.json")
        self.active_user: str | None = None
        self.users: dict[str, dict[str, str]] = {}
        self._load_users()
    
    def _load_users(self: any) -> None:
        """Load the userlist from users.json or create a new file."""
        log("Load Userlist...")
        if os.path.exists(self.users_file):
            with open(self.users_file, "r", encoding="utf-8") as file:
                try:
                    self.users: dict[str, dict[str, str]] = json.load(file)
                except json.JSONDecodeError:
                    log("Error with loading userlist. Creating new file.")
                    self.users: dict[str, dict[str, str]] = {}
        else:
            log("No userlist found. Creating new file.")
            self.users: dict[str, dict[str, str]] = {}
            self._save_users()
    
    def _save_users(self: 'PasswordManagerAPI') -> None:
        """Saving the current userlist in users.json."""
        log("Saving userlist...")
        with open(self.users_file, "w", encoding="utf-8") as file:
            json.dump(self.users, file, indent=4)
    
    def _hash_password(self: 'PasswordManagerAPI', password: str) -> str:
        """Creates secure sha256 hash of user password."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self: 'PasswordManagerAPI', username: str, email: str, password: str) -> None:
        """Creates new user and saves it to users.json."""
        if username in self.users:
            log(f"Error: Username '{username}' already in use.")
            raise ValueError(f"Username '{username}' already in use.")
        
        log(f"Register new user: {username}")
        self.users[username] = {
            "email": email,
            "password": self._hash_password(password)
        }
        self._save_users()
        
        user_data_file: str = os.path.join(self.data_dir, "data", f"{username}.json")
        if not os.path.exists(user_data_file):
            with open(user_data_file, "w", encoding="utf-8") as file:
                json.dump({"accounts": {}}, file, indent=4)
        log(f"User data for {username} created.")

    def delete_user(self: 'PasswordManagerAPI', username: str) -> None:
        """Deletes user and related data.""" 
        if username not in self.users:
            log(f"Error: User '{username}' doesn't exist.")
            raise ValueError(f"Error: User '{username}' doesn't exist.")
        
        log(f"Deleting user: {username}")
        
        del self.users[username]
        self._save_users()
        
        # Delete the user data file
        user_data_file = os.path.join(self.data_dir, "data", f"{username}.json")
        if os.path.exists(user_data_file):
            os.remove(user_data_file)
            log(f"User data for {username} deleted.")
        else:
            log(f"Warning: User data file for {username} not found.")
        
    def login(self: 'PasswordManagerAPI', username: str, password: str) -> None:
        """Logs in a user if the credentials are correct."""
        log(f"Attempting login for user: {username}")
        if username in self.users and self.users[username]["password"] == self._hash_password(password):
            self.active_user = username
            log(f"User {username} successfully logged in.")
        else:
            log("Failed login attempt.")
            raise ValueError("Invalid login credentials.")
    
    def logout(self: 'PasswordManagerAPI') -> None:
        """Logs out the current user."""
        if self.active_user:
            log(f"User {self.active_user} is logging out.")
        self.active_user = None
    
    def get_active_user(self: 'PasswordManagerAPI') -> str | None:
        """Returns the currently logged-in user or None if no one is logged in."""
        return self.active_user
    
    def add_entry(self: 'PasswordManagerAPI', service: str, username: str, password: str) -> None:
        """Adds a new entry for the currently logged-in user."""
        if not self.active_user:
            log("Error: No user logged in.")
            raise ValueError("No user logged in.")
        
        user_data_file: str = os.path.join(self.data_dir, "data", f"{self.active_user}.json")
        with open(user_data_file, "r", encoding="utf-8") as file:
            data: dict = json.load(file)
        
        data["accounts"][service] = {"username": username, "password": password}
        
        with open(user_data_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        log(f"New entry for {service} added.")
    
    def remove_entry(self: 'PasswordManagerAPI', service: str) -> None:
        """Removes an entry for the currently logged-in user."""
        if not self.active_user:
            log("Error: No user logged in.")
            raise ValueError("No user logged in.")
        
        user_data_file: str = os.path.join(self.data_dir, "data", f"{self.active_user}.json")
        with open(user_data_file, "r", encoding="utf-8") as file:
            data: dict = json.load(file)
        
        if service in data["accounts"]:
            del data["accounts"][service]
            with open(user_data_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            log(f"Entry for {service} removed.")
        else:
            log(f"Error: No entry found for {service}.")
            raise ValueError("Entry not found.")
        
    def get_entry(self: 'PasswordManagerAPI', service: str) -> dict[str, str]:
        """Returns the entry for the currently logged-in user."""
        if not self.active_user:
            log("Error: No user logged in.")
            raise ValueError("No user logged in.")
        
        user_data_file: str = os.path.join(self.data_dir, "data", f"{self.active_user}.json")
        with open(user_data_file, "r", encoding="utf-8") as file:
            data: dict = json.load(file)
        
        if service in data["accounts"]:
            log(f"Entry for {service} found.")
            return data["accounts"][service]
        else:
            log(f"Error: No entry found for {service}.")
            raise ValueError("Entry not found.")
        
    def update_email(self: 'PasswordManagerAPI', username: str, new_email: str) -> None:
        """Updates the email address of a registered user."""
        if username not in self.users:
            log(f"Error: User '{username}' doesn't exist.")
            raise ValueError(f"User '{username}' doesn't exist.")
        
        log(f"Updating email for user: {username}")
        self.users[username]["email"] = new_email
        self._save_users()
        log(f"Email for user {username} updated to {new_email}.")

    def change_password(self: 'PasswordManagerAPI', old_password: str, new_password: str) -> None:
        """Changes the password of the currently logged-in user."""
        if not self.active_user:
            log("Error: No user logged in.")
            raise ValueError("No user logged in.")
        
        if self.users[self.active_user]["password"] != self._hash_password(old_password):
            log("Error: Incorrect old password.")
            raise ValueError("Incorrect old password.")
        
        log(f"Changing password for user: {self.active_user}")
        self.users[self.active_user]["password"] = self._hash_password(new_password)
        self._save_users()
        log("Password changed successfully.")

    def list_all_entries(self: 'PasswordManagerAPI') -> dict[str, dict[str, str]]:
        """Lists all entries for the currently logged-in user."""
        if not self.active_user:
            log("Error: No user logged in.")
            raise ValueError("No user logged in.")
        
        user_data_file: str = os.path.join(self.data_dir, "data", f"{self.active_user}.json")
        with open(user_data_file, "r", encoding="utf-8") as file:
            data: dict = json.load(file)
        
        log(f"Listing all entries for user: {self.active_user}")
        return data["accounts"]
    
    def export_data(self: 'PasswordManagerAPI', export_file: str) -> None:
        """Exports all data for the currently logged-in user to a file."""
        if not self.active_user:
            log("Error: No user logged in.")
            raise ValueError("No user logged in.")
        
        log(f"Exporting data for user: {self.active_user}")
        user_data_file: str = os.path.join(self.data_dir, "data", f"{self.active_user}.json")
        with open(user_data_file, "r", encoding="utf-8") as file:
            user_entries: dict = json.load(file)
        
        export_data = {
            "username": self.active_user,
            "email": self.users[self.active_user]["email"],
            "password": self.users[self.active_user]["password"],
            "entries": user_entries["accounts"]
        }
        
        with open(export_file, "w", encoding="utf-8") as file:
            json.dump(export_data, file, indent=4)
        log(f"Data for user {self.active_user} exported to {export_file}.")

#############################
# Entry Point Main Function #
#############################
def main() -> None:
    """Main entry point for the Password Manager API."""
    log("Starting Password Manager API...")
    api: PasswordManagerAPI = PasswordManagerAPI()
    api.register_user("testuser","email@mail.com", "newpassword123")
    sleep(2)
    api.login("testuser", "newpassword123")
    sleep(2)
    print(api.list_all_entries())
    sleep(2)
    api.export_data("export/export.json")
    sleep(2)

###############
# Entry Point #
###############
if __name__ == "__main__":
    main()