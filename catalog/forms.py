from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy  as _
import datetime 
from .models import BookInstance
from django.shortcuts import get_object_or_404

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data

class Fokus2(forms.ModelForm):
    class meta:
        model = BookInstance
        fields = ['due_back','status']
        disabled = {'due_back' : True, 'status':True,}
        initial = {'due_back' : datetime.date.today() + datetime.timedelta(weeks=2), 'status':'r',}
        
