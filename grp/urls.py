from django.urls import path
from . import views
from .views import (
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView
)

urlpatterns = [
    path('home/<name>/', views.Grphome, name='grouphome'),
    path('profile/<name>/',views.ShowProfile, name='userprofile'),
    path('sendmessage/',views.SendMessage, name = 'sendMessage'),
	path('checkmessages/',views.LoadMessages, name='checkMessages'),
	path('sendRequest/',views.sendRequest, name='sendRequest'),
	path('cancelRequest/',views.cancelRequest, name='cancelRequest'),
	path('acceptRequest/',views.acceptRequest, name='acceptRequest'),
	path('removeFriend/',views.removeFriend, name='removeFriend'),
	path('reportUser/',views.reportUser, name='reportUser'),
	path('rejectRequest/',views.rejectRequest, name='rejectRequest'),
	path('fetchNotifs/',views.fetchNotifs, name='fetchNotifs'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('post/new', PostCreateView.as_view(), name='post-create'),
	path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
	path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
	path('post/<int:pk>/comment', views.add_comment, name='post-comment')
]