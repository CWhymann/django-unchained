import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Mission, Exercise

def create_content():
    """Populate database with Backend 06 and 07 missions."""
    
    # Mission 7: Backend 06
    m7, _ = Mission.objects.get_or_create(
        code='m7',
        defaults={
            'title': 'Die Schatzkammer',
            'section': 'Backend 06 – Datenbanken & Admin',
            'intro': 'Daten sind das Gold des Westens. Lerne, wie du sie sicherst und verwaltest.',
            'outro': 'Deine Datenbank ist sicher. Das Gesetz des ORM ist auf deiner Seite.',
            'order': 7
        }
    )

    Exercise.objects.get_or_create(
        code='m7-1', mission=m7, type='quiz', order=1,
        title='Der blinde Passagier',
        question='Wofür steht die Abkürzung ORM in Django?',
        data={'options': ['Object-Relational Mapping', 'Online Resource Management', 'Optimal Routing Module', 'Original Raw Model']},
        solution=0,
        explain='Das ORM verbindet Python-Objekte mit relationalen Datenbank-Tabellen.',
        hint='Es hat mit Objekten und Beziehungen zu tun.'
    )

    Exercise.objects.get_or_create(
        code='m7-2', mission=m7, type='fill', order=2,
        title='Die Migrations-Kutsche',
        question='Welcher Befehl bringt die Änderungen an den Models in die Datenbank?',
        data={'code': 'python manage.py [[1]]\npython manage.py [[2]]'},
        solution=[['makemigrations'], ['migrate']],
        explain='makemigrations erstellt die Datei, migrate wendet sie auf die Datenbank an.',
        hint='Erst erstellen, dann anwenden.'
    )

    # Mission 8: Backend 07
    m8, _ = Mission.objects.get_or_create(
        code='m8',
        defaults={
            'title': 'Die Revolverhelden (DRF)',
            'section': 'Backend 07 – Django Rest Framework',
            'intro': 'Eine API ist dein schnellster Colt. Lerne, wie du sie ziehst.',
            'outro': 'Deine API feuert sauberes JSON. Die Kopfgeldjäger können kommen.',
            'order': 8
        }
    )

    Exercise.objects.get_or_create(
        code='m8-1', mission=m8, type='quiz', order=1,
        title='Die Waffe ziehen',
        question='Wofür ist der ModelSerializer zuständig?',
        data={'options': ['Er baut das Frontend.', 'Er wandelt Models in JSON um und validiert Daten.', 'Er startet den Server.', 'Er schreibt die HTML-Templates.']},
        solution=1,
        explain='Der ModelSerializer generiert automatisch Felder und Validierung für deine API.',
        hint='Er ist der Türsteher zwischen Model und JSON.'
    )

    Exercise.objects.get_or_create(
        code='m8-2', mission=m8, type='fill', order=2,
        title='Der Router',
        question='Welche Klasse generiert automatisch alle CRUD-URLs für ein ViewSet?',
        data={'code': 'from rest_framework.routers import [[1]]'},
        solution=[['DefaultRouter']],
        explain='Der DefaultRouter erstellt vollautomatisch die URLs für deine ViewSets.',
        hint='Er fängt mit Default an.'
    )

    print("Daten erfolgreich in die Datenbank geladen!")

if __name__ == '__main__':
    create_content()