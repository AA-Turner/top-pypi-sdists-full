from django.db import models


class Item(models.Model):
    slug = models.SlugField(max_length=30)
