
from rest_framework import serializers
from .models import NoteMetadata, NoteVersionHistory, NoteChanges

class NoteChangesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteChanges
        fields = '__all__'

class NoteVersionHistorySerializer(serializers.ModelSerializer):
    changes = NoteChangesSerializer(many=True, read_only=True)

    class Meta:
        model = NoteVersionHistory
        fields = '__all__'

class NoteMetadataSerializer(serializers.ModelSerializer):
    version_history = NoteVersionHistorySerializer(many=True, read_only=True)

    class Meta:
        model = NoteMetadata
        fields = '__all__'