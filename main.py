import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

from RecaptchaSolver import RecaptchaSolver

chrome_driver_path = "chromedriver"  # 替换为你的 ChromeDriver 路径

service = ChromeService(executable_path=chrome_driver_path)
chrome_options = Options()
chrome_options.add_argument("--lang=en-US")
chrome_options.add_argument("--incognito")
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.stylesheets": 2,
}

# 请求日志
driver = webdriver.Chrome(options=chrome_options, service=service)



driver.get("https://store.steampowered.com/join")
driver.set_window_size(600, 800)
WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
driver.find_element(By.ID, "email").send_keys("crzqi1022@gmail.com")
driver.find_element(By.ID, "reenter_email").send_keys("crzqi1022@gmail.com")
driver.find_element(By.ID, "i_agree_check").click()


t0 = time.time()
recaptchaSolver = RecaptchaSolver(driver)
recaptchaSolver.solveCaptcha()
print(f"Time to solve the captcha: {time.time()-t0:.2f} seconds")

