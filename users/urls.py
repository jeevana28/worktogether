from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import GroupCreateView
urlpatterns = [
    path('', views.home, name = 'homepage'),
     path('about/', views.about, name = 'about'),
    path('register/', views.UserRegister, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('home/',views.Homeacc, name = 'user-home'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('updateProfile/',views.updateProfile, name='updateProfile'),
    path('group/new', GroupCreateView.as_view(), name='group-create'),
    path('password-reset/', 
    auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', 
    auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/delete/confirmation/', views.deleteprofile, name='profile-delete-conf'),
    path('profile/delete/', views.deleteprof, name = 'profile-delete')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)