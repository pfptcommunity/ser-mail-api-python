import json

from ser_mail_api.v1 import *

if __name__ == "__main__":
    # Load API key
    with open("../ser.api_key", "r") as api_key_file:
        api_key_data = json.load(api_key_file)

    client = Client(api_key_data.get("client_id"), api_key_data.get("client_secret"))

    # Create a new Message object
    message = Message("This is a test email", MailUser("sender@proofpoint.com", "Joe Sender"))

    # Add content body
    message.add_content(Content("This is a test message", ContentType.Text))
    message.add_content(Content("<b>This is a test message</b>", ContentType.Html))

    # Add To
    message.add_to(MailUser("to_recipient1@proofpoint.com", "Recipient 1"))
    message.add_to(MailUser("to_recipien2@proofpoint.com", "Recipient 2"))

    # Add Cc
    message.add_cc(MailUser("cc_recipien1@proofpoint.com", "Carbon Copy 1"))
    message.add_cc(MailUser("cc_recipien2@proofpoint.com", "Carbon Copy 2"))

    # Add Bcc
    message.add_bcc(MailUser("bcc_recipien1@proofpoint.com", "Blind Carbon Copy 1"))
    message.add_bcc(MailUser("bcc_recipien2@proofpoint.com", "Blind Carbon Copy 2"))

    # Add Base64 encoded attachment
    message.add_attachment(Attachment("VGhpcyBpcyBhIHRlc3Qh", Disposition.Attachment, "test.txt", "text/plain"))

    # Add File attachment from disk, if disposition is not passed, the default is Disposition.Attachment
    message.add_attachment(FileAttachment(r"C:\temp\file.csv", Disposition.Attachment))

    # In the following example, we will create a byte stream from a string. This byte array is converted
    # to base64 encoding within the BinaryAttachment object
    text = "This is a sample text stream."

    # Convert the string into bytes
    bytes = text.encode("utf-8")

    # Add Byte array as attachment, if disposition is not passed, the default is Disposition.Attachment
    message.add_attachment(BinaryAttachment(bytes,"bytes.txt", "text/plain", Disposition.Attachment))

    result = client.send(message)

    print("HTTP Status", result.get_status())
    print("HTTP Reason", result.get_reason())

    print("Reason:", result.reason)
    print("Message ID:", result.message_id)
    print("Request ID:", result.request_id)
