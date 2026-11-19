# django-unchained – Plan & Status

## Ziel

Interaktive Browser-Übungsseite für den BACKEND-05-Kurs (Django Grundlagen).
Theme: Django Unchained (Western/Sci-Fi). Der Cowboy aus dem Comic erscheint
animiert wie ein Windows-Assistent, stellt Fragen, gibt Tipps und korrigiert.

## Aufbau

- `core/content.py`: 6 Missionen, 30 Übungen (Quiz, Lückencode, Bug-Jagd, Reihenfolge, Live-Request). Lösungen bleiben auf dem Server.
- `core/views.py`: `/api/missions/` (Aufgaben), `/api/check/` (Antwort prüfen, CSRF-geschützt), Demo-Endpunkte unter `/demo/` für die Live-Übungen.
- `core/templates/core/index.html`, `core/static/core/{css,js,img}`: Oberfläche, Logik und Cowboy-Animation.
- Fortschritt liegt im Browser (localStorage), keine Datenbank-Models.
- Django liefert die Seite selbst unter `/` aus (ein Server, kein Live Server nötig).

## Stand

Alle 6 Missionen sind umgesetzt und getestet. Der alte Challenge-Stand ist entfernt.

## Nächster Schritt

Optik im Browser prüfen und Feinschliff (Texte, Animationen, weitere Übungen).

## Arbeitsregeln (gelten weiter)

- Schritt für Schritt, kein Vorauseilen
- Vollständige Dateien, PowerShell-Befehl zuerst bei neuen Dateien
- Commit-Befehl mit englischer Message nach jedem Schritt
- Keine ungefragten Features
