# Generated by Django 3.1.7 on 2021-04-04 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctapp', '0010_assignment_assignfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='test_for_sem',
            field=models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8)], default='6', max_length=20),
        ),
    ]
