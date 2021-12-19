#### sending a daily email with an attachment with today's date written on it ####
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import datetime
import os
import re
import sys
import io

### PART 1 WRIING DATE ON PDF FILE ###
packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
ddj_write = datetime.date.today().strftime(
    "%d    %m      %Y"
)  # spaces to fit in the pdf boxes
can.drawString(365, 632, ddj_write)
can.save()
# move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open(r"../Emargement.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
ddj_formate = datetime.date.today().strftime(
    "%d_%m"
)  # récupère la date du jour sous un autre format pour l'insérer dans le nom du document
outputStream = open(
    "raphael_bitoun_emargement_Data_analyst_" + ddj_formate + ".pdf", "wb"
)
output.write(outputStream)
outputStream.close()

print("la récupération du fichier s'est faite avec succès")
#### PART 2 SEND EMAIL#####

# Date du jour
ddj = datetime.date.today().strftime("%d/%m/%Y")

# Email adress
email_user = ""

# Email_pwd
email_pwd = ""

# reception email  --> xxxxx@cefim.eu
email_destination = ""

# Subject of the message
Subject = "Emargement Rbitoun data analyst " + ddj


filename = "emargement.pdf"

# message body
body = "Bonjour Séverine\nci-joint mon émargement du {}\nBonne Journée\nBien à toi\nRaphaël Bitoun".format(
    ddj
)

# Retrieving the pdf at the root of the script
path = os.getcwd()
files = os.listdir(path)
research = re.compile(".*\.pdf")
# Attached document
filename = (list(filter(research.match, files)))[0]

# message instantiation
msg = MIMEMultipart()
msg["From"] = email_user
msg["to"] = email_destination
msg["subject"] = Subject
msg.attach(MIMEText(body, "plain"))
attachment = open(filename, "rb")

# encoding document
part = MIMEBase("application", "octet-stream")
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", "attachment; filename= " + filename)

msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email_user, email_pwd)

server.sendmail(email_user, email_destination, text)
server.quit()
print("l'envoi de l'email s'est bien effectué!")
