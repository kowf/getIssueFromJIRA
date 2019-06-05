import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml
import base64

#read config

with open("c:/Users/KathyKo/Desktop/getissue.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

url = config['JIRA']['domain']+"/rest/api/3/search"
querystring = {"jql":"project='"+config['JIRA']['projectName']+"' and created > '-" +config['frequency']+"'"}

secret = config['JIRA']['email']+':'+config['JIRA']['token']

auth = str(base64.b64encode(secret.encode('utf-8')),'utf-8')

headers = {
    'Accept': "application/json",
    'Authorization': "Basic "+auth,
    'Cache-Control': "no-cache",
    }

response = requests.request("GET", url, headers=headers, params=querystring).json()
print(response['total'])

if response['total']>0:

    #curate the email content
    content = """\
    <html>
    <head></head>
    <body>
        <h3>Total: {total}</h3>
    """.format(total = str(response['total']))

    for issue in response['issues']:
        result = { 'key':issue['key'],
                    'summary':issue['fields']['summary'],
                    'priority':issue['fields']['priority']['name'],
                    'status':issue['fields']['status']['name'],
                    'created':issue['fields']['created']}
        content += f"""\
            <a href={config['JIRA']['domain']}"""
        content +="""/browse/{key}">{key}</a> 
            <strong>Priority: </strong> {priority} <strong>Status: </strong>{status} <strong>Created: </strong>{created} 
            <div>{summary}</div><br>
        """.format_map(result)

    content += """\
            </body>
        </html>
        """

    #email--content
    msg = MIMEMultipart() 

    msg['Subject'] = "New issue on OCCITPOT JIRA"
    msg['From']=config['mailing']['senderEmail']
    msg['To']=config['mailing']['mailingList']

    msg.attach(MIMEText(content, 'html'))

    #email--connection
    mail = smtplib.SMTP(config['mailing']['host'],config['mailing']['port'])
    
    mail.ehlo()

    mail.starttls()

    mail.login(config['mailing']['senderEmail'],config['mailing']['password'])

    mail.send_message(msg)

    mail.close()