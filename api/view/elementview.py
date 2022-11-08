from datetime import date

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from main.model.refbook import Refbook
from main.model.version import Version
from main.model.element import Element
from api.serializers import ElementSerializer


refbook_pk_param = openapi.Parameter(
    'refbook_pk',
    openapi.IN_PATH,
    description="""Идентификатор справочника""",
    type=openapi.TYPE_INTEGER,
)
version_in_query_param = openapi.Parameter(
    'version',
    openapi.IN_QUERY,
    description="""Версия справочника. Если не указана,
    то возвращаются элементы текущей версии. Текущей является та версия, дата начала действия которой
    позже всех остальных версий данного справочника, но не позже текущей даты""",
    type=openapi.TYPE_STRING,
    required=False,
)
refbook_elements_response_200 = openapi.Response(
    """При отсутствии `version` запрос возвращает список элементов `elements` текущей версии.
    При наличии `version`- возвращает `elements` только этой версии. Список `elements` может быть пустым.
    Ответ с кодом 200 содержит Идентификатор справочника `refbook_pk`, его Текущую версию `currentVersion_num`,
    список `elements` и Запрошенную версию `requestedVersion_num` если запрос содержал параметр `version`""",
    ElementSerializer,
    examples={
        "application/json": {
            "refbook_pk": 64,
            "currentVersion_num": "H81",
            "STATUS": "OK",
            "requestedVersion_num": "H86",
            "elements": [
                {
                    "code": "H861",
                    "value": "h861"
                },
                {
                    "code": "H862",
                    "value": "h862"
                },
            ]
        },
    }
)
refbook_elements_response_400 = openapi.Response(
    """Ответ с кодом 400 содержит Идентификатор справочника `refbook_pk`, и одно из трех сообщений `MESSAGE`:
    • "The key does not exist" означающее, что Справочника с кодом `refbook_pk` не существует
    • "The refbook has no versions" означающее, что Справочник `refbook_pk` существует, но у него нет ни одной версии
    • "Requested version does not exist" означающее Справочник `refbook_pk` существует у него есть версии,
    но среди них нет версии с номером `version`.
    В последнем случае ответ будет содержать еще два параметра: `currentVersion_num` и `requestedVersion_num`
    """,
    examples={
        "application/json": {
            "refbook_pk": 64,
            "currentVersion_num": "H81",
            "STATUS": "FAILED",
            "requestedVersion_num": "H89",
            "MESSAGE": "Requested version does not exist"
        },
    }
)


@swagger_auto_schema(
    method='get',
    manual_parameters=[refbook_pk_param, version_in_query_param],
    responses={
        200: refbook_elements_response_200,
        400: refbook_elements_response_400,
    },
)
@api_view(['GET', ])
def refbook_elements(request, refbook_pk):
    return rb_elements(request, refbook_pk)  # во втором контроллере вызывается эта же функция


def rb_elements(request, refbook_pk):
    if request.method == 'GET':
        http_request_status = HTTP_200_OK
        try:
            rb = Refbook.objects.get(pk=refbook_pk)
            resp_dict = dict()  # исключение не произошло, нужный объект справочника найден (и он единственный)
            resp_dict['refbook_pk'] = refbook_pk  # сохраняем его ключ
            # и вычисляем актуальную версию этого справочника, она понадобится в любом случае
            current_version = Version.objects\
                .filter(refbook__exact=rb).exclude(date_start__gt=date.today()).order_by('-date_start').first()
            if current_version:  # вернет либо None, либо единственный объект Version
                resp_dict['currentVersion_num'] = current_version.num  # сохраняем номер текущей версии
                # теперь можно попробовать найти версию, запрошенную в get-параметре ?version=<version>
                ver = current_version  # в конце будем выбирать элементы, относящиеся к ver
                resp_dict['STATUS'] = 'OK'
                if 'version' in request.GET:
                    resp_dict['requestedVersion_num'] = request.GET['version']
                    if resp_dict['requestedVersion_num'] != current_version.num:  # если запрошена не текущая версия...
                        requested_version = Version.objects\
                            .filter(refbook__exact=rb, num__exact=resp_dict['requestedVersion_num']).first()
                        if requested_version:  # если запись нашлась, то запоминаем ее
                            ver = requested_version
                        else:  # а если не нашлась, то меняем статус на FAILED
                            http_request_status = HTTP_400_BAD_REQUEST
                            resp_dict['STATUS'] = 'FAILED'
                            resp_dict['MESSAGE'] = 'Requested version does not exist'
                if resp_dict['STATUS'] == 'OK':
                    serializer = ElementSerializer(Element.objects.filter(version__exact=ver), many=True)
                    resp_dict['elements'] = serializer.data
            else:
                http_request_status = HTTP_400_BAD_REQUEST
                resp_dict['STATUS'] = 'FAILED'
                resp_dict['MESSAGE'] = 'The refbook has no versions'
        except Refbook.DoesNotExist:
            http_request_status = HTTP_400_BAD_REQUEST
            resp_dict = {'refbook_pk': refbook_pk, 'STATUS': 'FAILED', 'MESSAGE': 'The key does not exist'}
        return Response(resp_dict, status=http_request_status)


