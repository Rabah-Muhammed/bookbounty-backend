# Generated by Django 5.1.7 on 2025-03-29 15:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_book_pdf_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reading_lists', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
