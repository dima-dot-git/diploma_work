from django import forms
from .models import ProductInCart, User, Subscribe
from django.forms import inlineformset_factory


class ProductInCartForm(forms.ModelForm):
    class Meta:
        model = ProductInCart
        exclude = ['amount']


class RegUserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Устанавливаем хешированный пароль
        if commit:
            user.save()
        return user


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = "__all__"
