# django-unchained – Plan & Status

## Ziel

Interaktive Browser-Übungsseite für den BACKEND-05-Kurs (Django Grundlagen).
Theme: Django Unchained (Western/Sci-Fi). Der Cowboy aus dem Comic erscheint
animiert wie ein Windows-Assistent, stellt Fragen, gibt Tipps und korrigiert.

## Aufbau

- `core/content.py`: 8 Missionen (m1 bis m8), Übungen vom Typ Quiz, Lückencode, Bug-Jagd, Reihenfolge und Live-Request. Lösungen bleiben auf dem Server.
- `core/models.py`: Models `Mission` und `Exercise` mit Migration `0004_initial.py`. Die Views lesen die Missionen aktuell aus `content.py`, nicht aus der Datenbank.
- `core/views.py`: `/api/missions/` (Aufgaben), `/api/check/` (Antwort prüfen, CSRF-geschützt), Demo-Endpunkte unter `/demo/` für die Live-Übungen.
- `core/templates/core/index.html`, `core/static/core/{css,js,img}`: Oberfläche, Logik und Cowboy-Animation.
- Fortschritt liegt im Browser (localStorage).
- Django liefert die Seite selbst unter `/` aus.

## Stand

- 8 Missionen sind in `content.py` vorhanden.
- Live unter https://chowman.pythonanywhere.com/ erreichbar. Die Missionsliste wird per JavaScript geladen und ist noch nicht vollständig geprüft.
- `core/tests.py` ist leer. Es gibt noch keine Tests.
- `requirements.txt` ist nicht gepinnt.

## Nächster Schritt

- Klären, ob die Models `Mission` und `Exercise` gebraucht werden.
- Live-Seite prüfen: Missionsliste, Übungen und Fortschritt.
- Fallback-SECRET_KEY in `config/settings.py` durch Umgebungsvariable ersetzen.

## Arbeitsregeln (gelten weiter)

- Schritt für Schritt, kein Vorauseilen
- Vollständige Dateien, PowerShell-Befehl zuerst bei neuen Dateien
- Commit-Befehl mit englischer Message nach jedem Schritt
- Keine ungefragten Features
