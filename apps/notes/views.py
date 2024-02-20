from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.notes.models import NoteChanges, NoteVersionHistory, NoteMetadata
from apps.notes.serializers import NoteChangesSerializer, NoteVersionHistorySerializer, NoteMetadataSerializer
from django.db.models import Subquery, OuterRef, Max, F, CharField, Value, TextField
from django.db.models.functions import Concat, ConcatPair

# Create your views here.
@api_view(['GET'])
def getListofNotes(request):
    noteVersionHistoryList = NoteVersionHistory.objects.filter(note_metadata__shared_users=request.user)
    notesList = NoteChanges.objects.filter(note_version_history__note_metadata__shared_users = request.user)
    notesList = notesList.order_by('-note_version_history__note_metadata','-note_version_history')
    # latest_versions = NoteVersionHistory.objects.filter(
    #     note_metadata__shared_users=request.user
    # ).values('note_metadata').annotate(latest_timestamp=Max('timestamp'))
    # latest_note_versions = NoteVersionHistory.objects.filter(note_metadata__shared_users=request.user,timestamp__in=latest_versions.values('latest_timestamp')
    # )
    
    latest_versions_per_note = NoteMetadata.objects.filter(
    shared_users=request.user).annotate(latest_version=Max('noteversionhistory__id'))

    # Retrieve all NoteChanges for each latest NoteVersionHistory
    all_changes = NoteChanges.objects.filter(
    note_version_history__in=latest_versions_per_note.values('latest_version'))

    grouped_changes = all_changes.values(
    notemetadata_id=F('note_version_history__note_metadata__id'),
    notemetadata_text=Concat(
        'note_version_history__note_metadata__id', Value(': '), 'text',
        output_field=TextField()
    )).annotate(
    all_text=ConcatPair('text', Value('\n'), output_field=TextField())).distinct()

    # Now 'grouped_changes' contains the concatenated text for each NoteMetadata
    for entry in grouped_changes:
        print(f"NoteMetadata ID: {entry['notemetadata_id']}\nText: {entry['all_text']}\n")

    for i in all_changes:
        print(i)
    # print(noteVersionHistoryList)
    # for i in noteVersionHistoryList:
    #     print(i)
    return HttpResponse("Hello, world. getListofNotes View.")

@api_view(['POST'])
def create(request):
    return HttpResponse("Hello, world. create View.")

@api_view(['GET'])
def getNotebyId(request, id):
    return HttpResponse("Hello, world. getNotebyId View. "+ id)

@api_view(['POST'])
def share(request):
    return HttpResponse("Hello, world. share View.")

@api_view(['PUT'])
def updateNote(request, id):
    return HttpResponse("Hello, world. updateNote View.")

@api_view(['GET'])
def getVersionHistory(request):
    return HttpResponse("Hello, world. version-history View.")
