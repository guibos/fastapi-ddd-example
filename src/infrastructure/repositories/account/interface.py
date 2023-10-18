import abc
from abc import ABC
from typing import List

from domain.aggregates.account import Account
from domain.types.user_id import UserId
from domain.value_objects.pagination import Pagination


class AccountRepositoryInterface(ABC):
    @abc.abstractmethod
    async def create_account(self, account: Account) -> Account:
        pass

    @abc.abstractmethod
    async def get_account(self, user_id: UserId) -> Account:
        pass

    @abc.abstractmethod
    async def get_accounts(self, pagination: Pagination) -> List[Account]:
        pass

    @abc.abstractmethod
    async def patch_account(self, account: Account) -> Account:
        pass

    @abc.abstractmethod
    async def delete_account(self, user_id: UserId) -> Account:
        pass
