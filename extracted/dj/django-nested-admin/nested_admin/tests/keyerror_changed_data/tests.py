from datetime import date
import time

from nested_admin.tests.base import BaseNestedAdminTestCase
from .models import Country, Person, Passport, TravelHistory


class TestKeyErrorChangedData(BaseNestedAdminTestCase):
    root_model = Person
    nested_models = (Passport, TravelHistory)

    def test_issue_245(self):
        countries = {}
        for code, name in (
            ("US", "United States"),
            ("DE", "Germany"),
            ("FR", "France"),
            ("BR", "Brazil"),
            ("PH", "Philippines"),
            ("ET", "Ethiopia"),
            ("CN", "China"),
        ):
            countries[code] = Country.objects.create(code=code, name=name)
        person = Person.objects.create(name="Jane Doe")
        passport = Passport.objects.create(
            passport_id="A1B2C3D4E", country=countries["US"], person=person
        )
        TravelHistory.objects.bulk_create(
            [
                TravelHistory(
                    passport=passport, country=countries["DE"], date=date(2010, 12, 16)
                ),
                TravelHistory(
                    passport=passport, country=countries["CN"], date=date(2013, 3, 22)
                ),
                TravelHistory(
                    passport=passport, country=countries["BR"], date=date(2016, 1, 25)
                ),
                TravelHistory(
                    passport=passport, country=countries["FR"], date=date(2010, 6, 19)
                ),
                TravelHistory(
                    passport=passport, country=countries["ET"], date=date(2018, 4, 10)
                ),
            ]
        )
        self.load_admin(person)
        time.sleep(1000)
        # Here, make a change to the parent, delete one or more inlines, and save
        print(person)
