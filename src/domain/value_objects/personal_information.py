from pydantic import BaseModel, ConfigDict

from domain.types.personal_age import PersonalAge
from domain.types.personal_name import PersonalName


class PersonalInformation(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    age: PersonalAge
    name: PersonalName
