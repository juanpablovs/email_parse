import imaplib
import email
import json
import re
from email.header import decode_header

# variables
fileName = "thisisthefilename.json"
recipient = "INBOX"

data = json.load(open(fileName))

fileNameMessagesInit = (len(data))

# for validating an Email
isValidEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

username = "<INSERT USERNAME>"
password = "<INSERT PASSWORD>"

imap = imaplib.IMAP4_SSL("imap-mail.outlook.com")

# authenticate
imap.login(username, password)

status, messages = imap.select(recipient)

# total number of emails
messages = int(messages[0])

messagesProcessed = 0
messagesDeleted = 0

def getEmailSecureserver(msg):
    for payload in msg.get_payload():
        pay = payload.get_payload()
        if isinstance(pay, str) and "To:" in pay:
            start = pay.find("To:") + 3
            end = pay.find("From") - 1
            return pay[start:end].strip()


def getGoogleEmail(msg):
    payload = msg.get_payload(decode=True).decode()
    start = payload.find("To:") + 3
    end = payload.find("From") - 1
    return payload[start:end].strip()



for i in range(1, messages + 1):
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            rejectFrom = msg.get_all('From', [])

            if "mailer-daemon@secureserver.net" in rejectFrom:
                emailToSave = getEmailSecureserver(msg)
                if re.fullmatch(isValidEmail, emailToSave):
                    if emailToSave not in data:
                        messagesProcessed += 1
                        data.append(emailToSave)
                    if imap.store(str(i), "+FLAGS", "\\Deleted"):
                        messagesDeleted += 1

            if "postmaster@secureserver.net" in rejectFrom:
                emailToSave = getEmailSecureserver(msg)
                if re.fullmatch(isValidEmail, emailToSave):
                    if emailToSave not in data:
                        messagesProcessed += 1
                        data.append(emailToSave)
                    if imap.store(str(i), "+FLAGS", "\\Deleted"):
                        messagesDeleted += 1


#deletes marked emails
imap.expunge()

with open(fileName, 'w') as f:
    json.dump(data, f)

print(f'filename: {fileName}')
print(f'initial number of emails in file: {fileNameMessagesInit}')
print(f'final number of emails in file: {(len(data))}')
print(f'initial number of email messages: {messages}')
print(f'emails added: {messagesProcessed}')
print(f'emails deleted: {messagesDeleted}')
status, messagesLeft = imap.select(recipient)
print(f'emails left: {int(messagesLeft[0])}')

imap.close()
imap.logout()