from django import forms
from .models import review_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = review_data
        fields = ['p_id', 'c_id', 'rating', 'review']
        widgets = {
            'review': forms.Textarea(attrs={'class': 'form-group quantity-box w-50 mx-5', 'rows': '1'}),
            'rating': forms.NumberInput(attrs={'class': 'form-group quantity-box w-50 mx-5', 'min': 1, 'max': 5})
        }
        