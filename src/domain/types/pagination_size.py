from typing import Annotated

from pydantic import Field

# TODO: Implement: https://docs.pydantic.dev/latest/concepts/types/#handling-third-party-types
PaginationSize = Annotated[int, Field(gt=0)]
