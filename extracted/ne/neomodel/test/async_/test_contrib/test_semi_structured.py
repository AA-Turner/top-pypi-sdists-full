from test._async_compat import mark_async_test

import pytest

from neomodel import (
    DeflateConflict,
    InflateConflict,
    IntegerProperty,
    StringProperty,
    adb,
)
from neomodel.contrib import AsyncSemiStructuredNode


class UserProf(AsyncSemiStructuredNode):
    email = StringProperty(unique_index=True, required=True)
    age = IntegerProperty(index=True)


class Dummy(AsyncSemiStructuredNode):
    pass


@mark_async_test
async def test_to_save_to_model_with_required_only():
    u = UserProf(email="dummy@test.com")
    assert await u.save()


@mark_async_test
async def test_save_to_model_with_extras():
    u = UserProf(email="jim@test.com", age=3, bar=99)
    u.foo = True
    assert await u.save()
    u = await UserProf.nodes.get(age=3)
    assert u.foo is True
    assert u.bar == 99


@mark_async_test
async def test_save_empty_model():
    dummy = Dummy()
    assert await dummy.save()


@mark_async_test
async def test_inflate_conflict():
    class PersonForInflateTest(AsyncSemiStructuredNode):
        name = StringProperty()
        age = IntegerProperty()

        def hello(self):
            print("Hi my names " + self.name)

    # An ok model
    props = {"name": "Jim", "age": 8, "weight": 11}
    await adb.cypher_query("CREATE (n:PersonForInflateTest $props)", {"props": props})
    jim = await PersonForInflateTest.nodes.get(name="Jim")
    assert jim.name == "Jim"
    assert jim.age == 8
    assert jim.weight == 11

    # A model that conflicts on `hello`
    props = {"name": "Tim", "age": 8, "hello": "goodbye"}
    await adb.cypher_query("CREATE (n:PersonForInflateTest $props)", {"props": props})
    with pytest.raises(InflateConflict):
        await PersonForInflateTest.nodes.get(name="Tim")


@mark_async_test
async def test_save_with_injection_in_property_key():
    # A SemiStructuredNode lets arbitrary property keys through deflate. A key
    # crafted to break out of the SET clause must not be able to inject Cypher.
    malicious_key = "x` = 1 DETACH DELETE n //"
    u = UserProf(email="injection@test.com", age=42)
    setattr(u, malicious_key, "value")
    await u.save()

    # The node must still exist (it was not DETACH DELETE-ed) and the malicious
    # key must have been stored verbatim as a property name.
    fetched = await UserProf.nodes.get(email="injection@test.com")
    assert fetched.age == 42
    assert getattr(fetched, malicious_key) == "value"


@mark_async_test
async def test_deflate_conflict():
    class PersonForDeflateTest(AsyncSemiStructuredNode):
        name = StringProperty()
        age = IntegerProperty()

        def hello(self):
            print("Hi my names " + self.name)

    tim = await PersonForDeflateTest(name="Tim", age=8, weight=11).save()
    tim.hello = "Hi"
    with pytest.raises(DeflateConflict):
        await tim.save()
