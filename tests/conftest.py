import pytest
from starlette.testclient import TestClient

from application.services.account_service import AccountService
from application.use_case.accounts.views import account_service_callable
from domain.aggregates.account import Account
from domain.entities.user import User
from domain.types.personal_age import PersonalAge
from domain.types.personal_name import PersonalName
from domain.types.user_id import UserId
from domain.value_objects.personal_information import PersonalInformation
from infrastructure.repositories.account.interface import AccountRepositoryInterface
from infrastructure.repositories.account.repositories.account_repository_in_memory.repository import \
    AccountRepositoryInMemory
from main import app


@pytest.fixture
def personal_information_1() -> PersonalInformation:
    return PersonalInformation(
        age=PersonalAge(0),
        name=PersonalName("Alex")
    )


@pytest.fixture
def user_1(personal_information_1: PersonalInformation):
    return User(
        id=UserId(0),
        personal_information=personal_information_1
    )


@pytest.fixture
def account_1(user_1: User) -> Account:
    return Account(user=user_1)


@pytest.fixture
def personal_information_2() -> PersonalInformation:
    return PersonalInformation(
        age=PersonalAge(0),
        name=PersonalName("Alex2")
    )


@pytest.fixture
def user_2(personal_information_2: PersonalInformation):
    return User(
        id=UserId(1),
        personal_information=personal_information_2
    )


@pytest.fixture
def account_2(user_2: User) -> Account:
    return Account(user=user_2)


@pytest.fixture
def personal_information_3() -> PersonalInformation:
    return PersonalInformation(
        age=PersonalAge(0),
        name=PersonalName("Alex3")
    )


@pytest.fixture
def user_3(personal_information_3: PersonalInformation):
    return User(
        id=UserId(2),
        personal_information=personal_information_3
    )


@pytest.fixture
def account_3(user_3: User) -> Account:
    return Account(user=user_3)


@pytest.fixture
async def account_repository_mock(account_1: Account, account_2: Account, account_3: Account) -> AccountRepositoryInterface:
    """InMemory repository could be perfectly our mock"""
    repo = AccountRepositoryInMemory()
    await repo.create_account(account_1)
    await repo.create_account(account_2)
    await repo.create_account(account_3)
    await repo.create_account(account_1)
    return repo


@pytest.fixture
async def account_service_mock(account_repository_mock: AccountRepositoryInterface) -> AccountService:
    """Account service with repository mocked."""
    return AccountService(account_repository_mock)


@pytest.fixture
async def test_client(account_1: Account, account_2, account_3, account_service_mock) -> TestClient:
    def call():
        return account_service_mock

    client = TestClient(app)
    app.dependency_overrides[account_service_callable] = call
    return client
