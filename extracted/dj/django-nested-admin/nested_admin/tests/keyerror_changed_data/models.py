from django.db import models
from django.db.models import ForeignKey, CASCADE, OneToOneField


class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Passport(models.Model):
    passport_id = models.CharField(max_length=9)
    country = models.ForeignKey(Country, on_delete=CASCADE)
    person = OneToOneField(Person, on_delete=CASCADE)

    def __str__(self):
        return f"Passport {self.passport_id} [{self.person}]"


class TravelHistory(models.Model):
    country = models.ForeignKey(Country, on_delete=CASCADE)
    date = models.DateField()
    passport = ForeignKey(Passport, on_delete=CASCADE)

    class Meta:
        ordering = ("-date", "country")

    def __str__(self):
        return f"{self.passport}: {self.country} ({self.date.isoformat()})"
