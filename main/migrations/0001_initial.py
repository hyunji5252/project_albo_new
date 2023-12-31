# Generated by Django 4.2.3 on 2023-08-04 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_img', models.ImageField(blank=True, null=True, upload_to='trade_images/')),
                ('item_price', models.IntegerField(null=True)),
                ('trade_date', models.DateField(auto_now_add=True, null=True)),
                ('user_gender', models.IntegerField(blank=True, default=0, null=True)),
                ('user_age', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20, unique=True)),
                ('user_date', models.DateTimeField(auto_now_add=True)),
                ('user_email', models.EmailField(max_length=254, unique=True)),
                ('user_password', models.CharField(max_length=100)),
                ('user_gender', models.IntegerField(blank=True, default=0, null=True)),
                ('user_age', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'user_tb',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=20)),
                ('trade_status', models.CharField(choices=[('거래 전', '거래 전'), ('거래 완료', '거래 완료')], default='거래 전', max_length=5, null=True)),
                ('item_price', models.IntegerField(null=True)),
                ('item_content', models.TextField(max_length=200)),
                ('item_img', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('user_name', models.ForeignKey(db_column='user_name', max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='main.users', to_field='user_name')),
            ],
            options={
                'db_table': 'item_tb',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('item_id', models.ForeignKey(db_column='item_id', on_delete=django.db.models.deletion.CASCADE, related_name='post', to='main.item')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='main.comment')),
                ('user_name', models.ForeignKey(db_column='user_name', max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to='main.users', to_field='user_name')),
            ],
            options={
                'ordering': ['-comment_date'],
            },
        ),
    ]
