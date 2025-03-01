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
from packages.logger import log
from packages.config import json_base_dir

#################################
# PasswordManagerAPI Main-Class #
#################################
class PasswordManagerAPI:
    def __init__(self: any, data_dir: str = json_base_dir) -> None:
        self.data_dir: str = data_dir
        self.users_file: str = os.path.join(self.data_dir, "users.json")
        self.active_user: str = None
        self._load_users()
    
    def _load_users(self: any) -> None:
        """Load the userlist from users.json or create a new file."""
        log("Load Userlist...")
        if os.path.exists(self.users_file):
            with open(self.users_file, "r", encoding="utf-8") as file:
                try:
                    self.users = json.load(file)
                except json.JSONDecodeError:
                    log("Error with loading userlist. Creating new file.")
                    self.users: dict = {}
        else:
            log("No userlist found. Creating new file.")
            self.users: dict = {}
            self._save_users()
    
    def _save_users(self: any) -> None:
        """Saving the current userlist in users.json."""
        log("Saving userlist...")
        with open(self.users_file, "w", encoding="utf-8") as file:
            json.dump(self.users, file, indent=4)
    
    def _hash_password(self: any, password: str) -> None:
        """Creates secure sha256 hash of user password."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self: any, username: str, email: str, password: str) -> None:
        """Creates new user and saves it to users.json."""
        if username in self.users:
            log(f"Error: Username '{username}' already in use.")
            raise ValueError(f"Username '{username}' already in use.")
        
        log(f"Regiszer new user: {username}")
        self.users[username] = {
            "email": email,
            "password": self._hash_password(password)
        }
        self._save_users()
        
        user_data_file = os.path.join(self.data_dir, "data", f"{username}.json")
        if not os.path.exists(user_data_file):
            with open(user_data_file, "w", encoding="utf-8") as file:
                json.dump({"accounts": {}}, file, indent=4)
        log(f"Userdate for {username} created.")

    def delete_user(self: any, username: str) -> None:
        """Deletes user and related data.""" 
        if username not in self.users:
            log(f"Error: User '{username}' doesn't exist.")
            raise ValueError(f"Error: User '{username}' doesn't exist.")
        
        log(f"Lösche Benutzer: {username}")
        
        del self.users[username]
        self._save_users()
        
        # Lösche die Benutzerdaten-Datei
        user_data_file = os.path.join(self.data_dir, "data", f"{username}.json")
        if os.path.exists(user_data_file):
            os.remove(user_data_file)
            log(f"Benutzerdaten für {username} gelöscht.")
        else:
            log(f"Warnung: Benutzerdaten-Datei für {username} nicht gefunden.")
        
    def login(self, username, password):
        """Meldet einen Benutzer an, wenn die Zugangsdaten stimmen."""
        log(f"Versuche Anmeldung für Benutzer: {username}")
        if username in self.users and self.users[username]["password"] == self._hash_password(password):
            self.active_user = username
            log(f"Benutzer {username} erfolgreich angemeldet.")
        else:
            log("Fehlgeschlagene Anmeldung.")
            raise ValueError("Ungültige Anmeldedaten.")
    
    def logout(self):
        """Meldet den aktuellen Benutzer ab."""
        if self.active_user:
            log(f"Benutzer {self.active_user} wird abgemeldet.")
        self.active_user = None
    
    def get_active_user(self):
        """Gibt den aktuell angemeldeten Benutzer zurück oder None, wenn niemand angemeldet ist."""
        return self.active_user
    
    def add_entry(self, service, username, password):
        """Fügt einen neuen Eintrag für den aktuell angemeldeten Benutzer hinzu."""
        if not self.active_user:
            log("Fehler: Kein Benutzer angemeldet.")
            raise ValueError("Kein Benutzer angemeldet.")
        
        user_data_file = os.path.join(self.data_dir, "data", f"{self.active_user}.json")
        with open(user_data_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        data["accounts"][service] = {"username": username, "password": password}
        
        with open(user_data_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        log(f"Neuer Eintrag für {service} hinzugefügt.")
    
    def remove_entry(self, service):
        """Entfernt einen Eintrag für den aktuell angemeldeten Benutzer."""
        if not self.active_user:
            log("Fehler: Kein Benutzer angemeldet.")
            raise ValueError("Kein Benutzer angemeldet.")
        
        user_data_file = os.path.join(self.data_dir, "data", f"{self.active_user}.json")
        with open(user_data_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        if service in data["accounts"]:
            del data["accounts"][service]
            with open(user_data_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            log(f"Eintrag für {service} entfernt.")
        else:
            log(f"Fehler: Kein Eintrag für {service} gefunden.")
            raise ValueError("Eintrag nicht gefunden.")

def main():
    log("Starte Passwort-Manager API...")
    api = PasswordManagerAPI()
    api.register_user("Hans", "hansi@lol.de", "123")
    
if __name__ == "__main__":
    main()
