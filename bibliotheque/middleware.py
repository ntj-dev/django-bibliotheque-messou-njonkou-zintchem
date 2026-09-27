
import time
from django.http import HttpResponseForbidden
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
from django.urls import resolve

def journalisation_middleware(get_response):
    # 23. MiddlewareNotUsed
    if not getattr(settings, "ACTIVER", False):
        raise MiddlewareNotUsed("Journalisation désactivée")

    def middleware(request):
        print("Requete debut")
        print(f"{request.method} {request.path}")
        response = get_response(request)
        print("Requete fin")
        return response
    return middleware

# 20. Mesurer un temps de traitement
def temps_traitement_middleware(get_response):
    def middleware(request):
        debut = time.perf_counter()
        response = get_response(request)
        duree = (time.perf_counter() - debut) * 1000
        print(f"{request.path} traitee en {duree} ms")
        return response
    return middleware

# 22. Court-circuiter la chaîne
def protection_livres_middleware(get_response):
    def middleware(request):
        if request.path.startswith("/bibliotheque/livres/") and "X-Client-Autorise" not in request.headers:
            return HttpResponseForbidden("Accès refusé")
        return get_response(request)
    return middleware

# 24. Vue ou middleware : il faut utiliser un middleware pour protéger une route car 
# L'enregistrement de la derniere visite doit s'effectuer lors d'une interaction sur le site, 
# peu importe la page ou la vue consultee par l'utilisateur connecte

# 25. Tout assembler : Proteger livre par genre
TOKEN = "jeton"
def protection_genre_middleware(get_response):
    def middleware(request):
        if request.path.startswith("/genres/") and request.headers.get("X-Token") != TOKEN:
            match = resolve(request.path)
            if match.url_name == "livres-par-genre":
                return HttpResponseForbidden("Accès non autorisé")
        return get_response(request)
    return middleware

