from django.db import models


"""
Модель Справочник:
     - Идентификатор
     - Код (строка, 100 символов, обязательно для заполнения)
     - Наименование (строка, 300 символов, обязательно для заполнения)
     - Описание (текст произвольной длины)
     
Ограничения:
     - Не может существовать более одного Справочника с одинаковым значением в поле Код
"""


class Refbook(models.Model):
    code = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Код справочника',
        help_text='Строка, 100 символов',
    )
    name = models.CharField(
        max_length=300,
        verbose_name='Наименование',
        help_text='Строка, 300 символов',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Текст произвольной длины',
    )

    def __str__(self):
        return '[' + self.code + '] ' + self.name

    class Meta:
        ordering = ['code']
        verbose_name_plural = ' Справочники'
        verbose_name = 'Справочник'
