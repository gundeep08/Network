# Generated by Django 3.0.7 on 2020-07-26 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_auto_20200726_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(blank=True, max_length=50)),
                ('followingId', models.IntegerField()),
            ],
        ),
    ]
