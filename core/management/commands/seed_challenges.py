from django.core.management.base import BaseCommand

from core.models import Challenge

S1 = 'Sektion 1 – Installation & Einrichtung'
S2 = 'Sektion 2 – URL & Views'
S3 = 'Sektion III – ClassViews & Templates'
S4 = 'Sektion IV – Aufgabe'

COURSE_CHALLENGES = [
    (S1, 1, 'Django installieren (auch venv)', 'easy',
     'Django wird als Paket in einem venv installiert, damit das Framework sauber vom System getrennt bleibt. Stichworte: pip install django, venv'),
    (S1, 2, 'requirements.txt', 'easy',
     'Listet alle Projektabhängigkeiten mit Version auf, damit das Projekt woanders reproduzierbar ist. Stichworte: requirements.txt'),
    (S1, 3, 'VS-Code-Erweiterungen', 'easy',
     'Empfohlene Extensions erleichtern die Arbeit mit Django (Syntax-Highlighting, Snippets). Stichworte: Extensions'),
    (S1, 4, 'Projektaufbau und lokalen Server starten', 'easy',
     'django-admin startproject legt die Grundstruktur an, runserver startet die Entwicklungsumgebung. Stichworte: startproject, runserver'),
    (S1, 5, 'Neue App erstellen (startapp)', 'easy',
     'Ein Django-Projekt besteht aus mehreren Apps, jede App kapselt einen Funktionsbereich. Stichworte: startapp, App-Struktur'),
    (S1, 6, 'django-cors-headers installieren', 'easy',
     'Erlaubt Anfragen von einem anderen Origin, sonst blockiert der Browser die Requests. Stichworte: CORS, Cross-Origin'),

    (S2, 1, 'Deine erste View', 'easy',
     'Eine View ist eine Funktion, die einen Request entgegennimmt und eine Response zurückgibt. Stichworte: View-Funktion'),
    (S2, 2, 'urlpatterns in App auslagern', 'easy',
     'URLs werden pro App in einer eigenen urls.py definiert statt zentral. Stichworte: urls.py, include()'),
    (S2, 3, 'redirect()', 'easy',
     'Leitet einen Request auf eine andere URL um. Stichworte: redirect()'),
    (S2, 4, 'Dummydaten hinzufügen', 'easy',
     'Testdaten direkt im Code, um Views ohne Datenbank auszuprobieren. Stichworte: Dummydaten'),
    (S2, 5, 'HttpResponse mit JSON', 'medium',
     'Die Antwort wird manuell als JSON-String in eine HttpResponse verpackt. Stichworte: HttpResponse, json.dumps'),
    (S2, 6, 'JsonResponse', 'medium',
     'Eigene Response-Klasse, die ein Dict automatisch korrekt als JSON mit Content-Type serialisiert. Stichworte: JsonResponse'),
    (S2, 7, 'Test mit Mini-Frontend', 'medium',
     'Die eigene View wird gegen ein kleines Frontend getestet, um die reale Kommunikation zu prüfen. Stichworte: Frontend-Test'),
    (S2, 8, 'URL-Parameter', 'medium',
     'Werte werden direkt als Teil der URL übergeben und in der View ausgelesen. Stichworte: int:id, Pfadparameter'),
    (S2, 9, 'URL-Parameter Reihenfolge beachten', 'medium',
     'Django prüft urlpatterns der Reihe nach, allgemeinere Muster vor spezifischeren können Routen blockieren. Stichworte: Reihenfolge, Routing'),
    (S2, 10, 'type slug und slugify', 'medium',
     'Ein Slug ist eine URL-freundliche Kurzform eines Textes, slugify() erzeugt sie automatisch. Stichworte: slug, slugify()'),
    (S2, 11, 'Slug anwenden', 'medium',
     'Slugs werden als URL-Parameter genutzt, z. B. für lesbare Artikel-URLs. Stichworte: Slug-URLs'),
    (S2, 12, 'redirect und reverse', 'medium',
     'reverse() erzeugt eine URL aus dem Namen der urlpattern statt sie hart zu codieren. Stichworte: reverse(), URL-Namen'),
    (S2, 13, 'Http404 und HttpResponseNotFound', 'medium',
     'Http404 nutzt Djangos Fehlerbehandlung, HttpResponseNotFound ist direkter. Stichworte: Http404, 404-Handling'),
    (S2, 14, 'DEBUG = False und 404.html', 'medium',
     'Im Produktivmodus zeigt Django eine eigene 404.html statt der Debug-Fehlerseite. Stichworte: DEBUG, 404.html'),
    (S2, 15, 'Die erste POST-View', 'medium',
     'Eine View, die gezielt auf POST-Requests reagiert und Daten entgegennimmt. Stichworte: POST-View'),
    (S2, 16, 'Die erste POST-View testen mit Frontend', 'medium',
     'Die POST-View wird gegen ein echtes Frontend-Formular getestet. Stichworte: POST testen'),

    (S3, 1, 'GET und POST in einer View', 'medium',
     'Eine Funktion unterscheidet per request.method zwischen GET und POST. Stichworte: request.method'),
    (S3, 2, 'Basic ClassViews', 'hard',
     'Views als Klassen mit einer Methode pro HTTP-Verb statt if-Verzweigungen. Stichworte: View-Klasse, get(), post()'),
    (S3, 3, 'BaseView und RedirectView', 'hard',
     'Django liefert fertige Basisklassen für häufige Fälle wie reine Weiterleitungen. Stichworte: BaseView, RedirectView'),
    (S3, 4, 'Wann HTML-Templates sinnvoll sind', 'medium',
     'Templates lohnen sich, sobald eine View direkt HTML statt reiner Daten ausliefern soll. Stichworte: Template vs. JSON'),
    (S3, 5, 'Eigene 404.html', 'medium',
     'Eine eigene Fehlerseite im Corporate Design statt der Django-Standardseite. Stichworte: Custom 404'),
    (S3, 6, 'render()', 'hard',
     'Kombiniert ein Template mit Kontextdaten zu einer fertigen HTML-Response. Stichworte: render()'),
    (S3, 7, 'Django-Templates (for-Schleifen)', 'hard',
     'Die Template-Sprache erlaubt Schleifen und Bedingungen direkt im HTML. Stichworte: {% for %}, Template-Tags'),
    (S3, 8, 'Static Files (CSS einbinden)', 'hard',
     'CSS, JS und Bilder werden über einen static-Ordner und {% load static %} eingebunden. Stichworte: static, {% load static %}'),
    (S3, 9, 'base.html und extends', 'hard',
     'Ein Basis-Template mit gemeinsamem Grundgerüst, andere Templates erweitern es per extends. Stichworte: base.html, {% extends %}'),

    (S4, 1, 'Praxisaufgabe zum Kursabschluss', 'hard',
     'Die Aufgabe fasst Routing, Views und Templates zu einem eigenen Mini-Projekt zusammen. Stichworte: Übungsaufgabe'),
]


class Command(BaseCommand):
    help = 'Legt die Kurs-Challenges an oder aktualisiert sie'

    def handle(self, *args, **options):
        for section, order, title, difficulty, description in COURSE_CHALLENGES:
            _, created = Challenge.objects.update_or_create(
                title=title,
                defaults={
                    'section': section,
                    'order': order,
                    'difficulty': difficulty,
                    'description': description,
                },
            )
            status = 'angelegt' if created else 'aktualisiert'
            self.stdout.write(f'{section} / {title}: {status}')