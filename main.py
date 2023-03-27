import os
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup


# Environment variables for hiding data from public
sender_email = os.environ['MY_SENDER_EMAIL']
sender_pass = os.environ['MY_SENDER_PASS']
receiver_email = os.environ['RECEIVER_EMAIL']
phone_num = os.environ['PHONE_NUM']


# Send a request to the website and get its HTML content
url = "https://www.alim.org/hadith-of-the-day/"
response = requests.get(url)
html_content = response.content

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Get the hadith text inside div of class 
hadith_text = (soup.find("div", class_="hadith-text")).text
# print(hadith_text)

# Get the reference of the Hadith from div tag
hadith_ref = (soup.find("div", class_="btn btn-small hadith-of-day-ref")).text
# print(hadith_ref)


# create a message
msg = MIMEMultipart("alternative")
# msg['From'] = sender_email
# msg['From'] = 'Daily Quote <sender@gmail.com>'
msg['From'] = 'Daily Hadith'
msg['To'] = receiver_email
# Generating random string to add to subject in order not to grouped the message in recepients inbox
msg['Subject'] = f"Today's Hadith - ({str(uuid.uuid4())[:7]})"
# msg['Subject'] = f'Hello There - {datetime.datetime.now()}'


# Create the HTML email body with the quote and author
html = """
<html>
  <head>
    <style>
      /* Add some styling to the email body */
      p {{
        color: black;
        font-size: 16px;
        line-height: 1.5;
      }}
    </style>
  </head>
  <body style="font-family: Arial, sans-serif; background-color: #F0ceff; padding: 20px;">
    <h1 style="color: black; font-size: 28px; font-weight: bold; margin-top: 0;">Your Daily Hadith</h1>
    <p>Salam,</p>
    <p>Today's Hadith is:</p>
    <p style="color:purple; font-size: 18px; font-family: 'Lucida Bright'; line-height: 1.5;">"{}"</p>
    <p>- {}</p>
    <hr>
    <p>Thank you for subscribing to my daily Hadith service. I hope that the Hadith we share with you each day serves as a reminder of the beautiful teachings of Islam and brings you peace and inspiration.</p>
    <p>Best regards, Musawer Khan</p>
    <p>WhatsApp Me: {}</p>
  </body>
</html>
""".format(hadith_text, hadith_ref, phone_num)


# Create a MIMEText object to represent the HTML body
html_part = MIMEText(html, "html")

# Attach the HTML body to the email message
msg.attach(html_part)

# create a secure SSL/TLS connection to Gmail's SMTP server
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(sender_email, sender_pass)

# send the message
server.sendmail(sender_email, receiver_email, msg.as_string())

# close the connection to the SMTP server
server.quit()

print("Email sent Successful. ")
