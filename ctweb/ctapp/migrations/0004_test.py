# Generated by Django 3.1.7 on 2021-04-02 10:06

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('ctapp', '0003_auto_20210312_0801'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='auth.user')),
                ('enrollment_number', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('college_name', models.CharField(choices=[('LNCT', 'LNCT'), ('LNCTS', 'LNCTS'), ('LNCTE', 'LNCTE')], default='LNCT', max_length=10)),
                ('sem', models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8)], default='6', max_length=20)),
                ('sec', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], default='A', max_length=1)),
                ('branch', models.CharField(choices=[('IT', 'IT'), ('CS', 'CS'), ('EC', 'EC'), ('MECH', 'MECH'), ('EE', 'EE'), ('EX', 'EX'), ('CIVIL', 'CIVIL')], default='IT', max_length=20)),
                ('mobile_no', models.CharField(max_length=10)),
                ('alt_email', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]