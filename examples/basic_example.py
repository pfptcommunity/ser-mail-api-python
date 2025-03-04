import json

from ser_mail_api.v1 import *

if __name__ == "__main__":
    # Load API key
    with open("../ser.api_key", "r") as api_key_file:
        api_key_data = json.load(api_key_file)

    # Initialize the Client with OAuth credentials from the config
    client = Client(api_key_data.get("client_id"), api_key_data.get("client_secret"))

    # Use the fluent builder to construct and send an email
    message = (
        Message.Builder()
        .subject("This is a test email")
        .from_address("sender@example.com", "Joe Sender")
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
