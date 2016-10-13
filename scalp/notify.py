import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


def send_email(email_config=None, file=None):
    """
    Helper method to send email notifications containing scalp output files.
    """
    if email_config is None or file is None:
        print ('Requires email credentials and file location.')
        return False
    # Get data from email_config
    server = email_config.get('host', 'localhost')
    port = email_config.get('port', '587')
    username = email_config.get('username', '')
    password = email_config.get('password', '')
    from_address = email_config.get('from', 'no-reply@localhost')
    recipients = email_config.get('recipients', [])
    todays_date = formatdate(localtime=True)

    # Setup mail credentials
    try:
        smtp = smtplib.SMTP('{0}:{1}'.format(server, port))
    except Exception as e:
        print ('Unable to crate an SMTP object from server:port. %s' % str(e))
        return False

    # Create message object
    msg = MIMEMultipart('alternative')
    msg['From'] = from_address
    msg['To'] = ','.join(recipients)
    msg['Date'] = todays_date
    msg['Subject'] = 'Apache Scalp Error Logs {}'.format(todays_date)

    msg.attach(MIMEText("Today's Apache logs are attached as HTML.", 'plain'))

    # Attach file to email
    try:
        with open(file, 'rb') as html:
            msg.attach(MIMEText(bytes.decode(html.read()), 'html'))
    except Exception as e:
        print ('Unable to attach HTML file to email message. %s' % str(e))
        return False

    # Start smtp authentication
    try:
        smtp.starttls()
        smtp.login(username, password)
    except Exception as e:
        print ('Cannot authenticate with username and password. %s' % str(e))
        return False

    # Send
    try:
        smtp.sendmail(from_address, recipients, msg.as_string())
    except Exception as e:
        print ('Sending email message failed. %s' % str(e))
        return False

    return True
