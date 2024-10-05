from googleapiclient.discovery import build
import base64
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def authenticate_gmail():
    creds = None
    #token.json stores the user's access and refresh tokens, and is
    #created when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    #If there are no credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        #save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def fetch_emails(service, query):
    try:
        result = service.users().messages().list(userId='me', q=query).execute()
        messages = result.get('messages', [])

        if not messages:
            print('No messages found.')
            return []

        for msg in messages[:10]:  #limit to first 10 emails
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            msg_snippet = msg_data['snippet']
            msg_subject = ''
            msg_from = ''
            for header in msg_data['payload']['headers']:
                if header['name'] == 'Subject':
                    msg_subject = header['value']
                if header['name'] == 'From':
                    msg_from = header['value']
            print(f'Message from: {msg_from}\nSubject: {msg_subject}')

        return messages

    except HttpError as error:
        print(f'An error occurred: {error}')
        return []


def add_label_to_email(service, email_id, label_id):
    try:
        service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'addLabelIds': [label_id]}
        ).execute()
        print(f'Added label {label_id} to email ID: {email_id}')
    except HttpError as error:
        print(f'An error occurred: {error}')


def filter_emails_by_keyword(service, keyword, label_id):
    try:
        query = f'subject:{keyword}'
        messages = fetch_emails(service, query)
        if not messages:
            print(f'No emails found with subject containing "{keyword}"')
            return

        for msg in messages:
            add_label_to_email(service, msg['id'], label_id)

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    service = authenticate_gmail()

    if service:
        #set the label ID from the fetched labels
        label_id = "IMPORTANT"  #you can change this to another valid label ID
        keyword = "Important: New SWE roles for CS Students"  #customize this keyword

        #apply the label to emails that match the keyword in the subject
        filter_emails_by_keyword(service, keyword, label_id)
