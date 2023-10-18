from pydantic import BaseModel, ConfigDict

from domain.types.pagination_page import PaginationPage
from domain.types.pagination_size import PaginationSize


class Pagination(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    size: PaginationSize
    page: PaginationPage
