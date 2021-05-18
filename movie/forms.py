from django import forms

from .models import Review, RATE_CHOICES

class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':"form-control"}), required=False)
    rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)

    class Meta:
        model = Review
        fields = ('text', 'rate')



