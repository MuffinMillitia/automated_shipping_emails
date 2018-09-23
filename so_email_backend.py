from fishwrapper import Fishbowlapi
import pandas as pd
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import connecttest


class EmailBackend:
    def __init__(self):
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.host = "stmp.gmail.com"
        self.port = 587
        self.my_email = None
        self.my_password = None
        self.subject = "Comm/Net Systems Automated Shipping Notice"
        self.so_data = None
        with open("sample query.txt") as file:
            self.query = file.read()
        self.recipient_data = pd.read_excel("sample email list.xlsx")
        self.groups = None

    def find_sales_orders(self):
        # results = connecttest.create_connection_second_option(sql=self.query, port=28193, ip="192.168.10.54")
        # excel = connecttest.makeexcelsheet(results)
        # connecttest.save_workbook(excel, ".", "so_data.xlsx")
        self.so_data = pd.read_excel("so_data.xlsx")
        self.so_data["ShipDate"] = self.so_data["ShipDate"].apply(self.trunc_cell)
        self.so_data = self.so_data[self.so_data["ShipDate"] == "2018-09-21"].set_index("ShipDate", drop=True)
        self.groups = set(self.so_data["LocGroup"].tolist())
        print(self.so_data)
        print(self.groups)

    def send_messages(self):
        # s = smtplib.SMTP(host=self.host, port=self.port)
        # s.starttls()
        # s.login(self.my_email, self.my_password)
        for group in self.groups:
            print(group)
            try:
                emails = self.recipient_data[self.recipient_data["SO Region"] == group]["Email"].tolist()[0].split(";")
            except IndexError:
                print("Email for group", group, "not found.")
                continue
            for email in emails:
                if len(email) < 5:
                    continue
                message = MIMEMultipart()

                message["From"] = self.my_email
                message["To"] = email
                message["Subject"] = self.subject
                message_text = self.so_data[self.so_data["LocGroup"] == group].to_string()
                message.attach(MIMEText(message_text, "plain"))
                print("Sending message to", email)
                print(message_text, "\n")
                # s.send_message(message)

    @staticmethod
    def read_template(file_name):
        with open(file_name) as file:
            file_content = file.read()
        return Template(file_content)

    @staticmethod
    def trunc_cell(string):
        return string[:10]

    def run(self):
        self.find_sales_orders()
        self.send_messages()


if __name__ == "__main__":
    email_backend = EmailBackend()
    email_backend.find_sales_orders()
    email_backend.send_messages()