import os
import smtplib
from time import sleep
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException



# Secrets Import
from env import username, password  # Fernuni Zugangsdaten
from env import sender_mail as sender  # Versendender Mailserver
from env import empfaenger # Empfängeradresse

refresh_intervall = 600 # Refresh Intervall
debug = 0   # 0 bedeutet headless; 1 nur für debug nutzen!

chrome_options = Options()
if not debug:
    chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get("https://pos.fernuni-hagen.de/qisserver/rds?state=user&type=0&category=auth.logout")#put here the adress of your page
elem = driver.find_element_by_id("loginForm:login")
print(elem.get_attribute("class"))
user = driver.find_element_by_id("asdf")
pwd = driver.find_element_by_id("fdsa")
user.send_keys(username)
pwd.send_keys(password)
elem.click()
print("Loggin in...")
verwaltung = driver.find_element_by_xpath("/html/body/div/div[5]/div[1]/ul/li/a")
verwaltung.click()
notenuebersicht = driver.find_element_by_xpath("/html/body/div/div[5]/div[2]/div/form/div/ul/li[3]/a")
notenuebersicht.click()
Leistungen = driver.find_element_by_xpath("/html/body/div/div[5]/div[2]/form/ul/li[2]/a[1]")
Leistungen.click()
leistungstabelle = "/html/body/div/div[5]/div[2]/form/table[2]"
tabelle = driver.find_element_by_xpath(leistungstabelle).text
tabelle_neu = driver.find_element_by_xpath(leistungstabelle).text
print("starting the idle")
while tabelle_neu == tabelle:
    sleep(refresh_intervall)
    driver.refresh()
    print("Refreshing")
    tabelle_neu = driver.find_element_by_xpath(leistungstabelle).text

smtpObject = smtplib.SMTP_SSL(host=sender['host'], port=465)
FROM = sender['emailaddress']
smtpObject.login(FROM, sender['password'])
x = empfaenger  # TODO needs testing if mail is send
if len(tabelle_neu) > len(tabelle):        
    try:
        msg = MIMEText(
            'Es sind Noten in der Tabelle hinzugefügt worden \n \n https://pos.fernuni-hagen.de/qisserver/rds?state=user&type=0&topitem= \n \n '+ tabelle_neu)
        msg['Subject'] = 'Neue Noten bei der Fernuni'
        msg['From'] = FROM
        msg['To'] = x
        smtpObject.sendmail(FROM, x, msg.as_string())
        print('Successfully sent email')
    except smtplib.SMTPException:
        print("Error: unable to send email")
else:
    try:
        msg = MIMEText(
            'Etwas ist beim Notenchecker Script schief gegenagen')
        msg['Subject'] = 'Fehler im Notenchecker Script'
        msg['From'] = FROM
        msg['To'] = x
        smtpObject.sendmail(FROM, x, msg.as_string())
        print('Successfully sent email')
    except smtplib.SMTPException:
        print("Error: unable to send email")
driver.close()
