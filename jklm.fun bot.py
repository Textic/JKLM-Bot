from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Back, init
import time
import requests
import os
import json
import random

def getDictionary(lang):
    res = requests.get("https://textic.github.io/assets/dictionary.json")
    if res.status_code == 200:
        data = json.loads(res.text)
        return data[lang]
    else:
        input("Error to get dictionary, press enter to exit")
        exit()

def searchWord(dictionary, word, max, mode):
    wordsList = []
    for i in dictionary:
        if word.lower() in i:
            wordsList.append(i)
    if mode == True:
        return wordsList
    if max < 0 and max > 100:
        input("Error, Max words must be between 0 and 100, press enter to exit")
        exit()
    if max != 0:
        if len(wordsList) > max:
            wordsList = random.sample(wordsList, max)
    return wordsList

auto = True
autoSlow = True
maxWords = 30
rows = 3

os.system("cls")
print("Getting dictionary...")
init(autoreset=True)
link = "https://jklm.fun/"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())
driver.maximize_window()
dictionary = getDictionary("spanish")
lastWord = ""
pickedWord = ""

xpath_iframe = "/html/body/div[2]/div[4]/div[1]/iframe"
xpath_word = "/html/body/div[2]/div[2]/div[2]/div[2]/div"
xpath_currentPlayer = "/html/body/div[2]/div[3]/div[2]/div[1]/span[1]"
xpath_input = "/html/body/div[2]/div[3]/div[2]/div[2]/form/input"


try:
    driver.get(link)
except:
    print("Can't open the link")
    driver.quit()
    exit()

os.system("cls")
print("Waiting for the game to start...")
while True:
    driver.switch_to.default_content()
    localstorage = json.loads(driver.execute_script("return localStorage.getItem('jklmSettings')"))
    if auto == False:
        try:
            time.sleep(0.1)
            driver.switch_to.frame(driver.find_element(By.XPATH, xpath_iframe))
            word = driver.find_element(By.XPATH, xpath_word).text
            if word != lastWord and word != "":
                os.system("cls")
                lastWord = word
                print(f"Current word: {Fore.BLUE}{word}")
                wordList = searchWord(dictionary, word, maxWords, auto)
                for i in range(len(wordList)):
                    if i % rows == 0:
                        print()
                    print(wordList[i], end=f"  {Fore.CYAN}|  ")
        except:
            pass
    else:
        try:
            driver.switch_to.frame(driver.find_element(By.XPATH, xpath_iframe))
            localName = localstorage["nickname"]
            currentPlayer = driver.find_element(By.XPATH, xpath_currentPlayer).get_attribute("textContent")
            # execute word = driver.find_element(By.XPATH, xpath_word).text asynchronusly
            word = driver.execute_script(f"return document.querySelector('/html/body/div[2]/div[2]/div[2]/div[2]/div').textContent")
            while currentPlayer == localName and currentPlayer != "":
                os.system("cls")
                print(f"{Fore.BLUE}You are in auto mode\n")
                print(f"Your name: {Fore.GREEN}{localName}")
                print(f"Current player: {Fore.RED}{currentPlayer}")
                print(f"\nCurrent word: {Fore.BLUE}{word}")
                wordList = searchWord(dictionary, word, maxWords, auto)
                pickedWord = random.choice(wordList)
                print(f"Picked: {Fore.YELLOW}{pickedWord}")
                time.sleep(0.6)
                if autoSlow == True:
                    for i in pickedWord:
                        driver.find_element(By.XPATH, xpath_input).send_keys(i)
                        numbertest = random.uniform(0.05, 0.2)
                        time.sleep(numbertest)
                else:
                    driver.find_element(By.XPATH, xpath_input).send_keys(pickedWord)
                driver.find_element(By.XPATH, xpath_input).send_keys(Keys.ENTER)
                currentPlayer = driver.find_element(By.XPATH, xpath_currentPlayer).text
        except:
            pass