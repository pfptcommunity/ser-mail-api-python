# Proofpoint Secure Email Relay Mail API Package

[![PyPI Downloads](https://static.pepy.tech/badge/ser-mail-api)](https://pepy.tech/projects/ser-mail-api)  
Library implements all the functions of the SER Email Relay API via Python.

## Requirements
* Python 3.9+
* requests
* requests-oauth2client
* pysocks
* Active Proofpoint SER API credentials

### Installing the Package

You can install the tool using the following command directly from Github.

```
pip install git+https://github.com/pfptcommunity/ser-mail-api-python.git
```

or can install the tool using pip.

```
# When testing on Ubuntu 24.04 the following will not work:
pip install ser-mail-api
```

If you see an error similar to the following:

```
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.

    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.

    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.

    See /usr/share/doc/python3.12/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

You should use install pipx or you can configure your own virtual environment and use the command referenced above.

```
pipx install ser-mail-api
```

## Features

- **Send Emails**: Easily compose and send emails with minimal code.
- **Support for Attachments**
    - Attach files from disk
    - Encode attachments as Base64
    - Send byte[] attachments
- **Support for Inline HTML Content**
    - Using the following syntax `<img src=\"cid:logo\">`
    - Content-ID can be set manually or auto generated
- **HTML & Plain Text Content**: Supports both plain text and HTML email bodies.
- **Recipient Management**: Add `To`, `CC`, and `BCC` recipients with ease.
- **Reply Management**: Add 'Reply-To' addresses to redirect replies.

## Quick Start

```python
import json
from ser_mail_api.v1 import *

if __name__ == "__main__":
    client = Client("<client_id>", "<client_secret>")

    # Create a new Message object
    message = Message("This is a test email", MailUser("sender@example.com", "Joe Sender"))

    # Add text content body
    message.add_content(Content("This is a test message", ContentType.Text))

    # Add html content body, with embedded image.
    message.add_content(Content("<b>This is a test message</b><br><img src=\"cid:logo\">", ContentType.Html))
    # Create an inline attachment from disk and set the cid.
    message.add_attachment(Attachment.from_file("C:/temp/logo.png", disposition=Disposition.Inline, cid="logo"))

    # Add recipients
    message.add_to(MailUser("recipient1@example.com", "Recipient 1"))
    message.add_to(MailUser("recipient2@example.com", "Recipient 2"))

    # Add CC and BCC
    message.add_cc(MailUser("cc1@example.com", "CC Recipient 1"))
    message.add_bcc(MailUser("bcc1@example.com", "BCC Recipient 1"))

    # Add attachments
    message.add_attachment(Attachment.from_base64("VGhpcyBpcyBhIHRlc3Qh", "test.txt"))
    message.add_attachment(Attachment.from_file("C:/temp/file.csv"))
    message.add_attachment(Attachment.from_bytes(b"Sample bytes", "bytes.txt", "text/plain"))

    # Set or more Reply-To addresses
    message.add_reply_to(MailUser("noreply@proofpoint.com", "No Reply"))

    # Send the email
    result = client.send(message)

    print("HTTP Status:", result.get_status())
    print("HTTP Reason:", result.get_reason())
    print("Message ID:", result.message_id)
    print("Request ID:", result.request_id)
```

---

## Attachment mime type deduction behavior

When creating attachments, the library automatically attempts to determine the MIME type. This detection is based on:

- The `filename` argument when using `Attachment.from_bytes` or `Attachment.from_base64`.
- The `filepath` when using `Attachment.from_file`.

If the MIME type cannot be determined, an exception will be raised.

By default, attachments use `Disposition.Attachment`. If you need to reference an attachment using a **Content-ID** (
e.g., `<img src="cid:logo">`), you must explicitly set `Disposition.Inline`.

```python
from ser_mail_api.v1 import *

if __name__ == "__main__":
    # Create an attachment from disk, the mime type will be "application/vnd.ms-excel", and disposition will be "Disposition.Attachment"
    Attachment.from_file("C:/temp/file.csv")
    # This will throw an error, as the mime type is unknown.  
    Attachment.from_file("C:/temp/file.unknown")
    # Create an attachment and specify the type information. The disposition will be "Disposition.Attachment", filename will be unknown.txt, and mime type "text/plain"
    Attachment.from_file("C:/temp/file.unknown", filename="unknown.txt")
    # Create an attachment and specify the type information. The disposition will be "Disposition.Attachment", filename will be file.unknown, and mime type "text/plain"
    Attachment.from_file("C:/temp/file.unknown", mime_type="text/plain")
```

---

## Known Issues

There is a known issue where **empty file content** results in a **400 Bad Request** error.

```json
{
  "content": "",
  "disposition": "attachment",
  "filename": "empty.txt",
  "id": "1ed38149-70b2-4476-84a1-83e73913d43c",
  "type": "text/plain"
}
```

🔹 **API Response:**

```
Status Code: 400 BadRequest
Message ID:
Reason: attachments[0].content is required
Request ID: fe9a1acf60a20c9d90bed843f6530156
Raw JSON: {"request_id":"fe9a1acf60a20c9d90bed843f6530156","reason":"attachments[0].content is required"}
```

This issue has been reported to **Proofpoint Product Management**.

---

## Limitations

- Currently, **empty attachments are not supported** by the API.
- No other known limitations.

---

## Additional Resources

For more information, refer to the official **Proofpoint Secure Email Relay API documentation**:  
[**API Documentation**](https://api-docs.ser.proofpoint.com/docs/email-submission)
