from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from main.model.refbook import Refbook
from api.serializers import RefbookSerializer


refbooks_date_in_query_param = openapi.Parameter(
    'date',
    openapi.IN_QUERY,
    description="""Дата начала действия YYYY-MM-DD
    Если она указана, то запрос вернет только актуальные на эту дату Справочники
    т.е. Справочники, в которых имеются Версии с Датой начала действия <= `date`""",
    type=openapi.FORMAT_DATE,
    required=False,
)
refbooks_response_200 = openapi.Response(
    """При отсутствии `date` запрос вернет список refbooks, содержащий все Справочники.
    При наличии `date`- в возвращаемый список попадут только Справочники актуальные на эту дату;
    значение параметра `date` в этом случае будет содержаться в ответе""",
    RefbookSerializer,
    examples={
        "application/json": {
            "STATUS": "OK",
            "date": "2022-10-27",
            "refbooks": [
                {
                    "id": 1,
                    "code": "A1",
                    "name": "классификатор"
                },
                {
                    "id": 2,
                    "code": "A2",
                    "name": "классификатор"
                },
            ]
        },
    }
)
refbooks_response_400 = openapi.Response(
    """При наличии `date` значение в нем должно быть корректной датой /refbooks/?date=2022-12-32""",
    # RefbookSerializer,
    examples={
        "application/json": {
            "STATUS": "FAILED",
            "MESSAGE": "Invalid value of `date` parameter"
        },
    }
)


@swagger_auto_schema(
    method='get',
    manual_parameters=[refbooks_date_in_query_param],
    responses={
        200: refbooks_response_200,
        400: refbooks_response_400,
    },
)
@api_view(['GET', ])
def refbooks(request):
    if request.method == 'GET':
        http_request_status = HTTP_200_OK
        resp_dict = dict()
        if 'date' in request.GET:
            try:
                date_str = request.GET['date']
                datetime_object = datetime.strptime(date_str, '%Y-%m-%d')
                # выбираем только те Справочники в которых имеются Версии с Датой начала действия <= get-параметра date
                rbs = Refbook.objects.filter(version__date_start__lte=datetime_object.date()).distinct()
                resp_dict['STATUS'] = 'OK'
                resp_dict['date'] = date_str
            except ValueError:
                rbs = None
                http_request_status = HTTP_400_BAD_REQUEST
                resp_dict['STATUS'] = 'FAILED'
                resp_dict['MESSAGE'] = 'Invalid value of `date` parameter'  # сообщаем об ошибке
        else:
            resp_dict['STATUS'] = 'OK'
            rbs = Refbook.objects.all()  # если get-параметра date нет, то просто выбираем все записи

        if rbs is not None:
            serializer = RefbookSerializer(rbs, many=True)
            resp_dict['refbooks'] = serializer.data

        return Response(resp_dict, status=http_request_status)
