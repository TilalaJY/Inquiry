from django import forms
from .models import Inquiry

class InquiryForms(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = "__all__"

        widgets = {
            'product_start_date' : forms.widgets.DateInput(attrs={'type': 'date'}),
            'product_end_date' : forms.widgets.DateInput(attrs={'type': 'date'}),
        }
