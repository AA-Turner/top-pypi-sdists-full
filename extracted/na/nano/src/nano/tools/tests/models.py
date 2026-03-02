# coding: utf-8

from django.utils.timezone import now as tznow
from django.test import TestCase

from nano.tools.models import UnorderedTreeManager
from nano.tools.models import UnorderedTreeMixin


class TreeItem(UnorderedTreeMixin):

    tree = UnorderedTreeManager()
