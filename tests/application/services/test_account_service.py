"""Module related with Account service tests"""

import pytest

from application.services.account_service import AccountService
from domain.aggregates.account import Account
from domain.types.pagination_page import PaginationPage
from domain.types.pagination_size import PaginationSize
from domain.types.personal_age import PersonalAge
from domain.types.personal_name import PersonalName
from domain.types.user_id import UserId
from domain.value_objects.pagination import Pagination
from domain.value_objects.personal_information import PersonalInformation
from infrastructure.repositories.account.exceptions.account_not_found_error import AccountNotFoundError


async def test_account_service_in_memory_create(account_service_mock: AccountService, account_1: Account):
    """Test account service creation workflow."""
    await account_service_mock.create_account(account_1)

    account = await account_service_mock.get_account(UserId(0))

    assert account.user.id == 0
    assert account_1.user.id == 4
    assert account.user.personal_information == account_1.user.personal_information


async def test_account_service_in_memory_get(account_service_mock: AccountService, account_3: Account):
    """Test service get workflow."""
    account = await account_service_mock.get_account(UserId(2))
    assert account.user.personal_information == account_3.user.personal_information


async def test_account_service_in_memory_get_not_found(account_service_mock: AccountService):
    """Test service get workflow with a missing account."""

    with pytest.raises(AccountNotFoundError):
        await account_service_mock.get_account(UserId(-1))


async def test_account_service_in_memory_list(account_service_mock: AccountService, account_1: Account,
                                                 account_3: Account):
    """Test service list workflow."""
    accounts = await account_service_mock.get_accounts(Pagination(size=PaginationSize(2), page=PaginationPage(1)))

    assert len(accounts) == 2
    assert accounts[0].user.personal_information == account_3.user.personal_information
    assert accounts[1].user.personal_information == account_1.user.personal_information


async def test_account_service_in_memory_patch(account_service_mock: AccountService, account_1: Account):
    """Test service patch workflow."""
    personal_information = PersonalInformation(
        age=PersonalAge(99),
        name=PersonalName("test")
    )

    account_1.user.personal_information = personal_information
    account_resp = await account_service_mock.patch_account(account_1)

    account = await account_service_mock.get_account(account_1.user.id)

    assert account.user.personal_information.name == 'test'
    assert account.user.personal_information.age == PersonalAge(99)
    assert account_resp.user.personal_information.name == "test"
    assert account_resp.user.personal_information.age == PersonalAge(99)


async def test_account_service_in_memory_patch_not_found(account_service_mock: AccountService,
                                                         account_1: Account):
    """Test service patch workflow when account is not found."""
    account_1.user.id = UserId(-1)
    with pytest.raises(AccountNotFoundError):
        await account_service_mock.patch_account(account_1)


async def test_account_service_in_memory_delete(account_service_mock: AccountService):
    """Test service delete workflow."""
    accounts_past = await account_service_mock.get_accounts(Pagination(size=PaginationSize(999), page=PaginationPage(0)))

    await account_service_mock.delete_account(UserId(1))
    accounts_present = await account_service_mock.get_accounts(Pagination(size=PaginationSize(999), page=PaginationPage(0)))
    assert len(accounts_past) == 4
    assert len(accounts_present) == 3
    with pytest.raises(AccountNotFoundError):
        await account_service_mock.get_account(UserId(1))


async def test_account_service_in_memory_delete_not_found(account_service_mock: AccountService):
    """Test service delete workflow when account is not found."""
    with pytest.raises(AccountNotFoundError):
        await account_service_mock.delete_account(UserId(-1))
