from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['POST'])
def login(request):
    return HttpResponse("Hello, world. Login View.")


@api_view(['POST'])
def signup(request):
    return HttpResponse("Hello, world. SignUp View.")