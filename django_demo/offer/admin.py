from django.contrib import admin

from .models import Candidate


# Register your models here.


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'grade', 'location', 'create_date', 'offer_date', 'offer_generated')
    list_filter = ['location', 'grade', 'create_date', 'offer_date', 'offer_generated']
    search_fields = ['name', 'email', 'mobile']

    date_hierarchy = 'create_date'

admin.site.register(Candidate, CandidateAdmin)
