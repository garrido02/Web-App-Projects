# Generated by Django 4.2.1 on 2023-06-29 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalproject', '0002_remove_message_author_message_email_message_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]