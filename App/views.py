from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("This will become an AI to detect an image you upload, and correctly identify the animal. We may even suggest some fun names!")