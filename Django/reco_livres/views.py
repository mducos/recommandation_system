from django.shortcuts import render
from django.http import JsonResponse
from .models import Livre
from django.db.models import Q

def bdd_livres(request):
    livres = Livre.objects.all()
    return render(request, 'bdd_livres.html', {'livres': livres})

def recherche_livres(request):
    livres = []
    livres_aimes = request.session.get('livres_aimes', [])

    if 1 not in livres_aimes:
        livres_aimes.append(1)
        request.session['livres_aimes'] = livres_aimes

    if request.method == 'POST':
        query = request.POST.get('search_book', '')
        livres = Livre.objects.filter(Q(titre__icontains=query) | Q(auteur__icontains=query) | Q(annee_publication__icontains=query))
        
        if 'add_to_favorites' in request.POST:
            livre_id = request.POST.get('livre_id')
            if livre_id not in livres_aimes:
                livres_aimes.append(livre_id)
                request.session['livres_aimes'] = livres_aimes

        #livres_aimes_obj = Livre.objects.filter(id__in=livres_aimes)

        # Rediriger vers la même page après le traitement POST
        #return render(request, 'recherche_livre.html', {'livres': livres, 'livres_aimes': livres_aimes})

    livres_aimes_obj = Livre.objects.filter(id__in=livres_aimes)
    print(livres_aimes)
    
    return render(request, 'recherche_livre.html', {'livres': livres, 'livres_aimes': livres_aimes_obj})
