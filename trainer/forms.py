from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Word, WordImport

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Simplify but keep basic validation
        self.fields['password1'].help_text = 'Enter any password (minimum 4 characters)'
        self.fields['password2'].help_text = 'Enter the same password again'
        self.fields['password1'].widget.attrs.update({'minlength': '4'})
        self.fields['password2'].widget.attrs.update({'minlength': '4'})

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['english', 'translation', 'example']
        widgets = {
            'english': forms.TextInput(attrs={'class': 'form-control'}),
            'translation': forms.TextInput(attrs={'class': 'form-control'}),
            'example': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'english': 'English Word',
            'translation': 'Translation',
            'example': 'Example Sentence (optional)'
        }

class WordImportForm(forms.ModelForm):
    class Meta:
        model = WordImport
        fields = ['csv_file']
        widgets = {
            'csv_file': forms.FileInput(attrs={
                'accept': '.csv',
                'class': 'form-control'
            })
        }

class WordEditForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['translation', 'example']
        widgets = {
            'translation': forms.TextInput(attrs={'class': 'form-control'}),
            'example': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }