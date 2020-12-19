# pyAutoMailer
a simple Mailer - should run once a day and check config for birthday or other periodic mails to send.

## Functional Description
pyAutoMail.py reads the config.json file.

The config consists of two sections. The Email-Config-section - and the Event-Section.

For all Events - the date and the execution intervall is checked. Valid intervalls are : yearly, monthly, daily.
Two event-actions are implemented - Send simple-Mail to receiver - it ready a configured simple txt file and send the content; and a Happy-Birthday-Email.

The Happy-Birthday-Action is a bit more complex. 
The folder hb contains a configured template - "content" - which then build a email from "anrede" (greeting-intro) - a random txt-file with a little poem or text and a greeting pose - and also adds a picture. Due to copyright-issues the repository just contains some random text-jpg.

## Installation

Requisits: 'pip install html2text'

Pretty just run 'python pyAutoMail.py' 

pyAutoMail.py should run in a cronjob on a daily basis.