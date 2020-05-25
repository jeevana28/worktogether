from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from .models import Profile, Groupf, group_new
from .forms import UserRegistrationForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.forms import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.core.mail import EmailMessage
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    return render(request, 'users/homepage.html')

def about(request):
    return render(request, 'users/about.html')

def activation_sent_view(request):
    return render(request, 'users/activation_sent.html')


def UserRegister(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get('email')
            user.profile.group = form.cleaned_data.get('group')
            user.profile.institute = form.cleaned_data.get('institute')
            # user.save()
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=password)
            # login(request, user)
            # r_user = User.objects.filter(username = username).first()
            # r_pro = Profile.objects.filter(user = r_user).first()
            # r_group = Groupf.objects.filter(group_name = r_pro.group).first()
            # r_group.users.add(r_pro)
            # messages.success(request,"Account Created for %s is created. Login!" %username)
            # return redirect('login') 
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('users/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            to_email = user.profile.email
            email_user = EmailMessage(subject, message, to=[to_email])
            email_user.send()
            return redirect('activation_sent')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form}) 

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        username = user.username
        r_user = User.objects.filter(username = username).first()
        r_pro = Profile.objects.filter(user = r_user).first()
        r_pro.notif_count = 0
        r_group = Groupf.objects.filter(group_name = r_pro.group).first()
        r_group.users.add(r_pro)
        messages.success(request,"Account Created for %s is created. Login!" %username)
        return redirect('login')
    else:
        return render(request, 'users/activation_invalid.html')

def Homeacc(request):
    groups = Groupf.objects.all() 
    return render(request, 'users/acchome.html', {'groups':groups})
    
@login_required
def updateProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            group = p_form.cleaned_data.get('group')
            r_group = Groupf.objects.filter(group_name = group).first()
            r_pro = Profile.objects.filter(user = request.user).first()
            r_group.users.add(r_pro)
            messages.success(request, f'Your account has been updated')
            return redirect('login')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form': u_form,
        'p_form': p_form,
     }
    return render(request, 'users/updatepro.html', context)

class GroupCreateView(SuccessMessageMixin, CreateView):
    model= group_new
    fields = ['groupname']
    success_url = '/home'
    success_message = "Group will be created! After a while, go to profile and update your group"

    def form_valid(self, form):
        return super().form_valid(form)

# class ProfileDelete(LoginRequiredMixin, DeleteView):
#     model = Profile
#     def get_success_url(self):
#         profile = self.get_object()
#         return reverse_lazy('homepage')


def deleteprofile(request):
    profile = Profile.objects.filter(user = request.user).first()
    user = User.objects.filter(username = request.user.username).first()
    #profile.delete()
    #messages.success(request, "Your profile is deleted") 
    return render(request, 'users/profiledelete.html')
def deleteprof(request):
    profile = Profile.objects.filter(user = request.user).first()
    user = User.objects.filter(username = request.user.username).first()
    profile.delete()
    user.delete()
    messages.success(request, "Your profile is deleted, Logout before proceeding")
    return render(request, 'users/delete.html') 