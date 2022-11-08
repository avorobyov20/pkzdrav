from django.urls import path
from .view.elementview import refbook_elements, refbook_check_element
from .view.refbookview import refbooks

urlpatterns = [
    # 2.4.3 Валидация элементов
    # GET refbooks/<id>/check_element?code=<code>&value=<value>[&version=<version>]
    path('refbooks/<int:refbook_pk>/check_element/', refbook_check_element),

    # 2.4.2. Получение элементов заданного справочника
    # GET refbooks/<id>/elements[?version=<version>]
    path('refbooks/<int:refbook_pk>/elements/', refbook_elements),

    # 2.4.1. Получение списка справочников [актуальных на указанную дату]
    # GET refbooks/[?date=ГГГГ-ММ-ДД]  Если указана, то должны возвратиться только те справочники,
    # в которых имеются Версии с Датой начала действия раннее или равной указанной
    path('refbooks/', refbooks),
]
