# Generated by Django 5.1.7 on 2025-03-29 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_book_pdf_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='pdf_file',
        ),
    ]
