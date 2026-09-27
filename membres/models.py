from django.db import models

# Create your models here.

class Emprunteur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    livres = models.ManyToManyField(
        "bibliotheque.Livre",
        through="bibliotheque.Emprunt",
        related_name="emprunteurs",
    )

    def __str__(self):
        return self.nom