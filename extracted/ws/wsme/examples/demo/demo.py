# coding=utf8
"""
A mini-demo of what wsme can do.

To run it::

    python setup.py develop

Then::

    python demo.py
"""

from wsme import WSRoot, expose, validate
from wsme.types import File

import bottle

import logging


class Person(object):
    id = int
    firstname = str
    lastname = str

    hobbies = [str]

    def __repr__(self):
        return "Person(%s, %s %s, %s)" % (
            self.id,
            self.firstname, self.lastname,
            self.hobbies
        )


class DemoRoot(WSRoot):
    @expose(int)
    @validate(int, int)
    def multiply(self, a, b):
        return a * b

    @expose(File)
    @validate(File)
    def echofile(self, afile):
        return afile

    @expose(str)
    def helloworld(self):
        return u"Здраво, свете (<- Hello World in Serbian !)"

    @expose(Person)
    def getperson(self):
        p = Person()
        p.id = 12
        p.firstname = 'Ross'
        p.lastname = 'Geler'
        p.hobbies = []
        print(p)
        return p

    @expose([Person])
    def listpersons(self):
        p = Person()
        p.id = 12
        p.firstname = 'Ross'
        p.lastname = 'Geler'
        r = [p]
        p = Person()
        p.id = 13
        p.firstname = 'Rachel'
        p.lastname = 'Green'
        r.append(p)
        print(r)
        return r

    @expose(Person)
    @validate(Person)
    def setperson(self, person):
        return person

    @expose([Person])
    @validate([Person])
    def setpersons(self, persons):
        print(persons)
        return persons


root = DemoRoot(webpath='/ws')

root.addprotocol('restjson')

bottle.mount('/ws/', root.wsgiapp())

logging.basicConfig(level=logging.DEBUG)
bottle.run()
