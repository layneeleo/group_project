from .models import Flood_report
from django import forms

class FloodForm(forms.ModelForm):
    class Meta:
        model=Flood_report
        fields='__all__'
  