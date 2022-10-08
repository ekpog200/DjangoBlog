from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView, DetailView
from .models import *
from django.db.models import F, Prefetch
from .forms import *
from blog.utils.tokenregistrationgenerate import account_activation_token
from django.core.mail import EmailMessage, BadHeaderError
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordResetView


def add_news(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            forms = Add_new(request.POST, request.FILES)
            if forms.is_valid():
                forms.save(commit=False)

                return redirect(forms.save())
        else:
            forms = Add_new()
    else:
        return redirect('home')
    return render(request, 'blog/add_news.html', {'forms': forms})



def logoutuser(request):
    logout(request)
    return redirect('home')


def reset_password_new(request):
    if request.method == "POST":
        forms = PasswordResetForm(request.POST)
        if forms.is_valid():
            mail = forms.cleaned_data['email']
            try:
                user = User.objects.get(email=mail)
            except Exception:
                user = False
            if user:
                subject = "Попытка изменения пароля"
                current_site = get_current_site(request)
                message = render_to_string('blog/password_reset_email.html', {
                    'user': user,
                    'domain': '127.0.0.1:8000',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = forms.cleaned_data.get('email')

                email = EmailMessage(
                    subject, message, from_email='martamstart@yandex.ru', to=[to_email]
                )
                try:
                    email.send()
                except BadHeaderError:
                    return HttpResponse("Обнаружен недопустимый заголовок!")
                return redirect('password_reset_done')
            else:
                messages.error(request, 'Пользователь не найден, напишите администратору')
                return redirect('reset_password_new')
    return render(request=request, template_name='blog/password_reset_form.html')


def loginuser(request):
    if request.method == "POST":
        forms = LoginUser(data=request.POST)
        if forms.is_valid():
            user = forms.get_user()
            login(request, user)
            return redirect('home')
    else:
        forms = LoginUser()
    return render(request, 'blog/login.html', {'forms': forms})


def activateuser(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        message = 'error'
        return render(request, 'blog/afteractivateuser.html', {'message': message})
    else:
        message = 'success'
        return render(request, 'blog/afteractivateuser.html', {'message': message})


def registrationuser(request):
    if request.method == "POST":
        forms = Register(request.POST)
        if forms.is_valid():
            user = forms.save(commit=False)  # сохраняем форму в памяти, а не в ДБ
            user.is_active = False  # Не даем активировать учетку до подтверждения
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('blog/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = forms.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, from_email='martamstart@yandex.ru', to=[to_email]
            )
            email.send()
            rd = 'success'
            return render(request, 'blog/afterregisteruser.html', {'message': rd})
    else:
        forms = Register()
    return render(request, 'blog/register.html', {'forms': forms, 'message': messages})


class Home(ListView):
    model = Post
    paginate_by = 4
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog by Me'
        return context


class PotsByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 3
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return content


class PostsByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 3
    allow_empty = False

    # def get_queryset(self):
    #     return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_queryset(self):
        queryset = Post.objects.prefetch_related(
            Prefetch('tags', queryset=Tag.objects.filter(slug=self.kwargs['slug'])))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        return content


class GetPost(DetailView):
    context_object_name = 'posts'
    template_name = 'blog/single.html'

    def get_queryset(self):
        return Post.objects.prefetch_related('tags').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        return content


class Search(ListView):
    context_object_name = 'posts'
    template_name = 'blog/search.html'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context
