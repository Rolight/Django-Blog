from django import forms

class LoginForm(forms.Form):
    uid = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'uid',
        'placeholder': 'Username'
    }))

    pwd = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'pwd',
        'placeholder': 'Password'
    }))


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'uid',
        'placeholder': 'Username'
    }))
    email = forms.EmailField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

class SetInfoForm(forms.Form):
    username = forms.CharField()

class CommentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={
        'cols': '60',
        'rows': '6'
    }))

class SearchForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput)



