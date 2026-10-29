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