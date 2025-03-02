# /src/PWM_ApiBase.py
# Copyright (C) 2025 H.-C. Knolle
# Licensed under the MIT License
# PasswordManagerAPI Base Source Code

###########
# Imports #
###########
import json
import os
import hashlib

###########
# Globals #
###########

def log(message: str) -> None:
    """Returns a log Message."""
    print(f"[LOG] {message}")

json_base_dir: str = "C:\\Users\\Hansisi\\Documents\\Privat\\Dev\\Python\\PasswordManagerAPI\\src\\json"

#################################
# PasswordManagerAPI Main-Class #
#################################
class PasswordManagerAPI:
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
        

################################
# PasswordManagerAPI Main-Code #
################################
def main() -> None:
    log("Starting Password Manager API...")
    api = PasswordManagerAPI()
    api.register_user("Hans", "hansi@lol.de", "123")
    
#############################
# Entry point of the script #
#############################
if __name__ == "__main__":
    main()
