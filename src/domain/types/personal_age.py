from typing import Annotated

from pydantic import Field

# TODO: Implement: https://docs.pydantic.dev/latest/concepts/types/#handling-third-party-types
PersonalAge = Annotated[int, Field(ge=0)]
