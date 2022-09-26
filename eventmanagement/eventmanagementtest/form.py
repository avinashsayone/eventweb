from django import forms


class Register(forms.Form):
	name = forms.CharField(max_length=20)
	age = forms.CharField(max_length=3)
	address = forms.CharField(widget=forms.Textarea)
	phonenumber=forms.CharField(max_length=20)
	username=forms.CharField(max_length=100)
	password=forms.CharField(widget=forms.PasswordInput())

class Addevent(forms.Form):
    event_name=forms.CharField(max_length=20)
    description=forms.CharField(widget=forms.Textarea)
    date=forms.DateField()
    time=forms.TimeField()