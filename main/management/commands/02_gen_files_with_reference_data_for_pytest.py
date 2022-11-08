from django.core.management.base import BaseCommand
from datetime import date
import json
import os
import pathlib

from main.model.refbook import Refbook
from main.model.version import Version
from main.model.element import Element

class Command(BaseCommand):
    """"""
    def handle(self, *args, **options):
        reference_data_for_refbooks_with_date_request = []
        for d in Version.objects.values('date_start').distinct():  # цикл по датам появления новых версий
            refbooks = []  # здесь будут собираться справочники, которые были активными к моменту времени d
            for r in Refbook.objects.filter(version__date_start__lte=d['date_start']).distinct():
                refbooks.append((r.pk, r.code, r.name))
            reference_data_for_refbooks_with_date_request.append((d['date_start'].strftime('%Y-%m-%d'), refbooks))
            print(d['date_start'].strftime('%Y-%m-%d') + ' - ' + str(len(refbooks)))
        fname = os.path.join(
            os.path.join(
                os.path.join(pathlib.Path(__file__).resolve().parent.parent.parent.parent, 'api'),
                'test_data'),
            'reference_data_for_refbooks_with_date_request.json'
        )
        with open(fname, "w") as outfile:
            json.dump({'list': reference_data_for_refbooks_with_date_request}, outfile, indent=4)
        print(fname)

        """"""
        reference_data_for_refbooks_request = []
        refbooks = []  # здесь будут собираться все справочники
        for r in Refbook.objects.all():
            refbooks.append((r.pk, r.code, r.name))
        reference_data_for_refbooks_request.append(('2999-12-31', refbooks))
        print('2999-12-31 - ' + str(len(refbooks)))
        fname = os.path.join(
            os.path.join(
                os.path.join(pathlib.Path(__file__).resolve().parent.parent.parent.parent, 'api'),
                'test_data'),
            'reference_data_for_refbooks_request.json'
        )
        with open(fname, "w") as outfile:
            json.dump({'list': reference_data_for_refbooks_request}, outfile, indent=4)
        print(fname)

        """"""
        reference_data_for_elements_with_version = []
        for v in Version.objects.all():  # проходим по версиям
            r = v.refbook  # достаем справочник, к которому относится версия
            # вычисляем текущую версию этого справочника
            cv = Version.objects\
                .filter(refbook__exact=r).exclude(date_start__gt=date.today()).order_by('-date_start').first()
            elements = []
            for e in Element.objects.filter(version__exact=v):
                elements.append((e.code, e.value))
            reference_data_for_elements_with_version.append((r.pk, cv.num, v.num, elements))
            print(str(r.pk) + ' ' + cv.num + ' ' + v.num + ' - ' + str(len(elements)))
        fname = os.path.join(
            os.path.join(
                os.path.join(pathlib.Path(__file__).resolve().parent.parent.parent.parent, 'api'),
                'test_data'),
            'reference_data_for_elements_with_version_request.json'
        )
        with open(fname, "w") as outfile:
            json.dump({'list': reference_data_for_elements_with_version}, outfile, indent=4)
        print(fname)

        """"""
        reference_data_for_elements = []
        for v in Version.objects.all():  # проходим по версиям
            r = v.refbook  # достаем справочник, к которому относится версия
            # вычисляем текущую версию этого справочника
            cv = Version.objects\
                .filter(refbook__exact=r).exclude(date_start__gt=date.today()).order_by('-date_start').first()
            if v == cv:
                elements = []
                for e in Element.objects.filter(version__exact=v):
                    elements.append((e.code, e.value))
                reference_data_for_elements.append((r.pk, cv.num, elements))
                print(str(r.pk) + ' ' + cv.num + ' - ' + str(len(elements)))

        fname = os.path.join(
            os.path.join(
                os.path.join(pathlib.Path(__file__).resolve().parent.parent.parent.parent, 'api'),
                'test_data'),
            'reference_data_for_elements_request.json'
        )
        with open(fname, "w") as outfile:
            json.dump({'list': reference_data_for_elements}, outfile, indent=4)
        print(fname)

        """"""
        reference_data_for_check_element_with_version = []
        for v in Version.objects.all():  # проходим по версиям
            r = v.refbook  # достаем справочник, к которому относится версия
            # вычисляем текущую версию этого справочника
            cv = Version.objects\
                .filter(refbook__exact=r).exclude(date_start__gt=date.today()).order_by('-date_start').first()
            for e in Element.objects.filter(version__exact=v):
                reference_data_for_check_element_with_version.append((r.pk, cv.num, v.num, e.code, e.value))
                print(r.pk, cv.num, v.num, e.code, e.value)
        fname = os.path.join(
            os.path.join(
                os.path.join(pathlib.Path(__file__).resolve().parent.parent.parent.parent, 'api'),
                'test_data'),
            'reference_data_for_check_element_with_version_request.json'
        )
        with open(fname, "w") as outfile:
            json.dump({'list': reference_data_for_check_element_with_version}, outfile, indent=4)
        print(fname)

        """"""
        reference_data_for_check_element = []
        for v in Version.objects.all():  # проходим по версиям
            r = v.refbook  # достаем справочник, к которому относится версия
            # вычисляем текущую версию этого справочника
            cv = Version.objects\
                .filter(refbook__exact=r).exclude(date_start__gt=date.today()).order_by('-date_start').first()
            if cv == v:
                for e in Element.objects.filter(version__exact=v):
                    reference_data_for_check_element.append((r.pk, cv.num, e.code, e.value))
                    print(r.pk, cv.num, e.code, e.value)
        fname = os.path.join(
            os.path.join(
                os.path.join(pathlib.Path(__file__).resolve().parent.parent.parent.parent, 'api'),
                'test_data'),
            'reference_data_for_check_element_request.json'
        )
        with open(fname, "w") as outfile:
            json.dump({'list': reference_data_for_check_element}, outfile, indent=4)
        print(fname)
