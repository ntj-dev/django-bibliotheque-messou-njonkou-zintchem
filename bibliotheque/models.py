from django.db import models

# Create your models here.

class Auteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Genre(models.Model):
    nom = models.CharField(max_length=50)
    class Meta:
        verbose_name = "genre"
        verbose_name_plural = "genres"
    def __str__(self):
        return self.nom

class Livre(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    titre = models.CharField(max_length=200)
    nombre_pages = models.PositiveIntegerField()

    LANGUE_CHOICES = [
        ("fr", "Français"),
        ("en", "Anglais"),
        ("es", "Espagnol"),
        ("de", "Allemand"),
    ]
    resume = models.TextField(blank=True) # car le champ peut etre vide au niveau du formulaire
    langue = models.CharField(max_length=2, choices=LANGUE_CHOICES, blank=True) # car le champ peut etre vide au niveau du formulaire
    date_publication = models.DateField(null=True, blank=True) # La colonne peut contenir NULL en base de donnees
    auteur = models.ForeignKey(
        "Auteur",
        on_delete=models.CASCADE,
        related_name="livres"
    )
    genres = models.ManyToManyField("Genre", related_name="livres", blank=True)

    class Meta:
        ordering = ["titre"]
    def __str__(self):
        return self.titre
    @property
    def est_disponible(self):
        return not self.emprunts.filter(date_retour_effective__isnull=True).exists()

    def save(self, *args, **kwargs):
        self.titre = self.titre.title()
        super().save(*args, **kwargs)

# class Emprunteur(models.Model):
#     nom = models.CharField(max_length=100)
#     email = models.EmailField()

#     livres = models.ManyToManyField(
#         "Livre",
#         through="Emprunt",
#         related_name="emprunteurs",
#     )
#     def __str__(self):
#         return self.nom


class Emprunt(models.Model):
    emprunteur = models.ForeignKey(
        "membres.Emprunteur",
        on_delete=models.CASCADE,
    )
    livre = models.ForeignKey("Livre", on_delete=models.CASCADE, related_name="emprunts")
    date_emprunt = models.DateField()
    date_retour_prevue = models.DateField()
    date_retour_effective = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.emprunteur} — {self.livre} ({self.date_emprunt})"


class FicheAuteur(models.Model):
    auteur = models.OneToOneField(
        "Auteur",
        on_delete=models.CASCADE,
        related_name="fiche",
    )
    biographie = models.TextField(blank=True)
    site_web = models.URLField(blank=True)
    def __str__(self):
        return f"Fiche de {self.auteur}"