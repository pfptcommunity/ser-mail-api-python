# Proofpoint Secure Email Relay Mail API Python Library

[![PyPI Downloads](https://static.pepy.tech/badge/ser-mail-api)](https://pepy.tech/projects/ser-mail-api)  
This library implements all the functions of the SER Email Relay API via Python.

## Requirements

- Python 3.9+
- `requests`
- `requests-oauth2client`
- `pysocks`
- Active Proofpoint SER API credentials

### Installing the Package

You can install the tool using the following command directly from GitHub:

```bash
pip install git+https://github.com/pfptcommunity/ser-mail-api-python.git
```

Alternatively, you can install the tool using pip:

```bash
# Note: This may not work on Ubuntu 24.04:
pip install ser-mail-api
```

If you encounter an error similar to the following:

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

You should install `pipx` or configure your own virtual environment and use the command referenced above:

```bash
pipx install ser-mail-api
```

## Features

- **Send Emails**: Easily compose and send emails with minimal code using a fluent builder pattern.
- **Support for Attachments**:
    - Attach files from disk
    - Encode attachments as Base64
    - Send byte[] attachments
- **Support for Inline HTML Content**:
    - Using the syntax `<img src="cid:logo">`
    - Content-ID can be set manually or auto-generated
- **HTML & Plain Text Content**: Supports both plain text and HTML email bodies.
- **Recipient Management**: Add `To`, `CC`, and `BCC` recipients with ease.
- **Reply Management**: Add `Reply-To` addresses to redirect replies.

## Quick Start

```python
from ser_mail_api.v1 import *

if __name__ == "__main__":
  # Initialize the Client with OAuth credentials from the config
  client = Client("<client_id>", "<client_secret>")

  # Use the fluent builder to construct and send an email
  message = (
    Message.Builder()
    .subject("This is a test email")
    .sender("sender@example.com", "Joe Sender")
    .add_content("This is a test message", ContentType.Text)
    .add_to("recipient1@example.com", "Recipient 1")
    .build()
  )

  # Send the message asynchronously and wait for the result
  result = client.send(message)

  # Output the HTTP status code from the API response
  print("HTTP Response: {}/{}".format(result.get_status(), result.get_reason()))
  # Output the message ID from the API response
  print("Message ID:", result.message_id)
  # Output the reason (if any) from the API response
  print("Reason:", result.reason)
  # Output the request ID from the API response
  print("Request ID:", result.request_id)
```

## Advanced Emails

```python
from ser_mail_api.v1 import *

if __name__ == "__main__":
  # Initialize the Client with OAuth credentials from the config
  client = Client("<client_id>", "<client_secret>")

  # Construct logo_a attachment with dynamic content ID
  logo_b = (
    Attachment.Builder()
    .from_file("c:/temp/logo_b.png")  # Load logo_b from file
    .disposition_inline()  # Set dynamic content ID
    .build()
  )

  # Use the fluent builder to construct the Message in a single chain
  message = (
    Message.Builder()
    .subject("This is a test email")  # Sets the email subject (required)
    .sender("sender@example.com", "Joe Sender")  # Sets the sender (required)
    .add_content("This is a test message", ContentType.Text)  # Adds plain text content (required minimum)
    .add_content(  # Required: Adds HTML content referencing both static and dynamic CIDs
      f"<b>Static CID</b><br><img src=\"cid:logo\"><br><b>Dynamic CID</b><br><img src=\"cid:{logo_b.cid}\">",
      ContentType.Html)  # Uses logo_b's auto-assigned content ID retrieved from logo_b.cid
    .add_attachment(Attachment.Builder()
                    .from_file("C:/temp/logo_a.png")
                    .disposition_inline("logo")
                    .build())  # Adds an inline attachment with content ID "logo"
    .add_attachment(logo_b)  # Adds logo_b with its dynamically assigned content ID
    .add_to("recipient1@example.com", "Recipient 1")  # Adds a primary recipient (required minimum)
    .add_to("recipient2@example.com", "Recipient 2")  # Adds a second primary recipient
    .add_cc("cc1@example.com", "CC Recipient 1")  # Adds a CC recipient
    .add_cc("cc2@example.com", "CC Recipient 2")  # Adds a second CC recipient
    .add_bcc("bcc1@example.com", "BCC Recipient 1")  # Adds a BCC recipient
    .add_bcc("bcc2@example.com", "BCC Recipient 2")  # Adds a second BCC recipient
    .add_attachment(Attachment.Builder()
                    .from_base64("VGhpcyBpcyBhIHRlc3Qh", "test.txt")
                    .build())  # Adds an attachment from Base64-encoded text
    .add_attachment(Attachment.Builder()
                    .from_file("C:/temp/file.csv")
                    .build())  # Adds an attachment from a file
    .add_attachment(Attachment.Builder()
                    .from_bytes(b"Sample bytes", "bytes.txt")
                    .mime_type("text/plain")
                    .build())  # Adds an attachment from a byte array
    .header_from("fancysender@example.com", "Header From")  # Sets the header "From" field
    .add_reply_to("noreply@proofpoint.com", "No Reply")  # Sets a Reply-To address
    .build()  # Constructs the Message, enforcing required fields (from, tos, subject, content)
  )

  # Send the message asynchronously and wait for the result
  result = client.send(message)

  # Output the HTTP status code from the API response
  print("HTTP Response: {}/{}".format(result.get_status(), result.get_reason()))
  # Output the message ID from the API response
  print("Message ID:", result.message_id)
  # Output the reason (if any) from the API response
  print("Reason:", result.reason)
  # Output the request ID from the API response
  print("Request ID:", result.request_id)
```

## Attachment MIME Type Deduction Behavior

When creating attachments, the library automatically attempts to determine the MIME type. This detection is based on:

- The `filename` argument when using `Attachment.from_bytes` or `Attachment.from_base64`.
- The `filepath` when using `Attachment.from_file`.

If the MIME type cannot be determined, an exception will be raised.

```python
from ser_mail_api.v1 import *

if __name__ == "__main__":
    # Create an attachment from disk; the MIME type will be "application/vnd.ms-excel", and disposition will be "Disposition.Attachment"
    Attachment.Builder().from_file("C:/temp/file.csv").build()
    # This will throw an error, as the MIME type is unknown
    Attachment.Builder().from_file("C:/temp/file.unknown").build()
    # Create an attachment and specify the type information. The disposition will be "Disposition.Attachment", filename will be unknown.txt, and MIME type "text/plain"
    Attachment.Builder().from_file("C:/temp/file.unknown").filename("unknown.txt").build()
    # Create an attachment and specify the type information. The disposition will be "Disposition.Attachment", filename will be file.unknown, and MIME type "text/plain"
    Attachment.Builder().from_file("C:/temp/file.unknown").mime_type("text/plain").build()
```

## Inline Attachments and Content-IDs

When creating attachments, they are `Disposition.Attachment` by default. To use a **Content-ID** (e.g.,
`<img src="cid:logo">`) in HTML content, set the disposition to `Disposition.Inline`. The library supports both manual
and auto-generated content IDs.

### Using Dynamically Generated Content-ID

The example below demonstrates how to create inline content with a dynamically generated Content-ID inside an HTML
message body.

```python
from ser_mail_api.v1 import *

if __name__ == "__main__":
  # Create an inline attachment with an auto-generated content ID
  logo = Attachment.Builder().from_file("C:/temp/logo.png").disposition_inline().build()

  # Use the dynamic content ID in HTML content
  message = (Message.Builder()
             .subject("Dynamic CID Test")
             .sender("sender@example.com")
             .add_to("recipient@example.com")
             .add_content(f"<b>Test</b><br><img src=\"cid:{logo.cid}\">", ContentType.Html)
             .add_attachment(logo)
             .build())
```

### Setting a Custom Content-ID

The example below demonstrates how to create inline content with a custom Content-ID inside an HTML message body.

```python
from ser_mail_api.v1 import *

if __name__ == "__main__":
  message = (Message.Builder()
             .subject("Static CID Test")
             .sender("sender@example.com")
             .add_to("recipient@example.com")
             .add_content("<b>Test</b><br><img src=\"cid:logo\">", ContentType.Html)
             .add_attachment(Attachment.Builder()
                             .from_file("C:/temp/logo.png")
                             .disposition_inline("logo")
                             .build())
             .build())
```

### Proxy Support

Socks5 Proxy Example:

```python
from ser_mail_api.v1 import *

if __name__ == '__main__':
    client = Client("<client_id>", "<client_secret>")
    credentials = "{}:{}@".format("proxyuser", "proxypass")
    client._session.proxies = {'https': "{}://{}{}:{}".format('socks5', credentials, '<your_proxy>', '8128')}
```

HTTP Proxy Example (Squid):

```python
from ser_mail_api.v1 import *

if __name__ == '__main__':
    client = Client("<client_id>", "<client_secret>")
    credentials = "{}:{}@".format("proxyuser", "proxypass")
    client._session.proxies = {'https': "{}://{}{}:{}".format('http', credentials, '<your_proxy>', '3128')}

```

### HTTP Timeout Settings

```python
from ser_mail_api.v1 import *

if __name__ == '__main__':
    client = Client("<client_id>", "<client_secret>")
    # Timeout in seconds, connect timeout
    client.timeout = 600
    # Timeout advanced, connect / read timeout
    client.timeout = (3.05, 27)
```

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
Status Code: 400/BadRequest
Message ID:
Reason: attachments[0].content is required
Request ID: fe9a1acf60a20c9d90bed843f6530156
Raw JSON: {"request_id":"fe9a1acf60a20c9d90bed843f6530156","reason":"attachments[0].content is required"}
```

This issue has been reported to **Proofpoint Product Management**.

## Limitations

- The Proofpoint API currently does not support **empty file attachments**.
- If an empty file is sent, you will receive a **400 Bad Request** error.

## Additional Resources

For more information, refer to the official **Proofpoint Secure Email Relay API documentation**:  
[**API Documentation**](https://api-docs.ser.proofpoint.com/docs/email-submission)
