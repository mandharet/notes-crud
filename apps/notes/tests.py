from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.authapp.models import CustomUser
from apps.notes.models import NoteMetadata, NoteChanges, NoteVersionHistory

class NoteAPITests(TestCase):
    # setUp
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser1', password='testpassword')
        CustomUser.objects.create_user(username='testuser2', password='testpassword')
        CustomUser.objects.create_user(username='testuser3', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def create_test_note(self):
        note_metadata = NoteMetadata.objects.create(owner=self.user)
        note_metadata.shared_users.add(self.user)
        initial_version = NoteVersionHistory.objects.create(user=self.user, note_metadata=note_metadata)
        NoteChanges.objects.create(line_no=1, text="1Test note content\n2Lorem Ipsum\n3ipsum lorem\n4EOF", note_version_history=initial_version)
        return note_metadata
    
    # getListofNotes
    def test_get_list_of_notes(self):
        self.test_create_note()
        self.test_create_note()
        url = reverse('getListofNotes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_of_notes_no_notes(self):
        NoteMetadata.objects.all().delete()  # Ensure there are no notes
        url = reverse('getListofNotes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'No notes found for the user'})


    # create note
    def test_create_note(self):
        url = reverse('create')
        data = {"noteContent": "1Test note content\n2Lorem Ipsum\n3ipsum lorem\n4EOF"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_note_missing_content(self):
        url = reverse('create')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Note Content is required'})

    # get_or_update_note
    # get noteDetails
    def test_get_note_details(self):
        note_metadata = self.create_test_note()
        url = reverse('get_or_update_note', args=[note_metadata.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note_details_invalid_note_id(self):
        url = reverse('get_or_update_note', args=[0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_note_details_unauthorized_user(self):
        note_metadata = self.create_test_note()
        self.client.force_authenticate(user=CustomUser.objects.create_user(username='unauthorized_user', password='testpassword'))
        url = reverse('get_or_update_note', args=[note_metadata.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # update noteDetails
    def test_update_note(self):
        note_metadata = self.create_test_note()
        url = reverse('get_or_update_note', args=[note_metadata.id])
        data = {"noteContent": "Updated note content\n4.New content"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_note_missing_content(self):
        note_metadata = self.create_test_note()
        url = reverse('get_or_update_note', args=[note_metadata.id])
        response = self.client.put(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Note Content is required'})

    # share note
    def test_share_note(self):
        note_metadata = self.create_test_note()
        url = reverse('share')
        data = {"noteId": note_metadata.id, "sharedUsers": [2, 3]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_share_note_missing_note_id(self):
        url = reverse('share')
        response = self.client.post(url, {'sharedUsers': [2, 3]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Note Id is required'})

    def test_share_note_missing_shared_users(self):
        note_metadata = self.create_test_note()
        url = reverse('share')
        response = self.client.post(url, {'noteId': note_metadata.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'List of shared_users is required'})

    def test_share_note_invalid_note_id(self):
        url = reverse('share')
        data = {"noteId": 0, "sharedUsers": [2, 3]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # getVersionHistory
    def test_get_version_history(self):
        note_metadata = self.create_test_note()
        url = reverse('getVersions', args=[note_metadata.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_version_history_invalid_note_id(self):
        url = reverse('getVersions', args=[0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        pass
