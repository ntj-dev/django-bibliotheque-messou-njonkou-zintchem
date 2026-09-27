from django.shortcuts import get_object_or_404

# Create your views here.
# from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .models import Livre, Genre
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic import DetailView


def liste_livres(request):
    livres = Livre.objects.all()
    return livres

def detail_livre(request, isbn):
    livre = Livre.objects.get(isbn=isbn)
    return HttpResponse(livre.titre)
    
def liste_livres(request):
    livres = Livre.objects.all()
    paths_livres =[]
    for livre in livres:
        paths_livres.append(f"<h1><a href='{reverse('detail-livre', args=[livre.isbn])}'>{livre.titre}</a></h1>")
    return HttpResponse(paths_livres)

# 8. Gerer l'abscence d'un livre
# def detail_livre(request, isbn):
#     try:
#         livre = Livre.objects.get(isbn=isbn)
#     except Livre.DoesNotExist:
#         raise Http404("Aucun livre correspondant")
#     return HttpResponse(f"<h1>{livre.titre}</h1>")

# 9. Répondre selon la méthode
def ajouter_livre(request):
    if request.method == "POST":
        return HttpResponse("Requete POST")
    elif request.method == "GET":
        return HttpResponse("Requete GET")
    return HttpResponse("Autre requete")    

# 10. Un endpoint JSON
def livres_json(request):
    data = list(Livre.objects.values())
    return JsonResponse(data, safe=False)

# Le QueryDict vide est faux donc si on renvoit un formulaire vide on ne peut pas le traiter comme un formulaire rempli
# Pour corriger cela on doit verifier la methode de la requete et non pas le contenu du QueryDict
def ajouter_commentaire(request):
    if request.method == "POST":
        # traitement du commentaire
        return HttpResponse("Commentaire ajoute")
    return HttpResponse("Formulaire vide")
    
# 12. Convertir en CBV
# 13. Premier ListView
# Django va chercher un template dans le dossier templates/bibliotheque/livre_list.html, 
# il prend le nom du modele en minuscule et ajoute _list.html
class ListeLivresView(ListView):
    model = Livre
    # 14. Personnaliser la vue générique
    context_object_name = "livres" 
    
    def get_queryset(self):
        return Livre.objects.order_by("titre")


class LivresParGenreView(ListView):
    model = Livre
    template_name = "bibliotheque/livres_par_genre.html"
    context_object_name = "livres"
    
    # 15. Filtrer dynamiquement
    def get_queryset(self):
        self.genre = get_object_or_404(Genre, nom=self.kwargs["nom"])
        return Livre.objects.filter(genres=self.genre)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nombre_livres"] = context["livres"].count()
        context["genre_livre"] = self.genre
        return context

# 17. DetailView : Django se charge desormais de la gestion du livre introuvable
class LivreDetailView(DetailView):
    model = Livre
    pk_url_kwarg = "isbn"

# 18. FBV ou CBV ?
# On préférera une vue générique (CBV) pour les opérations CRUD standards où le comportement est prévisible, 
# afin de maximiser la réutilisation de code

# À l'inverse, on préférera une vue fonction (FBV) lorsque la logique métier est complexe, fortement personnalisée 
# ou implique plusieurs modèles orchestrés hors d'un schéma CRUD classique ;

# 25. Lien vers la page livres par genre
def lien_livres_par_genre(request):
    link = reverse("livres-par-genre", args=["EDUCATION"])
    return HttpResponse(f'<a href="{link}">Voir les livres par genre</a>')

