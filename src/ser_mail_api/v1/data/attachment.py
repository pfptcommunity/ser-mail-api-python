from __future__ import annotations

import base64
import json
import mimetypes
import os
import uuid
import warnings
from enum import Enum
from typing import Dict, Optional


def _deduce_mime_type(file_path: str) -> str:
    """Deduce the MIME type from a file path using the mimetypes module.

    Args:
        file_path (str): The path or filename to deduce the MIME type from.

    Returns:
        str: The deduced MIME type.

    Raises:
        ValueError: If the MIME type cannot be deduced.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        raise ValueError(f"Unable to deduce MIME type for file: {file_path}")
    return mime_type


def _encode_file_content(file_path: str) -> str:
    """Encode the content of a file as a Base64 string.

    Args:
        file_path (str): The path to the file to encode.

    Returns:
        str: The Base64-encoded content of the file.
    """
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def _is_valid_base64(s: str) -> bool:
    """Check if a string is a valid Base64-encoded value.

    Args:
        s (str): The string to validate.

    Returns:
        bool: True if the string is valid Base64, False otherwise.
    """
    try:
        return base64.b64encode(base64.b64decode(s)).decode('utf-8') == s
    except Exception:
        return False


class Disposition(Enum):
    """Enumeration for the disposition of an attachment."""
    Inline = "inline"
    Attachment = "attachment"


class Attachment:
    """Represents an attachment with Base64-encoded content and metadata.

    Use `Attachment.build()` for step-wise construction or static methods for direct creation.
    """

    def __init__(self, content: str, filename: str, mime_type: Optional[str] = None,
                 disposition: Disposition = Disposition.Attachment, content_id: Optional[str] = None):
        """
        Args:
            content (str): Base64-encoded content of the attachment.
            filename (str): Filename of the attachment.
            mime_type (Optional[str]): MIME type of the content. If None, deduced from filename.
            disposition (Disposition): The disposition (inline or attachment). Defaults to Attachment.
            content_id (Optional[str]): Content-ID for inline attachments. If None or empty for inline, a UUID is generated.

        Raises:
            TypeError: If content, filename, disposition, mime_type, or content_id are of incorrect types.
            ValueError: If content is invalid Base64, filename is empty, or MIME type cannot be determined.
        """
        # Validate input types
        if not isinstance(content, str):
            raise TypeError(f"Expected 'content' to be a string, got {type(content).__name__}")
        if not isinstance(disposition, Disposition):
            raise TypeError(f"Expected 'disposition' to be a Disposition, got {type(disposition).__name__}")
        if not isinstance(filename, str):
            raise TypeError(f"Expected 'filename' to be a string, got {type(filename).__name__}")
        if mime_type is not None and not isinstance(mime_type, str):
            raise TypeError(f"Expected 'mime_type' to be a string, got {type(mime_type).__name__}")

        # Validate specific constraints
        if not _is_valid_base64(content):
            raise ValueError("Invalid Base64 content")
        if not filename.strip():
            raise ValueError("Filename must be a non-empty string")
        if len(filename) > 1000:
            raise ValueError("Filename must be at most 1000 characters long")

        # User provided mime_type or try to deduce it from filename
        if mime_type is None:
            mime_type = _deduce_mime_type(filename)
        if not mime_type.strip():
            raise ValueError("Mime type must be a non-empty string")

        # Covers None, empty string, or whitespace-only strings
        if not content_id or content_id.isspace():
            self.__content_id = str(uuid.uuid4())  # Generate a UUID
        elif isinstance(content_id, str):
            self.__content_id = content_id  # Use provided string
        else:
            raise TypeError(f"Expected 'content_id' to be a string or None, got {type(content_id).__name__}")

        # Content-ID only applies to inline attachments
        if disposition == Disposition.Attachment:
            self.__content_id = None

        self.__content = content
        self.__disposition = disposition
        self.__filename = filename
        self.__mime_type = mime_type

    @property
    def id(self) -> str:
        """The Content-ID of the attachment (alias for content_id)."""
        warnings.warn("cid is deprecated; use content_id instead", DeprecationWarning)
        return self.__content_id

    @property
    def cid(self) -> str:
        """The Content-ID of the attachment (alias for content_id)."""
        return self.__content_id

    @property
    def content_id(self) -> str:
        """The Content-ID of the attachment, if inline."""
        return self.__content_id

    @property
    def content(self) -> str:
        """The Base64-encoded content of the attachment."""
        return self.__content

    @property
    def disposition(self) -> Disposition:
        """The disposition of the attachment (inline or attachment)."""
        return self.__disposition

    @property
    def filename(self) -> str:
        """The filename of the attachment."""
        return self.__filename

    @property
    def mime_type(self) -> str:
        """The MIME type of the attachment."""
        return self.__mime_type

    def to_dict(self) -> Dict:
        """Convert the attachment to a dictionary representation.

        Returns:
            Dict: A dictionary with content, disposition, filename, type, and optionally id.
        """
        data = {
            "content": self.__content,
            "disposition": self.__disposition.value,
            "filename": self.__filename,
            "type": self.__mime_type,
        }
        if self.disposition == Disposition.Inline:
            data["id"] = self.__content_id
        return data

    def __str__(self) -> str:
        """Return a JSON string representation of the attachment.

        Returns:
            str: A formatted JSON string.
        """
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

    @staticmethod
    def from_base64(base64string: str, filename: str, mime_type: Optional[str] = None,
                    disposition: Disposition = Disposition.Attachment, content_id: Optional[str] = None) -> Attachment:
        """Create an Attachment from a Base64-encoded string.

        Args:
            base64string (str): Base64-encoded content.
            filename (str): Filename of the attachment.
            mime_type (Optional[str]): MIME type. If None, deduced from filename.
            disposition (Disposition): Disposition (inline or attachment). Defaults to Attachment.
            content_id (Optional[str]): Content-ID for inline attachments. If None, a UUID is generated.

        Returns:
            Attachment: A new Attachment instance.
        """
        return Attachment(base64string, filename, mime_type, disposition, content_id)

    @staticmethod
    def from_file(file_path: str, disposition: Disposition = Disposition.Attachment, content_id: Optional[str] = None,
                  filename: Optional[str] = None, mime_type: Optional[str] = None) -> Attachment:
        """Create an Attachment from a file.

        Args:
            file_path (str): Path to the file.
            disposition (Disposition): Disposition (inline or attachment). Defaults to Attachment.
            content_id (Optional[str]): Content-ID for inline attachments. If None, a UUID is generated.
            filename (Optional[str]): Filename override. Defaults to basename of file_path.
            mime_type (Optional[str]): MIME type override. Defaults to deduced from filename.

        Returns:
            Attachment: A new Attachment instance.

        Raises:
            TypeError: If file_path is not a string.
            FileNotFoundError: If the file does not exist.
        """
        if not isinstance(file_path, str):
            raise TypeError(f"Expected 'file_path' to be a string, got {type(file_path).__name__}")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file at path '{file_path}' does not exist.")
        if filename is None:
            filename = os.path.basename(file_path)
        content = _encode_file_content(file_path)
        return Attachment(content, filename, mime_type, disposition, content_id)

    @staticmethod
    def from_bytes(data: bytes, filename: str, mime_type: Optional[str] = None,
                   disposition: Disposition = Disposition.Attachment,
                   content_id: Optional[str] = None) -> Attachment:
        """Create an Attachment from a byte array.

        Args:
            data (bytes): Byte array content.
            filename (str): Filename of the attachment.
            mime_type (Optional[str]): MIME type. If None, deduced from filename.
            disposition (Disposition): Disposition (inline or attachment). Defaults to Attachment.
            content_id (Optional[str]): Content-ID for inline attachments. If None, a UUID is generated.

        Returns:
            Attachment: A new Attachment instance.

        Raises:
            TypeError: If data is not bytes.
        """
        if not isinstance(data, bytes):
            raise TypeError(f"Expected 'data' to be bytes, got {type(data).__name__}")
        content = base64.b64encode(data).decode("utf-8")
        return Attachment(content, filename, mime_type, disposition, content_id)

    class Builder:
        """Initial step for constructing an Attachment, requiring content and filename specification."""

        def from_base64(self, base64_content: str, filename: str) -> _OptionalStep:
            """Set content from a Base64-encoded string.

            Args:
                base64_content (str): Base64-encoded content.
                filename (str): Filename of the attachment.

            Returns:
                OptionalStep: The next step for optional configuration.

            Raises:
                ValueError: If base64_content or filename is None, or if Base64 is invalid.
            """
            if base64_content is None:
                raise ValueError("Base64 content must not be None")
            if filename is None:
                raise ValueError("Filename must not be None")
            if not _is_valid_base64(base64_content):
                raise ValueError("Content must be a valid Base64-encoded string")
            return Attachment.Builder._OptionalStep(base64_content, filename)

        def from_file(self, file_path: str) -> _OptionalStep:
            """Set content from a file.

            Args:
                file_path (str): Path to the file.

            Returns:
                OptionalStep: The next step for optional configuration.

            Raises:
                ValueError: If file_path is None, empty, or whitespace.
                FileNotFoundError: If the file does not exist.
            """
            if not file_path or file_path.isspace():
                raise ValueError("File path cannot be None, empty, or contain only whitespace")
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"File not found: '{file_path}'")
            filename = os.path.basename(file_path)
            content = _encode_file_content(file_path)
            return Attachment.Builder._OptionalStep(content, filename)

        def from_bytes(self, data: bytes, filename: str) -> _OptionalStep:
            """Set content from a byte array.

            Args:
                data (bytes): Byte array content.
                filename (str): Filename of the attachment.

            Returns:
                OptionalStep: The next step for optional configuration.

            Raises:
                ValueError: If data or filename is None.
            """
            if data is None:
                raise ValueError("Byte array must not be None")
            if filename is None:
                raise ValueError("Filename must not be None")
            content = base64.b64encode(data).decode("utf-8")
            return Attachment.Builder._OptionalStep(content, filename)

        class _OptionalStep:
            """Optional configuration step for an Attachment before final construction."""

            def __init__(self, content: str, filename: str):
                self.__content = content
                self.__filename = filename
                self.__mime_type = None
                self.__disposition = Disposition.Attachment
                self.__content_id = None

            def disposition_attached(self) -> Attachment.Builder._OptionalStep:
                """Set the disposition to Attachment, clearing any Content-ID.

                Returns:
                    OptionalStep: Self, for method chaining.
                """
                self.__disposition = Disposition.Attachment
                self.__content_id = None
                return self

            def disposition_inline(self, content_id: Optional[str] = None) -> Attachment.Builder._OptionalStep:
                """Set the disposition to Inline with an optional Content-ID.

                Args:
                    content_id (Optional[str]): Content-ID for the inline attachment. If None, a UUID will be generated.

                Returns:
                    OptionalStep: Self, for method chaining.

                Raises:
                    TypeError: If content_id is neither a string nor None.
                """
                if content_id is not None and not isinstance(content_id, str):
                    raise TypeError(f"Expected 'content_id' to be a string or None, got {type(content_id).__name__}")
                self.__disposition = Disposition.Inline
                self.__content_id = content_id
                return self

            def filename(self, filename: str) -> Attachment.Builder._OptionalStep:
                """Override the filename.

                Args:
                    filename (str): New filename for the attachment.

                Returns:
                    OptionalStep: Self, for method chaining.

                Raises:
                    ValueError: If filename is None.
                """
                if filename is None:
                    raise ValueError("Filename must not be None")
                self.__filename = filename
                return self

            def mime_type(self, mime_type: str) -> Attachment.Builder._OptionalStep:
                """Set the MIME type.

                Args:
                    mime_type (str): MIME type for the attachment.

                Returns:
                    OptionalStep: Self, for method chaining.

                Raises:
                    ValueError: If mime_type is None.
                """
                if mime_type is None:
                    raise ValueError("MimeType must not be None")
                self.__mime_type = mime_type
                return self

            def build(self) -> Attachment:
                """Finalize and construct the Attachment instance.

                Returns:
                    Attachment: The fully constructed Attachment object.
                """
                return Attachment(
                    content=self.__content,
                    filename=self.__filename,
                    mime_type=self.__mime_type,
                    disposition=self.__disposition,
                    content_id=self.__content_id
                )
