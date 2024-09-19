from django import forms


class ClockInForm(forms.Form):
    date_from = forms.DateTimeField()
    date_to = forms.DateTimeField()


class SickLeaveForm(ClockInForm):
    description = forms.CharField(max_length=255)
