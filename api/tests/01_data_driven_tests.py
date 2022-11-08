import requests
import pytest
import json
import os
import pathlib


def read_test_data_from_json_file(fname):
    """Вспомогательная функция. Помещает данные из json-файла в список,
    которым будут пользоваться все data-driven тесты"""
    jsonfile = open(os.path.join(os.path.join(pathlib.Path(__file__).resolve().parent.parent, 'test_data'), fname))
    test_data = json.load(jsonfile)
    jsonfile.close()
    return test_data['list']


@pytest.mark.parametrize("date, refbooks",
                         read_test_data_from_json_file('reference_data_for_refbooks_with_date_request.json'))
def test_refbooks_with_date_param(date, refbooks):
    response = requests.get(f'http://127.0.0.1:8000/refbooks/?date={date}')
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["STATUS"] == "OK"
    assert response_body["date"] == date
    assert len(response_body["refbooks"]) == len(refbooks)
    for r1 in response_body["refbooks"]:  # переходим к сравнению элементов
        r1_in_refbooks_flag = False
        for r2 in refbooks:
            if r1['id'] == r2[0] and r1['code'] == r2[1] and r1['name'] == r2[2]:
                r1_in_refbooks_flag = True  # элемент найден
                break
        # все элементы, которые вернет запрос должны присутствовать в тестовой выборке
        assert r1_in_refbooks_flag


@pytest.mark.parametrize("date, refbooks",
                         read_test_data_from_json_file('reference_data_for_refbooks_request.json'))
def test_refbooks(date, refbooks):  # переменная date в reference-файле равна 2999-12-31 и не влияет на выборку
    response = requests.get(f'http://127.0.0.1:8000/refbooks/')
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["STATUS"] == "OK"
    assert len(response_body["refbooks"]) == len(refbooks)
    for r1 in response_body["refbooks"]:  # переходим к сравнению элементов
        r1_in_refbooks_flag = False
        for r2 in refbooks:
            if r1['id'] == r2[0] and r1['code'] == r2[1] and r1['name'] == r2[2]:
                r1_in_refbooks_flag = True  # элемент найден
                break
        # все элементы, которые вернет запрос должны присутствовать в тестовой выборке
        assert r1_in_refbooks_flag


def test_refbooks_with_invalid_date_param():
    response = requests.get(f'http://127.0.0.1:8000/refbooks/?date=2022-12-32')  # 32 декабря
    response_body = response.json()
    assert response.status_code == 400
    assert response_body["STATUS"] == "FAILED"
    assert response_body["MESSAGE"] == "Invalid value of `date` parameter"


def test_elements_with_invalid_refbook_pk_param():
    response = requests.get('http://127.0.0.1:8000/refbooks/9999999999/elements')
    response_body = response.json()
    assert response.status_code == 400
    assert response_body["STATUS"] == "FAILED"
    assert response_body["refbook_pk"] == 9999999999
    assert response_body["MESSAGE"] == "The key does not exist"


def test_elements_refbook_has_no_versions():
    response = requests.get('http://127.0.0.1:8000/refbooks/1/elements?version=A11')
    response_body = response.json()
    assert response.status_code == 400
    assert response_body["STATUS"] == "FAILED"
    assert response_body["refbook_pk"] == 1  # у этого справочника вообще не существует версий
    assert response_body["MESSAGE"] == "The refbook has no versions"


def test_elements_with_invalid_version_param():
    response = requests.get('http://127.0.0.1:8000/refbooks/2/elements?version=A999')
    response_body = response.json()
    assert response.status_code == 400
    assert response_body["STATUS"] == "FAILED"
    assert response_body["refbook_pk"] == 2
    assert response_body["requestedVersion_num"] == "A999"
    assert response_body["MESSAGE"] == "Requested version does not exist"


@pytest.mark.parametrize("refbook_pk, currentversion_num, requestedversion_num, elements",
                         read_test_data_from_json_file('reference_data_for_elements_with_version_request.json'))
def test_elements_with_version_param(refbook_pk, currentversion_num, requestedversion_num, elements):
    response = requests.get(f'http://127.0.0.1:8000/refbooks/{refbook_pk}/elements?version={requestedversion_num}')
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["STATUS"] == "OK"
    assert response_body["refbook_pk"] == refbook_pk
    assert response_body["currentVersion_num"] == currentversion_num
    assert response_body["requestedVersion_num"] == requestedversion_num
    assert len(response_body["elements"]) == len(elements)
    for e1 in response_body["elements"]:  # переходим к сравнению элементов
        e1_in_elements_flag = False
        for e2 in elements:
            if e1['code'] == e2[0] and e1['value'] == e2[1]:
                e1_in_elements_flag = True  # элемент найден
                break
        # все элементы, которые вернет запрос должны присутствовать в тестовой выборке
        assert e1_in_elements_flag


@pytest.mark.parametrize("refbook_pk, currentversion_num, elements",
                         read_test_data_from_json_file('reference_data_for_elements_request.json'))
def test_elements(refbook_pk, currentversion_num, elements):
    response = requests.get(f'http://127.0.0.1:8000/refbooks/{refbook_pk}/elements')
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["STATUS"] == "OK"
    assert response_body["refbook_pk"] == refbook_pk
    assert response_body["currentVersion_num"] == currentversion_num
    assert len(response_body["elements"]) == len(elements)
    for e1 in response_body["elements"]:  # переходим к сравнению элементов
        e1_in_elements_flag = False
        for e2 in elements:
            if e1['code'] == e2[0] and e1['value'] == e2[1]:
                e1_in_elements_flag = True  # элемент найден
                break
        # все элементы, которые вернет запрос должны присутствовать в тестовой выборке
        assert e1_in_elements_flag


