import os
import uuid
import smtplib
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Environment variables for hiding secret data from public
sender_email = os.environ['MY_SENDER_EMAIL']
sender_pass = os.environ['MY_SENDER_PASS']
receiver_email = os.environ['RECEIVER_EMAIL']
phone_num = os.environ['PHONE_NUM']


# Send request to the website and get its HTML content
url = "https://www.alim.org/hadith-of-the-day/"
response = requests.get(url)
html_content = response.content

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Get the hadith text inside div of class 
hadith_text = (soup.find("div", class_="hadith-text")).text
hadith_ref = (soup.find("div", class_="btn btn-small hadith-of-day-ref")).text


# create a message
msg = MIMEMultipart("alternative")
msg['From'] = 'Daily Hadith'
msg['To'] = receiver_email
# Generating random string to add to subject in order not to grouped the messages in recepients inbox
# msg['Subject'] = f"Today's Hadith - ({str(uuid.uuid4())[:7]})"
msg['Subject'] = f"Today's Hadith - {datetime.now().strftime('(%d-%m-%Y)')}"


# Create the HTML email body with the quote and reference
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
    <p>Salam,<br>Today's Hadith is:</p>
    <p style="color:purple; font-size: 18px; font-family: 'Lucida Bright'; line-height: 1.5; font-style: italic;">"{}"</p>
    <p>- {}</p>
    <hr>
    <p>Thank you for subscribing to my daily Hadith service. I hope that the Hadith, shared with you each day, serves as a reminder of the beautiful teachings of Islam and brings you peace and inspiration.</p>
    <center><p>Best regards, Musawer Khan <br>WhatsApp me: {}</p></center>
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

print("Hadith emailed successfully. ")
