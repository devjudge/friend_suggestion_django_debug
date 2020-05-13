# Generated by Django 2.1 on 2020-05-13 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='friend_suggestor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200, unique=True)),
                ('friends', models.TextField()),
                ('friend_request', models.TextField()),
                ('request_pending', models.TextField()),
            ],
        ),
    ]
