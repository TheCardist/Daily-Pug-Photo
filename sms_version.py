import os
import praw
import random
from twilio.rest import Client
import keyring


def get_pug():
    '''Get a random pug image from the Pug Reddit page'''

    reddit = praw.Reddit(
    client_id= keyring.get_password('reddit', 'client-id'),
    client_secret= keyring.get_password('reddit', 'client-secret'),
    user_agent= "useragent",
    password= keyring.get_password('reddit', 'password'),
    username= keyring.get_password('reddit', 'username'),
    )

    sub = reddit.subreddit('pugs').top(time_filter='week', limit=100)

    submissions = []

    for post in sub:
        if not post.stickied and not post.is_self and not post.is_video:
            submissions.append(post.url)

    url = random.choice(submissions)

    return url


def get_contacts():
    with open('phone_contact.txt', 'r') as file:
        contacts = [contact.strip() for contact in file]
    return contacts


def send_sms(url, contacts):
    for item in contacts:
        # Set environment variables for your credentials
        account_sid = keyring.get_password('twilio', 'sid')
        auth_token = keyring.get_password('twilio', 'token')
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body="Pug of the day! 🐕\n Automated text, Please do not reply.",
            media_url=[f'{url}'],
            from_="+1234567890",
            to=f"+1{item}"
        )

        print(message.sid)


if __name__ == '__main__':
    url = get_pug()
    contacts = get_contacts()
    send_sms(url, contacts)
