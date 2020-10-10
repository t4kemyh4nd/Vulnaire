# Generated by Django 3.1.2 on 2020-10-10 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201010_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='status',
            field=models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSE', 'CLOSE')], default='OPEN', max_length=10),
        ),
    ]
