from typing import List

from pydantic import  TypeAdapter
from starlette.testclient import TestClient

from domain.aggregates.account import Account
from domain.types.personal_age import PersonalAge
from domain.types.personal_name import PersonalName
from domain.value_objects.personal_information import PersonalInformation


def test_get(test_client: TestClient, account_1: Account):
    account = Account.model_validate_json(test_client.get('/api/account/0').content)

    assert account.user.personal_information == account_1.user.personal_information


def test_get_404(test_client: TestClient):
    assert test_client.get('/api/account/-1').status_code == 404


def test_list(test_client: TestClient, account_1: Account, account_2: Account, account_3: Account ):
    validator = TypeAdapter(List[Account])
    accounts = validator.validate_python(test_client.get('/api/account/?page=0&size=3').json())

    for api, mock in zip(accounts, [account_1, account_2, account_3]):
        assert api.user.personal_information == mock.user.personal_information


def test_list_overflow(test_client: TestClient, account_1: Account, account_2: Account, account_3: Account ):
    validator = TypeAdapter(List[Account])
    accounts = validator.validate_python(test_client.get('/api/account/?page=1&size=2').json())

    for api, mock in zip(accounts, [account_3]):
        assert api.user.personal_information == mock.user.personal_information


def test_create(test_client: TestClient, account_1: Account):
    data = account_1.model_dump()
    create = Account.model_validate_json(test_client.post('/api/account/', json=data).content)

    get = Account.model_validate_json(test_client.get(f'/api/account/{create.user.id}').content)

    assert create == get
    assert create.user.personal_information == account_1.user.personal_information


def test_patch(test_client: TestClient, account_1: Account):
    personal_information = PersonalInformation(name=PersonalName("patched"), age=PersonalAge(1))
    account_1.user.personal_information = personal_information

    patch = Account.model_validate(test_client.patch('/api/account/0', json=account_1.model_dump()).json())
    get = Account.model_validate(test_client.get('/api/account/0').json())
    assert patch == get
    assert get.user.personal_information == personal_information


def test_patch(test_client: TestClient, account_1: Account):
    personal_information = PersonalInformation(name=PersonalName("patched"), age=PersonalAge(1))
    account_1.user.personal_information = personal_information

    assert test_client.patch('/api/account/-1', json=account_1.model_dump()).status_code == 404


def test_delete(test_client: TestClient):
    validator = TypeAdapter(List[Account])
    accounts_pre = validator.validate_python(test_client.get('/api/account/?page=0&size=9999').json())
    test_client.delete('/api/account/0')
    accounts_post = validator.validate_python(test_client.get('/api/account/?page=0&size=9999').json())

    assert len(accounts_pre) == 4
    assert len(accounts_post) == 3


def test_delete_404(test_client: TestClient):
    assert test_client.delete('/api/account/-1').status_code == 404



