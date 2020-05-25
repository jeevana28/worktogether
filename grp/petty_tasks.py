from django.contrib.auth.models import User
from .models import Message, FriendRequest, Notification
from users.models import Profile

def getProfiles(user, profiler):
	u_pro = Profile.objects.filter(user=user).first()
	p_pro = Profile.objects.filter(user=profiler).first()
	return u_pro,p_pro

def getFriendStatus(user, profiler):
			# 0 for no relation, 1 for request sent to profiler, 2 for request received from profiler, 3 for friends
	user_profile = Profile.objects.filter(user=user).first()
	if 	user.fr_sent_to.filter(receiver=profiler).first() : 
		status = '1'
		button = 'Cancel Request' 
	elif user.fr_rec_from.filter(sender=profiler).first() : 
		status = '2'
		button = 'Accept Request'
	elif user_profile.friends.filter(user=profiler).first() : 		
		status = '3'
		button = 'Disconnect'
	else : 
		status = '0'
		button = 'Connect'
	return status,button

def createNotification(own,gen,status):
	n = Notification()		
	n.owner = own
	n.generator = gen
	ctnt = ''
	if 	 status == 0:
		ctnt = 'sent you a friend request'
	elif status == 1:
		ctnt 	= 'accepted your friend request'
	elif status == 2:
		ctnt 	= 'sent you a message'
	else: 
		pass		
	n.content = ctnt
	owner_profile = Profile.objects.filter(user=own).first()
	owner_profile.notif_count = owner_profile.notif_count + 1
	owner_profile.save()
	n.save()	

def fetchFriendsOf(u):
	profile = Profile.objects.filter(user=u).first()
	return profile.friends.all()