# PasswordManagerAPI

## 📂 Beschreibung
PasswordManagerAPI ist eine einfache, lokale Passwort-Manager-API, die das Speichern und Verwalten von Benutzerkonten und Passwörtern ermöglicht. Sie verwendet JSON-Dateien zur Speicherung und SHA-256 zur Hashing von Passwörtern.

## 🛠️ Installation
### Voraussetzungen
- Python 3.13
- Git (optional)

### Installation
1. Repository klonen oder herunterladen:
   ```sh
   git clone https://github.com/HansKnolle08/PasswordManagerAPI.git
   ```
   Alternativ kannst du das Repository als ZIP herunterladen und entpacken.

2. In das Projektverzeichnis wechseln:
   ```sh
   cd PasswordManagerAPI/src
   ```

## 📑 Nutzung
### API initialisieren
```python
from PWM_ApiBase import PasswordManagerAPI
api = PasswordManagerAPI()
```

### Benutzerregistrierung
```python
api.register_user("testuser", "test@example.com", "meinpasswort")
```

### Login
```python
api.login("testuser", "meinpasswort")
```

### Logout
```python
api.logout()
```

### Passwort-Einträge verwalten
**Neuen Eintrag hinzufügen:**
```python
api.add_entry("Google", "testuser", "geheimespasswort")
```

**Eintrag abrufen:**
```python
entry = api.get_entry("Google")
print(entry)
```

**Eintrag entfernen:**
```python
api.remove_entry("Google")
```

### Benutzer löschen
```python
api.delete_user("testuser")
```

## 📝 Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe [LICENSE](LICENSE) für weitere Informationen.

