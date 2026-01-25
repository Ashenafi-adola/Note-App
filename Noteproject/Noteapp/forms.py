from django.forms import ModelForm
from .models import Subject, Note
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['user']

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
        exclude = ['user','subject']
        widgets = {
            'note': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
