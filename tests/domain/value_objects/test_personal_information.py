"""Module related with personal information tests."""
import pytest
from pydantic import ValidationError

from domain.types.personal_age import PersonalAge
from domain.types.personal_name import PersonalName
from domain.value_objects.personal_information import PersonalInformation


def test_personal_information_correct_validation(personal_information_1: PersonalInformation):
    """Personal information correct validation"""
    assert personal_information_1.age == 0  # FIXME: it is correct until types will be implemented correctly.
    assert personal_information_1.name == "Alex"  # FIXME: it is correct until types will be implemented correctly.


def test_personal_information_invalid_age():
    """Test with invalid age. Note this test should be removed when Annotations will be replaced by Classes."""
    with pytest.raises(ValidationError):
        PersonalInformation(
            age=PersonalAge(-1),
            name=PersonalName("Alex")
        )


def test_personal_information_invalid_name():
    """Test with invalid name. Note this test should be removed when Annotations will be replaced by Classes."""
    with pytest.raises(ValidationError):
        PersonalInformation(
            age=PersonalAge(0),
            name=PersonalName("")
        )