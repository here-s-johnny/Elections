 # This Python file uses the following encoding: utf-8

from __future__ import division

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json
from django.forms.models import model_to_dict
from datetime import datetime
import pytz
from django.db import transaction

from .models import Voivodeship, Candidate, Community, Vote

from django.db.models import Sum

# helper function

def validate_posted_data(vote, date):


    # preparing dates for comparison
    tmp = Community.objects.get(name=vote.community_ptr)  
    # date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    # date_aware = pytz.utc.localize(date)
    # date_aware = date_aware.replace(microsecond=0)
    # tmp.last_modification = tmp.last_modification.replace(microsecond=0)

    # if tmp.last_modification != date_aware:
        # print(date_aware)
        # print(tmp.last_modification)
        # return 4

    if tmp.allowed < int(vote.voting_cards):
        return 1 

    if int(vote.voting_cards) < int(vote.votes):
        return 2

    if int(vote.votes) < int(vote.valid_votes):
        return 3
    return 0

# Create your views here.

def update_vote(request):
    if request.method == 'POST':
        if request.is_ajax():
            name = request.POST.get('name')
            with transaction.atomic():
                comm = Community.objects.get(name=name)
                vote = Vote.objects.select_for_update().filter(community_ptr = comm)
                date = request.POST.get('mod_date')

                vote.update(
                    voting_cards = request.POST.get('voting_cards'),
                    votes = request.POST.get('votes'),
                    valid_votes = request.POST.get('valid_votes'),
                    votes_for_cand_1 = request.POST.get('votes_for_cand_1'),
                    votes_for_cand_2 = request.POST.get('votes_for_cand_2'),
                    # last_modification = timezone.now(),
                )


                vote = vote[0]

                if (validate_posted_data(vote, date) == 0):
                    vote.save()
                    ret = "Success"
                    ret_val = 0
                elif (validate_posted_data(vote, date) == 1):
                    ret = "Liczba dopuszczonych do głosowania jest mniejsza niż wpisana liczba kart do głosowania"
                    ret_val = 1
                elif (validate_posted_data(vote, date) == 2):
                    ret = "Liczba kart do głosowania nie może być mniejsza niż liczba głosów"
                    ret_val = 2
                elif (validate_posted_data(vote, date) == 4):
                    ret = "Od momentu otwarcia okna modyfikacji dane uległy zmianie, spróbuj ponownie"
                    ret_val = 4
                else:
                    ret = "Liczba głosów nie może być mniejsza niż liczba głosów ważnych"
                    ret_val = 3

                data = {"ret" : ret, "ret_val" : ret_val}

                return JsonResponse(data)



