from django import forms


class DateInputForm(forms.Form):
    month = forms.IntegerField(label='Month', min_value=1, max_value=12)
    day = forms.IntegerField(label='Day', min_value=1, max_value=31)