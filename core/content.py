"""Missionen und Übungen für Django Unchained.

Die Lösungen bleiben auf dem Server: Der Browser bekommt nur die Aufgaben
(public_missions) und schickt seine Antwort zur Prüfung an check().
"""
import copy
import random


# ---------- Bausteine für Übungen ----------

def quiz(ex_id, title, q, options, solution, explain, hint='', request=None):
    ex = {
        'id': ex_id, 'type': 'live' if request else 'quiz', 'title': title, 'q': q,
        'options': options, 'solution': solution, 'explain': explain, 'hint': hint,
    }
    if request:
        ex['request'] = request
    return ex


def fill(ex_id, title, q, code, solution, explain, hint=''):
    return {
        'id': ex_id, 'type': 'fill', 'title': title, 'q': q, 'code': code,
        'solution': solution, 'explain': explain, 'hint': hint,
    }


def bug(ex_id, title, q, lines, solution, explain, hint=''):
    return {
        'id': ex_id, 'type': 'bug', 'title': title, 'q': q, 'lines': lines,
        'solution': solution, 'explain': explain, 'hint': hint,
    }


def order(ex_id, title, q, items, solution, explain, hint='', probes=None):
    ex = {
        'id': ex_id, 'type': 'order', 'title': title, 'q': q, 'items': items,
        'solution': solution, 'explain': explain, 'hint': hint,
    }
    if probes:
        ex['probes'] = probes
    return ex


# ---------- Missionen ----------

