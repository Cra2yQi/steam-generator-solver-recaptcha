import os
import urllib
import random
import pydub
import speech_recognition as sr
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class RecaptchaSolver:
    def __init__(self, driver):
        self.driver = driver

    def solveCaptcha(self):
        inner_frame_1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe")))
        self.driver.switch_to.frame(inner_frame_1)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".recaptcha-checkbox-border"))
        ).click()
        time.sleep(3)
        if self.isSolved():
            return
        self.driver.switch_to.default_content()


        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]"))
        )
        self.driver.switch_to.frame(2)
        # Wait until the reCAPTCHA is fully loaded and the iframe is present

        # Click on the audio button
        self.driver.find_element(By.ID, "recaptcha-audio-button").click()
        time.sleep(0.3)

        # Get the audio source
        src = self.driver.find_element(By.ID, "audio-source").get_attribute('src')

        # Download the audio to the temp folder
        path_to_mp3 = os.path.join((os.getenv("TEMP") if os.name == "nt" else "/tmp/"),
                                   f"{random.randrange(1, 1000)}.mp3")
        path_to_wav = os.path.join((os.getenv("TEMP") if os.name == "nt" else "/tmp/"),
                                   f"{random.randrange(1, 1000)}.wav")

        urllib.request.urlretrieve(src, path_to_mp3)

        # Convert mp3 to wav
        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
        sound.export(path_to_wav, format="wav")
        sample_audio = sr.AudioFile(path_to_wav)
        recognizer = sr.Recognizer()
        with sample_audio as source:
            audio = recognizer.record(source)

        # Recognize the audio
        key = recognizer.recognize_google(audio)

        # Input the key
        self.driver.find_element(By.ID, "audio-response").send_keys(key.lower())
        time.sleep(0.1)

        # Submit the key
        self.driver.find_element(By.ID, "audio-response").send_keys(Keys.ENTER)
        time.sleep(0.4)

        # Check if the captcha is solved
        if self.isSolved():
            return
        else:
            raise Exception("Failed to solve the captcha")

    def isSolved(self):
        try:
            self.driver.switch_to.default_content()
            inner_frame_1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe")))
            self.driver.switch_to.frame(inner_frame_1)
            # 找到 reCAPTCHA 复选框
            checkbox = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="recaptcha-anchor"]/div[4]'))
            )

            # 打印元素的 outerHTML
            outer_html = checkbox.get_attribute('outerHTML')
            return 'style' in outer_html
        except:
            return False
