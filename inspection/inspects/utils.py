from .models import *
import requests

def search_managers(self, request, *args, **kwargs,):
    serch=Marked_Officers.objects.filter()
    for data in serch:
        