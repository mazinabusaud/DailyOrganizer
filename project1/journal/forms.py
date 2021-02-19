from django import forms
from journal.models import Journal
from core.models import UserProfile

class NewJournalForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    entry = forms.CharField(widget=forms.Textarea(attrs={'size': '500'}))
    class Meta():
        model = Journal
        fields = ('description', 'entry')

class EditJournalForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    entry = forms.CharField(widget=forms.Textarea(attrs={'size': '500'}))
    class Meta():
        model = Journal
        fields = ('description', 'entry')
