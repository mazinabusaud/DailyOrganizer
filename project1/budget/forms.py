from django import forms
from budget.models import Budget
from core.models import UserProfile
from django.core import validators

class NewBudgetForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    projected = forms.IntegerField(validators=[validators.MinValueValidator(0)])
    actual = forms.IntegerField(validators=[validators.MinValueValidator(0)])
    class Meta():
        model = Budget
        fields = ('description', 'projected', 'actual', 'category')

class EditBudgetForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    projected = forms.IntegerField(validators=[validators.MinValueValidator(0)])
    actual = forms.IntegerField(validators=[validators.MinValueValidator(0)])
    class Meta():
        model = Budget
        fields = ('description', 'projected', 'actual', 'category')
