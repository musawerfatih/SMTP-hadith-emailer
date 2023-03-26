import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests


# get today's quote and its author using API
response = requests.get("https://zenquotes.io/api/today")
data = response.json()

today_quote = data[0]["q"]
auth = data[0]["a"]


# create a message
msg = MIMEMultipart("alternative")
# msg['From'] = 'twitterdvlpr@gmail.com'
# msg['From'] = 'Daily Quote <sender@gmail.com>'
msg['From'] = 'Daily Quote'
msg['To'] = 'musawerfatih@gmail.com'
msg['Subject'] = "Today's Quote"


# Define the quote and author information
quote = today_quote.strip()
author = auth

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

    <h1 style="color: black; font-size: 28px; font-weight: bold; margin-top: 0;">Your Daily Quote</h1>

    <p>Hello there,</p>
    <p>Today's quote is:</p>
    <p style="color:purple; font-size: 20px; font-family: 'Lucida Bright'; line-height: 1.5;">"{}"</p>
    <p>- {}</p>
    <p>Thank you for using my daily quote free service. I hope this quote inspires and motivates you throughout your day.</p>
    <p>Best regards, Musawer Khan</p>
    <p>WhatsApp Me: 03408848212</p>
  </body>
</html>
""".format(quote, author)


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
