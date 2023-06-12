from celery import shared_task
from rest_framework.response import Response
from .models import *
from rest_framework import status
import requests
from datetime import datetime, timedelta
import requests
import json


@shared_task(serializer='json', name='Create and Update of User')
def savingUser(data):
    saving = User(**data)
    saving.save()


