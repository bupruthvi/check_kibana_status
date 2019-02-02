import datetime
import smtplib
import config
import json
import os
from email.mime.text import MIMEText

SMTP_PORT=587 #give smtp port
SMTP_SERVER='smtp.gmail.com' #smtp server

def send_email(sender, reciever, down):
    subject='The following Kibana services may be down'
    all_kibana_services=""

    for services in down:
        all_kibana_services = all_kibana_services + str(services) + "<br>"

    html = """\
        <html>
            <head>Following services are either down or not listening. Please take an action as soon as possible:</br></head>
            <body>
                <p>""" + all_kibana_services + """</p>
                <p>Regards, ESaaS</p>
            </body>
        </html>
        """

    msg = MIMEText(html,'html')
    msg['SUBJECT']=subject
    msg['FROM']=sender
    msg['TO']=reciever

    s = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
    s.starttls()
    s.login(config.username,config.password)
    s.sendmail(sender,reciever,msg.as_string())
    print ("Sending email...\nEmail Sent!")
    s.quit()

x=0
down_services=[]

with open('kibana_services.json', 'r') as json_file:
    data = json.load(json_file)
    for key, value in data.items():
        for da in data:
            for d in data[da]:
                while x<len(data[da][d]):
                    resp = os.system('ping ' + data[da][d][x] + ' -c 1')
                    if resp == 0:
                        pass
                    else:
                        down_services.append("Service from " + str(key) + " : " + str(data[da][d][x]) + " time: " + str(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")))
                    x+=1
                x=0

if len(down_services)>0:
    send_email(config.username,config.username,down_services)
