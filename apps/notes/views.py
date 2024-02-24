from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.notes.models import NoteChanges, NoteVersionHistory, NoteMetadata
from django.db.models import Max

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
        noteVersion = NoteVersionHistory.objects.filter(id=lvh.latest_version).last()

        noteDetail = {
            "content":[{"line_no": change.line_no, "text": change.text} for change in all_notes],
            "modified-by":noteVersion.user.username,
            "modified-on":noteVersion.timestamp,
            "noteId":lvh.id,
            "owner":lvh.owner.username,
            "sharedWith":','.join([x.username for x in lvh.shared_users.all()]),
            "VersionHash":lvh.latest_version,
        }
        noteDetailsList.append(noteDetail)

    return Response(noteDetailsList, status=200)

@api_view(['POST'])
def create(request):
    content = request.data.get('noteContent', None) 

    if content is None:
        return Response({"error": "Note Content is required"}, status=status.HTTP_400_BAD_REQUEST)

    note_metadata = NoteMetadata.objects.create(owner=request.user)
    note_metadata.shared_users.add(request.user)

    initial_version = NoteVersionHistory.objects.create(
        user=request.user,
        note_metadata=note_metadata
    )
    listofLines = content.split('\n')
    for line_no, line_text in enumerate(listofLines, start=1):
        NoteChanges.objects.create(
            line_no=line_no,
            text=line_text,
            note_version_history=initial_version
        )

    return Response({"message": "Note created successfully"}, status=status.HTTP_201_CREATED)
@api_view(['GET', 'PUT'])
def get_or_update_note(request, note_id):

    note_metadata = get_object_or_404(NoteMetadata, id=note_id, shared_users=request.user)

    if request.method == 'GET':
        latest_version_id = NoteMetadata.objects.filter(
            id=note_id, shared_users=request.user
        ).aggregate(latest_version=Max('noteversionhistory__id'))['latest_version']

        all_changes = NoteChanges.objects.filter(note_version_history=latest_version_id)

        note_version = NoteVersionHistory.objects.filter(id=latest_version_id).last()

        note_detail = {
            "content": [{"line_no": change.line_no, "text": change.text} for change in all_changes],
            "modified-by": note_version.user.username,
            "modified-on": note_version.timestamp,
            "noteId": note_metadata.id,
            "owner": note_metadata.owner.username,
            "sharedWith": ','.join([user.username for user in note_metadata.shared_users.all()]),
            "VersionHash": latest_version_id,
        }

        return Response(note_detail, status=200)

    elif request.method == 'PUT':
        content = request.data.get('noteContent', None) 

        if content is None:
            return Response({"error": "Note Content is required"}, status=status.HTTP_400_BAD_REQUEST)

        new_version = NoteVersionHistory.objects.create(
            user=request.user,
            note_metadata=note_metadata
        )

        list_of_lines = content.split('\n')
        for line_no, line_text in enumerate(list_of_lines, start=1):
            NoteChanges.objects.create(
                line_no=line_no,
                text=line_text,
                note_version_history=new_version
            )

        return Response({"message": "Note updated successfully"}, status=status.HTTP_200_OK)

    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
@api_view(['POST'])
def share(request):
    note_id = request.data.get('noteId', None)
    shared_users_ids = request.data.get('sharedUsers', [])

    
    if note_id is None:
        return Response({"error": "Note Id is required"}, status=status.HTTP_400_BAD_REQUEST)
    print(request.data)
    if not shared_users_ids:
        return Response({"error": "List of shared_users is required"}, status=status.HTTP_400_BAD_REQUEST)

    note_metadata = get_object_or_404(NoteMetadata, id=note_id, owner=request.user)

    note_metadata.shared_users.add(*shared_users_ids)

    return Response({"message": "Note shared successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getVersionHistory(request, note_id):
    note_metadata = get_object_or_404(NoteMetadata, id=note_id, shared_users=request.user)

    version_history_list = NoteVersionHistory.objects.filter(note_metadata=note_metadata)

    commit_history = []
    for version_history in version_history_list:
        changes_list = NoteChanges.objects.filter(note_version_history=version_history)

        version_data = {
            "versionHash": version_history.id,
            "modified-on": version_history.timestamp,
            "modified-by": version_history.user.username,
            "changes": [{"line_no": change.line_no, "text": change.text} for change in changes_list]
        }

        commit_history.append(version_data)

    return Response(commit_history, status=status.HTTP_200_OK)
