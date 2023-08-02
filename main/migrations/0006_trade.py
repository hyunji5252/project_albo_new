# Generated by Django 4.2.3 on 2023-08-01 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_users_user_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_img', models.ImageField(blank=True, null=True, upload_to='trade_images/')),
                ('item_price', models.IntegerField(null=True)),
                ('item_date', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
    ]