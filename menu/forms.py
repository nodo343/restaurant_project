from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='სახელი', max_length=150)
    last_name = forms.CharField(label='გვარი', max_length=150)
    email = forms.EmailField(label='ელ. ფოსტა')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'მომხმარებლის სახელი',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'პაროლი'
        self.fields['password2'].label = 'გაიმეორეთ პაროლი'

        for field in self.fields.values():
            field.help_text = ''

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('ამ ელ. ფოსტით ანგარიში უკვე არსებობს.')
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='მომხმარებლის სახელი')
    password = forms.CharField(label='პაროლი', widget=forms.PasswordInput)


class CheckoutForm(forms.Form):
    full_name = forms.CharField(label='სახელი და გვარი', max_length=180)
    phone = forms.CharField(label='ტელეფონი', max_length=30)
    address = forms.CharField(label='მისამართი', max_length=255)
    note = forms.CharField(
        label='შენიშვნა',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
    )
