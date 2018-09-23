import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


def read_template(file_name):
    with open(file_name) as file:
        file_content = file.read()
    return Template(file_content)


my_address = "matuskajd@gmail.com"
contact_address = "j.matuska@icloud.com"

s = smtplib.SMTP(host="smtp.gmail.com", port=587)
s.starttls()
s.login(my_address, "njorumsfuylelnmg")

message_template = read_template("message.txt")
msg = MIMEMultipart()

sales_order = "123456"
date = datetime.datetime.now().strftime("%Y-%m-%d")
ship_company = "Acme"
tracking_number = "135792468"
subject = "Automated Shipping Notice"

message = message_template.substitute(SALES_ORDER=sales_order, SHIP_DATE=date,
                                      SHIP_COMPANY=ship_company, TRACKING_NUMBER=tracking_number)

msg["From"] = my_address
msg["To"] = contact_address
msg["Subject"] = subject

msg.attach(MIMEText(message, "plain"))

s.send_message(msg)

del msg