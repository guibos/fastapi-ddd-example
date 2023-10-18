from typing import List

from domain.aggregates.account import Account
from domain.types.user_id import UserId
from domain.value_objects.pagination import Pagination
from infrastructure.repositories.account.interface import AccountRepositoryInterface


class AccountService:
    def __init__(self, account_repository: AccountRepositoryInterface):
        self._account_repository = account_repository

    async def create_account(self, account_aggregation: Account) -> Account:
        return await self._account_repository.create_account(account_aggregation)

    async def get_account(self, user_id: UserId) -> Account:
        return await self._account_repository.get_account(user_id)

    async def get_accounts(self, pagination: Pagination) -> List[Account]:
        return await self._account_repository.get_accounts(pagination)

    async def patch_account(self, account_aggregation: Account) -> Account:
        return await self._account_repository.patch_account(account_aggregation)

    async def delete_account(self, user_id: UserId):
        await self._account_repository.delete_account(user_id)
