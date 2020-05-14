#### ENVOI EMAIL JOURNALIER DATA ANALYST ####
### NECESSITE D'AVOIR SIGNE LA FEUILLE PDF ET ENREGISTRE A LA RACINE DE CE FICHIER 
### test git###
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

### PARTIE 1 ECRITURE DE LA DATE DU JOUR SUR LE FICHIER PDF ########
packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
ddj_write  = datetime.date.today().strftime('%d    %m      %Y')        #récupère la date du jour pour l'écrire sur le pdf
can.drawString(365, 632, ddj_write)            # écriture ddj dans le document à la bonne place
can.save()
#move to the beginning of the StringIO buffer
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
ddj_formate  = datetime.date.today().strftime('%d_%m')                                  #récupère la date du jour sous un autre format pour l'insérer dans le nom du document
outputStream = open("raphael_bitoun_emargement_Data_analyst_"+ddj_formate+".pdf", "wb")
output.write(outputStream)
outputStream.close()

print("la récupération du fichier s'est faite avec succès")
#### PARTIE 2 ENVOI DE L'EMAIL #####




#Date du jour 
ddj  = datetime.date.today().strftime('%d/%m/%Y')

## Email d'envoi
email_user = "37raphael.bitoun@gmail.com"

## Email de reception  --> xxxxx@cefim.eu
email_destination = 

#Objet du message
Subject = 'Emargement Rbitoun data analyst '+ddj

## pièce jointe
filename = 'emargement.pdf'

# Corps du message
body = "Bonjour Séverine\nci-joint mon émargement du {}\nBonne Journée\nBien à toi\nRaphaël Bitoun".format(ddj)

### RECUPERATION DU FICHIER PDF SUR LE BUREAU ###
path = os.getcwd()
files = os.listdir(path)
research = re.compile('.*\.pdf')
filename = (list(filter(research.match, files)))[0] ## liste des fichier matchant avec la RegExp -> normalement un seul le pdf à envoyer

# instanciation du message
msg = MIMEMultipart()
msg['From'] = email_user
msg['to'] = email_destination
msg['subject'] = Subject
msg.attach(MIMEText(body, 'plain'))
attachment = open(filename, 'rb')

# Instanciation de l'objet permettant d'encoder le document
part = MIMEBase("application", 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= "+filename)

msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email_user, <votre-mot-de-passe) 

server.sendmail(email_user,email_destination, text)
server.quit()
print("l'envoi de l'email s'est bien effectué!")

