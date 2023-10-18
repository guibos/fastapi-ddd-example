"""Module related with pagination tests."""
import pytest
from pydantic import ValidationError

from domain.value_objects.pagination import Pagination
from domain.types.pagination_page import PaginationPage
from domain.types.pagination_size import PaginationSize


def test_pagination_correct_validation():
    """Test with correct validation"""

    pagination = Pagination(page=PaginationPage(0), size=PaginationSize(1))
    assert pagination.page == 0  # FIXME: it is correct until types will be implemented correctly.
    assert pagination.size == 1  # FIXME: it is correct until types will be implemented correctly.


def test_pagination_invalid_pagination_page():
    """Test with invalid pagination page. Note this test should be removed when Annotations will be replaced by Classes.
    """

    with pytest.raises(ValidationError):
        Pagination(page=PaginationPage(-1), size=PaginationSize(1))


def test_pagination_invalid_pagination_size():
    """Test with invalid pagination size. Note this test should be removed when Annotations will be replaced by Classes.
    """

    with pytest.raises(ValidationError):
        Pagination(page=PaginationPage(0), size=PaginationSize(0))
