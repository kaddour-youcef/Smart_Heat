# Generated by Django 3.2 on 2021-05-03 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Smart_heat', '0003_alter_fichier_csv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichier',
            name='csv',
            field=models.FileField(blank=True, upload_to='fichiers'),
        ),
    ]
