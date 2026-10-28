from django.core.management.base import BaseCommand

from core.models import Challenge

S1 = 'Sektion 1 – Installation & Einrichtung'
S2 = 'Sektion 2 – URL & Views'
S3 = 'Sektion III – ClassViews & Templates'
S4 = 'Sektion IV – Aufgabe'

COURSE_CHALLENGES = [
    (S1, 1, 'Django installieren (auch venv)', 'easy',
     'Django wird wie jedes andere Python-Paket per pip ins zuvor erstellte venv installiert. Das venv isoliert die Pakete dieses Projekts vom Rest des Systems, sodass sich Django-Versionen verschiedener Projekte nicht gegenseitig in die Quere kommen.'),
    (S1, 2, 'requirements.txt', 'easy',
     'pip freeze gibt alle installierten Pakete mit exakter Version aus, die Umleitung in requirements.txt schreibt das in eine Datei. Damit lässt sich das Projekt auf einem anderen Rechner mit denselben Abhängigkeiten reproduzieren.'),
    (S1, 3, 'VS-Code-Erweiterungen', 'easy',
     'Empfohlene Extensions erleichtern die Arbeit mit Django, zum Beispiel Syntax-Highlighting und Snippets.'),
    (S1, 4, 'Projektaufbau und lokalen Server starten', 'easy',
     'django-admin startproject config . legt die Grundstruktur eines Django-Projekts im aktuellen Ordner an (der Punkt verhindert einen zusätzlichen Unterordner). runserver startet danach den lokalen Entwicklungsserver, über den sich das Projekt im Browser testen lässt.'),
    (S1, 5, 'Neue App erstellen (startapp)', 'easy',
     'Ein Django-Projekt besteht aus einer oder mehreren Apps. startapp core legt eine neue App namens core an, die als eigenständiger Funktionsbereich eigene Views, URLs und später Models bekommt.'),
    (S1, 6, 'django-cors-headers installieren', 'easy',
     'Installiert und in settings.py eingebunden (INSTALLED_APPS, MIDDLEWARE, CORS_ALLOW_ALL_ORIGINS). Ohne das würde der Browser Requests von einem anderen Origin aus Sicherheitsgründen blockieren.'),

    (S2, 1, 'Deine erste View', 'easy',
     'Eine View ist im Kern nur eine Funktion: Sie nimmt ein request-Objekt entgegen und muss eine HttpResponse (oder eine Unterklasse davon) zurückgeben.'),
    (S2, 2, 'urlpatterns in App auslagern', 'easy',
     'Statt alle Routen zentral in config/urls.py zu sammeln, bekommt die App core eine eigene urls.py. Über include(\'core.urls\') bindet config/urls.py diese Routen ein. Das hält das Projekt übersichtlich, sobald mehrere Apps dazukommen.'),
    (S2, 3, 'redirect()', 'easy',
     'redirect(\'/\') gibt eine HttpResponseRedirect zurück, die den Browser anweist, eine andere URL aufzurufen. Der Browser folgt dem automatisch.'),
    (S2, 4, 'Dummydaten hinzufügen', 'easy',
     'posts ist eine einfache Python-Liste aus Dicts, direkt im Modul definiert. Sie simuliert Datenbankinhalte, ohne dass eine Datenbank-Anbindung nötig ist, und eignet sich, um Views isoliert zu testen.'),
    (S2, 5, 'HttpResponse mit JSON', 'medium',
     'json.dumps(posts) wandelt die Python-Liste in einen JSON-String um. Dieser wird manuell in eine HttpResponse gepackt. Der Content-Type muss dabei selbst auf \'application/json\' gesetzt werden, sonst interpretiert der Client die Antwort nicht als JSON.'),
    (S2, 6, 'JsonResponse', 'medium',
     'JsonResponse(posts, safe=False) übernimmt Serialisierung und Content-Type-Header automatisch. safe=False ist nötig, weil JsonResponse standardmäßig nur Dicts akzeptiert, hier aber eine Liste übergeben wird.'),
    (S2, 7, 'Test mit Mini-Frontend', 'medium',
     'Eine separate index.html holt mit fetch(\'http://127.0.0.1:8000/posts/\') die Daten von der Django-API und rendert sie in eine Liste. Das bestätigt, dass CORS korrekt konfiguriert ist und die View von einem fremden Origin aus erreichbar ist.'),
    (S2, 8, 'URL-Parameter', 'medium',
     'In der Route posts/int:post_id/ ist int:post_id ein URL-Konverter: Django extrahiert den passenden Teil der URL, wandelt ihn automatisch in einen int um und übergibt ihn als Parameter an die View-Funktion.'),
    (S2, 9, 'URL-Parameter Reihenfolge beachten', 'medium',
     'Django prüft urlpatterns von oben nach unten und nimmt die erste passende Route. posts/latest/ muss daher vor posts/int:post_id/ stehen, sonst würde eine zu allgemeine Regel weiter oben spezifischere Routen darunter blockieren.'),
    (S2, 10, 'type slug und slugify', 'medium',
     'slugify(\'First post\') erzeugt \'first-post\': Kleinbuchstaben, Leerzeichen zu Bindestrichen, Sonderzeichen entfernt. slug:post_slug ist der passende URL-Konverter, der nur gültige Slug-Zeichen akzeptiert.'),
    (S2, 11, 'Slug anwenden', 'medium',
     'Eine eigene View (post_by_slug) durchsucht die posts-Liste und gibt den Post zurück, dessen slug-Feld mit dem URL-Parameter übereinstimmt. Dieselbe Logik wie post_detail, nur über den Slug statt die ID.'),
    (S2, 12, 'redirect und reverse', 'medium',
     'reverse(\'latest-post\') baut die URL anhand des name-Parameters der Route, statt den Pfad als festen String zu hinterlegen. Ändert sich später die URL selbst, muss nur die path()-Zeile angepasst werden, nicht jede Stelle im Code, die dorthin verweist.'),
    (S2, 13, 'Http404 und HttpResponseNotFound', 'medium',
     'raise Http404(...) nutzt Djangos eigene Fehlerbehandlung: Bei DEBUG=True zeigt es eine ausführliche Debug-Seite, bei DEBUG=False die eigene 404.html. HttpResponseNotFound(...) ist der direktere Weg, eine einfache 404-Response ohne diesen Umweg.'),
    (S2, 14, 'DEBUG = False und 404.html', 'medium',
     'Mit DEBUG=False sucht Django bei einem Http404 automatisch nach einer 404.html im Template-Verzeichnis und zeigt diese statt der Debug-Seite. Dafür muss zusätzlich ALLOWED_HOSTS gesetzt sein, sonst verweigert der Server den Request.'),
    (S2, 15, 'Die erste POST-View', 'medium',
     'request.POST ist ein Dict-ähnliches Objekt mit den per POST gesendeten Formulardaten. Die View liest title und content daraus aus, baut ein neues Post-Dict und hängt es an die posts-Liste an.'),
    (S2, 16, 'Die erste POST-View testen mit Frontend', 'medium',
     'Das Mini-Frontend sendet die Formulardaten per FormData und fetch(method: \'POST\') an die View. @csrf_exempt war nötig, weil Djangos CSRF-Schutz POST-Requests ohne gültiges Token mit 403 Forbidden ablehnt. Der Decorator deaktiviert diesen Schutz gezielt für diese eine View.'),

    (S3, 1, 'GET und POST in einer View', 'medium',
     'request.method enthält die HTTP-Methode als String (\'GET\', \'POST\', …). Eine if/elif-Abfrage darauf erlaubt es, Listen-Anzeige und Erstellen in derselben Funktion zu behandeln, statt zwei getrennte Views zu brauchen. Wird die Kette bei weiteren Methoden schnell unübersichtlich.'),
    (S3, 2, 'Basic ClassViews', 'hard',
     'Statt if/elif bekommt die Klasse PostsListView eine get()- und eine post()-Methode. Django ruft automatisch die zur HTTP-Methode passende Methode auf. .as_view() wandelt die Klasse in eine View-Funktion um, die in urlpatterns verwendet werden kann. @method_decorator(csrf_exempt, name=\'dispatch\') ist nötig, weil sich @csrf_exempt bei Klassen nicht direkt über eine einzelne Methode legen lässt.'),
    (S3, 3, 'BaseView und RedirectView', 'hard',
     'RedirectView ist eine fertige generische View zum Weiterleiten, ohne eigene get()-Methode. Entweder per festem Attribut url = \'/ziel/\' oder per pattern_name = \'name-der-route\' (dynamisch über denselben Mechanismus wie reverse()). Letzteres bleibt auch dann korrekt, wenn sich die Ziel-URL später ändert.'),
    (S3, 4, 'Wann HTML-Templates sinnvoll sind', 'medium',
     'Templates lohnen sich, sobald eine View direkt fertiges HTML statt reiner Daten liefern soll. Bei reinen API-Endpunkten bleibt JsonResponse die bessere Wahl.'),
    (S3, 5, 'Eigene 404.html', 'medium',
     'Eine eigene Fehlerseite im eigenen Design statt der Django-Standardseite. Sie wird bei DEBUG=False automatisch angezeigt, sobald ein Http404 ausgelöst wird.'),
    (S3, 6, 'render()', 'hard',
     'render(request, \'template.html\', context) kombiniert eine Template-Datei mit einem Kontext-Dict zu einer fertigen HttpResponse. Das übernimmt das Laden des Templates, das Einsetzen der Daten und das Verpacken in eine Response in einem Schritt.'),
    (S3, 7, 'Django-Templates (for-Schleifen)', 'hard',
     'Im Template kann man mit {% for post in posts %} … {% endfor %} über eine aus dem Kontext übergebene Liste iterieren und pro Element HTML ausgeben, z. B. {{ post.title }}. {% %} ist für Logik da, {{ }} gibt Werte aus.'),
    (S3, 8, 'Static Files (CSS einbinden)', 'hard',
     'Eigene statische Dateien liegen in einem static-Ordner der App, zum Beispiel core/static/core/style.css. Im Template werden sie mit {% load static %} und {% static \'core/style.css\' %} eingebunden. Voraussetzung sind \'django.contrib.staticfiles\' in INSTALLED_APPS und STATIC_URL in settings.py.'),
    (S3, 9, 'base.html und extends', 'hard',
     'base.html ist ein gemeinsames Grundgerüst mit benannten Platzhaltern über {% block name %}{% endblock %}. Andere Templates erben davon mit {% extends "base.html" %} und füllen nur die Platzhalter mit eigenem Inhalt. Die gemeinsame Struktur muss so nicht in jeder Seite wiederholt werden.'),

    (S4, 1, 'Praxisaufgabe zum Kursabschluss', 'hard',
     'Die Aufgabe fasst Routing, Views und Templates zu einem eigenen Mini-Projekt zusammen. Sie zeigt, ob die einzelnen Konzepte wirklich sitzen oder nur im geführten Beispiel funktioniert haben.'),
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