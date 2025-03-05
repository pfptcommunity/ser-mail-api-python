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
    Attributes use double underscores to indicate they are private and not intended for direct modification.
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
        warnings.warn("Direct instantiation of 'Message' deprecated; use Message.Builder", DeprecationWarning, stacklevel=2)
        if not isinstance(sender, MailUser):
            raise TypeError(f"Expected sender to be a MailUser, got {type(sender).__name__}")
        if header_from is not None and not isinstance(header_from, MailUser):
            raise TypeError(f"Expected header_from to be a MailUser or None, got {type(header_from).__name__}")
        if not isinstance(subject, str):
            raise TypeError(f"Expected subject to be a string, got {type(subject).__name__}")

        self.__subject = subject
        self.__sender = sender
        self.__headers = None
        if header_from is not None:
            self.header_from = header_from
        self.__to: List[MailUser] = []
        self.__cc: List[MailUser] = []
        self.__bcc: List[MailUser] = []
        self.__reply_tos: List[MailUser] = []
        self.__attachments: List[Attachment] = []
        self.__content: List[Content] = []

    @classmethod
    def __create(cls,
                subject: str,
                sender: MailUser,
                header_from: MailUser,
                attachments: List[Attachment],
                content: List[Content],
                to: List[MailUser],
                cc: List[MailUser],
                bcc: List[MailUser],
                reply_tos: List[MailUser]) -> Message:
        """ Internal method to create an Email instance. """
        obj = cls.__new__(cls)
        obj.__subject = subject
        obj.__sender = sender
        obj.__headers = MessageHeaders(header_from) if header_from is not None else None
        obj.__attachments = attachments
        obj.__content = content
        obj.__to = to
        obj.__cc = cc
        obj.__bcc = bcc
        obj.__reply_tos = reply_tos
        return obj

    @property
    def sender(self) -> MailUser:
        """Get the sender of the email.

        Returns:
            MailUser: The sender.
        """
        return self.__sender

    @sender.setter
    def sender(self, sender: MailUser):
        """Set the sender of the email.

        Args:
            sender (MailUser): The new sender.

        Raises:
            TypeError: If sender is not a MailUser.
        """
        warnings.warn("sender is deprecated; use Message.Builder().sender() instead", DeprecationWarning)
        if not isinstance(sender, MailUser):
            raise TypeError(f"Expected sender to be a MailUser, got {type(sender).__name__}")
        self.__sender = sender

    @property
    def header_sender(self) -> Optional[MailUser]:
        """Get the sender from the headers (alias for header_from).

        Returns:
            Optional[MailUser]: The header sender, or None if not set.
        """
        warnings.warn("header_sender is deprecated; use header_from instead", DeprecationWarning)
        return self.header_from

    @header_sender.setter
    def header_sender(self, sender: MailUser):
        """Set the sender in the headers (alias for header_from setter).

        Args:
            sender (MailUser): The new header sender.
        """
        warnings.warn("header_sender is deprecated; use header_from instead", DeprecationWarning)
        self.header_from = sender

    @property
    def header_from(self) -> Optional[MailUser]:
        """Get the sender from the headers.

        Returns:
            Optional[MailUser]: The header sender, or None if no headers are set.
        """
        return self.__headers.header_from if self.__headers else None

    @header_from.setter
    def header_from(self, header_from: Optional[MailUser]):
        """Set the sender in the headers.

        Args:
            header_from (Optional[MailUser]): The sender for the 'From' header, or None to clear headers.
        """
        if header_from is None:
            self.__headers = None
        else:
            self.__headers = MessageHeaders(header_from)  # Fixed from .From to constructor

    @property
    def headers(self) -> Optional[MessageHeaders]:
        """Get the message headers.

        Returns:
            Optional[MessageHeaders]: The headers, or None if not set.
        """
        return self.__headers

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
        self.__headers = headers

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
        self.__to.append(to_user)

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
        self.__cc.append(cc_user)

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
        self.__bcc.append(bcc_user)

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
        self.__reply_tos.append(reply_to_user)

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
        self.__attachments.append(attachment)

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
        self.__content.append(content)

    def to_dict(self) -> Dict:
        """Convert the Message to a dictionary representation.

        Returns:
            Dict: A dictionary with email fields (from, subject, content, headers, recipients, attachments).
        """
        data = {
            "from": self.__sender.to_dict(),
            "subject": self.__subject,
        }
        if self.__content:
            data['content'] = [content.to_dict() for content in self.__content]
        if self.__headers is not None:
            data['headers'] = self.__headers.to_dict()
        if self.__to:
            data['tos'] = [recipient.to_dict() for recipient in self.__to]
        if self.__cc:
            data['cc'] = [cc_user.to_dict() for cc_user in self.__cc]
        if self.__bcc:
            data['bcc'] = [bcc_user.to_dict() for bcc_user in self.__bcc]
        if self.__reply_tos:
            data['replyTos'] = [reply_to_user.to_dict() for reply_to_user in self.__reply_tos]
        if self.__attachments:
            data['attachments'] = [attachment.to_dict() for attachment in self.__attachments]
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
        Methods suffixed with '_mailuser' accept pre-constructed MailUser objects,
        while their non-suffixed counterparts construct MailUser objects from email and name strings.
        """

        def __init__(self):
            """Initialize the Builder with empty lists and default values."""
            self.__attachments: List[Attachment] = []
            self.__content: List[Content] = []
            self.__tos: List[MailUser] = []
            self.__cc: List[MailUser] = []
            self.__bcc: List[MailUser] = []
            self.__reply_tos: List[MailUser] = []
            self.__subject: Optional[str] = None
            self.__from: Optional[MailUser] = None
            self.__header_from: Optional[MailUser] = None

        def subject(self, subject: str) -> Message.Builder:
            """Set the subject of the email.

            Args:
                subject (str): The subject to set.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If subject is not a string (including if it is None).
            """
            if not isinstance(subject, str):
                raise TypeError(f"Expected subject to be a string, got {type(subject).__name__}")
            self.__subject = subject
            return self

        def sender_mailuser(self, sender: MailUser) -> Message.Builder:
            """Set the sender of the email using a pre-constructed MailUser object.

            Use this method when you already have a MailUser instance. For constructing a sender
            from an email and name, use sender() instead.

            Args:
                sender (MailUser): The sender as a MailUser object.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If from_ is not a MailUser instance (including if it is None).
            """
            if not isinstance(sender, MailUser):
                raise TypeError(f"Expected sender to be a MailUser, got {type(sender).__name__}")
            self.__from = sender
            return self

        def sender(self, email: str, name: Optional[str] = None) -> Message.Builder:
            """Set the sender using an email address and optional name.

            This method constructs a MailUser object internally. If you have an existing
            MailUser object, use sender_mailuser() instead.

            Args:
                email (str): The sender's email address.
                name (Optional[str]): The sender's name, if any. Defaults to None.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If email is not a string (including if it is None) or name is provided and not a string.
            """
            if not isinstance(email, str):
                raise TypeError(f"Expected email to be a string, got {type(email).__name__}")
            if name is not None and not isinstance(name, str):
                raise TypeError(f"Expected name to be a string or None, got {type(name).__name__}")
            self.__from = MailUser(email, name)
            return self

        def header_from_mailuser(self, header_from: MailUser) -> Message.Builder:
            """Set the header 'From' value using a pre-constructed MailUser object.

            Use this method when you have a MailUser instance for the header sender.
            For constructing from an email and name, use header_from() instead.

            Args:
                header_from (MailUser): The sender to appear in the headers as a MailUser object.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If header_from is not a MailUser instance (including if it is None).
            """
            if not isinstance(header_from, MailUser):
                raise TypeError(f"Expected header_from to be a MailUser, got {type(header_from).__name__}")
            self.__header_from = header_from
            return self

        def header_from(self, email: str, name: Optional[str] = None) -> Message.Builder:
            """Set the header 'From' value using an email address and optional name.

            This method constructs a MailUser object internally. If you have an existing
            MailUser object, use header_from_mailuser() instead.

            Args:
                email (str): The header sender's email address.
                name (Optional[str]): The header sender's name, if any. Defaults to None.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If email is not a string (including if it is None) or name is provided and not a string.
            """
            if not isinstance(email, str):
                raise TypeError(f"Expected email to be a string, got {type(email).__name__}")
            if name is not None and not isinstance(name, str):
                raise TypeError(f"Expected name to be a string or None, got {type(name).__name__}")
            self.__header_from = MailUser(email, name)
            return self

        def add_attachment(self, attachment: Attachment) -> Message.Builder:
            """Add an attachment to the email.

            Args:
                attachment (Attachment): The attachment to add.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                ValueError: If attachment is None.
                TypeError: If attachment is not an Attachment instance.
            """
            if attachment is None:
                raise ValueError("Attachment must not be None")
            if not isinstance(attachment, Attachment):
                raise TypeError(f"Expected attachment to be an Attachment, got {type(attachment).__name__}")
            self.__attachments.append(attachment)
            return self

        def add_content_ct(self, content: Content) -> Message.Builder:
            """Add a content item to the email.

            Args:
                content (Content): The content item to add.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                ValueError: If content is None.
                TypeError: If content is not a Content instance.
            """
            if content is None:
                raise ValueError("Content must not be None")
            if not isinstance(content, Content):
                raise TypeError(f"Expected content to be a Content, got {type(content).__name__}")
            self.__content.append(content)
            return self

        def add_content(self, body: str, type_: ContentType) -> Message.Builder:
            """Add a content item using a body and content type.

            Args:
                body (str): The content body (e.g., text or HTML).
                type_ (ContentType): The type of content (TEXT or HTML).

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If body is not a string (including if it is None) or type_ is not a ContentType (including if it is None).
            """
            if not isinstance(body, str):
                raise TypeError(f"Expected body to be a string, got {type(body).__name__}")
            if not isinstance(type_, ContentType):
                raise TypeError(f"Expected type_ to be a ContentType, got {type(type_).__name__}")
            self.__content.append(Content(body, type_))
            return self

        def add_to_mailuser(self, to: MailUser) -> Message.Builder:
            """Add a primary recipient (To field) to the email using a pre-constructed MailUser object.

            Use this method when you have an existing MailUser instance. For constructing a recipient
            from an email and name, use add_to() instead.

            Args:
                to (MailUser): The recipient as a MailUser object.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If to is not a MailUser instance (including if it is None).
            """
            if not isinstance(to, MailUser):
                raise TypeError(f"Expected to to be a MailUser, got {type(to).__name__}")
            self.__tos.append(to)
            return self

        def add_to(self, email: str, name: Optional[str] = None) -> Message.Builder:
            """Add a primary recipient (To field) using an email address and optional name.

            This method constructs a MailUser object internally. If you have an existing
            MailUser object, use add_to_mailuser() instead.

            Args:
                email (str): The recipient's email address.
                name (Optional[str]): The recipient's name, if any. Defaults to None.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If email is not a string (including if it is None) or name is provided and not a string.
            """
            if not isinstance(email, str):
                raise TypeError(f"Expected email to be a string, got {type(email).__name__}")
            if name is not None and not isinstance(name, str):
                raise TypeError(f"Expected name to be a string or None, got {type(name).__name__}")
            self.__tos.append(MailUser(email, name))
            return self

        def add_cc_mailuser(self, cc: MailUser) -> Message.Builder:
            """Add a CC recipient to the email using a pre-constructed MailUser object.

            Use this method when you have an existing MailUser instance. For constructing a CC
            recipient from an email and name, use add_cc() instead.

            Args:
                cc (MailUser): The CC recipient as a MailUser object.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If cc is not a MailUser instance (including if it is None).
            """
            if not isinstance(cc, MailUser):
                raise TypeError(f"Expected cc to be a MailUser, got {type(cc).__name__}")
            self.__cc.append(cc)
            return self

        def add_cc(self, email: str, name: Optional[str] = None) -> Message.Builder:
            """Add a CC recipient using an email address and optional name.

            This method constructs a MailUser object internally. If you have an existing
            MailUser object, use add_cc_mailuser() instead.

            Args:
                email (str): The CC recipient's email address.
                name (Optional[str]): The CC recipient's name, if any. Defaults to None.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If email is not a string (including if it is None) or name is provided and not a string.
            """
            if not isinstance(email, str):
                raise TypeError(f"Expected email to be a string, got {type(email).__name__}")
            if name is not None and not isinstance(name, str):
                raise TypeError(f"Expected name to be a string or None, got {type(name).__name__}")
            self.__cc.append(MailUser(email, name))
            return self

        def add_bcc_mailuser(self, bcc: MailUser) -> Message.Builder:
            """Add a BCC recipient to the email using a pre-constructed MailUser object.

            Use this method when you have an existing MailUser instance. For constructing a BCC
            recipient from an email and name, use add_bcc() instead.

            Args:
                bcc (MailUser): The BCC recipient as a MailUser object.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If bcc is not a MailUser instance (including if it is None).
            """
            if not isinstance(bcc, MailUser):
                raise TypeError(f"Expected bcc to be a MailUser, got {type(bcc).__name__}")
            self.__bcc.append(bcc)
            return self

        def add_bcc(self, email: str, name: Optional[str] = None) -> Message.Builder:
            """Add a BCC recipient using an email address and optional name.

            This method constructs a MailUser object internally. If you have an existing
            MailUser object, use add_bcc_mailuser() instead.

            Args:
                email (str): The BCC recipient's email address.
                name (Optional[str]): The BCC recipient's name, if any. Defaults to None.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If email is not a string (including if it is None) or name is provided and not a string.
            """
            if not isinstance(email, str):
                raise TypeError(f"Expected email to be a string, got {type(email).__name__}")
            if name is not None and not isinstance(name, str):
                raise TypeError(f"Expected name to be a string or None, got {type(name).__name__}")
            self.__bcc.append(MailUser(email, name))
            return self

        def add_reply_to_mailuser(self, reply_to: MailUser) -> Message.Builder:
            """Add a Reply-To recipient to the email using a pre-constructed MailUser object.

            Use this method when you have an existing MailUser instance. For constructing a Reply-To
            recipient from an email and name, use add_reply_to() instead.

            Args:
                reply_to (MailUser): The Reply-To recipient as a MailUser object.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If reply_to is not a MailUser instance (including if it is None).
            """
            if not isinstance(reply_to, MailUser):
                raise TypeError(f"Expected reply_to to be a MailUser, got {type(reply_to).__name__}")
            self.__reply_tos.append(reply_to)
            return self

        def add_reply_to(self, email: str, name: Optional[str] = None) -> Message.Builder:
            """Add a Reply-To recipient using an email address and optional name.

            This method constructs a MailUser object internally. If you have an existing
            MailUser object, use add_reply_to_mailuser() instead.

            Args:
                email (str): The Reply-To recipient's email address.
                name (Optional[str]): The Reply-To recipient's name, if any. Defaults to None.

            Returns:
                Message.Builder: Self for chaining.

            Raises:
                TypeError: If email is not a string (including if it is None) or name is provided and not a string.
            """
            if not isinstance(email, str):
                raise TypeError(f"Expected email to be a string, got {type(email).__name__}")
            if name is not None and not isinstance(name, str):
                raise TypeError(f"Expected name to be a string or None, got {type(name).__name__}")
            self.__reply_tos.append(MailUser(email, name))
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
            if self.__from is None:
                raise ValueError("Sender (from) is required")
            if not self.__tos:
                raise ValueError("At least one recipient (to) is required")
            if self.__subject is None:
                raise ValueError("Subject is required")
            if not self.__content:
                raise ValueError("At least one content item is required")

            return Message._Message__create(self.__subject, self.__from, self.__header_from, self.__attachments, self.__content,
                                   self.__tos, self.__cc, self.__bcc, self.__reply_tos)
