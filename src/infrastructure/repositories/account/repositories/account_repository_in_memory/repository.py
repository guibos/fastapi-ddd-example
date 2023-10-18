from itertools import count
from typing import Dict, List, Union

from domain.aggregates.account import Account
from domain.entities.user import User
from domain.types.personal_age import PersonalAge
from domain.types.personal_name import PersonalName
from domain.types.user_id import UserId
from domain.value_objects.pagination import Pagination
from domain.value_objects.personal_information import PersonalInformation
from infrastructure.repositories.account.exceptions.account_not_found_error import AccountNotFoundError
from infrastructure.repositories.account.interface import AccountRepositoryInterface
from infrastructure.repositories.account.repositories.account_repository_in_memory.alias import ItemData


class AccountRepositoryInMemory(AccountRepositoryInterface):
    _USER_ID_FIELD_NAME = 'id'
    _USER_NAME_FIELD_NAME = 'name'
    _USER_AGE_FIELD_NAME = 'age'

    def __init__(self):
        self._counter = count()
        self._data: List[Dict[str, Union[str, int]]] = []

    async def create_account(self, account_aggregate: Account) -> Account:
        account_aggregate.user.id = self._counter.__next__()
        self._data.append(self._aggregate_to_dict_factory(account_aggregate))
        return account_aggregate

    async def get_account(self, user_id: UserId) -> Account:
        user_data = await self._find_user_data(user_id)
        return self._dict_to_aggregate_factory(user_data)

    async def get_accounts(self, pagination: Pagination) -> List[Account]:
        start = pagination.page * pagination.size
        end = start + pagination.size
        return [self._dict_to_aggregate_factory(user_data) for user_data in self._data[start:end]]

    async def delete_account(self, user_id: UserId):
        index = await self._find_user_index(user_id)
        self._data.pop(index)

    async def patch_account(self, account_aggregate: Account) -> Account:
        index = await self._find_user_index(account_aggregate.user.id)
        self._data[index] = self._aggregate_to_dict_factory(account_aggregate)
        return account_aggregate

    async def _find_user_data(self, account_id: UserId) -> ItemData:
        try:
            return filter(lambda x: x[self._USER_ID_FIELD_NAME] == account_id, self._data).__next__()
        except StopIteration:
            raise AccountNotFoundError(f"Account with id {account_id} is not found.")

    async def _find_user_index(self, account_id: UserId) -> int:
        try:
            index, _ = filter(lambda x: x[1][self._USER_ID_FIELD_NAME] == account_id, enumerate(self._data)).__next__()
        except StopIteration:
            raise AccountNotFoundError(f"Account with id {account_id} is not found.")
        return index

    def _dict_to_aggregate_factory(self, user_data: ItemData) -> Account:
        return Account(
            user=User(
                id=user_data[self._USER_ID_FIELD_NAME],
                personal_information=PersonalInformation(
                    age=PersonalAge(user_data[self._USER_AGE_FIELD_NAME]),
                    name=PersonalName(user_data[self._USER_NAME_FIELD_NAME])
                )
            )
        )

    def _aggregate_to_dict_factory(self, account_aggregate: Account) -> ItemData:
        return {
            self._USER_ID_FIELD_NAME: account_aggregate.user.id,
            self._USER_NAME_FIELD_NAME: account_aggregate.user.personal_information.name,
            self._USER_AGE_FIELD_NAME: account_aggregate.user.personal_information.age
        }
