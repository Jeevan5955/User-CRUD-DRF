# Generated by Django 4.2.1 on 2023-06-12 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('mobileNumber', models.BigIntegerField()),
                ('age', models.BigIntegerField()),
                ('height', models.BigIntegerField()),
                ('profilePicture', models.URLField()),
            ],
            options={
                'verbose_name': 'User Details',
                'db_table': 'User',
            },
        ),
    ]
