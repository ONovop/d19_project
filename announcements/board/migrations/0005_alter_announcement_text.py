# Generated by Django 4.1.5 on 2023-02-03 16:06

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_alter_response_announcement_alter_response_responser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
