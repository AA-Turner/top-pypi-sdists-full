from importlib.util import find_spec
import typing as t
import pytest
from tests.utils import EnumTypeMixin, try_convert
from django.test import TestCase
from tests.djenum.models import EnumTester
from django.urls import reverse
from bs4 import BeautifulSoup as Soup
from django.test import Client
from django.http import QueryDict
from django.db import connection
from datetime import date, datetime, time, timedelta
from decimal import Decimal


class TestRequests(EnumTypeMixin, TestCase):
    MODEL_CLASS = EnumTester
    NAMESPACE = "tests_djenum"

    objects = []
    values = {}

    maxDiff = None

    fields = [
        "small_pos_int",
        "small_int",
        "pos_int",
        "int",
        "big_pos_int",
        "big_int",
        "constant",
        "text",
        "extern",
        "date_enum",
        "datetime_enum",
        "duration_enum",
        "time_enum",
        "decimal_enum",
        "dj_int_enum",
        "dj_text_enum",
        "non_strict_int",
        "non_strict_text",
        "no_coerce",
    ]

    def setUp(self):
        self.values = {val: {} for val in self.compared_attributes}
        self.objects = []
        self.MODEL_CLASS.objects.all().delete()
        self.objects.append(self.MODEL_CLASS.objects.create())
        self.objects[-1].refresh_from_db()

        self.objects.append(
            self.MODEL_CLASS.objects.create(
                small_pos_int=self.SmallPosIntEnum.VAL1,
                small_int=self.SmallIntEnum.VAL1,
                pos_int=self.PosIntEnum.VAL1,
                int=self.IntEnum.VAL1,
                big_pos_int=self.BigPosIntEnum.VAL1,
                big_int=self.BigIntEnum.VAL1,
                constant=self.Constants.PI,
                text=self.TextEnum.VALUE1,
                date_enum=self.DateEnum.BRIAN,
                datetime_enum=self.DateTimeEnum.PINATUBO,
                duration_enum=self.DurationEnum.WEEK,
                time_enum=self.TimeEnum.LUNCH,
                decimal_enum=self.DecimalEnum.TWO,
                extern=self.ExternEnum.ONE,
                non_strict_int=self.SmallPosIntEnum.VAL1,
                non_strict_text=self.TextEnum.VALUE1,
                no_coerce=self.SmallPosIntEnum.VAL1,
            )
        )
        self.objects[-1].refresh_from_db()

        for _ in range(0, 2):
            self.objects.append(
                self.MODEL_CLASS.objects.create(
                    small_pos_int=self.SmallPosIntEnum.VAL2,
                    small_int=self.SmallIntEnum.VAL2,
                    pos_int=self.PosIntEnum.VAL2,
                    int=self.IntEnum.VAL2,
                    big_pos_int=self.BigPosIntEnum.VAL2,
                    big_int=self.BigIntEnum.VAL2,
                    constant=self.Constants.e,
                    text=self.TextEnum.VALUE2,
                    extern=self.ExternEnum.TWO,
                    date_enum=self.DateEnum.EMMA,
                    datetime_enum=self.DateTimeEnum.ST_HELENS,
                    duration_enum=self.DurationEnum.DAY,
                    time_enum=self.TimeEnum.MORNING,
                    decimal_enum=self.DecimalEnum.ONE,
                    non_strict_int=self.SmallPosIntEnum.VAL2,
                    non_strict_text=self.TextEnum.VALUE2,
                    no_coerce=self.SmallPosIntEnum.VAL2,
                )
            )
            self.objects[-1].refresh_from_db()

        for _ in range(0, 3):
            self.objects.append(
                self.MODEL_CLASS.objects.create(
                    small_pos_int=self.SmallPosIntEnum.VAL3,
                    small_int=self.SmallIntEnum.VAL3,
                    pos_int=self.PosIntEnum.VAL3,
                    int=self.IntEnum.VAL3,
                    big_pos_int=self.BigPosIntEnum.VAL3,
                    big_int=self.BigIntEnum.VAL3,
                    constant=self.Constants.GOLDEN_RATIO,
                    text=self.TextEnum.VALUE3,
                    extern=self.ExternEnum.THREE,
                    date_enum=self.DateEnum.HUGO,
                    datetime_enum=self.DateTimeEnum.KATRINA,
                    duration_enum=self.DurationEnum.FORTNIGHT,
                    time_enum=self.TimeEnum.COB,
                    decimal_enum=self.DecimalEnum.FIVE,
                    non_strict_int=self.SmallPosIntEnum.VAL3,
                    non_strict_text=self.TextEnum.VALUE3,
                    no_coerce=self.SmallPosIntEnum.VAL3,
                )
            )
            self.objects[-1].refresh_from_db()

        self.objects.append(
            self.MODEL_CLASS.objects.create(
                non_strict_int=88, non_strict_text="arbitrary"
            )
        )

        for obj in self.objects:
            for attr in self.values.keys():
                self.values[attr].setdefault(getattr(obj, attr), [])
                self.values[attr][getattr(obj, attr)].append(obj.pk)

    def tearDown(self):
        self.MODEL_CLASS.objects.all().delete()

    @property
    def post_params(self):
        return {
            "small_pos_int": self.SmallPosIntEnum.VAL2,
            "small_int": self.SmallIntEnum.VAL0,
            "pos_int": self.PosIntEnum.VAL1,
            "int": self.IntEnum.VALn1,
            "big_pos_int": self.BigPosIntEnum.VAL2,
            "big_int": self.BigIntEnum.VAL2,
            "constant": self.Constants.GOLDEN_RATIO,
            "text": self.TextEnum.VALUE2,
            "extern": self.ExternEnum.TWO,
            "date_enum": self.DateEnum.EMMA.value,
            "datetime_enum": self.DateTimeEnum.ST_HELENS.value,
            "duration_enum": self.DurationEnum.DAY.value,
            "time_enum": self.TimeEnum.MORNING.value,
            "decimal_enum": self.DecimalEnum.ONE.value,
            "dj_int_enum": self.DJIntEnum.TWO,
            "dj_text_enum": self.DJTextEnum.C,
            "non_strict_int": self.SmallPosIntEnum.VAL1,
            "non_strict_text": self.TextEnum.VALUE3,
            "no_coerce": self.SmallPosIntEnum.VAL3,
        }

    @property
    def post_params_symmetric(self):
        return {
            **self.post_params,
        }

    if find_spec("rest_framework"):  # pragma: no cover

        def test_non_strict_drf_field(self):
            from rest_framework import fields

            from django_enum.drf import EnumField

            field = EnumField(self.SmallPosIntEnum, strict=False)
            self.assertEqual(field.to_internal_value("1"), 1)
            self.assertEqual(field.to_representation(1), 1)
            self.assertEqual(field.primitive_field.__class__, fields.IntegerField)

            field = EnumField(self.Constants, strict=False)
            self.assertEqual(field.to_internal_value("5.43"), 5.43)
            self.assertEqual(field.to_representation(5.43), 5.43)
            self.assertEqual(field.primitive_field.__class__, fields.FloatField)

            field = EnumField(self.TextEnum, strict=False)
            self.assertEqual(field.to_internal_value("random text"), "random text")
            self.assertEqual(field.to_representation("random text"), "random text")
            self.assertEqual(field.primitive_field.__class__, fields.CharField)

            field = EnumField(self.DateEnum, strict=False)
            self.assertEqual(
                field.to_internal_value("2017-12-05"), date(year=2017, day=5, month=12)
            )
            self.assertEqual(
                field.to_representation(date(year=2017, day=5, month=12)),
                date(year=2017, day=5, month=12),
            )
            self.assertEqual(field.primitive_field.__class__, fields.DateField)

            field = EnumField(self.DateTimeEnum, strict=False)
            self.assertEqual(
                field.to_internal_value("2017-12-05T01:02:30Z"),
                datetime(year=2017, day=5, month=12, hour=1, minute=2, second=30),
            )
            self.assertEqual(
                field.to_representation(
                    datetime(year=2017, day=5, month=12, hour=1, minute=2, second=30)
                ),
                datetime(year=2017, day=5, month=12, hour=1, minute=2, second=30),
            )
            self.assertEqual(field.primitive_field.__class__, fields.DateTimeField)

            field = EnumField(self.DurationEnum, strict=False)
            self.assertEqual(
                field.to_internal_value("P5DT01H00M01.312500S"),
                timedelta(days=5, hours=1, seconds=1.3125),
            )
            self.assertEqual(
                field.to_representation(timedelta(days=5, hours=1, seconds=1.3125)),
                timedelta(days=5, hours=1, seconds=1.3125),
            )
            self.assertEqual(field.primitive_field.__class__, fields.DurationField)

            field = EnumField(self.TimeEnum, strict=False)
            self.assertEqual(
                field.to_internal_value("01:02:30"), time(hour=1, minute=2, second=30)
            )
            self.assertEqual(
                field.to_representation(time(hour=1, minute=2, second=30)),
                time(hour=1, minute=2, second=30),
            )
            self.assertEqual(field.primitive_field.__class__, fields.TimeField)

            field = EnumField(self.DecimalEnum, strict=False)
            self.assertEqual(field.to_internal_value("1.67"), Decimal("1.67"))
            self.assertEqual(field.to_representation(Decimal("1.67")), Decimal("1.67"))
            self.assertEqual(field.primitive_field.__class__, fields.DecimalField)

            from enum import Enum

            class UnsupportedPrimitiveEnum(Enum):
                VAL1 = (1,)
                VAL2 = (1, 2)
                VAL3 = (1, 2, 3)

            field = EnumField(
                UnsupportedPrimitiveEnum,
                strict=False,
                choices=[
                    (UnsupportedPrimitiveEnum.VAL1, "VAL1"),
                    (UnsupportedPrimitiveEnum.VAL2, "VAL2"),
                    (UnsupportedPrimitiveEnum.VAL3, "VAL3"),
                ],
            )
            self.assertEqual(field.to_internal_value((1, 2, 4)), (1, 2, 4))
            self.assertEqual(field.to_representation((1, 2, 4)), (1, 2, 4))
            self.assertIsNone(field.primitive_field)

        def test_drf_serializer(self):
            from rest_framework import serializers

            from django_enum.drf import EnumField

            class TestSerializer(serializers.ModelSerializer):
                small_pos_int = EnumField(self.SmallPosIntEnum)
                small_int = EnumField(self.SmallIntEnum)
                pos_int = EnumField(self.PosIntEnum)
                int = EnumField(self.IntEnum)
                big_pos_int = EnumField(self.BigPosIntEnum)
                big_int = EnumField(self.BigIntEnum)
                constant = EnumField(self.Constants)
                date_enum = EnumField(self.DateEnum)
                datetime_enum = EnumField(self.DateTimeEnum, strict=False)
                duration_enum = EnumField(self.DurationEnum)
                time_enum = EnumField(self.TimeEnum)
                decimal_enum = EnumField(self.DecimalEnum)
                text = EnumField(self.TextEnum)
                extern = EnumField(self.ExternEnum)
                dj_int_enum = EnumField(self.DJIntEnum)
                dj_text_enum = EnumField(self.DJTextEnum)
                non_strict_int = EnumField(self.SmallPosIntEnum, strict=False)
                non_strict_text = EnumField(
                    self.TextEnum, strict=False, allow_blank=True
                )
                no_coerce = EnumField(self.SmallPosIntEnum)

                class Meta:
                    model = self.MODEL_CLASS
                    fields = "__all__"

            ser = TestSerializer(data=self.post_params)
            self.assertTrue(ser.is_valid())
            inst = ser.save()
            for param, value in self.post_params.items():
                self.assertEqual(value, getattr(inst, param))

            ser_bad = TestSerializer(
                data={
                    **self.post_params,
                    "small_pos_int": -1,
                    "constant": 3.14,
                    "text": "wrong",
                    "extern": 0,
                    "pos_int": -50,
                    "date_enum": date(year=2017, day=5, month=12),
                    "decimal_enum": Decimal("1.89"),
                }
            )

            self.assertFalse(ser_bad.is_valid())
            self.assertTrue("small_pos_int" in ser_bad.errors)
            self.assertTrue("constant" in ser_bad.errors)
            self.assertTrue("text" in ser_bad.errors)
            self.assertTrue("extern" in ser_bad.errors)
            self.assertTrue("pos_int" in ser_bad.errors)
            self.assertTrue("date_enum" in ser_bad.errors)
            self.assertTrue("decimal_enum" in ser_bad.errors)

        def test_drf_read(self):
            c = Client()
            response = c.get(reverse(f"{self.NAMESPACE}:enumtester-list"))
            read_objects = response.json()
            self.assertEqual(len(read_objects), len(self.objects))

            for idx, obj in enumerate(response.json()):
                # should be same order
                self.assertEqual(obj["id"], self.objects[idx].id)
                for field in self.fields:
                    self.assertEqual(obj[field], getattr(self.objects[idx], field))
                    if obj[field] is not None:
                        self.assertIsInstance(
                            try_convert(
                                self.enum_primitive(field),
                                obj[field],
                                raise_on_error=False,
                            ),
                            self.enum_primitive(field),
                        )

        def test_drf_update(self):
            c = Client()
            params = self.post_params_symmetric
            response = c.put(
                reverse(
                    f"{self.NAMESPACE}:enumtester-detail",
                    kwargs={"pk": self.objects[0].id},
                ),
                params,
                follow=True,
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            fetched = c.get(
                reverse(
                    f"{self.NAMESPACE}:enumtester-detail",
                    kwargs={"pk": self.objects[0].id},
                ),
                follow=True,
            ).json()

            obj = self.MODEL_CLASS.objects.get(pk=self.objects[0].id)

            self.assertEqual(fetched["id"], obj.id)
            for field in self.fields:
                self.assertEqual(
                    try_convert(
                        self.enum_primitive(field), fetched[field], raise_on_error=False
                    ),
                    getattr(obj, field),
                )
                if self.MODEL_CLASS._meta.get_field(field).coerce:
                    self.assertEqual(params[field], getattr(obj, field))

        def test_drf_post(self):
            c = Client()
            params = {**self.post_params_symmetric, "non_strict_text": "", "text": None}
            response = c.post(
                reverse(f"{self.NAMESPACE}:enumtester-list"),
                params,
                follow=True,
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 201)
            created = response.json()

            obj = self.MODEL_CLASS.objects.last()

            self.assertEqual(created["id"], obj.id)
            for field in self.fields:
                self.assertEqual(
                    getattr(obj, field),
                    try_convert(
                        self.enum_primitive(field), created[field], raise_on_error=False
                    ),
                )
                if self.MODEL_CLASS._meta.get_field(field).coerce:
                    self.assertEqual(getattr(obj, field), params[field])

    else:
        pass  # pragma: no cover

    def test_add(self):
        """
        Test that add forms work and that EnumField type allows creations
        from symmetric values
        """
        c = Client()

        # test normal choice field and our EnumChoiceField
        form_url = "enum-add"
        params = self.post_params_symmetric
        response = c.post(reverse(f"{self.NAMESPACE}:{form_url}"), params, follow=True)
        soup = Soup(response.content, features="html.parser")
        added_resp = soup.find_all("div", class_="enum")[-1]
        added = self.MODEL_CLASS.objects.last()

        for param, value in params.items():
            form_val = added_resp.find(class_=param).find("span", class_="value").text
            try:
                form_val = self.enum_primitive(param)(form_val)
            except (TypeError, ValueError):
                if form_val:
                    form_val = try_convert(
                        self.enum_primitive(param), form_val, raise_on_error=True
                    )
                else:  # pragma: no cover
                    pass
            if self.MODEL_CLASS._meta.get_field(param).strict:
                self.assertEqual(
                    self.enum_type(param)(form_val), self.enum_type(param)(value)
                )
            else:
                self.assertEqual(form_val, value)
            self.assertEqual(getattr(added, param), form_val)
        added.delete()

    def test_update(self):
        """
        Test that update forms work and that EnumField type allows updates
        from symmetric values
        """
        c = Client()

        # test normal choice field and our EnumChoiceField
        form_url = "enum-update"
        params = self.post_params_symmetric
        updated = self.MODEL_CLASS.objects.create()
        response = c.post(
            reverse(f"{self.NAMESPACE}:{form_url}", kwargs={"pk": updated.pk}),
            data=params,
            follow=True,
        )
        updated.refresh_from_db()
        soup = Soup(response.content, features="html.parser")
        self.verify_form(updated, soup)

        for param, value in params.items():
            if (
                not self.MODEL_CLASS._meta.get_field(param).coerce
                and self.MODEL_CLASS._meta.get_field(param).strict
            ):
                value = self.enum_type(param)(value)
            self.assertEqual(getattr(updated, param), value)
        updated.delete()

    def test_delete(self):
        c = Client()
        form_url = "enum-delete"
        deleted = self.MODEL_CLASS.objects.create()
        c.delete(reverse(f"{self.NAMESPACE}:{form_url}", kwargs={"pk": deleted.pk}))
        self.assertRaises(
            self.MODEL_CLASS.DoesNotExist, self.MODEL_CLASS.objects.get, pk=deleted.pk
        )

    def get_enum_val(self, enum, value, primitive, null=True, coerce=True, strict=True):
        try:
            if coerce:
                if value is None or value == "":
                    return None if null else ""
                if int in enum.__mro__:
                    return enum(int(value))
                if float in enum.__mro__:
                    return enum(float(value))
                return enum(value)
        except ValueError as err:
            if strict:  # pragma: no cover
                raise err

        if value not in {None, ""}:
            try:
                return try_convert(primitive, value, raise_on_error=True)
            except ValueError as err:
                return primitive(value)
        return None if null else ""

    def test_add_form(self):
        c = Client()
        # test normal choice field and our EnumChoiceField
        form_url = "enum-add"
        response = c.get(reverse(f"{self.NAMESPACE}:{form_url}"))
        soup = Soup(response.content, features="html.parser")
        self.verify_form(self.MODEL_CLASS(), soup)

    def verify_form(self, obj, soup):
        """
        Verify form structure, options and selected values reflect object.

        :param obj: The model object if this is an update form, None if it's a
            create form
        :param soup: The html form for the object
        :return:
        """
        for field in self.fields:
            field = self.MODEL_CLASS._meta.get_field(field)

            expected = {}
            for en in field.enum:
                for val, label in field.choices:
                    if en == val:
                        expected[en if field.coerce else val] = label

            if not any(
                [getattr(obj, field.name) == exp for exp in expected]
            ) and getattr(obj, field.name) not in {None, ""}:
                # add any non-strict values
                expected[getattr(obj, field.name)] = str(getattr(obj, field.name))
                self.assertFalse(field.strict)

            null_opt = False
            for option in soup.find("select", id=f"id_{field.name}").find_all("option"):
                if (
                    option["value"] is None or option["value"] == ""
                ) and option.text.count("-") >= 2:
                    self.assertTrue(field.blank or field.null)
                    null_opt = True
                    if option.has_attr("selected"):
                        self.assertTrue(getattr(obj, field.name) in {None, ""})
                    if getattr(obj, field.name) == option["value"]:
                        self.assertTrue(option.has_attr("selected"))
                    # (coverage error?? the line below gets hit)
                    continue  # pragma: no cover

                try:
                    try:
                        value = self.get_enum_val(
                            field.enum,
                            option["value"],
                            primitive=self.enum_primitive(field.name),
                            null=field.null,
                            coerce=field.coerce,
                            strict=field.strict,
                        )
                    except ValueError:  # pragma: no cover
                        self.assertFalse(field.strict)
                        value = self.enum_primitive(field.name)(option["value"])
                    self.assertEqual(str(expected[value]), option.text)
                    if option.has_attr("selected"):
                        self.assertEqual(getattr(obj, field.name), value)
                    if getattr(obj, field.name) == value and not (
                        # problem if our enum compares equal to null
                        getattr(obj, field.name) is None and field.null
                    ):
                        self.assertTrue(option.has_attr("selected"))
                    del expected[value]
                except KeyError:  # pragma: no cover
                    import ipdb

                    ipdb.set_trace()
                    self.fail(
                        f"{field.name} did not expect option "
                        f"{option['value']}: {option.text}."
                    )

            self.assertEqual(len(expected), 0)

            if not field.blank:
                self.assertFalse(
                    null_opt, f"An unexpected null option is present on {field.name}"
                )
            elif field.blank:  # pragma: no cover
                self.assertTrue(
                    null_opt,
                    f"Expected a null option on field {field.name}, but none was present.",
                )

    def test_update_form(self):
        client = Client()
        # test normal choice field and our EnumChoiceField
        form_url = "enum-update"
        for obj in self.objects:
            response = client.get(
                reverse(f"{self.NAMESPACE}:{form_url}", kwargs={"pk": obj.pk})
            )
            soup = Soup(response.content, features="html.parser")
            self.verify_form(obj, soup)

    def test_non_strict_select(self):
        client = Client()
        obj = self.MODEL_CLASS.objects.create(non_strict_int=233)
        form_url = "enum-update"
        response = client.get(
            reverse(f"{self.NAMESPACE}:{form_url}", kwargs={"pk": obj.pk})
        )
        soup = Soup(response.content, features="html.parser")
        self.verify_form(obj, soup)
        for option in soup.find("select", id=f"id_non_strict_int").find_all("option"):
            if option.has_attr("selected"):
                self.assertEqual(option["value"], "233")

    @property
    def field_filter_properties(self):
        return {
            "small_pos_int": ["value"],
            "small_int": ["value"],
            "pos_int": ["value"],
            "int": ["value"],
            "big_pos_int": ["value"],
            "big_int": ["value"],
            "constant": ["value"],
            "text": ["value"],
            "date_enum": ["value"],
            "datetime_enum": ["value"],
            "time_enum": ["value"],
            "duration_enum": ["value"],
            "decimal_enum": ["value"],
            "extern": ["value"],
            "dj_int_enum": ["value"],
            "dj_text_enum": ["value"],
            "non_strict_int": ["value"],
            "non_strict_text": ["value"],
            "no_coerce": ["value"],
        }

    @property
    def compared_attributes(self):
        return [
            "small_pos_int",
            "small_int",
            "pos_int",
            "int",
            "big_pos_int",
            "big_int",
            "constant",
            "text",
            "date_enum",
            "datetime_enum",
            "time_enum",
            "duration_enum",
            "decimal_enum",
            "extern",
            "dj_int_enum",
            "dj_text_enum",
            "non_strict_int",
            "non_strict_text",
            "no_coerce",
        ]

    def list_to_objects(self, resp_content):
        objects = {}
        for obj_div in resp_content.find("body").find_all(f"div", class_="enum"):
            objects[int(obj_div["data-obj-id"])] = {
                attr: self.get_enum_val(
                    self.MODEL_CLASS._meta.get_field(attr).enum,
                    obj_div.find(f"p", {"class": attr})
                    .find("span", class_="value")
                    .text,
                    primitive=self.enum_primitive(attr),
                    null=self.MODEL_CLASS._meta.get_field(attr).null,
                    coerce=self.MODEL_CLASS._meta.get_field(attr).coerce,
                    strict=self.MODEL_CLASS._meta.get_field(attr).strict,
                )
                for attr in self.compared_attributes
            }
        return objects

    if find_spec("django_filters"):  # pragma: no cover

        def test_django_filter(self):
            self.do_test_django_filter(reverse(f"{self.NAMESPACE}:enum-filter"))
            self.do_test_django_filter(reverse(f"{self.NAMESPACE}:enum-filter-viewset"))

        @pytest.mark.skipif(
            connection.vendor == "oracle",
            reason="strict NULL behavior on Oracle >21c breaks exclude filter tests",
        )
        def test_django_filter_exclude(self):
            self.do_test_django_filter(
                reverse(f"{self.NAMESPACE}:enum-filter-viewset-exclude"), exclude=True
            )

        def test_django_filter_multiple(self):
            self.do_test_django_filter(
                reverse(f"{self.NAMESPACE}:enum-filter-multiple"), multi=True
            )

        @pytest.mark.skipif(
            connection.vendor == "oracle",
            reason="strict NULL behavior on Oracle >21c breaks exclude filter tests",
        )
        def test_django_filter_multiple_exclude(self):
            self.do_test_django_filter(
                reverse(f"{self.NAMESPACE}:enum-filter-multiple-exclude"),
                multi=True,
                exclude=True,
            )

        def do_test_django_filter(
            self, url, skip_non_strict=True, multi=False, exclude=False
        ):
            """
            Exhaustively test query parameter permutations based on data
            created in setUp
            """
            filter = (
                self.MODEL_CLASS.objects.exclude
                if exclude
                else self.MODEL_CLASS.objects.filter
            )
            client = Client()
            for attr, val_map in self.values.items():
                tests: t.List[t.Tuple[t.Any, t.List[int]]] = []
                for val, objs in val_map.items():
                    if (
                        skip_non_strict
                        and not self.MODEL_CLASS._meta.get_field(attr).strict
                        and not any(
                            [
                                val == en
                                for en in self.MODEL_CLASS._meta.get_field(attr).enum
                            ]
                        )
                    ):
                        continue
                    if val in {None, ""}:
                        # todo how to query None or empty?
                        continue
                    if multi:
                        # split up into several multi searches
                        if not tests or len(tests[-1][0]) > 1:
                            tests.append(([val], objs))
                        else:
                            tests[-1][0].append(val)
                            tests[-1][1].extend(objs)
                    else:
                        tests.append((val, objs))

                for val, objs in tests:
                    for prop in self.field_filter_properties[attr]:
                        qry = QueryDict(mutable=True)
                        if not isinstance(val, list):
                            val = [val]

                        prop_vals = []
                        for v in val:
                            try:
                                resolved = getattr(v, prop)
                                if isinstance(resolved, (list, tuple, set)):
                                    prop_vals.extend(resolved)
                                else:
                                    prop_vals.append(resolved)
                            except AttributeError:
                                prop_vals.append(v)
                        if multi:
                            prop_vals = [prop_vals]
                        for prop_val in prop_vals:
                            if isinstance(prop_val, list):
                                qry.setlist(attr, prop_val)
                            else:
                                qry[attr] = prop_val
                            objects = {
                                obj.pk: {
                                    attr: getattr(obj, attr)
                                    for attr in self.compared_attributes
                                }
                                for obj in filter(id__in=objs)
                            }
                            if exclude:
                                self.assertEqual(
                                    len(set(objects)),
                                    self.MODEL_CLASS.objects.count() - len(set(objs)),
                                )
                            else:
                                self.assertEqual(len(objects), len(objs))
                            response = client.get(f"{url}?{qry.urlencode()}")
                            resp_objects = self.list_to_objects(
                                Soup(response.content, features="html.parser")
                            )
                            self.assertEqual(objects, resp_objects)
