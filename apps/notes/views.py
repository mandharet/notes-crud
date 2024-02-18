from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def create(request):
    return HttpResponse("Hello, world. create View.")

def getNotebyId(request):
    return HttpResponse("Hello, world. getNotebyId View.")

def share(request):
    return HttpResponse("Hello, world. share View.")

def updateNote(request):
    return HttpResponse("Hello, world. updateNote View.")

def getVersionHistory(request):
    return HttpResponse("Hello, world. version-history View.")
