from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Post,Message, FriendRequest, Notification, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from datetime import datetime
#from .forms import CommentForm
from users.models import Profile, Groupf
from .petty_tasks import *
from .forms import CommentForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy


@login_required
def Grphome(request, name):
    users = Profile.objects.filter(group = name)
    user_profile = Profile.objects.filter(user = request.user).first()
    posts = Post.objects.filter(grpname = name)
    if user_profile.group==name:
        return render(request, 'grp/grphome.html', {'users':users, 'user_profile': user_profile, 'posts': posts})
    return HttpResponse("<h1>Invalid Link</h1>")

def ShowProfile(request, name):
    profiler_user = User.objects.filter(username = name).first() 
    profiler_profile = Profile.objects.filter(user=profiler_user).first()
    user_profile 	 = Profile.objects.filter(user=request.user).first()
    if profiler_user:
        msgs_query = Message.objects.filter(receiver = profiler_user, sender = request.user) | Message.objects.filter(sender=profiler_user, receiver=request.user)
        msgs_count = msgs_query.count()
        msgs = msgs_query.order_by("-time_sent").all()
        status, fr_button = getFriendStatus(request.user, profiler_user)
        profiler_friends = fetchFriendsOf(profiler_user)
        return render(request, 'users/profile.html',{'user_profile':user_profile,'profiler_profile':profiler_profile, 'profiler_friends':profiler_friends, 'msgs' : msgs, 'msgs_count' : msgs_count, 'status' : status, 'fr_button' : fr_button})
    else:
        return 	HttpResponse("<h1>Invalid Link</h1>")


@login_required
def SendMessage(request):
    if request.method == 'GET':
        m = Message()
        m.sender = request.user
        r = User.objects.filter(username = request.GET['rcvr']).first()
        m.receiver 	= r
        m.content	= request.GET['mg']
        m.save()
        createNotification(r,request.user,2)
        return HttpResponse('success')
    else:
        return HttpResponse('unsuccessful')	

@login_required
def LoadMessages(request): 		#I would GET user,profiler,timechecked
    if request.method == 'GET':
        profiler_name = request.GET['profiler']
        profiler_u	 = User.objects.filter(username = profiler_name).first()
        profiler_pro = Profile.objects.filter(user = profiler_u).first()
        if request.GET['count'] != 'NaN':	
            old_count = int(request.GET['count'])
            m_set = Message.objects.filter(receiver = request.user, sender = profiler_pro.user) | Message.objects.filter(sender=request.user, receiver=profiler_pro.user)
            new_count=m_set.count()
            if new_count != old_count:
                msgs = m_set.order_by("time_sent").all()[old_count:]
                msgs_arr = []
                lekha = {}
                i=0
                for msg in msgs:	
                    msgs_arr.append(msg.content)
                    i+=1
                lekha["msgs"]=msgs_arr
                lekha["curr_count"]=i	
                lekha["total_count"]=new_count
                return JsonResponse (lekha)
        return JsonResponse({"curr_count":0})
    else:
        pass

def sendRequest(request):
    if request.is_ajax():			
        if request.method == 'GET':
            p_name = request.GET['rcvr']
            p_u_acc= User.objects.filter(username=p_name).first()
            fr = FriendRequest()
            fr.sender = request.user
            fr.receiver = p_u_acc
            fr.save()
            createNotification(p_u_acc,request.user,0)
            return HttpResponse ('Ajax is successful!') 
        else:
            return HttpResponse ('Ajax failed')	
    else:
        return HttpResponse ('Ajax failed')		

def cancelRequest(request):
    if request.is_ajax():			
        if request.method == 'GET':
            p_name = request.GET['rcvr']
            p_u_acc= User.objects.filter(username=p_name).first()
            fr = request.user.fr_sent_to.filter(receiver = p_u_acc).first()
            fr.delete()
            n = Notification.objects.filter(owner=p_u_acc,generator=request.user).first()
            n.delete()
            p_pro = Profile.objects.filter(user=p_u_acc).first()
            p_pro.notif_count -= 1
            return HttpResponse ('Ajax successful') 
        else:
            return HttpResponse ('Ajax failed')	
    else:
        return HttpResponse ('Ajax failed')

def acceptRequest(request):
    if request.is_ajax():			
        if request.method == 'GET':
            p_name = request.GET['rcvr']
            p_u_acc= User.objects.filter(username=p_name).first()
            profiler_pro = Profile.objects.filter(user=p_u_acc).first()
            fr = request.user.fr_rec_from.filter(sender = p_u_acc).first()
            fr.delete()
            user_pro = Profile.objects.filter(user = request.user).first()
            user_pro.friends.add(profiler_pro)
            createNotification(p_u_acc,request.user,1)
            return HttpResponse ('Ajax successful') 
        else:
            return HttpResponse ('Ajax failed')	
    else:
        return HttpResponse ('Ajax failed')

def removeFriend(request):
    if request.is_ajax():			
        if request.method == 'GET':
            p_name = request.GET['rcvr']
            p_u_acc= User.objects.filter(username=p_name).first()
            profiler_pro = Profile.objects.filter(user=p_u_acc).first()
            user_pro = Profile.objects.filter(user = request.user).first()
            user_pro.friends.remove(profiler_pro)
            return HttpResponse ('Ajax successful') 
        else:
            return HttpResponse ('Ajax failed')	
    else:
        return HttpResponse ('Ajax failed')

def rejectRequest(request):
    if request.is_ajax():			
        if request.method == 'GET':
            p_name = request.GET['rcvr']
            p_u_acc= User.objects.filter(username=p_name).first()
            fr = request.user.fr_rec_from.filter(sender = p_u_acc).first()
            fr.delete()
            return HttpResponse ('Ajax is successful') 
        else:
            return HttpResponse ('Ajax failed')	
    else:
        return HttpResponse ('Ajax failed')		

def reportUser(request):
    if request.is_ajax():			
        if request.method == 'GET':
            p_name = request.GET['rcvr']
            messages.success(request,"%s is reported successfully" %p_name)
            return HttpResponse ('Ajax is successful') 
        else:
            return HttpResponse ('Ajax failed 4')	
    else:
        return HttpResponse ('Ajax failed')	
def fetchNotifs(request):
    if request.is_ajax():
        if request.method == 'GET':				
            n_set = Notification.objects.filter(owner=request.user).order_by("-time_sent").all()
            if n_set:
                generators = []
                contents   = []	
                lekha = {}
                for n in n_set:
                    generators.append(n.generator.username)
                    contents.append(n.content)
                lekha["generators"] = generators
                lekha["contents"] = contents
                lekha["status"] = "notifs found"
                u_pro = Profile.objects.filter(user = request.user).first()
                u_pro.notif_count=0
                u_pro.save()
                return JsonResponse(lekha)
            else:
                return JsonResponse({"status" : "no notifs"})
        else:
            pass

class PostDetailView(DetailView):
    model= Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model= Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.author =  self.request.user
        form.instance.grpname = self.request.user.profile.group
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model= Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.author =  self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model= Post
    def get_success_url(self):
        post = self.get_object()
        return reverse_lazy('grouphome', kwargs={'name':post.grpname})
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# class CommentCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
#     model = Comment
#     fields = ['content']

#     def form_valid(self, form):
#         form.instance.author =  self.request.user
#         form.instance.post = 
#         return super().form_valid(form)

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    name = request.user.profile.group
    posts = Post.objects.filter(grpname = name)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'grp/add_comment.html', {'form': form, 'post':post})

