from django.contrib import admin
import nested_admin
from .models import Person, Passport, TravelHistory


class TravelHistoryInline(nested_admin.NestedStackedInline):
    model = TravelHistory
    extra = 0


class PassportInline(nested_admin.NestedStackedInline):
    model = Passport
    inlines = [TravelHistoryInline]
    extra = 0


@admin.register(Person)
class PersonAdmin(nested_admin.NestedModelAdmin):
    model = Person
    inlines = [PassportInline]
