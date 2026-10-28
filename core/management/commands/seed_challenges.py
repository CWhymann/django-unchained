from django.core.management.base import BaseCommand

from core.models import Challenge

DUMMY_CHALLENGES = [
    ('Der erste Duell-Test', 'Schreibe eine Funktion, die zwei Zahlen addiert.', 'easy'),
    ('Postkutschen-Route', 'Erstelle eine Liste der Stationen und gib sie sortiert aus.', 'medium'),
    ('Goldmine-Tresor', 'Implementiere eine Klasse, die Guthaben verwaltet.', 'hard'),
]


class Command(BaseCommand):
    help = 'Legt Dummy-Challenges an'

    def handle(self, *args, **options):
        for title, description, difficulty in DUMMY_CHALLENGES:
            _, created = Challenge.objects.get_or_create(
                title=title,
                defaults={'description': description, 'difficulty': difficulty},
            )
            status = 'angelegt' if created else 'existiert bereits'
            self.stdout.write(f'{title}: {status}')