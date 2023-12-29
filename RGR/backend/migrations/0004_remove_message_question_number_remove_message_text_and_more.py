# Generated by Django 5.0 on 2023-12-27 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_message_question_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='question_number',
        ),
        migrations.RemoveField(
            model_name='message',
            name='text',
        ),
        migrations.AddField(
            model_name='message',
            name='answer1',
            field=models.CharField(default='', max_length=255, verbose_name='Ответ на вопрос 1'),
        ),
        migrations.AddField(
            model_name='message',
            name='answer2',
            field=models.CharField(default='', max_length=255, verbose_name='Ответ на вопрос 2'),
        ),
        migrations.AddField(
            model_name='message',
            name='answer3',
            field=models.CharField(default='', max_length=255, verbose_name='Ответ на вопрос 3'),
        ),
        migrations.AddField(
            model_name='profile',
            name='subscription',
            field=models.BooleanField(default=False, verbose_name='Подписка на рассылку'),
        ),
    ]