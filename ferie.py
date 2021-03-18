from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from random import randint
from fake_useragent import UserAgent
import time
import os

options = Options()
options.headless = True
useragent = UserAgent()
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", useragent.random)
driver = webdriver.Firefox(options=options,firefox_profile=profile, executable_path=r'/usr/local/bin/geckodriver')

#What do we check for?
udbetal = 'udbetalt dine feriemidler endnu'
receivers = ['some@email']
counter = 0

def initiate():
  driver.get("https://www.borger.dk/Handlingsside?selfserviceId=eb55ce23-fa9a-4b26-8e94-f5c38037cfbb&referringPageId=650ddf9b-e874-4b5a-9a36-2fb3ae227a8a&type=DK")
  print(driver.page_source)

def check_page():
  driver.refresh()
  print('checking')

def sendMail(reciever):
  sendmail_location = "/usr/sbin/sendmail" #sendmail location
  p = os.popen("%s -t" % sendmail_location, "w")
  p.write("From: %s\n" % "your@email")
  p.write("To: %s\n" % reciever)
  p.write("Subject: Feriepenge er klar\n")
  p.write("\n") 
  p.write("Go go go")
  status = p.close()
  if status != 0:
    print("Sendmail exit status", status)

initiate()

while True:
  check_page()
  content = driver.page_source
  if udbetal in content: 
    counter = counter + 1
    random = randint(120, 200)
    print('Not yet ready - Try number '+str(counter)+' - Sleeping for '+str(random)+' seconds')
    time.sleep(random)
  else:
    print(content)
    print('It\'s ready!')
    for receiver in receivers:
      sendMail(receiver)
      print('Sent mail to '+receiver)
    break
driver.quit()
