from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from random import uniform
from time import sleep
import os
import urllib.request
import speech_recognition as sr

try:
    os.system('del audio.mp3')
    os.system('del audio.wav')
except:
    pass

def google(audio):
    try:
        return r.recognize_google(audio)
    except:
        print("Google could not understand")
        return "ERROR"

def type_like_bot(driver, element, string):
    string = str(string)
    sleep(1)
    driver.find_element(By.ID, element).send_keys(string)
    sleep(2)
type_style = type_like_bot

def hover(element):  
    hov = ActionChains(driver).move_to_element(element)
    hov.perform()

r = sr.Recognizer()
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(executable_path='chrome/chromedriver.exe', options=chrome_options)
driver.delete_all_cookies()

driver.get("https://www.google.com/recaptcha/api2/demo")
sleep(2)

WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="recaptcha-demo"]/div/div/iframe')))
sleep(3)
iframeSwitch = driver.find_element(By.XPATH, '//*[@id="recaptcha-demo"]/div/div/iframe')

driver.switch_to.frame(iframeSwitch)
WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.ID, "recaptcha-anchor")))
sleep(3)
CheckBox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID ,"recaptcha-anchor"))
        )
rand=uniform(1.0, 1.5)
print('waiting ', rand , ' seconds...')
sleep(rand) 
hover(CheckBox)
sleep(1)
ele = driver.find_element(By.ID, "recaptcha-anchor")
ele.click()
sleep(5)
checkmark_pos = driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-checkmark").get_attribute("style")
if checkmark_pos == "background-position: 0 -600px":
    sleep(3)
    driver.find_element(By.XPATH, '/html/body/div[1]/form/fieldset/ul/li[6]/input').click()
    sleep(3)   

driver.switch_to.default_content()

WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title=\"desafio reCAPTCHA\"]")))
sleep(3)
iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title=\"desafio reCAPTCHA\"]")
driver.switch_to.frame(iframe)
WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.ID, "rc-imageselect")))

WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.ID, "recaptcha-audio-button")))
sleep(3)

AudioBox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID ,"recaptcha-audio-button"))
        )
rand=uniform(1.0, 1.5)
print('waiting ', rand , ' seconds...')
sleep(rand) 
hover(AudioBox)
sleep(1)
driver.find_element(By.ID, "recaptcha-audio-button").click()

guess_again = True
while guess_again:
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.ID, "audio-source")))
    body = driver.find_element(By.CSS_SELECTOR, "body").get_attribute('innerHTML').encode("utf8")
    soup = BeautifulSoup(body, 'html.parser')
    driver.find_element(By.XPATH, '//*[@id=":2"]').click()
    link = soup.findAll("a", {"class": "rc-audiochallenge-tdownload-link"})[0]
    urllib.request.urlretrieve(link["href"],"audio.mp3")
    os.system("ffmpeg -i audio.mp3 audio.wav")

    with sr.AudioFile("audio.wav") as source:
        audio = r.record(source)
    guess_str = google(audio)
    type_style(driver, "audio-response", guess_str)

    sleep(5)
    driver.find_element(By.ID, "recaptcha-verify-button").click()
    sleep(3)