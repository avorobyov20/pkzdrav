from django.db import models
from .version import Version
from django.utils.safestring import mark_safe

"""
Модель Элемент справочника:
    - Идентификатор Версии справочника (обязательно для заполнения)
    - Код элемента (строка, 100 символов, обязательно для заполнения)
    - Значение элемента (строка, 300 символов, обязательно для заполнения)

Ограничения:
    - В одной Версии справочника не может сущ-ть более одного Элемента справочника с одинаковым значением в поле Код 
"""


class Element(models.Model):
    version = models.ForeignKey(Version, on_delete=models.PROTECT, verbose_name='Версия справочника')
    code = models.CharField(max_length=100, verbose_name='Код элемента')
    value = models.CharField(max_length=300, verbose_name='Значение')

    def __str__(self):  # Не забыть потом это убрать!
        href = '/refbooks/' + str(self.version.refbook.pk) + '/check_element?code=' + self.code +\
               '&value=' + self.value + '&version=' + self.version.num
        return mark_safe(
            '<a href="' + href + '" target="_blank">' + href + '</a>'
                         )

    class Meta:
        unique_together = (
            ('version', 'code'),
        )
        verbose_name_plural = 'Элементы справочников'
        verbose_name = 'Элемент справочника'
