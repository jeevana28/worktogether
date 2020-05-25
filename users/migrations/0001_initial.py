# Generated by Django 3.0.5 on 2020-04-28 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(choices=[('TECAPP', 'Tech: App development'), ('TECCP', 'Tech: Competitive Programming'), ('TECAI', 'Tech: Artificial Intelligence'), ('TECDS', 'Tech: Data Science'), ('CPEUPSC', 'Competitive exams: UPSC'), ('CPECAT', 'Competitive exams: CAT'), ('CPEGRE', 'Competitive exams: GRE'), ('CPEGATE', 'Competitive exams: GATE'), ('SPFGYM', 'Sports and Fitness: Gym'), ('SPFYOGA', 'Sports and Fitness: Yoga'), ('SPFFB', 'Sports and Fitness: Football'), ('SPFCRI', 'Sports and Fitness: Cricket'), ('ARTSKE', 'Arts and Crafts: Sketching'), ('ARTPAC', 'Arts and Crafts: Paper Craft'), ('ARTDA', 'Arts and Crafts: Digital Arts'), ('MAMMI', 'Music and Movies: Musical Instruments'), ('MAMVOC', 'Music and Movies: Vocals'), ('MAMFM', 'Music and Movies: Film making'), ('MAMACT', 'Music and Movies: Acting')], max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]