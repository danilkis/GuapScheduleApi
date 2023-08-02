import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

# Initialize the app with a service account
cred = credentials.Certificate("Cloud/guapschedule-firebase-adminsdk-3j62u-c9d211d7ab.json")
firebase_admin.initialize_app(cred)

def notify_schedule():
    # Define the message payload
    message = messaging.Message(
        notification=messaging.Notification(
            title="Расписание",
            body="В расписании появились изменения"
        ),
        topic="schedule"
    )

    # Send the message
    response = messaging.send(message)
    print("Successfully sent message:", response)