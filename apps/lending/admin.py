from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.lending.models import Borrower, Program, Application


@admin.register(Borrower)
class BorrowerAdmin(ModelAdmin):
    list_display = ['iin', 'created', 'birthday']
    search_fields = ['iin']
    fields = ['iin', 'birthday']
    readonly_fields = ['birthday']


@admin.register(Program)
class ProgramAdmin(ModelAdmin):
    list_display = ['name', 'created', 'min_amount', 'max_amount', 'min_age', 'max_age']
    search_fields = ['name']
    fields = ['name', ('min_age', 'max_age'), ('min_amount', 'max_amount')]


@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    list_display = ['__str__', 'created', 'borrower', 'program', 'amount', 'status', 'reason']
    list_filter = ['status', 'reason', 'program']
    search_fields = ['borrower__iin']

    def has_add_permission(self, request):
        return False
