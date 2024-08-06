# Generated by Django 5.0.7 on 2024-07-30 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_boss'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('count', models.IntegerField(verbose_name='人口')),
                ('logo', models.FileField(max_length=128, upload_to='city/', verbose_name='图片')),
            ],
        ),
    ]
