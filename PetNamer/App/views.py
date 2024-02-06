from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("This will become an AI used to upload your picture of a chosen animal, and accuractly identify it. We will also recommend some popular names based upon the species! ")
