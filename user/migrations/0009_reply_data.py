# Generated by Django 3.1.2 on 2021-01-27 11:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20210124_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='reply_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField(default='', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('contact_us', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.contact_us_data')),
            ],
        ),
    ]
