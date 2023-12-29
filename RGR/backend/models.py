from django.db import models

class Profile(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='ID пользователя')
    name = models.TextField(verbose_name='Имя пользователя')
    RESIDENCE_CHOICES = [
        ('left', 'Левый берег'),
        ('right', 'Правый берег'),
    ]
    residence = models.CharField(
        max_length=10,
        choices=RESIDENCE_CHOICES,
        default='left',  # Установите значение по умолчанию по вашему выбору
        verbose_name='Проживание'
    )
    subscription = models.BooleanField(default=False, verbose_name='Подписка на рассылку')

    def __str__(self):
        return f'#{self.external_id} {self.name} ({self.residence}){self.subscription}'
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Message(models.Model):
    profile = models.ForeignKey(to='backend.Profile', verbose_name='Профиль', on_delete=models.PROTECT)
    answer1 = models.CharField(max_length=255,default='', verbose_name='Ответ на вопрос 1')
    answer2 = models.CharField(max_length=255,default='', verbose_name='Ответ на вопрос 2')
    answer3 = models.CharField(max_length=255,default='', verbose_name='Ответ на вопрос 3')
    created_at = models.DateTimeField(verbose_name='Время получения', auto_now_add=True)

    def __str__(self):
        return f'Сообщение {self.pk} от {self.profile}'
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

class University(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    location = models.CharField(max_length=10, choices=[('left', 'Левый берег'), ('right', 'Правый берег')],
                                 verbose_name='Расположение')
    specialization = models.CharField(max_length=20, choices=[('technical', 'Технический'), ('humanitarian', 'Гуманитарный')],
                                       verbose_name='Специализация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вуз'
        verbose_name_plural = 'Вузы'