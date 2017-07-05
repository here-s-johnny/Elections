from django.contrib import admin

from .models import Voivodeship, Candidate, Community, Vote

# Register your models here.

admin.site.register(Voivodeship)
admin.site.register(Candidate)
admin.site.register(Community)
admin.site.register(Vote)