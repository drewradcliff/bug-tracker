from django import forms

from homepage.models import MyUser, Ticket


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ["username", "display_name"]


class AddTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description"]
