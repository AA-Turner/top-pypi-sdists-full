""" """

from django.db import models


class BaseModel(models.Model):
    """
    Allows adding common behaviour to the classes across the app.
    A common usage would be to define a custom id field like this:
        id = models.UUIDField(
            primary_key=True,
            editable=False,
        )


    """

    class Meta:
        abstract = True