MISSIONS = [
    {
        'id': 'm1',
        'title': 'Das Camp aufschlagen',
        'section': 'Sektion 1 – Installation & Einrichtung',
        'intro': 'Willkommen in der Prärie, Fremder. Bevor du Land bebaust, brauchst du ein sicheres Camp: venv, Django, ein Projekt.',
        'outro': 'Das Camp steht. Kein Chaos. Nur Kontrolle.',
        'exercises': [
            quiz('m1-1', 'Das Zelt im Sturm',
                 'Wozu legst du für jedes Projekt ein eigenes venv an?',
                 ['Damit Django schneller läuft',
                  'Damit die Pakete jedes Projekts voneinander isoliert bleiben',
                  'Damit pip nicht mehr gebraucht wird',
                  'Damit der Code verschlüsselt wird'],
                 1,
                 'Ein venv isoliert die installierten Pakete pro Projekt. So kollidieren die Django-Versionen verschiedener Projekte nicht.',
                 'Es geht um Ordnung zwischen mehreren Projekten.'),
            fill('m1-2', 'Die Ausrüstung packen',
                 'Ergänze die PowerShell-Befehle: venv anlegen, aktivieren und alle Pakete in die requirements.txt schreiben.',
                 'python -m venv [[1]]\n.\\venv\\Scripts\\[[2]]\npip install django\npip [[3]] > requirements.txt',
                 [['venv'], ['Activate.ps1', 'activate.ps1', 'Activate', 'activate'], ['freeze']],
                 'python -m venv venv legt die Umgebung an, Activate.ps1 aktiviert sie, pip freeze listet alle Pakete mit Version. Die Umleitung > schreibt das Ergebnis in requirements.txt.',
                 'Der Befehl, der alle installierten Pakete "einfriert".'),
            order('m1-3', 'Die Karawane ordnen',
                  'Bringe die Befehle in die richtige Reihenfolge, um ein Projekt zu starten.',
                  [{'id': 'a', 'text': 'python -m venv venv'},
                   {'id': 'b', 'text': '.\\venv\\Scripts\\Activate.ps1'},
                   {'id': 'c', 'text': 'pip install django'},
                   {'id': 'd', 'text': 'django-admin startproject config .'},
                   {'id': 'e', 'text': 'python manage.py runserver'}],
                  [['a', 'b', 'c', 'd', 'e']],
                  'Erst Umgebung anlegen und aktivieren, dann Django installieren, das Projekt erzeugen und zuletzt den Server starten.',
                  'Ohne installiertes Django gibt es kein django-admin.'),
            bug('m1-4', 'Der Posten am falschen Ort',
                'Klicke die Zeile, die in der Middleware-Liste falsch steht.',
                ['MIDDLEWARE = [',
                 "    'django.middleware.security.SecurityMiddleware',",
                 "    'django.middleware.common.CommonMiddleware',",
                 "    'corsheaders.middleware.CorsMiddleware',",
                 "    'django.middleware.csrf.CsrfViewMiddleware',",
                 ']'],
                [3, 4],
                'Die CorsMiddleware muss möglichst weit oben stehen, vor der CommonMiddleware. Sonst fehlen die CORS-Header, wenn eine andere Middleware schon eine Antwort erzeugt.',
                'Die Reihenfolge der Middleware zählt: CORS muss vor CommonMiddleware dran sein.'),
            quiz('m1-5', 'Der Server meldet sich',
                 'Unter welcher Adresse läuft der Entwicklungsserver nach runserver standardmäßig?',
                 ['http://127.0.0.1:8000/', 'http://127.0.0.1:5500/',
                  'http://localhost:3000/', 'http://0.0.0.0:80/'],
                 0,
                 'runserver nutzt standardmäßig 127.0.0.1:8000. Port 5500 ist der Live Server aus VS Code.',
                 'Django-Standard: Port 8000.'),
        ],
    },
    {
        'id': 'm2',
        'title': 'Die erste Spur',
        'section': 'Sektion 2 – URLs & Views',
        'intro': 'Jetzt wird es ernst: Eine Anfrage reitet ein, und deine View muss antworten.',
        'outro': 'Die Spur ist gelegt. Jede Anfrage findet ihren Weg.',
        'exercises': [
            quiz('m2-1', 'Das Gesetz der Prärie',
                 'Was muss eine View-Funktion immer zurückgeben?',
                 ['Einen String', 'Ein Dict', 'Eine HttpResponse (oder eine Unterklasse)', 'Nichts'],
                 2,
                 'Eine View nimmt das request entgegen und liefert eine HttpResponse, zum Beispiel HttpResponse, JsonResponse oder HttpResponseRedirect.',
                 'Auch JsonResponse gehört zu dieser Familie.'),
            fill('m2-2', 'Der erste Schuss',
                 'Schreibe eine View, die "Howdy, Fremder!" zurückgibt.',
                 'from django.http import HttpResponse\n\ndef hello([[1]]):\n    return [[2]]("Howdy, Fremder!")',
                 [['request'], ['HttpResponse']],
                 'Jede View bekommt das request-Objekt als ersten Parameter und gibt eine HttpResponse zurück.',
                 'Der erste Parameter beschreibt die eingehende Anfrage.'),
            fill('m2-3', 'Den Weg ausschildern',
                 'Binde die View unter /hello/ ein und nenne die Route "hello".',
                 "from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path('hello/', views.[[1]], [[2]]='hello'),\n]",
                 [['hello'], ['name']],
                 'path() verbindet URL und View. Mit name bekommt die Route einen Namen, den reverse() und redirect() später nutzen.',
                 'Der Parameter, mit dem eine Route einen Namen bekommt.'),
            quiz('m2-4', 'Das Lagerfeuer-Verzeichnis',
                 "Wozu dient include('core.urls') in config/urls.py?",
                 ['Es importiert die Models der App',
                  'Es bindet die URLs der App core in das Projekt ein',
                  'Es startet die App',
                  'Es erstellt eine neue Datenbank'],
                 1,
                 'Mit include() lagert man Routen in die App aus. Die config/urls.py bleibt übersichtlich, auch wenn mehrere Apps dazukommen.',
                 'Es hat mit den Routen der App zu tun.'),
            quiz('m2-5', 'Feuer frei!',
                 'Feuere den Request ab. Welchen Statuscode liefert die Liste der Posts?',
                 ['200 OK', '201 Created', '302 Found', '404 Not Found'],
                 0,
                 'JsonResponse(POSTS, safe=False) liefert die Liste als JSON mit Status 200. safe=False ist nötig, weil es eine Liste ist und kein Dict.',
                 'Alles ging gut, nichts wurde angelegt.',
                 request={'method': 'GET', 'url': '/demo/posts/'}),
            quiz('m2-6', 'Der Umweg',
                 'Feuere ab: /demo/alt/ ruft redirect() auf. Was ist passiert?',
                 ['Die View hat selbst JSON gebaut',
                  'Der Browser wurde automatisch auf /demo/posts/latest/ weitergeleitet',
                  'Die Route existiert nicht',
                  'Der Server ist abgestürzt'],
                 1,
                 'redirect() antwortet mit Status 302 und einer neuen URL. Der Browser folgt automatisch, im Panel siehst du die Weiterleitung.',
                 'Schau auf die Ziel-URL im Antwort-Panel.',
                 request={'method': 'GET', 'url': '/demo/alt/'}),
        ],
    },
    {
        'id': 'm3',
        'title': 'Wegweiser im Canyon',
        'section': 'Sektion 2 – URL-Parameter & Reverse',
        'intro': 'Im Canyon gabelt sich der Weg. Zahl, Slug oder Schlagwort: Django prüft die Wegweiser von oben nach unten.',
        'outro': 'Du liest Wegweiser wie ein Scout.',
        'exercises': [
            order('m3-1', 'Die Wegweiser-Falle',
                  'Sortiere die Routen so, dass jede Probe-URL bei der richtigen View landet. Die Proben unten reagieren live.',
                  [{'id': 'c', 'label': 'latest_post',
                    'text': "path('demo/posts/latest/', views.latest_post)",
                    're': '^demo/posts/latest/$'},
                   {'id': 'b', 'label': 'post_detail',
                    'text': "path('demo/posts/<int:post_id>/', views.post_detail)",
                    're': '^demo/posts/[0-9]+/$'},
                   {'id': 'a', 'label': 'post_by_slug',
                    'text': "path('demo/posts/<slug:post_slug>/', views.post_by_slug)",
                    're': '^demo/posts/[-a-zA-Z0-9_]+/$'}],
                  [['c', 'b', 'a'], ['b', 'c', 'a']],
                  'Django nimmt die erste passende Route. Der Slug-Konverter passt auf fast alles, auch auf "latest" und auf Zahlen. Deshalb gehört er ans Ende.',
                  'Die allgemeinste Regel gehört nach unten.',
                  probes=[{'url': 'demo/posts/latest/', 'expect': 'c'},
                          {'url': 'demo/posts/2/', 'expect': 'b'},
                          {'url': 'demo/posts/showdown-bei-sonnenuntergang/', 'expect': 'a'}]),
            quiz('m3-2', 'Aus Text wird Pfad',
                 "Was liefert slugify('Der Kopfgeldjäger von Mars Ridge')?",
                 ['der-kopfgeldjager-von-mars-ridge',
                  'Der_Kopfgeldjäger_von_Mars_Ridge',
                  'der kopfgeldjäger von mars ridge',
                  'DER-KOPFGELDJAGER-VON-MARS-RIDGE'],
                 0,
                 "slugify macht alles klein, ersetzt Leerzeichen durch Bindestriche und entfernt Sonderzeichen. Aus 'ä' wird 'a'.",
                 'Klein, Bindestriche, keine Umlaute.'),
            fill('m3-3', 'Beim Namen gerufen',
                 'Leite mit reverse() auf die Route mit dem Namen "latest-post" um.',
                 "from django.urls import reverse\n\ndef old_latest(request):\n    return redirect([[1]]('[[2]]'))",
                 [['reverse'], ['latest-post']],
                 'reverse() baut die URL aus dem Routennamen. Ändert sich der Pfad später, musst du nur die path()-Zeile anpassen.',
                 'Die Funktion, die aus einem Namen eine URL macht.'),
            bug('m3-4', 'Der Schuss ins Leere',
                'Ein unbekannter Post führt zu einem Serverfehler (500). Klicke die fehlerhafte Zeile.',
                ['def post_detail(request, post_id):',
                 '    for post in POSTS:',
                 "        if post['id'] == post_id:",
                 '            return JsonResponse(post)',
                 '    return JsonResponse(None)'],
                [5],
                "JsonResponse(None) wirft einen TypeError, weil es ohne safe=False nur Dicts akzeptiert. Richtig ist raise Http404('Post nicht gefunden'), dann antwortet Django sauber mit 404.",
                'Was soll passieren, wenn kein Post passt?'),
            quiz('m3-5', 'Typ-Prüfung',
                 "Du schreibst path('demo/posts/<int:post_id>/', ...). Welchen Typ hat post_id in der View?",
                 ['str', 'int', 'float', 'slug'],
                 1,
                 'Der Konverter int wandelt den URL-Teil automatisch in einen int um, bevor er an die View übergeben wird.',
                 'Der Konverter vor dem Doppelpunkt verrät es.'),
        ],
    },
    {
        'id': 'm4',
        'title': 'Showdown um JSON',
        'section': 'Sektion 2 – JSON, 404 & POST',
        'intro': 'Zeit für Daten. JSON rein, JSON raus, und mancher Request wird abgewiesen.',
        'outro': 'JSON, Fehler, POST: alles im Griff.',
        'exercises': [
            quiz('m4-1', 'Die Liste im Holster',
                 'Warum steht in JsonResponse(POSTS, safe=False) das safe=False?',
                 ['Damit der Server sicherer wird',
                  'Weil POSTS eine Liste ist und JsonResponse standardmäßig nur Dicts akzeptiert',
                  'Damit CORS funktioniert',
                  'Damit JSON schöner formatiert wird'],
                 1,
                 'Standardmäßig erlaubt JsonResponse nur Dicts (safe=True). Für Listen musst du safe=False setzen.',
                 'Standard: nur Dicts.'),
                        quiz('m4-2', 'Niemand zu Hause',
                 'Feuere ab: Post 999 gibt es nicht. Welchen Statuscode liefert Django, wenn die View Http404 auslöst?',
                 ['404 Not Found', '200 OK', '500 Internal Server Error', '403 Forbidden'],
                 0,
                 'Http404 führt zu Status 404. Mit DEBUG=True zeigt Django eine technische Fehlerseite, mit DEBUG=False eine schlichte Seite oder deine eigene 404.html (dann muss ALLOWED_HOSTS gesetzt sein).',
                 'Der Name der Exception verrät es.',
                 request={'method': 'GET', 'url': '/demo/posts/999/'}),
            quiz('m4-3', 'Ohne Marke kein Eintritt',
                 'Feuere einen POST ohne CSRF-Token ab. Warum kommt eine 403?',
                 ['Das CSRF-Token fehlt', 'Die Route existiert nicht',
                  'Der Titel ist zu lang', 'Django erlaubt kein POST'],
                 0,
                 'Djangos CSRF-Schutz lehnt POST-Requests ohne gültiges Token mit 403 ab. Deshalb brauchte die Kurs-View @csrf_exempt. Das ist nur für diese Übung gedacht, in echten Projekten setzt man es bewusst und sparsam ein.',
                 'Es fehlt ein Sicherheits-Token.',
                 request={'method': 'POST', 'url': '/demo/posts/strict/', 'body': {'title': 'Duell am Canyon'}}),
            quiz('m4-4', 'Der Aufschlag',
                 'Feuere einen POST an die csrf_exempt-View ab. Was bedeutet der Status 201?',
                 ['Created: etwas wurde angelegt', 'Forbidden', 'Redirect', 'Not Found'],
                 0,
                 '201 Created meldet: Die Ressource wurde angelegt. Im Body siehst du den neuen Post samt Slug.',
                 'Der Server hat etwas Neues erstellt.',
                 request={'method': 'POST', 'url': '/demo/posts/',
                          'body': {'title': 'Duell am Canyon', 'content': 'Zwei Revolver, ein Sonnenuntergang.'}}),
            fill('m4-5', 'Der eigene Revolver',
                 'Vervollständige die POST-Logik.',
                 "def create_post(request):\n    title = request.[[1]].get('title', '')\n    post = {'id': len(POSTS) + 1, 'title': title, 'slug': [[2]](title)}\n    POSTS.append(post)\n    return JsonResponse(post, status=[[3]])",
                 [['POST'], ['slugify'], ['201']],
                 'request.POST enthält die Formulardaten, slugify erzeugt den Slug und status=201 steht für Created.',
                 'Formulardaten eines POST liegen in request.POST.'),
        ],
    },
    {
        'id': 'm5',
        'title': 'Die Klassen-Kopfgeldjäger',
        'section': 'Sektion III – ClassViews & Templates',
        'intro': 'Jetzt kommen die Profis: Klassen statt Funktionen, HTML statt nur JSON.',
        'outro': 'Klassen, Templates, Vererbung: Du bist bereit für den letzten Ritt.',
        'exercises': [
            quiz('m5-1', 'Die richtige Methode',
                 'PostsListView.as_view() erhält einen GET-Request. Was ruft Django auf?',
                 ['Die Methode get()', 'Nur die Methode __init__()',
                  'Die Methode list()', 'Nichts, GET ist nicht erlaubt'],
                 0,
                 'as_view() macht die Klasse zur View-Funktion. dispatch() wählt anhand der HTTP-Methode die passende Methode: get() für GET, post() für POST.',
                 'Methodenname = HTTP-Methode in Kleinbuchstaben.'),
            fill('m5-2', 'Der Klassenschutz',
                 'Mache die Klasse csrf-frei und leite sie von der Basis-View ab.',
                 "@method_decorator(csrf_exempt, name='[[1]]')\nclass PostsListView([[2]]):\n    def get(self, request):\n        return JsonResponse(POSTS, safe=False)",
                 [['dispatch'], ['View']],
                 'Bei Klassen setzt man den Decorator auf dispatch(), weil dispatch() jeden Request entgegennimmt und an get() oder post() weiterreicht.',
                 'Die Methode, die jeden Request zuerst bekommt.'),
            fill('m5-3', 'Die Schleife',
                 'Gib alle Posts im Template als Liste aus.',
                 '<ul>\n  {% [[1]] post in posts %}\n    <li>{{ post.title }}</li>\n  {% [[2]] %}\n</ul>',
                 [['for'], ['endfor']],
                 '{% %} steuert die Logik (for, if, block), {{ }} gibt Werte aus. Jede for-Schleife endet mit endfor.',
                 'Wie in Python, nur mit End-Tag.'),
            order('m5-4', 'Das Erbe antreten',
                  'Bringe das Child-Template in die richtige Reihenfolge.',
                  [{'id': 'a', 'text': '{% extends "base.html" %}'},
                   {'id': 'b', 'text': '{% block content %}'},
                   {'id': 'c', 'text': '<h1>Showdown</h1>'},
                   {'id': 'd', 'text': '{% endblock %}'}],
                  [['a', 'b', 'c', 'd']],
                  'extends muss als Erstes stehen. Danach füllt der block den Platzhalter aus base.html, endblock schließt ihn.',
                  'Der Block umschließt den Inhalt.'),
            bug('m5-5', 'Das fehlende Argument',
                'Diese View soll ein Template rendern, wirft aber einen Fehler. Klicke die Zeile.',
                ['def index(request):',
                 '    posts = POSTS',
                 "    return render('core/index.html', {'posts': posts})"],
                [3],
                "render() braucht als erstes Argument das request: render(request, 'core/index.html', context).",
                'Wer fragt, muss mit in die Antwort.'),
            quiz('m5-6', 'Statisch wie ein Kaktus',
                 'Wie bindest du core/static/core/style.css im Template ein?',
                 ["{% load static %} und {% static 'core/style.css' %}",
                  'import static in der views.py',
                  "<link href='style.css'> reicht immer",
                  "{% include 'style.css' %}"],
                 0,
                 'Mit {% load static %} lädt man die Tag-Bibliothek, {% static %} baut die richtige URL. Voraussetzung: django.contrib.staticfiles und STATIC_URL in settings.py.',
                 'Erst laden, dann benutzen.'),
        ],
    },
    {
        'id': 'm6',
        'title': 'Der letzte Ritt',
        'section': 'Sektion IV – Aufgabe',
        'intro': 'Letzte Runde, Fremder. Alles, was du gelernt hast, auf einen Streich.',
        'outro': 'Du bist ICH. Und wiederholst dich nicht. Django Unchained: Mission erfüllt!',
        'exercises': [
            bug('m6-1', 'Der vergessene Import',
                'Beim Start kracht es mit einem NameError. Klicke die Zeile, die schuld ist.',
                ['from django.contrib import admin',
                 'from django.urls import path',
                 '',
                 'urlpatterns = [',
                 "    path('admin/', admin.site.urls),",
                 "    path('', include('core.urls')),",
                 ']'],
                [2, 6],
                'include wird verwendet, aber nicht importiert. Richtig ist: from django.urls import path, include.',
                'Woher kommt include?'),
            fill('m6-2', 'Der Finderlohn',
                 'Suche den Post per Slug und melde sauber, wenn es ihn nicht gibt.',
                 "def post_by_slug(request, post_slug):\n    for post in POSTS:\n        if post['slug'] == [[1]]:\n            return JsonResponse(post)\n    raise [[2]]('Post nicht gefunden')",
                 [['post_slug'], ['Http404']],
                 'Der Slug kommt als Parameter in die View. Wird nichts gefunden, löst raise Http404 die saubere 404-Antwort aus.',
                 'Der Parameter steht in der Funktionssignatur.'),
            quiz('m6-3', 'Die letzte Frage',
                 'Mit DEBUG = False soll bei einem Http404 deine eigene Seite erscheinen. Was brauchst du?',
                 ['Eine 404.html im Template-Verzeichnis und gesetzte ALLOWED_HOSTS',
                  'Nur ein neues Model',
                  'Eine zweite settings.py',
                  'Nichts, Django erkennt das selbst'],
                 0,
                 'Bei DEBUG=False sucht Django eine 404.html in den Templates. Zusätzlich muss ALLOWED_HOSTS gesetzt sein, sonst verweigert der Server die Anfragen.',
                 'Zwei Dinge: eine Datei und eine Einstellung.'),
        ],
    },
    {
        'id': 'm7',
        'title': 'Die Schatzkammer',
        'section': 'Backend 06 – Datenbanken & Admin',
        'intro': 'Daten sind das Gold des Westens. Lerne, wie du sie sicherst und verwaltest.',
        'outro': 'Deine Datenbank ist sicher. Das Gesetz des ORM ist auf deiner Seite.',
        'exercises': [
            quiz('m7-1', 'Der blinde Passagier',
                 'Wofür steht die Abkürzung ORM in Django?',
                 ['Object-Relational Mapping', 'Online Resource Management', 
                  'Optimal Routing Module', 'Original Raw Model'],
                 0,
                 'Das ORM verbindet Python-Objekte mit relationalen Datenbank-Tabellen.',
                 'Es hat mit Objekten und Beziehungen zu tun.'),
            fill('m7-2', 'Die Migrations-Kutsche',
                 'Welcher Befehl bringt die Änderungen an den Models in die Datenbank?',
                 'python manage.py [[1]]\npython manage.py [[2]]',
                 [['makemigrations'], ['migrate']],
                 'makemigrations erstellt die Datei, migrate wendet sie auf die Datenbank an.',
                 'Erst erstellen, dann anwenden.'),
        ],
    },
    {
        'id': 'm8',
        'title': 'Die Revolverhelden (DRF)',
        'section': 'Backend 07 – Django Rest Framework',
        'intro': 'Eine API ist dein schnellster Colt. Lerne, wie du sie ziehst.',
        'outro': 'Deine API feuert sauberes JSON. Die Kopfgeldjäger können kommen.',
        'exercises': [
            quiz('m8-1', 'Die Waffe ziehen',
                 'Wofür ist der ModelSerializer zuständig?',
                 ['Er baut das Frontend.', 'Er wandelt Models in JSON um und validiert Daten.', 
                  'Er startet den Server.', 'Er schreibt die HTML-Templates.'],
                 1,
                 'Der ModelSerializer generiert automatisch Felder und Validierung für deine API.',
                 'Er ist der Türsteher zwischen Model und JSON.'),
            fill('m8-2', 'Der Router',
                 'Welche Klasse generiert automatisch alle CRUD-URLs für ein ViewSet?',
                 'from rest_framework.routers import [[1]]',
                 [['DefaultRouter']],
                 'Der DefaultRouter erstellt vollautomatisch die URLs für deine ViewSets.',
                 'Er fängt mit Default an.'),
        ],
    },


    {
        'id': 'm9',
        'title': 'Der Sheriff kennt dein Gesicht',
        'section': 'Backend 08 – Authentication & Authorization',
        'intro': 'Halt, Fremder! Bevor du den Saloon betrittst, musst du beweisen, wer du bist. Und selbst dann entscheidet der Sheriff, was du darfst.',
        'outro': 'Deine Identität ist bestätigt. Du kennst den Unterschied zwischen Anmeldung und Berechtigung. Der Sheriff nickt anerkennend.',
        'exercises': [
            quiz('m9-1', 'Wer bist du, Fremder?',
                 'Was ist der Unterschied zwischen Authentication und Authorization?',
                 [
                     'Authentication prüft die Identität, Authorization die Berechtigungen.',
                     'Authentication prüft Berechtigungen, Authorization die Identität.',
                     'Beide Begriffe beschreiben ausschließlich das Login.',
                     'Authentication ist nur für Administratoren gedacht.'
                 ],
                 0,
                 'Authentication beantwortet die Frage: Wer bist du? Authorization beantwortet: Was darfst du? Erst wird die Identität festgestellt, anschließend werden Berechtigungen geprüft.',
                 'Ein Begriff prüft deine Identität, der andere deine Rechte.'),

            quiz('m9-2', 'Das geheime Passwort',
                 'Wie speichert Django das Passwort eines Users in der Datenbank?',
                 [
                     'Als normalen Klartext im username-Feld.',
                     'Verschlüsselt im email-Feld.',
                     'Als Hash mit zusätzlichen Sicherheitsinformationen im password-Feld.',
                     'Gar nicht. Das Passwort bleibt ausschließlich im Browser.'
                 ],
                 2,
                 'Django speichert kein Klartextpasswort. Im Feld password liegt ein kodierter Passwort-Hash mit Informationen zum verwendeten Verfahren und Salt. Django kann damit Passwörter sicher überprüfen.',
                 'Suche nach einer Einwegfunktion statt nach einer normalen Verschlüsselung.'),

            quiz('m9-3', 'Der Türsteher',
                 'Was macht die Django-Funktion authenticate() bei einer Anmeldung?',
                 [
                     'Sie erstellt automatisch einen neuen Benutzer.',
                     'Sie überprüft die Zugangsdaten und liefert einen passenden User oder None zurück.',
                     'Sie vergibt automatisch Administratorrechte.',
                     'Sie erstellt einen Token für jeden Benutzer.'
                 ],
                 1,
                 'authenticate() prüft die übergebenen Zugangsdaten über die konfigurierten Authentication Backends. Bei erfolgreicher Prüfung wird ein User-Objekt zurückgegeben, andernfalls None.',
                 'Die Funktion kontrolliert Zugangsdaten, erstellt aber nicht automatisch einen Account.'),

            quiz('m9-4', 'Der offene Saloon',
                 'Warum bekommt eine Login-APIView häufig permission_classes = [AllowAny]?',
                 [
                     'Damit nur Administratoren sich anmelden können.',
                     'Damit alle Benutzer automatisch Superuser werden.',
                     'Damit Django die Passwortprüfung überspringt.',
                     'Damit auch noch nicht angemeldete Benutzer den Login-Endpunkt aufrufen dürfen.'
                 ],
                 3,
                 'Ein Login muss auch für nicht angemeldete Besucher erreichbar sein. AllowAny erlaubt den Zugriff unabhängig vom bisherigen Anmeldestatus. Die Zugangsdaten werden trotzdem geprüft.',
                 'Ein Benutzer kann sich schlecht anmelden, wenn er dafür bereits angemeldet sein müsste.'),

            fill('m9-5', 'Die Anmeldung am Sheriff-Schalter',
                 'Vervollständige die Login-APIView. Ungültige Zugangsdaten müssen mit HTTP 401 beantwortet werden.',
                 'from django.contrib.auth import authenticate\nfrom rest_framework.views import APIView\nfrom rest_framework.response import Response\nfrom rest_framework import status\n\nclass LoginView([[1]]):\n    def post(self, request):\n        user = [[2]](\n            request,\n            username=request.data.get("username"),\n            password=request.data.get("password")\n        )\n        if user is None:\n            return Response(\n                {"detail": "Ungültige Zugangsdaten"},\n                status=status.[[3]]\n            )\n        return Response({"detail": "Anmeldung erfolgreich"})',
                 [
                     ['APIView'],
                     ['authenticate'],
                     ['HTTP_401_UNAUTHORIZED', 'HTTP_401']
                 ],
                 'Eine APIView verarbeitet den Request. authenticate() prüft Benutzername und Passwort. Gibt die Funktion None zurück, antwortet die API mit HTTP 401 Unauthorized.',
                 'Achte auf die Basisklasse, die Funktion zur Prüfung und den HTTP-Status für fehlende gültige Zugangsdaten.'),

            bug('m9-6', 'Der falsche Passwortvergleich',
                'Der Sheriff vergleicht das eingegebene Passwort direkt mit dem Datenbankwert. Welche Zeile ist fehlerhaft?',
                [
                    'def verify_password(user, raw_password):',
                    '    if user is None:',
                    '        return False',
                    '    if user.password == raw_password:',
                    '        return True',
                    '    return False'
                ],
                [4],
                'Das Passwortfeld enthält einen kodierten Hash und nicht das ursprüngliche Passwort. Ein direkter Vergleich kann deshalb nicht funktionieren. Django bietet user.check_password(raw_password) für die sichere Überprüfung an.',
                'Im User-Objekt liegt nicht das ursprüngliche Passwort im Klartext.')
        ],
    },


    {
        'id': 'm10',
        'title': 'Zutritt nur mit Erlaubnis',
        'section': 'Backend 08 – Permissions',
        'intro': 'Der Sheriff hat neue Regeln aufgestellt. Nicht jeder darf den Saloon betreten. Manche dürfen nur zuschauen, andere müssen ihre Identität nachweisen. Und wer an fremdes Eigentum will, braucht eine besondere Erlaubnis.',
        'outro': 'Du kennst jetzt die Regeln des Saloon. Du kannst Zugriffe auf ganze Views und einzelne Objekte kontrollieren. Der Sheriff übergibt dir seinen Schlüssel.',
        'exercises': [
            quiz('m10-1', 'Das Gesetz des Sheriffs',
                 'Was bewirkt DEFAULT_PERMISSION_CLASSES in der REST_FRAMEWORK-Konfiguration?',
                 [
                     'Es legt die Standard-Berechtigungen für API-Views fest, sofern eine View keine eigenen Permissions definiert.',
                     'Es legt fest, welche Benutzer sich registrieren dürfen.',
                     'Es bestimmt, welche Serializer verwendet werden.',
                     'Es aktiviert automatisch die Token-Authentifizierung.'
                 ],
                 0,
                 'DEFAULT_PERMISSION_CLASSES definiert die globalen Standardberechtigungen für DRF. Eine View kann diese mit eigenen permission_classes überschreiben.',
                 'Es geht um die Voreinstellung für den Zugriff auf API-Endpunkte.'),

            quiz('m10-2', 'Nur mit Ausweis',
                 'Was erlaubt die Permission-Klasse IsAuthenticatedOrReadOnly?',
                 [
                     'Alle Benutzer dürfen sämtliche HTTP-Methoden verwenden.',
                     'Nicht angemeldete Benutzer dürfen nur sichere Methoden wie GET, HEAD und OPTIONS verwenden. Schreibzugriffe erfordern eine Anmeldung.',
                     'Nur Administratoren dürfen GET-Requests ausführen.',
                     'Angemeldete Benutzer dürfen ausschließlich GET verwenden.'
                 ],
                 1,
                 'IsAuthenticatedOrReadOnly erlaubt anonymen Benutzern lesende Zugriffe über sichere Methoden. Für POST, PUT, PATCH und DELETE muss der Benutzer angemeldet sein.',
                 'Unterscheide zwischen Lesen und Verändern von Daten.'),

            quiz('m10-3', 'Der Sheriff entscheidet',
                 'Welche Voraussetzung prüft die DRF-Permission IsAdminUser standardmäßig?',
                 [
                     'Der Benutzer muss eine gültige E-Mail-Adresse besitzen.',
                     'Der Benutzer muss mindestens einen Token besitzen.',
                     'Der Benutzer muss die Eigenschaft is_staff = True haben.',
                     'Der Benutzer muss ein Superuser sein.'
                 ],
                 2,
                 'IsAdminUser prüft request.user.is_staff. Ein Benutzer muss also als Mitarbeiter gekennzeichnet sein. Die Permission verlangt nicht ausdrücklich is_superuser = True.',
                 'Schau auf die Kennzeichnung, die Django für den Zugang zum Admin-Bereich verwendet.'),

            fill('m10-4', 'Die Hausordnung',
                 'Konfiguriere globale Berechtigungen so, dass nur angemeldete Benutzer standardmäßig auf die API zugreifen dürfen.',
                 "REST_FRAMEWORK = {\n    'DEFAULT_PERMISSION_CLASSES': [\n        'rest_framework.permissions.[[1]]',\n    ],\n}",
                 [['IsAuthenticated']],
                 'Mit IsAuthenticated werden nicht angemeldete Benutzer standardmäßig abgewiesen. Für einzelne öffentliche Endpunkte kann eine View weiterhin AllowAny verwenden.',
                 'Die Permission beginnt mit Is und verlangt einen angemeldeten Benutzer.'),

            fill('m10-5', 'Der persönliche Türsteher',
                 'Schreibe eine eigene has_permission-Prüfung, die nur angemeldeten Benutzern Zugriff gewährt.',
                 "from rest_framework.permissions import BasePermission\n\nclass IsLoggedIn(BasePermission):\n    def has_permission(self, request, view):\n        return request.user.[[1]]",
                 [['is_authenticated']],
                 'has_permission() prüft den Zugriff auf die gesamte View. request.user.is_authenticated liefert True für angemeldete Benutzer und False für anonyme Benutzer.',
                 'Django stellt am User-Objekt eine Eigenschaft bereit, die den Anmeldestatus angibt.'),

            order('m10-6', 'Die Prüfung am Tresor',
                  'Bringe die Schritte einer Objektprüfung in einer DRF-Detail-View in die richtige Reihenfolge.',
                  [
                      {'id': 'c', 'text': 'has_object_permission(request, view, obj) prüft den Zugriff auf das Objekt.'},
                      {'id': 'a', 'text': 'has_permission(request, view) prüft den grundsätzlichen Zugriff auf die View.'},
                      {'id': 'd', 'text': 'Bei erlaubtem Zugriff verarbeitet die View das Objekt und erstellt die Response.'},
                      {'id': 'b', 'text': 'get_object() ermittelt das angeforderte Datenbankobjekt.'}
                  ],
                  [['a', 'b', 'c', 'd']],
                  'Zuerst wird die View-Berechtigung geprüft. Danach wird das Objekt ermittelt. Bei generischen DRF-Views führt get_object() anschließend die Objektprüfung über check_object_permissions() aus. Erst danach kann die View regulär mit dem Objekt arbeiten. Achtung: Bei Listen-Endpunkten werden Objektberechtigungen nicht automatisch für jedes einzelne Ergebnis geprüft.',
                  'Erst die Tür kontrollieren, dann den Tresor finden und anschließend dessen Schloss prüfen.'),

            bug('m10-7', 'Der fehlerhafte Türsteher',
                'Die eigene Objektberechtigung IsOwner soll prüfen, ob ein Benutzer Eigentümer eines Objekts ist. Klicke die fehlerhafte Zeile.',
                [
                    'class IsOwner(BasePermission):',
                    '    def has_object_permission(self, request, view):',
                    '        return obj.owner == request.user',
                    '',
                    '# Die Permission wird auf ein einzelnes Objekt angewendet.'
                ],
                [2],
                'Die Methodensignatur ist unvollständig. DRF übergibt bei einer Objektprüfung auch das zu prüfende Objekt. Richtig lautet die Signatur: def has_object_permission(self, request, view, obj):. Erst dadurch kann die Methode auf obj.owner zugreifen.',
                'Welche zusätzlichen Informationen benötigt eine Objektprüfung gegenüber einer normalen View-Prüfung?'),

            quiz('m10-8', 'Fremdes Eigentum',
                 'Ein Benutzer darf seine eigenen Beiträge bearbeiten, aber nicht die Beiträge anderer Benutzer. Welche Prüfung gehört dafür in eine IsOwner-Permission?',
                 [
                     'return obj.owner == request.user',
                     'return request.method == "POST"',
                     'return request.user.is_staff',
                     'return obj.owner is not None'
                 ],
                 0,
                 'Der Vergleich obj.owner == request.user prüft, ob der angemeldete Benutzer tatsächlich Eigentümer des angeforderten Objekts ist. Eine solche Prüfung gehört in has_object_permission().',
                 'Vergleiche den Eigentümer des Datensatzes mit dem aktuell angemeldeten Benutzer.')
        ],
    },


    {
        'id': 'm11',
        'title': 'Der Schlüssel zum Tresor',
        'section': 'Backend 08 – Token Authentication',
        'intro': 'Ein API-Zugang braucht einen Schlüssel. Du lernst Registrierung, Login und Token Authentication.',
        'outro': 'Der Schlüssel sitzt. Deine API erkennt ihre Benutzer.',
        'exercises': [
            quiz('m11-1', 'Der persönliche Schlüssel',
                 'Was ist die Aufgabe der Token Authentication?',
                 ['Sie verschlüsselt die gesamte Datenbank',
                  'Sie authentifiziert Requests anhand eines Tokens',
                  'Sie ersetzt alle Django-Models',
                  'Sie erstellt automatisch Benutzer'],
                 1,
                 'Der Client sendet bei geschützten Requests einen Token im Authorization-Header. Django REST Framework identifiziert damit den Benutzer.',
                 'Der Client weist seine Identität mit einem Schlüssel nach.'),

            fill('m11-2', 'Den Tresor vorbereiten',
                 'Aktiviere die Token-App in Django.',
                 "INSTALLED_APPS = [\n    'django.contrib.auth',\n    'rest_framework',\n    'rest_framework.[[1]]',\n]",
                 [['authtoken']],
                 'rest_framework.authtoken stellt die Token-Modelle und die dazugehörige Authentication bereit.',
                 'Die App heißt authtoken.'),

            order('m11-3', 'Die Schlüssel schmieden',
                  'Bringe die Einrichtung der Token Authentication in die richtige Reihenfolge.',
                  [
                      {'id': 'a', 'text': "'rest_framework.authtoken' zu INSTALLED_APPS hinzufügen"},
                      {'id': 'b', 'text': 'python manage.py migrate'},
                      {'id': 'c', 'text': 'TokenAuthentication in REST_FRAMEWORK konfigurieren'},
                      {'id': 'd', 'text': 'Geschützten API-Request mit Authorization-Header senden'}
                  ],
                  [['a', 'b', 'c', 'd']],
                  'Zuerst wird die App aktiviert, dann werden die Datenbanktabellen angelegt. Danach wird die Authentifizierung konfiguriert und der Token verwendet.',
                  'Ohne Migration existiert die Token-Tabelle noch nicht.'),

            fill('m11-4', 'Den Eingang bewachen',
                 'Ergänze den Authentication-Header für einen Token-Request.',
                 "Authorization: [[1]] <dein-token>",
                 [['Token']],
                 'DRF erwartet bei der Standard-TokenAuthentication das Schema Token gefolgt vom Token-Schlüssel.',
                 'Nicht Bearer, sondern Token.'),

            quiz('m11-5', 'Die Registrierung',
                 'Warum muss bei der Registrierung create_user() statt create() verwendet werden?',
                 ['Weil create_user() das Passwort korrekt hasht',
                  'Weil create() keine Datenbankeinträge erstellt',
                  'Weil create_user() automatisch einen Admin erstellt',
                  'Weil create() nur für GET funktioniert'],
                 0,
                 'create_user() verwendet set_password() und speichert das Passwort als sicheren Hash. create() würde das Passwort ohne zusätzliche Verarbeitung im Klartext speichern.',
                 'Denke an die Passwortverschlüsselung.'),

            bug('m11-6', 'Das Passwort liegt offen',
                'Klicke die fehlerhafte Zeile bei der Registrierung.',
                [
                    'def register(request):',
                    "    username = request.data['username']",
                    "    password = request.data['password']",
                    '    user = User.objects.create(',
                    '        username=username,',
                    '        password=password',
                    '    )',
                    '    return Response({"id": user.id})'
                ],
                [4, 6],
                'User.objects.create() speichert das Passwort nicht automatisch als Hash. Verwende User.objects.create_user(username=username, password=password).',
                'Ein Passwort darf niemals ungeschützt gespeichert werden.')
        ],
    },
    {
        'id': 'm12',
        'title': 'Der API-Prüfstand',
        'section': 'Backend 09 – Postman & API-Tests',
        'intro': 'Ein Revolverheld prüft seine Waffe. Du prüfst deine API mit Postman: erfolgreiche und fehlerhafte Requests.',
        'outro': 'Deine API ist getestet. Du weißt, wann sie trifft und wann sie abweist.',
        'exercises': [
            quiz('m12-1', 'Der erste Testschuss',
                 'Wofür verwendest du Postman?',
                 ['Zum Schreiben von Django-Models',
                  'Zum Testen von HTTP-Requests und API-Antworten',
                  'Zum Erstellen von CSS-Dateien',
                  'Zum Starten der Datenbank'],
                 1,
                 'Postman ermöglicht das Senden von HTTP-Requests und die Prüfung von Statuscodes, Headern und Response-Bodies.',
                 'Du testest damit deine API unabhängig vom Frontend.'),

            fill('m12-2', 'Die richtige Adresse',
                 'Ergänze die HTTP-Methode zum Abrufen einer Ressourcenliste.',
                 '[[1]] http://localhost:8000/api/boards/',
                 [['GET']],
                 'GET ruft vorhandene Ressourcen ab. Es soll dabei keine neue Ressource angelegt werden.',
                 'Lesen statt schreiben.'),

            quiz('m12-3', 'Kein Schlüssel, kein Zutritt',
                 'Was sollte eine geschützte API bei einem Request ohne gültige Authentifizierung zurückgeben?',
                 ['200 OK',
                  '201 Created',
                  '401 Unauthorized',
                  '404 Not Found'],
                 2,
                 'Eine nicht authentifizierte Anfrage an einen geschützten Endpunkt wird mit 401 beantwortet, wenn die verwendete Authentifizierungskonfiguration diesen Status vorsieht.',
                 'Der Benutzer konnte seine Identität nicht nachweisen.'),

            fill('m12-4', 'Den Token einsetzen',
                 'Ergänze die Postman-Header für einen authentifizierten Request.',
                 'Key: Authorization\nValue: [[1]] abc123token',
                 [['Token']],
                 'Der Header heißt Authorization. Der Wert beginnt bei DRFs TokenAuthentication mit Token und danach folgt der Schlüssel.',
                 'Schema und Token werden durch ein Leerzeichen getrennt.'),

            quiz('m12-5', 'Happy Path oder Fehler?',
                 'Du sendest einen gültigen POST mit korrekten Daten. Die Ressource wird angelegt. Welcher Statuscode ist typisch?',
                 ['200 OK',
                  '201 Created',
                  '401 Unauthorized',
                  '404 Not Found'],
                 1,
                 '201 Created signalisiert, dass eine neue Ressource erfolgreich angelegt wurde.',
                 'Die Ressource wurde neu erstellt.'),

            order('m12-6', 'Die Teststrecke',
                  'Bringe einen vollständigen API-Testablauf in die richtige Reihenfolge.',
                  [
                      {'id': 'a', 'text': 'Request-Methode und URL auswählen'},
                      {'id': 'b', 'text': 'Authorization-Header mit Token setzen'},
                      {'id': 'c', 'text': 'Request senden'},
                      {'id': 'd', 'text': 'Statuscode und Response-Body prüfen'}
                  ],
                  [['a', 'b', 'c', 'd']],
                  'Zuerst definierst du Request und URL, dann setzt du die Authentifizierung. Anschließend sendest du den Request und kontrollierst die Antwort.',
                  'Die Antwort kannst du erst nach dem Absenden prüfen.')
        ],
    },
    {
        'id': 'm13',
        'title': 'KanMind – Der letzte Auftrag',
        'section': 'Backend 10 – Abschlussprojekt KanMind',
        'intro': 'Der letzte Auftrag wartet. Verbinde Authentifizierung, Serializer, Views, Permissions und API-Tests zu einer funktionierenden Anwendung.',
        'outro': 'Auftrag erledigt! Du hast Django REST Framework nicht nur verstanden, sondern kannst es einsetzen.',
        'exercises': [
            quiz('m13-1', 'Der Bauplan',
                 'Welche Aufgabe hat ein Serializer in Django REST Framework?',
                 ['Er verwaltet die URL-Routen',
                  'Er wandelt Daten zwischen Python-Objekten und JSON um und validiert Eingaben',
                  'Er startet den Server',
                  'Er erstellt automatisch HTML-Seiten'],
                 1,
                 'Serializer übernehmen die Umwandlung und Validierung von Daten. ModelSerializer kann Felder eines Models automatisch abbilden.',
                 'Denk an die Verbindung zwischen Model und JSON.'),

            fill('m13-2', 'Das Board erstellen',
                 'Ergänze den Serializer für ein Board-Model.',
                 'class BoardSerializer(serializers.[[1]]):\n    class Meta:\n        model = Board\n        fields = [[2]]',
                 [['ModelSerializer'], ['__all__']],
                 'ModelSerializer erstellt die Felder anhand des Models. fields = "__all__" nimmt alle Model-Felder auf. In echten APIs sollten sensible Felder bewusst ausgeschlossen werden.',
                 'Der Serializer soll direkt auf dem Model basieren.'),

            quiz('m13-3', 'Wer darf das Board sehen?',
                 'Welche Permission erlaubt nur authentifizierten Benutzern den Zugriff?',
                 ['AllowAny',
                  'IsAuthenticated',
                  'IsAdminUser',
                  'ReadOnly'],
                 1,
                 'IsAuthenticated verlangt einen angemeldeten Benutzer. Nicht angemeldete Benutzer erhalten keinen Zugriff auf den geschützten Endpunkt.',
                 'Der Name der Permission verrät die Bedingung.'),

            fill('m13-4', 'Die Eigentümerprüfung',
                 'Ergänze die Objektberechtigung, damit nur der Besitzer ein Objekt bearbeiten darf.',
                 'def has_object_permission(self, request, view, obj):\n    return obj.owner == [[1]]',
                 [['request.user']],
                 'request.user ist der aktuell authentifizierte Benutzer. Der Vergleich mit obj.owner prüft, ob der Benutzer Eigentümer des Objekts ist.',
                 'Vergleiche den Besitzer mit dem angemeldeten Benutzer.'),

            bug('m13-5', 'Das offene Tor',
                'Ein fremder Benutzer kann ein Board bearbeiten. Klicke die fehlerhafte Zeile.',
                [
                    'class IsOwner(permissions.BasePermission):',
                    '    def has_object_permission(self, request, view, obj):',
                    '        if request.method in SAFE_METHODS:',
                    '            return True',
                    '        return True'
                ],
                [5],
                'Die letzte Zeile erlaubt jedem Benutzer Änderungen. Richtig ist beispielsweise return obj.owner == request.user. Sichere Lesezugriffe und Schreibzugriffe müssen getrennt betrachtet werden.',
                'Die letzte Zeile entscheidet über die Schreibberechtigung.'),

            order('m13-6', 'Der letzte Auftrag',
                  'Ordne die Bausteine eines typischen KanMind-API-Aufbaus.',
                  [
                      {'id': 'a', 'text': 'Models für Boards und Tasks definieren'},
                      {'id': 'b', 'text': 'Serializer und Validierung erstellen'},
                      {'id': 'c', 'text': 'Views und Permissions implementieren'},
                      {'id': 'd', 'text': 'URLs und Router verbinden'},
                      {'id': 'e', 'text': 'API mit Postman testen'}
                  ],
                  [['a', 'b', 'c', 'd', 'e']],
                  'Die Datenstruktur bildet die Grundlage. Danach folgen Serialisierung, Zugriffskontrolle, Routing und abschließende API-Tests.',
                  'Ohne Models gibt es keine Datenstruktur.')
        ],
    },

]

