from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Order


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
    payment_method = forms.ChoiceField(
        label='გადახდის მეთოდი',
        choices=Order.PaymentMethod.choices,
        initial=Order.PaymentMethod.CASH,
        widget=forms.RadioSelect,
    )
    card_number = forms.CharField(
        label='ბარათის ნომერი',
        required=False,
        max_length=19,
        widget=forms.TextInput(attrs={
            'autocomplete': 'cc-number',
            'inputmode': 'numeric',
            'placeholder': '1234 5678 9012 3456',
        }),
    )
    card_expiry = forms.CharField(
        label='ვადა',
        required=False,
        max_length=5,
        widget=forms.TextInput(attrs={
            'autocomplete': 'cc-exp',
            'placeholder': 'MM/YY',
        }),
    )
    card_cvv = forms.CharField(
        label='CVV',
        required=False,
        max_length=4,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'cc-csc',
            'inputmode': 'numeric',
            'placeholder': '123',
        }),
    )
    note = forms.CharField(
        label='შენიშვნა',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
    )

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        if payment_method == Order.PaymentMethod.CARD:
            card_number = ''.join((cleaned_data.get('card_number') or '').split())
            card_expiry = cleaned_data.get('card_expiry') or ''
            card_cvv = cleaned_data.get('card_cvv') or ''

            if not card_number.isdigit() or not 13 <= len(card_number) <= 19:
                self.add_error('card_number', 'შეიყვანეთ სწორი ბარათის ნომერი.')
            if len(card_expiry) != 5 or card_expiry[2] != '/' or not card_expiry[:2].isdigit() or not card_expiry[3:].isdigit():
                self.add_error('card_expiry', 'ვადა ჩაწერეთ ფორმატით MM/YY.')
            elif not 1 <= int(card_expiry[:2]) <= 12:
                self.add_error('card_expiry', 'მიუთითეთ სწორი თვე.')
            if not card_cvv.isdigit() or len(card_cvv) not in (3, 4):
                self.add_error('card_cvv', 'შეიყვანეთ სწორი CVV.')

        return cleaned_data
