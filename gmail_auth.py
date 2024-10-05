import os.path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

#first we need to define the scope we are requesting for the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def authenticate_gmail():
    creds = None
    #check if we already have a token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    #if no valid credentials, we need to log in and get them
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        #save the credentials for future runs
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


#to call the authentication function
service = authenticate_gmail()
print("Authenticated Successfully!")
