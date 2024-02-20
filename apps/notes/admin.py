from django.contrib import admin
from .models import NoteChanges, NoteVersionHistory, NoteMetadata

admin.site.register([NoteChanges, NoteVersionHistory, NoteMetadata])
# Register your models here.
