# Generated by Django 4.2.8 on 2024-09-28 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_maquina_pdf_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maquina',
            name='url_doc',
        ),
    ]
