from pydantic import BaseModel, ConfigDict

from domain.value_objects.personal_information import PersonalInformation


class UserCreation(BaseModel):
    model_config = ConfigDict(extra='forbid')

    personal_information: PersonalInformation
