from django.urls import path

from . import views

urlpatterns = [
    path("", views.getListofNotes, name="getListofNotes"),
    path("create", views.create, name="create"),
    path("<int:note_id>", views.get_or_update_note, name="get_or_update_note"),
    path("share", views.share, name="share"),
    path("version-history/<int:note_id>", views.getVersionHistory, name="getVersions"),
]



# POST /notes/create: Create a new note.
# GET /notes/{id}: Retrieve a specific note by its ID.
# PUT /notes/{id}: Update an existing note.
# POST /notes/share: Share the note with other users. 
# GET /notes/version-history/{id}: GET all the changes associated 