def index(request):

    candidates = Candidate.objects.all()
    voivodeships = Voivodeship.objects.all()
    communities = Community.objects.all()
    votes = Vote.objects.all()

    no_of_voivodeships = voivodeships.count()
    no_of_communities = communities.count()

    # da sie bez list???
    citizens = list(Voivodeship.objects.all().aggregate(Sum('citizens')).values())[0]
    allowed = list(Voivodeship.objects.all().aggregate(Sum('allowed')).values())[0]
    voting_cards = list(Voivodeship.objects.all().aggregate(Sum('voting_cards')).values())[0]
    votes = list(Voivodeship.objects.all().aggregate(Sum('votes')).values())[0]
    valid_votes = list(Voivodeship.objects.all().aggregate(Sum('valid_votes')).values())[0]

    votes_for_cand_1 = list(Voivodeship.objects.all().aggregate(Sum('votes_for_cand_1')).values())[0]
    votes_for_cand_2 = list(Voivodeship.objects.all().aggregate(Sum('votes_for_cand_2')).values())[0]


    cand_1_percentage = round((100 * votes_for_cand_1 / valid_votes), 2)
    cand_2_percentage = round((100 - cand_1_percentage), 2)

    tmp = 100 * votes_for_cand_1 / valid_votes

    candidate_1 = Candidate.objects.first()
    candidate_2 = Candidate.objects.last()

    distribution_by_type = []

    distribution_by_type.append( {'id': 1, 'name': 'Miasto',      'valid_votes': 0, 'votes_for_cand_1': 0, 'votes_for_cand_2': 0, 'percent_1': 0, 'percent_2': 0})
    distribution_by_type.append( {'id': 2, 'name': 'Wieś',        'valid_votes': 0, 'votes_for_cand_1': 0, 'votes_for_cand_2': 0, 'percent_1': 0, 'percent_2': 0})
    distribution_by_type.append( {'id': 3, 'name': 'Statki',      'valid_votes': 0, 'votes_for_cand_1': 0, 'votes_for_cand_2': 0, 'percent_1': 0, 'percent_2': 0})
    distribution_by_type.append( {'id': 4, 'name': 'Zagranica',   'valid_votes': 0, 'votes_for_cand_1': 0, 'votes_for_cand_2': 0, 'percent_1': 0, 'percent_2': 0})

    for d in distribution_by_type:
        d['valid_votes'] = list(Vote.objects.filter(community_ptr__kind=d['id']).aggregate(Sum('valid_votes')).values())[0]
        d['votes_for_cand_1'] = list(Vote.objects.filter(community_ptr__kind=d['id']).aggregate(Sum('votes_for_cand_1')).values())[0]
        d['votes_for_cand_2'] = list(Vote.objects.filter(community_ptr__kind=d['id']).aggregate(Sum('votes_for_cand_2')).values())[0]
        if d['votes_for_cand_1'] != None and d['valid_votes'] != None:
            d['percent_1'] = round((100 * d['votes_for_cand_1'] / d['valid_votes']), 2)
        else:
            d['percent_1'] = 0    
        d['percent_2'] = round((100 - d['percent_1']), 2)

    distribution_by_amount = []
     
    distribution_by_amount.append( {'name': 'do 5000',              'valid_votes': 0, 'votes_for_cand_1': 0, 'votes_for_cand_2': 0, 'percent_1': 0, 'percent_2': 0, 'min': 0, 'max': 5000})
    distribution_by_amount.append( {'name': 'od 5001 do 10000',     'valid_votes': 0, 'votes_for_cand_1': 0, 'votes_for_cand_2': 0, 'percent_1': 0, 'percent_2': 0, 'min': 5001, 'max': 10000})
    distribution_by_amount.append( {'name': 'od 10001 do 20000',    'valid_votes': 0, 'votes_for_cand_1': 0, 'votes_for_cand_2': 0, 'percent_1': 0, 'percent_2': 0, 'min': 10001, 'max': 20000})
    distribution_by_amount.append( {'name': 'od 20001 do 50000',    'valid_votes': 0, 'votes_for_cand_1': 0, 'votes_for_cand_2': 0, 'percent_1': 0, 'percent_2': 0, 'min': 20001, 'max': 50000})
    distribution_by_amount.append( {'name': 'od 50001 do 100000',   'valid_votes': 0, 'votes_for_cand_1': 0, 'votes_for_cand_2': 0, 'percent_1': 0, 'percent_2': 0, 'min': 50001, 'max': 100000})
    distribution_by_amount.append( {'name': 'od 100001 do 20000',   'valid_votes': 0, 'votes_for_cand_1': 0, 'votes_for_cand_2': 0, 'percent_1': 0, 'percent_2': 0, 'min': 100001, 'max': 200000})
    distribution_by_amount.append( {'name': 'od 200001 do 500000',  'valid_votes': 0, 'votes_for_cand_1': 0, 'votes_for_cand_2': 0, 'percent_1': 0, 'percent_2': 0, 'min': 200001, 'max': 500000})
    distribution_by_amount.append( {'name': 'pow 500 000',          'valid_votes': 0, 'votes_for_cand_1': 0, 'votes_for_cand_2': 0, 'percent_1': 0, 'percent_2': 0, 'min': 500000, 'max': 100000000})


    for d in distribution_by_amount:
        d['valid_votes'] = list(Vote.objects.filter(community_ptr__citizens__gte=d['min'], community_ptr__citizens__lte=d['max']).aggregate(Sum('valid_votes')).values())[0]
        d['votes_for_cand_1'] = list(Vote.objects.filter(community_ptr__citizens__gte=d['min'], community_ptr__citizens__lte=d['max']).aggregate(Sum('votes_for_cand_1')).values())[0]
        d['votes_for_cand_2'] = list(Vote.objects.filter(community_ptr__citizens__gte=d['min'], community_ptr__citizens__lte=d['max']).aggregate(Sum('votes_for_cand_2')).values())[0]
        if d['votes_for_cand_1'] != None and d['valid_votes'] != None:
            d['percent_1'] = round((100 * d['votes_for_cand_1'] / d['valid_votes']), 2)
        else:
            d['percent_1'] = 0    
        d['percent_2'] = round((100 - d['percent_1']), 2)

    context = { 'candidates' : candidates,
                'voivodeships' : voivodeships,
                'communities' : communities,
                'votes' : votes,
                'no_of_voivodeships' : no_of_voivodeships,
                'no_of_communities' : no_of_communities,
                'citizens' : citizens,
                'allowed' : allowed,
                'voting_cards' : voting_cards,
                'votes' : votes,
                'valid_votes' : valid_votes,
                'votes_for_cand_1' : votes_for_cand_1,
                'votes_for_cand_2' : votes_for_cand_2,
                'cand_1_percentage' : cand_1_percentage,
                'cand_2_percentage' : cand_2_percentage,
                'candidate_1' : candidate_1,
                'candidate_2' : candidate_2,
                'distribution_by_type' : distribution_by_type,
                'distribution_by_amount' : distribution_by_amount,
    }



    return render(request, 'elections/index.html', context)

def get_last_modification(request):
    if request.method == 'POST':
        community_name = request.POST.get('community_name')

        vote = Vote.objects.select_for_update().get(community_ptr=community_name)
        response_data = {}
        response_data['last_modification'] = vote.last_modification
        return JsonResponse(response_data)

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/elections/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'elections/login.html', {})

# @login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/elections/')

def ajax_get(request):


    communities = [model_to_dict(community) for community in Community.objects.all()]
    # for community in communities:
        # community['last_modification'] = community['last_modification'].isoformat()
    votes = [model_to_dict(vote) for vote in Vote.objects.all()]


    list = json.dumps({'communities': communities, 'votes': votes})

    return HttpResponse(list)

def ajax_post(request):
    if request.method == 'POST' and request.is_ajax():
        name = request.POST['name']
        city = request.POST['city']
        message = name + ' lives in ' + city

        return HttpResponse(json.dumps({'message': message})) #tried without the json. Doesn't work either

    return render(request, 'books/ajaxTest.html')

