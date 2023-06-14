from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
import datetime
from django.utils import timezone

from .models import PianoSheet, Musician, Note
from .forms import MusicianForm

from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.views.generic import TemplateView
from django.conf import settings

from piano_app import models


class LoginView(TemplateView):

  template_name = 'login.html'

  def post(self, request, **kwargs):

    username = request.POST.get('username', False)
    #password = request.POST.get('password', False)
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        response = HttpResponseRedirect('/identified/')
        response.set_cookie('first_name', username)
        response.set_cookie('date', datetime.date.today())
        return response

    return render(request, 'identified.html') # Redirection à voir


class LogoutView(TemplateView):

  template_name = 'identified.html'

  def get(self, request, **kwargs):

    logout(request)

    return render(request, self.template_name)


def home(request):
    """Display Home page & Ask for name & redirect on suggestion page."""

    if request.method == "POST":
        cookform = MusicianForm(request.POST)
        if cookform.is_valid():
            name = cookform.cleaned_data['first_name']
            response = HttpResponseRedirect('suggestion')
            response.set_cookie('first_name', name)
            response.set_cookie('date', datetime.date.today())
        return response
    else:
        musicianform = MusicianForm()

    # Add constraints on first_name : only letters & num

    return render(request, 'base.html', {'musicianform': musicianform})


def suggestion(request):
    """
    Suggestion : first suggestion & creation name,
    date & random choice of sheet & interro de BDD Sheet
    """

    href = 0

    # Recup de first_name et date
    first_name = request.COOKIES.get('first_name')
    date = request.COOKIES.get('date')

    # Definition date_visit
    date_visit = timezone.localtime(timezone.now())

    # Choix recette - random v0 # Partitions BDD à créer
    qs = PianoSheet.objects.order_by("?").first()
    rec_id = str(qs)
    sheet_id = int(rec_id)
    sheet = PianoSheet.objects.filter(sheet_id=rec_id).values()

    # Recherche des éléments à afficher
    for elem in sheet:
        title = elem['title'].encode(encoding='UTF-8', errors='strict').decode('UTF-8')
        author = elem['author'].encode(encoding='UTF-8', errors='strict').decode('UTF-8')
        level = elem['level']
        kind = elem['kind']
        compteur = elem['compteur']
        numsheet = elem['numsheet']

    # Mise en forme des éléments
    # ingredients = ingredients.replace("',", '\n')
    # ingredients = ingredients.replace("['", '- ')
    # ingredients = ingredients.replace("']", ' ')
    # ingredients = ingredients.replace("'", '- ')

    # instructions = instructions.replace("\n", '')
    # instructions = instructions.replace(".", '.\n')

    # Incrémentation des recettes choisies
    if compteur is None:
        compteur = 0
    new_compteur = 0
    new_compteur = compteur + 1
    count_recipe = PianoSheet.objects.get(sheet_id=sheet_id)
    count_recipe.compteur = new_compteur
    count_recipe.save()

    # To improve
    # imprim = 0
    # if request.method == 'POST':
    #     if 'imprim' in request.POST:
    #         imprim = 1
    #         # print(imprim)
    #         response = HttpResponse('success')
    #         response.set_cookie('imprim', imprim)
    #         return response
    # else:
    #     imprim = 0
        # print(imprim)

    # Création du user-rating et sauvegarde dans table Note
    save_rating = Note(user_name=first_name,
                       sheet_id=sheet_id, date_visit=date_visit)
    save_rating.save()

    rating_id = save_rating.rating_id
    request.session['rating_id'] = rating_id

    # Sauvegarde des éléments cuisinier dans Bdd #Imprim ici  ou pas?
    data_cook = Musician(first_name=first_name,
                          date_visit=date_visit,
                          sheet_id=sheet_id)
    data_cook.save()
    user_id = data_cook.user_id
    request.session['user_id'] = user_id

    return render(request, 'suggestion.html',
                  {'first_name': first_name, 'date': date, 'title': title,
                   'author': author, 'level': level,
                   'kind': kind, 'compteur': compteur, 'href': href,
                   'user_name': first_name, 'sheet_id': sheet_id,
                   'numsheet' : numsheet,
                   'date_visit': date_visit, 'user_id': user_id})