EXERCISES = {ex['id']: ex for m in MISSIONS for ex in m['exercises']}


# ---------- Ausgabe an den Browser und Prüfung ----------

def _public(ex):
    pub = {k: v for k, v in ex.items() if k not in ('solution', 'explain')}
    if ex['type'] == 'order':
        items = copy.deepcopy(ex['items'])
        while True:
            random.shuffle(items)
            if [i['id'] for i in items] not in ex['solution']:
                break
        pub['items'] = items
    return pub


def public_missions():
    result = []
    for m in MISSIONS:
        pub = {k: v for k, v in m.items() if k != 'exercises'}
        pub['exercises'] = [_public(ex) for ex in m['exercises']]
        result.append(pub)
    return result


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _norm(value):
    return ' '.join(str(value).replace('"', "'").split())


def check(ex, answer):
    """Gibt (richtig?, Details pro Lücke oder None) zurück."""
    kind, sol = ex['type'], ex['solution']
    if kind in ('quiz', 'live'):
        return _is_int(answer) and answer == sol, None
    if kind == 'bug':
        return _is_int(answer) and answer in sol, None
    if kind == 'order':
        return answer in sol, None
    if kind == 'fill':
        if not isinstance(answer, list) or len(answer) != len(sol):
            return False, None
        details = [_norm(a) in [_norm(s) for s in accepted] for a, accepted in zip(answer, sol)]
        return all(details), details
    return False, None