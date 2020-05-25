from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
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
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=150, required=True)
    group = forms.ChoiceField(choices=GROUPS, required=True)
    institute = forms.CharField(max_length=200, required=True)
    class Meta:
        model =  User
        fields = ('username', 'email', 'password1', 'password2', 'group', 'institute',)

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
    
class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['group', 'image', 'institute']