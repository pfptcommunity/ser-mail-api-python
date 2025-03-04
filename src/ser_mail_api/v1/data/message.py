from __future__ import annotations

import json
import warnings
from typing import List, Dict, Optional

from .attachment import Attachment
from .content import Content, ContentType
from .mailuser import MailUser
from .message_headers import MessageHeaders


class Message:
    """Represents an email message with sender, recipients, content, and attachments.

    Use Message.Builder() for step-wise construction (preferred method) or __init__ for minimal setup.
    Adder methods (e.g., add_to) are supported but deprecated in favor of the.Builder() pattern.
    Attributes use single underscores to indicate they are protected and not intended for direct modification.
    """

    def __init__(self, subject: str, sender: MailUser, header_from: Optional[MailUser] = None):
        """Initialize a Message with a subject, sender, and optional header sender.

        Args:
            subject (str): The subject of the email.
            sender (MailUser): The sender of the email.
            header_from (Optional[MailUser]): The sender for the 'From' header, if different from sender. Defaults to None.

        Raises:
            TypeError: If sender or header_from (if provided) is not a MailUser, or if subject is not a string.
        """
        if not isinstance(sender, MailUser):
            raise TypeError(f"Expected sender to be a MailUser, got {type(sender).__name__}")
        if header_from is not None and not isinstance(header_from, MailUser):
            raise TypeError(f"Expected header_from to be a MailUser or None, got {type(header_from).__name__}")
        if not isinstance(subject, str):
            raise TypeError(f"Expected subject to be a string, got {type(subject).__name__}")

        self._subject = subject
        self._sender = sender
        self._headers = None
        if header_from is not None:
            self.header_from = header_from
        self._to: List[MailUser] = []
        self._cc: List[MailUser] = []
        self._bcc: List[MailUser] = []
        self._reply_tos: List[MailUser] = []
        self._attachments: List[Attachment] = []
        self._content: List[Content] = []

    @property
    def sender(self) -> MailUser:
        """Get the sender of the email.

        Returns:
            MailUser: The sender.
        """
        return self._sender

    @sender.setter
    def sender(self, sender: MailUser):
        """Set the sender of the email.

        Args:
            sender (MailUser): The new sender.

        Raises:
            TypeError: If sender is not a MailUser.
        """
        if not isinstance(sender, MailUser):
            raise TypeError(f"Expected sender to be a MailUser, got {type(sender).__name__}")
        self._sender = sender

    @property
    def header_sender(self) -> Optional[MailUser]:
        """Get the sender from the headers (alias for header_from).

        Returns:
            Optional[MailUser]: The header sender, or None if not set.
        """
        return self.header_from

    @header_sender.setter
    def header_sender(self, sender: MailUser):
        """Set the sender in the headers (alias for header_from setter).

        Args:
            sender (MailUser): The new header sender.
        """
        self.header_from = sender

    @property
    def header_from(self) -> Optional[MailUser]:
        """Get the sender from the headers.

        Returns:
            Optional[MailUser]: The header sender, or None if no headers are set.
        """
        return self._headers.header_from if self._headers else None

    @header_from.setter
    def header_from(self, header_from: Optional["MailUser"]):
        """Set the sender in the headers.

        Args:
            header_from (Optional[MailUser]): The sender for the 'From' header, or None to clear headers.
        """
        if header_from is None:
            self._headers = None
        else:
            self._headers = MessageHeaders(header_from)  # Fixed from .From to constructor

    @property
    def headers(self) -> Optional[MessageHeaders]:
        """Get the message headers.

        Returns:
            Optional[MessageHeaders]: The headers, or None if not set.
        """
        return self._headers

    @headers.setter
    def headers(self, headers: Optional[MessageHeaders] = None):
        """Set the message headers.

        Args:
            headers (Optional[MessageHeaders]): The new headers, or None to clear. Defaults to None.

        Raises:
            TypeError: If headers is not a MessageHeaders instance when provided.
        """
        if headers is not None and not isinstance(headers, MessageHeaders):
            raise TypeError(f"Expected headers to be a MessageHeaders, got {type(headers).__name__}")
        self._headers = headers

    def add_to(self, to_user: MailUser):
        """Add a primary recipient (To field) to the email.

        Deprecated: Use Message.Builder().add_to() instead.

        Args:
            to_user (MailUser): The recipient to add.

        Raises:
            TypeError: If to_user is not a MailUser.
        """
        warnings.warn("add_to is deprecated; use Message.Builder().add_to() instead", DeprecationWarning)
        if not isinstance(to_user, MailUser):
            raise TypeError(f"Expected to_user to be a MailUser, got {type(to_user).__name__}")
        self._to.append(to_user)

    def add_cc(self, cc_user: MailUser):
        """Add a CC recipient to the email.

        Deprecated: Use Message.Builder().add_cc() instead.

        Args:
            cc_user (MailUser): The CC recipient to add.

        Raises:
            TypeError: If cc_user is not a MailUser.
        """
        warnings.warn("add_cc is deprecated; use Message.Builder().add_cc() instead", DeprecationWarning)
        if not isinstance(cc_user, MailUser):
            raise TypeError(f"Expected cc_user to be a MailUser, got {type(cc_user).__name__}")
        self._cc.append(cc_user)

    def add_bcc(self, bcc_user: MailUser):
        """Add a BCC recipient to the email.

        Deprecated: Use Message.Builder().add_bcc() instead.

        Args:
            bcc_user (MailUser): The BCC recipient to add.

        Raises:
            TypeError: If bcc_user is not a MailUser.
        """
        warnings.warn("add_bcc is deprecated; use Message.Builder().add_bcc() instead", DeprecationWarning)
        if not isinstance(bcc_user, MailUser):
            raise TypeError(f"Expected bcc_user to be a MailUser, got {type(bcc_user).__name__}")
        self._bcc.append(bcc_user)

    def add_reply_to(self, reply_to_user: MailUser):
        """Add a Reply-To recipient to the email.

        Deprecated: Use Message.Builder().add_reply_to() instead.

        Args:
            reply_to_user (MailUser): The Reply-To recipient to add.

        Raises:
            TypeError: If reply_to_user is not a MailUser.
        """
        warnings.warn("add_reply_to is deprecated; use Message.Builder().add_reply_to() instead", DeprecationWarning)
        if not isinstance(reply_to_user, MailUser):
            raise TypeError(f"Expected reply_to_user to be a MailUser, got {type(reply_to_user).__name__}")
        self._reply_tos.append(reply_to_user)

    def add_attachment(self, attachment: Attachment):
        """Add an attachment to the email.

        Deprecated: Use Message.Builder().add_attachment() instead.

        Args:
            attachment (Attachment): The attachment to add.

        Raises:
            TypeError: If attachment is not an Attachment.
        """
        warnings.warn("add_attachment is deprecated; use Message.Builder().add_attachment() instead",
                      DeprecationWarning)
        if not isinstance(attachment, Attachment):
            raise TypeError(f"Expected attachment to be an Attachment, got {type(attachment).__name__}")
        self._attachments.append(attachment)

    def add_content(self, content: Content):
        """Add a content item to the email.

        Deprecated: Use Message.Builder().add_content() instead.

        Args:
            content (Content): The content item to add.

        Raises:
            TypeError: If content is not a Content.
        """
        warnings.warn("add_content is deprecated; use Message.Builder().add_content() instead", DeprecationWarning)
        if not isinstance(content, Content):
            raise TypeError(f"Expected content to be a Content, got {type(content).__name__}")
        self._content.append(content)

    def to_dict(self) -> Dict:
        """Convert the Message to a dictionary representation.

        Returns:
            Dict: A dictionary with email fields (from, subject, content, headers, recipients, attachments).
        """
        data = {
            "from": self._sender.to_dict(),
            "subject": self._subject,
        }
        if self._content:
            data['content'] = [content.to_dict() for content in self._content]
        if self._headers is not None:
            data['headers'] = self._headers.to_dict()
        if self._to:
            data['tos'] = [recipient.to_dict() for recipient in self._to]
        if self._cc:
            data['cc'] = [cc_user.to_dict() for cc_user in self._cc]
        if self._bcc:
            data['bcc'] = [bcc_user.to_dict() for bcc_user in self._bcc]
        if self._reply_tos:
            data['replyTos'] = [reply_to_user.to_dict() for reply_to_user in self._reply_tos]
        if self._attachments:
            data['attachments'] = [attachment.to_dict() for attachment in self._attachments]
        return data

    def __str__(self) -> str:
        """Return a JSON string representation of the Message.

        Returns:
            str: A formatted JSON string.
        """
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

    class Builder:
        """Builder class for constructing Message instances fluently.

        Enforces minimum requirements (from, tos, subject, content) at build time.
        """

        def __init__(self):
            """Initialize the Builder with empty lists and default values."""
            self._attachments: List[Attachment] = []
            self._content: List[Content] = []
            self._tos: List[MailUser] = []
            self._cc: List[MailUser] = []
            self._bcc: List[MailUser] = []
            self._reply_tos: List[MailUser] = []
            self._subject: Optional[str] = None
            self._from: Optional[MailUser] = None
            self._header_from: Optional[MailUser] = None

        def subject(self, subject: str) -> Message.Builder:
            """Set the subject of the email.

            Args:
                subject (str): The subject to set.

            Returns:
                Message.Builder: Self for chaining.
            """
            self._subject = subject
            return self

        def from_address_mu(self, from_: MailUser) -> Message.Builder:
            """Set the sender of the email.

            Args:
                from_ (MailUser): The sender to set.

            Returns:
                Message.Builder: Self for chaining.
            """
            self._from = from_
            return self

        def from_address(self, email: str, name: Optional[str] = None) -> Message.Builder:
            """Set the sender using an email address and optional name.

            Args:
                email (str): The sender's email address.
                name (Optional[str]): The sender's name, if any. Defaults to None.

            Returns:
                Message.Builder: Self for chaining.
            """
            self._from = MailUser(email, name)
            return self

        def header_from_mu(self, header_from: MailUser) -> Message.Builder:
            """Set the header 'From' value.

            Args:
                header_from (MailUser): The sender to appear in the headers.

            Returns:
                Message.Builder: Self for chaining.
            """
            self._header_from = header_from
            return self

        def header_from(self, email: str, name: Optional[str] = None) -> Message.Builder:
            """Set the header 'From' value using an email address and optional name.

            Args:
                email (str): The header sender's email address.
                name (Optional[str]): The header sender's name, if any. Defaults to None.

            Returns:
                Message.Builder: Self for chaining.
            """
            self._header_from = MailUser(email, name)
            return self

        def add_attachment(self, attachment: Attachment) -> Message.Builder:
            """Add an attachment to the email.

            Args:
                attachment (Attachment): The attachment to add.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                ValueError: If attachment is None.
            """
            if attachment is None:
                raise ValueError("Attachment must not be None")
            self._attachments.append(attachment)
            return self

        def add_content_ct(self, content: Content) -> Message.Builder:
            """Add a content item to the email.

            Args:
                content (Content): The content item to add.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                ValueError: If content is None.
            """
            if content is None:
                raise ValueError("Content must not be None")
            self._content.append(content)
            return self

        def add_content(self, body: str, type_: ContentType) -> Message.Builder:
            """Add a content item using a body and content type.

            Args:
                body (str): The content body (e.g., text or HTML).
                type_ (ContentType): The type of content (TEXT or HTML).

            Returns:
                Message.Builder: Self for chaining.
            """
            self._content.append(Content(body, type_))
            return self

        def add_to_mu(self, to: MailUser) -> Message.Builder:
            """Add a primary recipient (To field) to the email.

            Args:
                to (MailUser): The recipient to add.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                ValueError: If to is None.
            """
            if to is None:
                raise ValueError("Recipient must not be None")
            self._tos.append(to)
            return self

        def add_to(self, email: str, name: Optional[str] = None) -> Message.Builder:
            """Add a primary recipient using an email address and optional name.

            Args:
                email (str): The recipient's email address.
                name (Optional[str]): The recipient's name, if any. Defaults to None.

            Returns:
                Message.Builder: Self for chaining.
            """
            self._tos.append(MailUser(email, name))
            return self

        def add_cc_mu(self, cc: MailUser) -> Message.Builder:
            """Add a CC recipient to the email.

            Args:
                cc (MailUser): The CC recipient to add.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                ValueError: If cc is None.
            """
            if cc is None:
                raise ValueError("CC recipient must not be None")
            self._cc.append(cc)
            return self

        def add_cc(self, email: str, name: Optional[str] = None) -> Message.Builder:
            """Add a CC recipient using an email address and optional name.

            Args:
                email (str): The CC recipient's email address.
                name (Optional[str]): The CC recipient's name, if any. Defaults to None.

            Returns:
                Message.Builder: Self for chaining.
            """
            self._cc.append(MailUser(email, name))
            return self

        def add_bcc_mu(self, bcc: MailUser) -> Message.Builder:
            """Add a BCC recipient to the email.

            Args:
                bcc (MailUser): The BCC recipient to add.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                ValueError: If bcc is None.
            """
            if bcc is None:
                raise ValueError("BCC recipient must not be None")
            self._bcc.append(bcc)
            return self

        def add_bcc(self, email: str, name: Optional[str] = None) -> Message.Builder:
            """Add a BCC recipient using an email address and optional name.

            Args:
                email (str): The BCC recipient's email address.
                name (Optional[str]): The BCC recipient's name, if any. Defaults to None.

            Returns:
                Message.Builder: Self for chaining.
            """
            self._bcc.append(MailUser(email, name))
            return self

        def add_reply_to_mu(self, reply_to: MailUser) -> Message.Builder:
            """Add a Reply-To recipient to the email.

            Args:
                reply_to (MailUser): The Reply-To recipient to add.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                ValueError: If reply_to is None.
            """
            if reply_to is None:
                raise ValueError("Reply-To recipient must not be None")
            self._reply_tos.append(reply_to)
            return self

        def add_reply_to(self, email: str, name: Optional[str] = None) -> Message.Builder:
            """Add a Reply-To recipient using an email address and optional name.

            Args:
                email (str): The Reply-To recipient's email address.
                name (Optional[str]): The Reply-To recipient's name, if any. Defaults to None.

            Returns:
                Message.Builder: Self for chaining.
            """
            self._reply_tos.append(MailUser(email, name))
            return self

        def build(self) -> Message:
            """Build a Message instance with the configured fields.

            Enforces minimum requirements: sender (from), at least one recipient (to),
            subject, and at least one content item.

            Returns:
                Message: A new Message instance.

            Raises:
                ValueError: If from, tos, subject, or content is not set appropriately.
            """
            if self._from is None:
                raise ValueError("Sender (from) is required")
            if not self._tos:
                raise ValueError("At least one recipient (to) is required")
            if self._subject is None:
                raise ValueError("Subject is required")
            if not self._content:
                raise ValueError("At least one content item is required")

            message = Message(self._subject, self._from, self._header_from)
            message._to = self._tos
            message._cc = self._cc
            message._bcc = self._bcc
            message._reply_tos = self._reply_tos
            message._attachments = self._attachments
            message._content = self._content
            return message