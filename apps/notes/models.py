from django.db import models
from django.contrib.auth.models import User
from apps.authapp.models import CustomUser

class NoteMetadata(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='note_metadata', on_delete=models.CASCADE)
    shared_users = models.ManyToManyField(CustomUser, related_name='shared_notes')
    def __str__(self):
    	return f'{self.id}'

class NoteVersionHistory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    note_metadata = models.ForeignKey(NoteMetadata, on_delete=models.CASCADE)

    def __str__(self):
        return f'nvh:{self.id} note: {self.note_metadata.id}'

class NoteChanges(models.Model):
    line_no = models.IntegerField()
    text = models.TextField()
    note_version_history = models.ForeignKey(NoteVersionHistory, on_delete=models.CASCADE)

    def __str__(self):
        return f'line: {self.line_no} nvh: {self.note_version_history.id} note: {self.note_version_history.note_metadata.id}'



								
	# [USER]	
		
	# username ++	
	# password	
		
		
	# [noteMetadata]	
		
	# id ++	
	# owner - FK user	
	# shared_user 1:m User	
		
	# [NoteVersionHistory]	
		
	# id ++	
	# timestamp	
	# user	
	# noteMetadata-  FK 	
		
		
	# [noteChanges]	
		
	# id ++	
	# line_no	
	# text	
	# NoteVersionHistory - FK 	
		