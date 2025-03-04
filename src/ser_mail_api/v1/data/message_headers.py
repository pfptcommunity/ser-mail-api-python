from __future__ import annotations  # Ensure forward type hints work (assuming this is in the file)

from .mailuser import MailUser  # Import MailUser from the local module


class MessageHeaders:
    """Represents immutable email message headers with a 'from' field.

    Instances are intended to be immutable after creation. Use the constructor directly;
    the 'header_from' attribute is read-only via its property. Modifying internal attributes
    (e.g., _MessageHeaders__header_from) is possible but strongly discouraged as it violates
    the immutability intent.
    """

    def __init__(self, header_from: MailUser):
        """Initialize the MessageHeaders with a sender (from) MailUser.

        Args:
            header_from (MailUser): The sender of the message.

        Raises:
            TypeError: If header_from is not a MailUser instance.
        """
        # Validate that header_from is a MailUser instance
        if not isinstance(header_from, MailUser):
            raise TypeError(f"Expected header from to be a MailUser, got {type(header_from).__name__}")

        # Set the attribute (intended to be immutable after initialization)
        self.__header_from = header_from

    @property
    def header_from(self) -> MailUser:
        """Get the sender (from) MailUser of the message.

        Returns:
            MailUser: The MailUser instance representing the sender.
        """
        return self.__header_from

    def to_dict(self) -> dict:  # Added return type annotation for consistency
        """Convert the MessageHeaders to a dictionary representation.

        Returns:
            dict: A dictionary with the 'from' field mapped to the sender's dictionary representation.
        """
        return {
            'from': self.header_from.to_dict()
        }