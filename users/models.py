from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import login, authenticate
# Create your models here.
GROUP =[
    ('TECAPP', 'Tech: App development'),
    ('TECCP', 'Tech: Competitive Programming'),
    ('TECAI', 'Tech: Artificial Intelligence'),
    ('TECDS', 'Tech: Data Science'),
    ('CPEUPSC', 'Competitive exams: UPSC'),
    ('CPECAT', 'Competitive exams: CAT'),
    ('CPEGRE', 'Competitive exams: GRE'),
    ('CPEGATE', 'Competitive exams: GATE'),
    ('SPFGYM', 'Sports and Fitness: Gym'),
    ('SPFFB', 'Sports and Fitness: Football'),
    ('ARTSKE', 'Arts and Crafts: Sketching'),
    ('ARTDA', 'Arts and Crafts: Digital Arts'),
    ('MAMMI', 'Music and Movies: Musical Instruments'),
    ('MAMFM', 'Music and Movies: Film making'),
]
GROUPS = [('','---------')] + GROUP
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=100, choices=GROUPS)
    email = models.EmailField(max_length=150)
    image = models.ImageField(default='default.JPG', upload_to='profile_pics')
    friends	= models.ManyToManyField("self")
    notif_count	= models.PositiveSmallIntegerField(default=0)
    institute = models.CharField(max_length = 200, default='')
    signup_confirmation = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Groupf(models.Model):
    group_name = models.CharField(max_length = 100,choices = GROUPS)
    users = models.ManyToManyField(Profile)

    def __str__(self):
        return self.group_name

class group_new(models.Model):
    groupname = models.CharField(max_length = 100, default='')

    def __str__(self):
        return self.groupname
