from django.db import models

from nano.mark.models import MarkedMixin


class Item(MarkedMixin):
    slug = models.SlugField(max_length=30)
