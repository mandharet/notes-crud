from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.notes.models import NoteChanges, NoteVersionHistory, NoteMetadata
from django.db.models import Max

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getListofNotes(request):
    """
    Retrieve a list of notes for the authenticated user.

    Request:
    - Method: GET

    Response:
    - Returns a list of note details including content, modification details, and metadata.
    - If no notes are found, returns a 404 status with an error message.
    """
    latest_versions_per_note = NoteMetadata.objects.filter(
    shared_users=request.user).annotate(latest_version=Max('noteversionhistory__id'))

    if not latest_versions_per_note.exists():
        return Response({"error": "No notes found for the user"}, status=status.HTTP_404_NOT_FOUND)

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

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create(request):
    """
    Create a new note for the authenticated user.

    Request:
    - Method: POST
    - Requires 'noteContent' field in the request data.

    Response:
    - Returns a success message if the note is created successfully.
    - If 'noteContent' is not provided, returns a 400 status with an error message.
    """
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

@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT'])
def get_or_update_note(request, note_id):
    """
    Retrieve or update a note for the authenticated user.

    Request:
    - Method: GET or PUT
    - Requires 'note_id' in the URL path for both methods.
    - For PUT method, requires 'noteContent' field in the request data.

    Response:
    - For GET, returns details of the latest version of the note.
    - For PUT, returns a success message if the note is updated successfully.
    - If 'note_id' is not found, returns a 404 status with an error message.
    - If 'noteContent' is not provided for PUT, returns a 400 status with an error message.
    - If method is other than GET or PUT, returns a 405 status with an error message.
    """
    note_metadata = get_object_or_404(NoteMetadata, id=note_id, shared_users=request.user)

    if request.method == 'GET':
        latest_version_id = NoteMetadata.objects.filter(
            id=note_id, shared_users=request.user
        ).aggregate(latest_version=Max('noteversionhistory__id'))['latest_version']

        if not latest_version_id :
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)


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
    
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def share(request):
    """
    Share a note with other users for the authenticated user.

    Request:
    - Method: POST
    - Requires 'noteId' and 'sharedUsers' fields in the request data.

    Response:
    - Returns a success message if the note is shared successfully.
    - If 'noteId' is not provided, returns a 400 status with an error message.
    - If 'sharedUsers' list is not provided, returns a 400 status with an error message.
    """
    note_id = request.data.get('noteId', None)
    shared_users_ids = request.data.get('sharedUsers', [])

    
    if note_id is None:
        return Response({"error": "Note Id is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not shared_users_ids:
        return Response({"error": "List of shared_users is required"}, status=status.HTTP_400_BAD_REQUEST)

    note_metadata = get_object_or_404(NoteMetadata, id=note_id, owner=request.user)

    note_metadata.shared_users.add(*shared_users_ids)

    return Response({"message": "Note shared successfully"}, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getVersionHistory(request, note_id):
    """
    Retrieve the version history of a note for the authenticated user.
    Request:
    - Method: GET
    - Requires 'note_id' in the URL path.
    Response:
    - Returns the version history of the note, including modification details and changes.
    - If 'note_id' is not found, returns a 404 status with an error message.
    """
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
