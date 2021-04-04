from .models import PostComment
from django import forms

class NewCommentForm(forms.ModelForm):
	class Meta:
		model = PostComment
		fields = ['content']