from django.urls import path

from . import views

urlpatterns = [
    path("create", views.create, name="create"),
    path("{id}", views.getNotebyId, name="getNote"),
    path("share", views.share, name="share"),
    path("{id}", views.updateNote, name="getNotes"),
    path("version-history/{id}", views.getVersionHistory, name="getVersions"),
]



# POST /notes/create: Create a new note.
# GET /notes/{id}: Retrieve a specific note by its ID.
# POST /notes/share: Share the note with other users. 
# PUT /notes/{id}: Update an existing note.
# GET /notes/version-history/{id}: GET all the changes associated 