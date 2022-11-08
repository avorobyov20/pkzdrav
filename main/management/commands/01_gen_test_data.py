from datetime import date, timedelta
from django.core.management.base import BaseCommand
import random

from .utils import update_sqlite_table
from main.model.refbook import Refbook
from main.model.version import Version
from main.model.element import Element


class Command(BaseCommand):
    """Наполняем базу тестовыми данными"""
    def handle(self, *args, **options):
        Element.objects.all().delete()
        Version.objects.all().delete()
        Refbook.objects.all().delete()

        # сбрасываем счетчики
        update_sqlite_table("""UPDATE sqlite_sequence SET seq = 0 WHERE name = 'main_element'""")
        update_sqlite_table("""UPDATE sqlite_sequence SET seq = 0 WHERE name = 'main_version'""")
        update_sqlite_table("""UPDATE sqlite_sequence SET seq = 0 WHERE name = 'main_refbook'""")

        letters = 'ABCDEFGH'
        digits = '12345678'
        llist = list('ABCDEabcde')
        for x in letters:
            for y in digits:
                random.shuffle(llist)
                code = x + y
                rb = Refbook(code=code, name='классификатор', description=''.join(llist))
                rb.save()
                for z in range(1, random.randrange(2, 11)):
                    if code == 'A1':  # пусть у справочника A1 не будет версий...
                        continue
                    num = code + str(z)
                    v = Version(refbook=rb, num=num, date_start=date.today() - timedelta(z))
                    v.save()
                    for e in range(1, random.randrange(2, 11)):
                        if num == 'B11':  # ...а у версии B11 не будет элементов
                            continue
                        ecode = num + str(e)
                        Element(version=v, code=ecode, value=ecode.lower()).save()
