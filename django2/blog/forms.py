from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.template.defaultfilters import slugify
from .models import *


class Add_new(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "author", "content", "photo", 'category','tags')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": " form-control"})

            # 'news_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        def clean_slug(self):
            title = self.cleaned_data['title'].strip()
            slug = slugify(title)
            if Post.objects.get(slug=slug).exists():
                slug += "1"

            return slug



class LoginUser(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class Register(forms.ModelForm):
    email = forms.EmailField(label='Почта', help_text='Required',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        clean_pass = self.cleaned_data
        if clean_pass['password1'] != clean_pass['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return clean_pass

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Данный e-mail адрес уже используется")
        return email

# class Resetpasswordnew(PasswordResetForm):
#
#     class Meta:
#         model = User
#         fields = ('email',)
#
#     def clean_email(self):
#         email = self.cleaned_data['email'].strip()
#         if User.objects.filter(email__iexact=email).exists():
#             return email
#         else:
#             raise forms.ValidationError("Данный e-mail адрес не найден")
