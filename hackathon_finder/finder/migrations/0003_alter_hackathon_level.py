# Generated by Django 5.2 on 2025-04-14 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0002_hackathon_level_profile_branch_profile_college_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hackathon',
            name='level',
            field=models.CharField(choices=[('local', 'Local'), ('national', 'National'), ('international', 'International'), ('other', 'Other')], default='other', max_length=20),
        ),
    ]
