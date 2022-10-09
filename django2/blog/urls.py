from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', Home.as_view(), name="home"),
    path('category/<str:slug>/', PotsByCategory.as_view(), name="category"),
    path('tag/<str:slug>/', PostsByTag.as_view(), name="tag"),
    path('post/<str:slug>/', GetPost.as_view(), name="post"),
    path('search/', Search.as_view(), name="search"),
    path('register/', registrationuser, name="register"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activateuser, name='activate'),
    path('login/', loginuser, name="login"),
    path('logout/', logoutuser, name ='logout'),
    path('add_news/', add_news, name='add_news'),




    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='blog/RegAuth/resetPassword/password_change_done.html'),
         name='password_reset_complete'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='blog/RegAuth/resetPassword/password_change.html'),
         name='password_reset_confirm'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='blog/RegAuth/resetPassword/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/', reset_password_new,
         name='reset_password_new'),


]
