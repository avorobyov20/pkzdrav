from django.db import models
from .refbook import Refbook


"""
Модель Версия справочника:
    - Идентификатор справочника (обязательно для заполнения)
    - Версия (строка, 50 символов, обязательно для заполнения)
    - Дата начала действия версии (дата)

Ограничения:
     - Не может существовать более одной Версии с одинаковым набором значений "Идентификатор справочника" и "Версия"
     - У одного Справочника не может быть более одной версии с одинаковой "Датой начала"
"""


class Version(models.Model):
    refbook = models.ForeignKey(Refbook, on_delete=models.PROTECT, verbose_name='Справочник')
    num = models.CharField(max_length=50, verbose_name='Номер версии')
    date_start = models.DateField(verbose_name='Дата начала действия')

    def __str__(self):
        return '[' + self.refbook.code + '] ' + self.refbook.name +\
              ' --' + self.num + '-- ' + self.date_start.strftime('%d.%m.%Y')

    class Meta:
        unique_together = (
            ('refbook', 'num'),
            ('refbook', 'date_start'),
        )
        verbose_name_plural = 'Версии справочников'
        verbose_name = 'Версия справочника'

