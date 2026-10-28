# django-unchained – Plan & Status

## Ziel

Interaktive Browser-Übungsseite für den kompletten BACKEND-05-Kurs (Django),
Fokus auf aktuelle Django/DRF-Praxis statt veralteter Kurs-Syntax.
Theme: Django Unchained (Western/Sci-Fi), interaktive Charakterfigur
(Cowboy aus Referenzbild) gibt wie ein Windows-Assistent Aufgaben/Korrekturen.

## Bisher erledigt

1. Projektordner `django-unchained` in DA_BD_Django angelegt
2. venv erstellt, django, djangorestframework, django-cors-headers installiert
3. Django-Projekt `config` + App `core` erstellt
4. `settings.py` ersetzt: DRF + CORS + core registriert
5. Git lokal initialisiert, erster Commit gemacht
6. GitHub-Repo `CWhymann/django-unchained` (privat) manuell angelegt
7. Branch auf `main` umbenannt, Push bestätigt
8. Model `Challenge` (title, description, difficulty, created_at) mit Migration 0001 angelegt
9. `Challenge` im Admin registriert (list_display, list_filter, search_fields), `manage.py check` ohne Fehler

## Nächster Schritt

API-Endpunkt für Challenges mit DRF (Serializer, ViewSet, Router in config/urls.py)

## Arbeitsregeln (gelten weiter)

- Schritt für Schritt, kein Vorauseilen
- Vollständige Dateien, PowerShell-Befehle bei neuen Dateien
- Commit-Befehl mit englischer Message nach jedem Schritt
- Tokens sparen, keine ungefragten Features
