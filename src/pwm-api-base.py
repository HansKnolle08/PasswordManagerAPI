# /src/pwm-api-base.py
# Copyright (C) 2025 H.-C. Knolle
# Licensed under the MIT License
# PasswordManagerAPI Base Source Code

###########
# Imports #
###########
import json
import os
import hashlib
from packages.log import log

#################################
# PasswordManagerAPI Main-Class #
#################################
class PasswordManagerAPI:
    def __init__(self: any, data_dir: str = "C:\\Users\\Hansisi\\Documents\\Privat\\Dev\\Python\\PasswordManagerAPI\\src\\json") -> None:
        self.data_dir: str = data_dir
        self.users_file: str = os.path.join(self.data_dir, "users.json")
        self.active_user: str = None
        self._load_users()
    
    def _load_users(self: any) -> None:
        """Load the userlist from users.json or create a new one."""
        log("Lade Benutzerliste...")
        if os.path.exists(self.users_file):
            with open(self.users_file, "r", encoding="utf-8") as file:
                try:
                    self.users = json.load(file)
                except json.JSONDecodeError:
                    log("Fehler beim Laden der Benutzerliste. Erstelle eine neue Datei.")
                    self.users = {}
        else:
            log("Keine Benutzerliste gefunden. Erstelle eine neue Datei.")
            self.users = {}
            self._save_users()
    
    def _save_users(self):
        """Speichert die aktuelle Benutzerliste in users.json."""
        log("Speichere Benutzerliste...")
        with open(self.users_file, "w", encoding="utf-8") as file:
            json.dump(self.users, file, indent=4)
    
    def _hash_password(self, password):
        """Erstellt einen sicheren Hash des Passworts."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, email, password):
        """Erstellt einen neuen Benutzer und speichert ihn in users.json."""
        if username in self.users:
            log(f"Fehler: Benutzername '{username}' ist bereits vergeben.")
            raise ValueError("Benutzername bereits vergeben.")
        
        log(f"Registriere neuen Benutzer: {username}")
        self.users[username] = {
            "email": email,
            "password": self._hash_password(password)
        }
        self._save_users()
        
        user_data_file = os.path.join(self.data_dir, "data", f"{username}.json")
        if not os.path.exists(user_data_file):
            with open(user_data_file, "w", encoding="utf-8") as file:
                json.dump({"accounts": {}}, file, indent=4)
        log(f"Benutzerdatei für {username} erstellt.")

    def delete_user(self, username):
        """Löscht einen Benutzer und dessen zugehörige Daten.""" 
        if username not in self.users:
            log(f"Fehler: Benutzer '{username}' existiert nicht.")
            raise ValueError("Benutzer existiert nicht.")
        
        log(f"Lösche Benutzer: {username}")
        
        # Entferne den Benutzer aus der Benutzerliste
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
    
if __name__ == "__main__":
    main()
