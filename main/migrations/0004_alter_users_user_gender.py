# Generated by Django 4.2.3 on 2023-07-29 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_users_user_age_alter_users_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_gender',
            field=models.SmallIntegerField(default=0),
        ),
    ]