code_in_query_param = openapi.Parameter(
    'code',
    openapi.IN_QUERY,
    description="""Код элемента справочника""",
    type=openapi.TYPE_STRING,
    required=True,
)
value_in_query_param = openapi.Parameter(
    'value',
    openapi.IN_QUERY,
    description="""Значение элемента справочника""",
    type=openapi.TYPE_STRING,
    required=True,
)
refbook_check_element_response_200 = openapi.Response(
    """При наличии параметра `version` запрос выполнит поиск пары `code`+`value` в строках Справочника этой версии.
    При отсутствии параметра `version` поиск `code`+`value` выполнится в строках Справочника текущей версии.
    Если поиск пары увенчается успехом, то ответ будет содержать ключ "EXISTS": "YES", а если не увенчается, то "NO"
    Ответ 200 обязательно содержит поля: refbook_pk, currentVersion_num, requestedVersion_num, code, value и EXISTS
    """,
    ElementSerializer,
    examples={
        "application/json": {
            "refbook_pk": 2,
            "currentVersion_num": "A21",
            "STATUS": "OK",
            "requestedVersion_num": "A27",
            "code": "A271",
            "value": "a271",
            "EXISTS": "YES"
        },
    }
)
refbook_check_element_response_400 = openapi.Response(
    refbook_elements_response_400.description +
    '\nЕсли один из параметров `code` или `value` будет отсутствовать, то ответ будет выглядеть так' +
    '\n{"refbook_pk": 841, "STATUS": "FAILED", "MESSAGE": "Both params code and value must be set"}',
    examples=refbook_elements_response_400.examples,
)


@swagger_auto_schema(
    method='get',
    manual_parameters=[refbook_pk_param, code_in_query_param, value_in_query_param, version_in_query_param],
    responses={
       200: refbook_check_element_response_200,
       400: refbook_check_element_response_400,
    },
)
@api_view(['GET', ])
def refbook_check_element(request, refbook_pk):
    resp_dict = rb_elements(request, refbook_pk).data  # вызываем вспомогательную функцию, кот. сделает почти всю работу
    if resp_dict['STATUS'] == 'OK':
        http_request_status = HTTP_200_OK
        if ('code' in request.GET) and ('value' in request.GET):
            code_value_exists = False
            for el in resp_dict['elements']:
                if el['code'] == request.GET['code'] and el['value'] == request.GET['value']:
                    code_value_exists = True
                    break
            del resp_dict['elements']  # удаляем массив с элементами
            resp_dict['code'] = request.GET['code']
            resp_dict['value'] = request.GET['value']
            resp_dict['EXISTS'] = 'YES' if code_value_exists else 'NO'
            return Response(resp_dict, status=http_request_status)
        else:
            http_request_status = HTTP_400_BAD_REQUEST
            resp_dict = {'refbook_pk': refbook_pk, 'STATUS': 'FAILED',
                         'MESSAGE': 'Both params code and value must be set'}
            return Response(resp_dict, status=http_request_status)
    else:
        http_request_status = HTTP_400_BAD_REQUEST
        return Response(resp_dict, http_request_status)  # неуспешные сообщения возвращаем как есть
