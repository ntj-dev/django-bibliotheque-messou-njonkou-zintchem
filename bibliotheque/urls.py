from django.urls import path, register_converter
from . import convertisseur, views

register_converter(convertisseur.ConvertisseurISBN, "conv_isbn")

urlpatterns = [
    
    #path("livres/", views.liste_livres, name="liste-livres"),=

    # La page nouveaute n'affiche jamais ce qu'on attent car une requete vers elle correspond au motif "livres/<str:isbn>/"
    # donc django essaye de trouver un livre avec pour isbn "nouveautes", il ne va jamais atteindre la vue nouveautes
    
    #Pour corriger cela on doit inverser l'ordre des motifs, les motifs les plus specifiques doivent etre places avant kes motifs plus generaux
    # path("livres/nouveautes/", views.nouveautes, name="nouveautes"),
    # On utilise str car le numero isbn peut contenir des tirets ce qui ne peut etre converti en int
    # path("livres/<conv_isbn:isbn>/", views.detail_livre, name="detail-livre"),
    path("livres/ajouter/", views.ajouter_livre, name="ajouter-livre"),
    path("livres.json", views.livres_json, name="livres-json"),
    path("livres/", views.ListeLivresView.as_view()), # Affiche la liste des livres en CBV
    # path("genres/<str:nom>/", views.LivresParGenresView.as_view(), name="livres-par-genre"), # Affiche la liste des livres par genre
    path("livres/<conv_isbn:isbn>/", views.LivreDetailView.as_view(), name='detail_livre'),
    path("genres/<str:nom>/", views.LivresParGenreView.as_view(), name="livres-par-genre"),
    path("livres-genre/", views.lien_livres_par_genre, name="livres_genre"),
    
]