@pytest.mark.parametrize("refbook_pk, currentversion_num, requestedversion_num, code, value",
                         read_test_data_from_json_file('reference_data_for_check_element_with_version_request.json'))
def test_check_element_with_version_param_exists_yes(refbook_pk, currentversion_num, requestedversion_num, code, value):
    response = requests.get(
        'http://127.0.0.1:8000/' +
        f'refbooks/{refbook_pk}/check_element/?code={code}&value={value}&version={requestedversion_num}'
    )
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["STATUS"] == "OK"
    assert response_body["refbook_pk"] == refbook_pk
    assert response_body["currentVersion_num"] == currentversion_num
    assert response_body["requestedVersion_num"] == requestedversion_num
    assert response_body["code"] == code
    assert response_body["value"] == value
    assert response_body["EXISTS"] == "YES"


@pytest.mark.parametrize("refbook_pk, currentversion_num, requestedversion_num, code, value",
                         read_test_data_from_json_file('reference_data_for_check_element_with_version_request.json'))
def test_check_element_with_version_param_exists_no(refbook_pk, currentversion_num, requestedversion_num, code, value):
    response = requests.get(
        'http://127.0.0.1:8000/' +
        f'refbooks/{refbook_pk}/check_element/?code={code}&value={value}x&version={requestedversion_num}'
    )
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["STATUS"] == "OK"
    assert response_body["refbook_pk"] == refbook_pk
    assert response_body["currentVersion_num"] == currentversion_num
    assert response_body["requestedVersion_num"] == requestedversion_num
    assert response_body["code"] == code
    assert response_body["value"] == value + 'x'
    assert response_body["EXISTS"] == "NO"


@pytest.mark.parametrize("refbook_pk, currentversion_num, code, value",
                         read_test_data_from_json_file('reference_data_for_check_element_request.json'))
def test_check_element_exists_yes(refbook_pk, currentversion_num, code, value):
    response = requests.get(
        'http://127.0.0.1:8000/' +
        f'refbooks/{refbook_pk}/check_element/?code={code}&value={value}'
    )
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["STATUS"] == "OK"
    assert response_body["refbook_pk"] == refbook_pk
    assert response_body["currentVersion_num"] == currentversion_num
    assert response_body["code"] == code
    assert response_body["value"] == value
    assert response_body["EXISTS"] == "YES"


@pytest.mark.parametrize("refbook_pk, currentversion_num, code, value",
                         read_test_data_from_json_file('reference_data_for_check_element_request.json'))
def test_check_element_exists_no(refbook_pk, currentversion_num, code, value):
    response = requests.get(
        'http://127.0.0.1:8000/' +
        f'refbooks/{refbook_pk}/check_element/?code={code}&value={value}x'
    )
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["STATUS"] == "OK"
    assert response_body["refbook_pk"] == refbook_pk
    assert response_body["currentVersion_num"] == currentversion_num
    assert response_body["code"] == code
    assert response_body["value"] == value + 'x'
    assert response_body["EXISTS"] == "NO"


def test_check_element_with_invalid_refbook_pk_param():
    response = requests.get('http://127.0.0.1:8000/refbooks/9999999999/check_element/?code=A211&value=a211')
    response_body = response.json()
    assert response.status_code == 400
    assert response_body["STATUS"] == "FAILED"
    assert response_body["refbook_pk"] == 9999999999
    assert response_body["MESSAGE"] == "The key does not exist"


def test_check_element_refbook_has_no_versions():
    response = requests.get('http://127.0.0.1:8000/refbooks/1/check_element/?code=A111&value=a111')
    response_body = response.json()
    assert response.status_code == 400
    assert response_body["STATUS"] == "FAILED"
    assert response_body["refbook_pk"] == 1  # у этого справочника вообще не существует версий
    assert response_body["MESSAGE"] == "The refbook has no versions"


def test_check_element_with_invalid_version_param():
    response = requests.get('http://127.0.0.1:8000/refbooks/2/check_element/?code=A211&value=a211&version=A999')
    response_body = response.json()
    assert response.status_code == 400
    assert response_body["STATUS"] == "FAILED"
    assert response_body["refbook_pk"] == 2
    assert response_body["requestedVersion_num"] == "A999"
    assert response_body["MESSAGE"] == "Requested version does not exist"


def test_check_element_without_code_param():
    response = requests.get('http://127.0.0.1:8000/refbooks/10/check_element/?value=b211&version=B21')
    response_body = response.json()
    assert response.status_code == 400
    assert response_body["STATUS"] == "FAILED"
    assert response_body["refbook_pk"] == 10
    assert response_body["MESSAGE"] == "Both params code and value must be set"


def test_check_element_without_value_param():
    response = requests.get('http://127.0.0.1:8000/refbooks/10/check_element/?code=B211&version=B21')
    response_body = response.json()
    assert response.status_code == 400
    assert response_body["STATUS"] == "FAILED"
    assert response_body["refbook_pk"] == 10
    assert response_body["MESSAGE"] == "Both params code and value must be set"
