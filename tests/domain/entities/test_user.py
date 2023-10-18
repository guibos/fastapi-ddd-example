"""Module related with user entity tests."""
import pytest
from pydantic import ValidationError

from domain.entities.user import User
from domain.types.user_id import UserId
from domain.value_objects.personal_information import PersonalInformation


def test_user_correct_validation(user_1: User):
    """Correct user entity validation."""
    assert user_1.id == 0  # FIXME: it is correct until types will be implemented correctly.


def test_user_invalid_id(personal_information_1: PersonalInformation):
    """Correct user entity validation."""
    with pytest.raises(ValidationError):
        User(
            id=UserId(-1),
            personal_information=personal_information_1
        )
