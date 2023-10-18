"""Accounts views."""
from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import ValidationError

from application.services.account_service import AccountService
from domain.aggregates.account import Account
from domain.types.pagination_page import PaginationPage
from domain.types.pagination_size import PaginationSize
from domain.types.user_id import UserId
from domain.value_objects.pagination import Pagination
from infrastructure.repositories.account.exceptions.account_not_found_error import AccountNotFoundError
from infrastructure.repositories.account.repositories.account_repository_in_memory.repository import \
    AccountRepositoryInMemory

accounts_router = APIRouter(prefix='/api/account', tags=['accounts'])
_ACCOUNT_SERVICE = AccountService(AccountRepositoryInMemory())


async def account_service_callable() -> AccountService:
    return _ACCOUNT_SERVICE


@accounts_router.post('/', response_model=Account)
async def _create_account(account_service: Annotated[AccountService, Depends(account_service_callable)],
                          account: Annotated[Account, Body()]):
    account = await account_service.create_account(account)
    return account


@accounts_router.get('/', response_model=List[Account])
async def _get_accounts(account_service: Annotated[AccountService, Depends(account_service_callable)], size: int = 100,
                        page: int = 0):
    """Returns accounts of the system in function of pagination."""
    # TODO: Pagination values should be classes and not an annotations. It should have his own domain.
    try:
        pagination = Pagination(size=PaginationSize(size), page=PaginationPage(page))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return await account_service.get_accounts(pagination)


@accounts_router.get('/{user_id}', response_model=Account)
async def _get_account(account_service: Annotated[AccountService, Depends(account_service_callable)], user_id: int):
    # TODO: user_id value should be a class and not an annotation. It should have his own domain.
    try:
        data = await account_service.get_account(UserId(user_id))
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return data


@accounts_router.patch('/{user_id}', response_model=Account)
async def _patch_account(account_service: Annotated[AccountService, Depends(account_service_callable)],
                          account: Annotated[Account, Body()], user_id: int):
    account.user.id = user_id
    try:
        account = await account_service.patch_account(account)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return account


@accounts_router.delete('/{user_id}')
async def _delete_account(account_service: Annotated[AccountService, Depends(account_service_callable)],
                          user_id: int):
    try:
        await account_service.delete_account(UserId(user_id))
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return
