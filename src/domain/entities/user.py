from typing import Optional

from domain.entities.user_creation import UserCreation
from domain.types.user_id import UserId


class User(UserCreation):
    """Root entity."""
    id: Optional[UserId]
