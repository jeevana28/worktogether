from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    content = models.CharField(max_length=100)
    grpname = models.CharField(max_length=100, default='TECAPP')
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.content
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Message(models.Model):
	sender			= models.ForeignKey(User, on_delete=models.CASCADE,related_name='sender')
	receiver		= models.ForeignKey(User, on_delete=models.CASCADE,related_name='receiver')
	content			= models.CharField(max_length=150)
	time_sent 		= models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.sender.username +'_M' + str(self.id) 

class FriendRequest(models.Model):
	sender			= models.ForeignKey(User, on_delete=models.CASCADE,related_name='fr_sent_to')
	receiver		= models.ForeignKey(User, on_delete=models.CASCADE,related_name='fr_rec_from')
	time_sent 		= models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.sender.username +'_FR' + str(self.id)	

class Notification(models.Model):
	owner			= models.ForeignKey(User, on_delete=models.CASCADE, related_name='owning_notifs')
	generator		= models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_notifs')
	content			= models.CharField(max_length=50)		 
	time_sent 		= models.DateTimeField(default=timezone.now)	
	
	def __str__(self):
		return self.owner.username +'_N' + str(self.id)				

class Comment(models.Model):
    post = models.ForeignKey('grp.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text