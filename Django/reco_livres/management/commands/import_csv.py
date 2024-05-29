# management/commands/import_csv.py
import csv
from django.core.management.base import BaseCommand
from reco_livres.models import Livre

class Command(BaseCommand):
    help = 'Importe les données du fichier CSV vers la base de données'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Chemin du fichier CSV à importer')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Livre.objects.create(
                    id_livre=row['ID (int)'],
                    titre=row['Titre (str)'],
                    auteur=row['Auteur (str)'],
                    annee_publication=row['Date (int)']
                )
        self.stdout.write(self.style.SUCCESS('Importation réussie'))
