import time
import os
import praw
import random
import smtplib
from email.message import EmailMessage
import keyring

# TODO: Refactor 

reddit = praw.Reddit(
    client_id= keyring.get_password('reddit', 'client-id'),
    client_secret= keyring.get_password('reddit', 'client-secret'),
    user_agent= "useragent",
    password= keyring.get_password('reddit', 'password'),
    username= keyring.get_password('reddit', 'username'),
)

def get_contacts():
	"""Get the individual contacts from the txt file."""
    addresses = []

    with open('contacts.txt', 'r') as data:
        addresses = [line.strip() for line in data]
    name = [line.split(', ')[0] for line in addresses]
    email = [line.split(', ')[1:][0] for line in addresses]

    send(name, email)

def send(name, email):
	"""Getting a random pug photo from Reddit and then emailing to contacts"""
	
    sub = reddit.subreddit('pugs').top(time_filter='week', limit=100)

    submissions = []

    for post in sub:
        if not post.stickied and not post.is_self:
            submissions.append(post.url)

    url = random.choice(submissions)

    for n, e in zip(name, email):
        contact_name = n.strip()
        email_to = e.strip()

        msg = EmailMessage()
        msg['Subject'] = "Daily Pug Delivery"
        msg['From'] = 'email@address.com'
        msg['To'] = email_to
        msg.set_content("Plain Text")
        msg.add_alternative(f"""\
            <!DOCTYPE html>
            <html>
                <body>
                    <p>Hi {contact_name}, here is your daily <a href="{url}">Pug!</a></p>
                    </br>
                    <p> This pug has been brought to you by an automated Pug finder.</p>
                </body>
            </html>
            """, subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('email@address.com', 'passsword')
            smtp.send_message(msg)

get_contacts()
