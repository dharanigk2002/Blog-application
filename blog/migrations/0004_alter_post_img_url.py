# Generated by Django 5.1.7 on 2025-03-19 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img_url',
            field=models.ImageField(null=True, upload_to='posts/images'),
        ),
    ]
