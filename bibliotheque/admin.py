from django.contrib import admin
from .models import Auteur, Livre
# Register your models here.

from .models import Auteur, Livre, Genre, Emprunt, FicheAuteur

admin.site.register(Auteur)
admin.site.register(Livre)
admin.site.register(Genre)
# admin.site.register(Emprunteur)
admin.site.register(Emprunt)
admin.site.register(FicheAuteur)
