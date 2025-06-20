import selenium
from dotenv import load_dotenv
import os

import logging, sys
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)

error_file_handler = logging.FileHandler('errors_creation.log')
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)

warning_file_handler = logging.FileHandler('warnings.log')
warning_file_handler.setLevel(logging.WARNING)
warning_file_handler.setFormatter(formatter)

logger.handlers = []
logger.addHandler(stdout_handler)
logger.addHandler(error_file_handler)

load_dotenv()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time, random

USER_NAME = "Teste0"
USER_EMAIL = f"{USER_NAME.lower()}@teste.com"
USER_PASSWORD = "#Teste123"

def human_delay(min_sec=0.5, max_sec=2.0):
    # time.sleep(random.uniform(min_sec, max_sec))
    pass



emails = [f"test{i}@teste.com" for i in range(0, 1)]
# emails = ["testeemail1@email.com"]
USER_PASSWORD = "#Teste123"

# # print(emails)
for email_address in emails:
    register(email_address, USER_PASSWORD)
#     human_delay()
# from concurrent.futures import ThreadPoolExecutor, as_completed

# with ThreadPoolExecutor(max_workers=5) as executor:
#     futures = [executor.submit(register, email, USER_PASSWORD) for email in emails]

#     for future in as_completed(futures):
#         try:
#             result = future.result()
#             # Optionally log or print result
#         except Exception as e:
#             print(f"Error: {e}")
#             # logger.error(f"Error occurred during registration: {e}", exc_info=True)
#             # logger.info(f"Error occurred: {e}")

import pandas as pd
# password = [USER_PASSWORD * len(emails)]
passwords = [USER_PASSWORD] * len(emails)
dictt = {"email": emails, "password": passwords}
print(dictt)
df = pd.DataFrame(dictt)
df.to_csv("registered_users.csv", mode="a", index=False)