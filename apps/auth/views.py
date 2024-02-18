from django.http import HttpResponse


def login(request):
    return HttpResponse("Hello, world. Login View.")


def signup(request):
    return HttpResponse("Hello, world. SignUp View.")