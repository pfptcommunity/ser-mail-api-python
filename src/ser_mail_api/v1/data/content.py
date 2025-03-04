from __future__ import annotations

import json
from enum import Enum
from typing import Dict


class ContentType(Enum):
    """Enumeration for content types."""
    Text = "text/plain"
    Html = "text/html"


class Content:
    """Represents immutable content with a body and type.

    Use this class directly via constructor; attributes are read-only via properties.
    """

    def __init__(self, body: str, content_type: ContentType):
        """Initialize the Content object with a body and content type.

        Args:
            body (str): The content body.
            content_type (ContentType): The type of content (Text or Html).

        Raises:
            TypeError: If body is not a string or content_type is not a ContentType.
        """
        # Validate body and content_type types
        if not isinstance(body, str):
            raise TypeError(f"Expected 'body' to be a string, got {type(body).__name__}")
        if not isinstance(content_type, ContentType):
            raise TypeError(f"Expected 'content_type' to be a ContentType, got {type(content_type).__name__}")

        # Set attributes (intended to be immutable after initialization)
        self.__body = body
        self.__content_type = content_type

    @property
    def body(self) -> str:
        """Get the content body.

        Returns:
            str: The content body.
        """
        return self.__body

    @property
    def type(self) -> ContentType:
        """Get the content type.

        Returns:
            ContentType: The content type enum value.
        """
        return self.__content_type

    def to_dict(self) -> Dict:
        """Convert the Content object to a dictionary.

        Returns:
            Dict: A dictionary with body and type.
        """
        return {
            "body": self.__body,
            "type": self.__content_type.value,
        }

    def __str__(self) -> str:
        """Return a JSON string representation of the content.

        Returns:
            str: A formatted JSON string.
        """
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)