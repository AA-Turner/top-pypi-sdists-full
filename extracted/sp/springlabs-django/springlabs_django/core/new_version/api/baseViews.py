# Django libraries
# 3rd party libraries
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
# Standard/core python libraries
# Our custom libraries (Managed by SPRINGLABS_DJANGO)
from core.utils import response_maker_1
from .serializers import *
from models_app.models import *
