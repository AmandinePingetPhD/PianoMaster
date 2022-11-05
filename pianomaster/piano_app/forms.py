"""Definition of form used."""

from django import forms
from .models import Note


class ContactForm(forms.Form):
    """Form for contact page."""

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    e_message = forms.CharField(widget=forms.Textarea, max_length=2000)


class MusicianForm(forms.Form):
    """Form for home page - Initial form."""

    first_name = forms.CharField(required=True, max_length=50)


class RatingForm(forms.ModelForm):
    """Star rating form for suggestions link to recipes."""

    class Meta:
        """Star rating form definition."""

        model = Note
        fields = ['rating']
        widgets = {'rating': forms.NumberInput(attrs={'class': 'Stars'})}
        labels = {'rating': 'Rating /5'}