def suggestions(request):
    """
    Suggestion : first suggestion & creation name,
    date & random choice of sheet & interro de BDD Sheet
    """

    href = 0

    # Recup de first_name et date
    first_name = request.COOKIES.get('first_name')
    date = request.COOKIES.get('date')

    # Definition date_visit
    date_visit = timezone.localtime(timezone.now())

    # Choix recette - random v0 # Partitions BDD à créer
    qs = PianoSheet.objects.order_by("?").first()
    rec_id = str(qs)
    sheet_id = int(rec_id)
    sheet = PianoSheet.objects.filter(sheet_id=rec_id).values()

    # Recherche des éléments à afficher
    for elem in sheet:
        title = elem['title']
        author = elem['author']
        level = elem['level']
        kind = elem['kind']
        compteur = elem['compteur']
        numsheet = elem['numsheet']

    # Mise en forme des éléments
    # ingredients = ingredients.replace("',", '\n')
    # ingredients = ingredients.replace("['", '- ')
    # ingredients = ingredients.replace("']", ' ')
    # ingredients = ingredients.replace("'", '- ')

    # instructions = instructions.replace("\n", '')
    # instructions = instructions.replace(".", '.\n')

    # Incrémentation des recettes choisies
    if compteur is None:
        compteur = 0
    new_compteur = 0
    new_compteur = compteur + 1
    count_recipe = PianoSheet.objects.get(sheet_id=sheet_id)
    count_recipe.compteur = new_compteur
    count_recipe.save()

    # To improve
    # imprim = 0
    # if request.method == 'POST':
    #     if 'imprim' in request.POST:
    #         imprim = 1
    #         # print(imprim)
    #         response = HttpResponse('success')
    #         response.set_cookie('imprim', imprim)
    #         return response
    # else:
    #     imprim = 0
        # print(imprim)

    # Création du user-rating et sauvegarde dans table Note
    save_rating = Note(user_name=first_name,
                       sheet_id=sheet_id, date_visit=date_visit)
    save_rating.save()

    rating_id = save_rating.rating_id
    request.session['rating_id'] = rating_id

    # Sauvegarde des éléments cuisinier dans Bdd #Imprim ici  ou pas?
    data_cook = Musician(first_name=first_name,
                          date_visit=date_visit,
                          sheet_id=sheet_id)
    data_cook.save()
    user_id = data_cook.user_id
    request.session['user_id'] = user_id

    return render(request, 'suggestion.html',
                  {'first_name': first_name, 'date': date, 'title': title,
                   'author': author, 'level': level,
                   'kind': kind, 'compteur': compteur, 'href': href,
                   'user_name': first_name, 'sheet_id': sheet_id,
                   'numsheet' : numsheet,
                   'date_visit': date_visit, 'user_id': user_id})


def continueornot(request, rating):
    """
    Ask for more suggestions
    """
    # Recup de first_name
    first_name = request.COOKIES.get('first_name')

    rating_id = request.session['rating_id']

    # Save rating
    data_rating = Note.objects.get(rating_id=rating_id)

    if (rating >= 0 and rating <= 5):
        data_rating.rating = rating
        data_rating.save()
    else:
        rating = 0
        data_rating.rating = rating
        data_rating.save()

    return render(request, 'continueOrNot.html', {'first_name': first_name})


def tobecontinued(request):
    """
    End of session page
    """
    # Recup de first_name
    first_name = request.COOKIES.get('first_name')

    return render(request, 'toBeContinued.html', {'first_name': first_name})

def custom_404(request, exception):
    """
    Custom 404 page
    """
    return render(request, '404.html', {}, status=404)


def custom_500(request, exception):
    """
    Custom 500 page
    """
    return render(request, '500.html', {}, status=500)
