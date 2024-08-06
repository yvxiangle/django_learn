# Generated by Django 5.0.7 on 2024-07-24 12:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.SmallIntegerField(choices=[(1, '紧急'), (2, '重要'), (3, '临时')], default=1, verbose_name='级别')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('detail', models.TextField(verbose_name='详细信息')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.admin', verbose_name='管理员')),
            ],
        ),
    ]
