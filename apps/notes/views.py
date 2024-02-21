from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.notes.models import NoteChanges, NoteVersionHistory, NoteMetadata
from apps.notes.serializers import NoteChangesSerializer, NoteVersionHistorySerializer, NoteMetadataSerializer
from django.db.models import Max, F

# Create your views here.
@api_view(['GET'])
def getListofNotes(request):
    latest_versions_per_note = NoteMetadata.objects.filter(
    shared_users=request.user).annotate(latest_version=Max('noteversionhistory__id'))

    all_changes = NoteChanges.objects.filter(
    note_version_history__in=latest_versions_per_note.values('latest_version'))
    noteDetailsList = []
    for lvh in latest_versions_per_note:
        all_notes = all_changes.filter(note_version_history=lvh.latest_version)
        textExtract= all_notes.annotate(m=F('text')).values('m')
        entireNote = '\n'.join([x['m'] for x in textExtract])
        noteVersion = NoteVersionHistory.objects.filter(id=lvh.latest_version).last()

        noteDetail = {
            "content":entireNote,
            "modified-by":noteVersion.user.name,
            "modified-on":noteVersion.timestamp,
            "noteId":lvh.id,
            "owner":lvh.owner.name,
            "sharedWith":','.join([x.name for x in lvh.shared_users.all()]),
            "Version-History":lvh.latest_version,
        }
        noteDetailsList.append(noteDetail)

    return Response(noteDetailsList, status=200)

@api_view(['POST'])
def create(request):
    return HttpResponse("Hello, world. create View.")

@api_view(['GET'])
def getNotebyId(request, note_id):
    note_metadata = get_object_or_404(NoteMetadata, id=note_id, shared_users=request.user)
    latest_version_id = NoteMetadata.objects.filter(
        id=note_id, shared_users=request.user
    ).aggregate(latest_version=Max('noteversionhistory__id'))['latest_version']

    all_changes = NoteChanges.objects.filter(note_version_history=latest_version_id)
    entire_note = '\n'.join(all_changes.values_list('text', flat=True))

    note_version = NoteVersionHistory.objects.filter(id=latest_version_id).last()

    # Prepare the response data
    note_detail = {
        "content": entire_note,
        "modified-by": note_version.user.name,
        "modified-on": note_version.timestamp,
        "noteId": note_metadata.id,
        "owner": note_metadata.owner.name,
        "sharedWith": ','.join([user.name for user in note_metadata.shared_users.all()]),
        "Version-History": latest_version_id,
    }

    return Response(note_detail, status=200)

@api_view(['POST'])
def share(request):
    return HttpResponse("Hello, world. share View.")

@api_view(['PUT'])
def updateNote(request, id):
    return HttpResponse("Hello, world. updateNote View.")

@api_view(['GET'])
def getVersionHistory(request):
    return HttpResponse("Hello, world. version-history View.")
