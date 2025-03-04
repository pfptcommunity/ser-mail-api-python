import json

from ser_mail_api.v1 import *

if __name__ == "__main__":
    # Load API key
    with open("../ser.api_key", "r") as api_key_file:
        api_key_data = json.load(api_key_file)

    # Initialize the Client with OAuth credentials from the config
    client = Client(api_key_data.get("client_id"), api_key_data.get("client_secret"))

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
        .subject("This is a test email") # Sets the email subject (required)
        .from_address("sender@example.com", "Joe Sender") # Sets the sender (required)
        .add_content("This is a test message", ContentType.Text) # Adds plain text content (required minimum)
        .add_content( # Required: Adds HTML content referencing both static and dynamic CIDs
            f"<b>Static CID</b><br><img src=\"cid:logo\"><br><b>Dynamic CID</b><br><img src=\"cid:{logo_b.cid}\">",
            ContentType.Html) # Uses logo_b's auto-assigned content ID retrieved from logo_b.cid
        .add_attachment(Attachment.Builder()
                        .from_file("C:/temp/logo_a.png")
                        .disposition_inline("logo")
                        .build()) # Adds an inline attachment with content ID "logo"
        .add_to("recipient1@example.com", "Recipient 1") # Adds a primary recipient (required minimum)
        .add_to("recipient2@example.com", "Recipient 2") # Adds a second primary recipient
        .add_cc("cc1@example.com", "CC Recipient 1") # Adds a CC recipient
        .add_cc("cc2@example.com", "CC Recipient 2") #  Adds a second CC recipient
        .add_bcc("bcc1@example.com", "BCC Recipient 1") #  Adds a BCC recipient
        .add_bcc("bcc2@example.com", "BCC Recipient 2") # Adds a second BCC recipient
        .add_attachment(Attachment.Builder()
                        .from_base64("VGhpcyBpcyBhIHRlc3Qh", "test.txt")
                        .build()) # Adds an attachment from Base64-encoded text
        .add_attachment(Attachment.Builder()
                        .from_file("C:/temp/file.csv")
                        .build()) # Adds an attachment from a file
        .add_attachment(Attachment.Builder()
                        .from_bytes(b"Sample bytes", "bytes.txt")
                        .mime_type("text/plain")
                        .build()) # Adds an attachment from a byte array
        .header_from("fancysender@example.com", "Header From") # Sets the header "From" field
        .add_reply_to("noreply@proofpoint.com", "No Reply") # Sets a Reply-To address
        .build() # Constructs the Message, enforcing required fields (from, tos, subject, content)
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
