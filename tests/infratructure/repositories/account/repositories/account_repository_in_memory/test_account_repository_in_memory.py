"""Module related with AccountRepositoryInMemory tests"""
import asyncio

import pytest

from domain.aggregates.account import Account
from domain.types.pagination_page import PaginationPage
from domain.types.pagination_size import PaginationSize
from domain.types.personal_age import PersonalAge
from domain.types.personal_name import PersonalName
from domain.types.user_id import UserId
from domain.value_objects.pagination import Pagination
from domain.value_objects.personal_information import PersonalInformation
from infrastructure.repositories.account.exceptions.account_not_found_error import AccountNotFoundError
from infrastructure.repositories.account.interface import AccountRepositoryInterface
from infrastructure.repositories.account.repositories.account_repository_in_memory.repository import \
    AccountRepositoryInMemory


@pytest.fixture
async def account_repository(account_1: Account, account_2: Account, account_3: Account) -> AccountRepositoryInterface:
    """Account AccountRepositoryInMemory fixture."""
    repo = AccountRepositoryInMemory()

    # Note: not use gather. It is required that in all cases should be created in order. Only applies on testing cases.
    await repo.create_account(account_1)
    await repo.create_account(account_2)
    await repo.create_account(account_3)
    await repo.create_account(account_1)

    return repo


async def test_account_repository_in_memory_create(account_1: Account):
    """Test AccountRepositoryInMemory creation workflow."""
    repo = AccountRepositoryInMemory()
    await repo.create_account(account_1)

    account = await repo.get_account(UserId(0))

    assert account.user.id == 0
    assert account_1.user.id == 0
    assert account.user.personal_information == account_1.user.personal_information


async def test_account_repository_in_memory_get(account_repository: AccountRepositoryInterface, account_2: Account):
    """Test repository get workflow."""
    account = await account_repository.get_account(UserId(1))
    assert account.user.personal_information == account_2.user.personal_information


async def test_account_repository_in_memory_get_not_found(account_repository: AccountRepositoryInterface):
    """Test repository get workflow with a missing account."""

    with pytest.raises(AccountNotFoundError):
        await account_repository.get_account(UserId(-1))


async def test_account_repository_in_memory_list(account_repository: AccountRepositoryInterface, account_1: Account,
                                                 account_3: Account):
    """Test repository list workflow."""
    accounts = await account_repository.get_accounts(Pagination(size=PaginationSize(2), page=PaginationPage(1)))

    assert len(accounts) == 2
    assert accounts[0].user.personal_information == account_3.user.personal_information
    assert accounts[1].user.personal_information == account_1.user.personal_information


async def test_account_repository_in_memory_patch(account_repository: AccountRepositoryInterface, account_1: Account):
    """Test repository patch workflow."""
    personal_information = PersonalInformation(
        age=PersonalAge(99),
        name=PersonalName("test")
    )

    account_1.user.personal_information = personal_information
    account_resp = await account_repository.patch_account(account_1)

    account = await account_repository.get_account(account_1.user.id)

    assert account.user.personal_information.name == 'test'
    assert account.user.personal_information.age == PersonalAge(99)
    assert account_resp.user.personal_information.name == "test"
    assert account_resp.user.personal_information.age == PersonalAge(99)


async def test_account_repository_in_memory_patch_not_found(account_repository: AccountRepositoryInterface,
                                                      account_1: Account):
    """Test repository patch workflow when account is not found."""
    account_1.user.id = UserId(-1)
    with pytest.raises(AccountNotFoundError):
        await account_repository.patch_account(account_1)


async def test_account_repository_in_memory_delete(account_repository: AccountRepositoryInterface):
    """Test repository delete workflow."""
    accounts_past = await account_repository.get_accounts(Pagination(size=PaginationSize(999), page=PaginationPage(0)))

    await account_repository.delete_account(UserId(1))
    accounts_present = await account_repository.get_accounts(Pagination(size=PaginationSize(999), page=PaginationPage(0)))
    assert len(accounts_past) == 4
    assert len(accounts_present) == 3
    with pytest.raises(AccountNotFoundError):
        await account_repository.get_account(UserId(1))


async def test_account_repository_in_memory_delete_not_found(account_repository: AccountRepositoryInterface):
    """Test repository delete workflow when account is not found."""
    with pytest.raises(AccountNotFoundError):
        await account_repository.delete_account(UserId(-1))
