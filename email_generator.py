from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#update with your email and password.
MY_ADDRESS = 'you_email_address'
PASSWORD = 'your_password'


def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for contact in contacts_file:
            names.append(contact.rsplit(' ', 1)[0])
            emails.append(contact.rsplit(' ', 1)[1])
    return names, emails


def read_template(filename):
    with open(filename, mode='r', encoding='utf-8') as template_file:
        template_content = template_file.read()
    return Template(template_content)


def main():
    names, emails = get_contacts('contacts.txt')
    message_template = read_template('message.txt')

    # set up SMTP server. Use different host and port if not using gmail.
    s = smtplib.SMTP(host='smtp.gmail.com', port='587')
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    for name, email in zip(names, emails):
        msg = MIMEMultipart()
        message = message_template.substitute(PERSON_NAME=name.title())
        print(message)
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = "some_subject here"  #customize subject.
        msg.attach(MIMEText(message, 'plain'))
        s.send_message(msg)
        del msg
    s.quit()


if __name__ == '__main__':
    main()
