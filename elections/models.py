 # This Python file uses the following encoding: utf-8

from __future__ import unicode_literals, division

from django.db import models

from datetime import datetime
from django.utils import timezone

from django.core.exceptions import ValidationError

# Create your models here.

class Candidate(models.Model):
    first_name = models.CharField(max_length = 20)
    middle_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)

    def __str__(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name

    def __unicode__(self):
        return u"%s %s %s" % (self.first_name, self.middle_name, self.last_name)

    def clean(self):
        if Candidate.objects.count() > 2:
            raise ValidationError('There can be no more than 2 candidates')    


class Voivodeship(models.Model):

    name = models.CharField(max_length = 20)
    citizens = models.IntegerField()
    allowed = models.IntegerField()
    voting_cards = models.IntegerField()
    votes = models.IntegerField()
    valid_votes = models.IntegerField()

    votes_for_cand_1 = models.IntegerField(default=0)
    votes_for_cand_2 = models.IntegerField(default=0)

    def percent_1(self):
        return round(
            (100 * self.votes_for_cand_1 / (self.votes_for_cand_1 + self.votes_for_cand_2)), 2)

    def percent_2(self):
        return round(
            (100 * self.votes_for_cand_2 / (self.votes_for_cand_1 + self.votes_for_cand_2)), 2)

    voi_choices = (
        ('PL-DS', 'dolnośląskie'),
        ('PL-KP', 'kujawsko-pomorskie'),
        ('PL-LU', 'lubelskie'),
        ('PL-LB', 'lubuskie'),
        ('PL-LD', 'łódzkie'),
        ('PL-MA', 'małopolskie'),
        ('PL-MZ', 'mazowieckie'),
        ('PL-OP', 'opolskie'),
        ('PL-PK', 'podkarpackie'),
        ('PL-PD', 'podlaskie'),
        ('PL-PM', 'pomorskie'),
        ('PL-SL', 'śląskie'),
        ('PL-SK', 'świętokrzystkie'),
        ('PL-WN', 'warmińsko-mazurskie'),
        ('PL-WP', 'wielkopolskie'),
        ('PL-ZP', 'zachodniopomorskie'),
    )

    voi_choice = models.CharField(max_length=5, choices=voi_choices, default='PL-MZ')
    
    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):

        # data = self.cleaned_data
        if self.citizens < self.allowed:
            raise ValidationError('Citizens number cannot be smaller than allowed number')

        if self.allowed < self.voting_cards:
            raise ValidationError('Allowed number cannot be smaller than voting cards number')

        if self.voting_cards < self.votes:
            raise ValidationError('Voting cards number cannot be smaller than votes number')

        if self.votes < self.valid_votes:
            raise ValidationError('Votes number cannot be smaller than valid votes number')

        # return data

    

class Community(models.Model):
    # community is an entity smaller than voivodeship, 
    # in a sense that a voivodeship consists of multiple communities

    kinds = (
        ('1', "miasto"),
        ('2', "wieś"),
        ('3', "statki"),
        ('4', "zagranica"),
    )

    name = models.CharField(primary_key = True, max_length = 20)
    voivodeship_ptr = models.ForeignKey(Voivodeship)

    # last_modification = models.DateTimeField(default=datetime.now)

    kind = models.CharField(max_length = 10, choices = kinds, default = "1")
    citizens = models.IntegerField(default = 0)
    allowed = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.name

    def get_votes(self):
        return Vote.objects.get(community_ptr = self.name)

    def clean(self):
    # moze dodac zeby sie citizensi w community sumowali do voivodeshipu?
    # https://docs.djangoproject.com/en/1.9/ref/models/conditional-expressions/

        # data = self.cleaned_data
        if self.citizens < self.allowed:
            raise ValidationError('Citizens number cannot be smaller than allowed number')


        tmp = Voivodeship.objects.get(name=self.voivodeship_ptr)    

        if self.citizens > tmp.citizens:
            raise ValidationError('A community cannot have more citizens than the voivodeship it belongs to')


class Vote(models.Model):

    community_ptr = models.ForeignKey(Community)

    voting_cards = models.IntegerField(default = 0)
    votes = models.IntegerField(default = 0)
    valid_votes = models.IntegerField(default = 0)

    last_modification = models.DateTimeField(auto_now=True)

    votes_for_cand_1 = models.IntegerField(default = 0)
    votes_for_cand_2 = models.IntegerField(default = 0)

    # last_modification = models.DateTimeField(default=datetime.now)
    def percent_1(self):
        return round(
            (100 * self.votes_for_cand_1 / (self.votes_for_cand_1 + self.votes_for_cand_2)), 2)

    def percent_2(self):
        return round(
            (100 * self.votes_for_cand_2 / (self.votes_for_cand_1 + self.votes_for_cand_2)), 2)

    def __str__(self):
        return self.community_ptr.name + " votes"

    def __unicode__(self):
        return u"%s" % self.community_ptr.name + " votes"

    def clean(self):

        tmp = Community.objects.get(name=self.community_ptr)  

        if tmp.allowed < self.voting_cards:
            raise ValidationError('Allowed number (%d) cannot be smaller than voting cards number' % tmp.allowed)

        if self.voting_cards < self.votes:
            raise ValidationError('Voting cards number cannot be smaller than votes number')

        if self.votes < self.valid_votes:
            raise ValidationError('Votes number cannot be smaller than valid votes number')

