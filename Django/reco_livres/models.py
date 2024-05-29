from django.db import models

class Livre(models.Model):
    id_livre = models.IntegerField(null=False)
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    annee_publication = models.IntegerField()

    def __str__(self):
        return self.auteur + " : " + self.titre
