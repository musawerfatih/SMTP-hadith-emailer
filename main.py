import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import uuid
from bs4 import BeautifulSoup

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
# msg['From'] = 'twitterdvlpr@gmail.com'
# msg['From'] = 'Daily Quote <sender@gmail.com>'
msg['From'] = 'Daily Hadith'
msg['To'] = 'musawerfatih@gmail.com'
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
    <p style="color:purple; font-size: 19px; font-family: 'Lucida Bright'; line-height: 1.5;">"{}"</p>
    <p>- {}</p>
    <p> </p>
    <hr>
    <p>Thank you for subscribing to my daily Hadith service. I hope that the Hadith we share with you each day serves as a reminder of the beautiful teachings of Islam and brings you peace and inspiration.</p>
    <p>Best regards, Musawer Khan</p>
    <p>WhatsApp Me: 03408848212</p>
  </body>
</html>
""".format(hadith_text, hadith_ref)



# Create a MIMEText object to represent the HTML body
html_part = MIMEText(html, "html")

# Attach the HTML body to the email message
msg.attach(html_part)


# create a secure SSL/TLS connection to Gmail's SMTP server
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login('twitterdvlpr@gmail.com', 'jtaulhaejigtosxp')

# send the message
server.sendmail('twitterdvlpr@gmail.com', 'musawerfatih@gmail.com', msg.as_string())

# close the connection to the SMTP server
server.quit()

print("Email sent Successful. ")
