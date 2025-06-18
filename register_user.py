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

error_file_handler = logging.FileHandler('errors.log')
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)

logger.handlers = []
logger.addHandler(stdout_handler)
logger.addHandler(error_file_handler)

load_dotenv()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver (assuming Chrome is installed and chromedriver is in PATH)
driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://dev.agromai.com.br/mapa/")

USER_NAME = "Teste4"
USER_EMAIL = f"{USER_NAME.lower()}@teste.com"
USER_PASSWORD = "#Teste123"

def wait(time: int):
    return WebDriverWait(driver, time)

def register(USER_EMAIL, USER_PASSWORD)->bool:
    try:
        driver.get("https://dev.agromai.com.br/mapa/login")
        logger.info("Navigated to login page.")
    except Exception as e:
        logger.error(f"Error when going to the login page: {e}", exc_info=True)
        return False

    try:
        register_button = wait(5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Registre-se')]"))
    )
        register_button.click()
        logger.info("Clicked 'Registre-se'")
    except Exception as e:
        logger.error(f"Error when clicking 'Registre-se': {e}", exc_info=True)
        return False
    
    try:
        email_field = wait(5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="exemplo@email.com.br"]'))
        )
        email_field.send_keys(USER_EMAIL)
        logger.info("Entered email to register")
    except Exception as e:
        logger.error(f"Error when entering email address: {e}", exc_info=True)
        return False
    
    try:
        continue_button = wait(10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    )
        continue_button.click()
        logger.info("Clicked 'Continuar'")    
    except Exception as e:
        logger.error(f"Error when clicking 'Continuar': {e}", exc_info=True)
        return False
    
    try:
        firstpassword_field = wait(5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Insira sua senha"]'))
        )
        firstpassword_field.send_keys(USER_PASSWORD)
        logger.info("Entered email to register")
    except Exception as e:
        logger.error(f"Error when entering password: {e}", exc_info=True)
        return False
    
    try:
        secondpassword_field = wait(5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Insira sua senha novamente"]'))
        )
        secondpassword_field.send_keys(USER_PASSWORD)
        logger.info("Entered email to register")
    except Exception as e:
        logger.error(f"Error when entering password confirmation: {e}", exc_info=True)
        return False
    
    try:
        continue_button = wait(10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    )
        continue_button.click()
        logger.info("Clicked 'Continuar' during password setup")    
    except Exception as e:
        logger.error(f"Error when clicking 'Continuar' during password setup: {e}", exc_info=True)
        return False
    
    try:
        confirmationcode_field = wait(5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="_ _ _ - _ _ _"]'))
        )
        confirmationcode_field.send_keys("111111")
        logger.info("Entered confirmation code")
    except Exception as e:
        logger.error(f"Error when entering confirmation code: {e}", exc_info=True)
        return False
    
    try:
        acessarconta_button = wait(10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Acessar conta')]"))
    )
        acessarconta_button.click()
        logger.info("Clicked 'Acessar conta' after entering confirmation code")    
    except Exception as e:
        logger.error(f"Error when clicking 'Acessar conta' after entering confirmation code: {e}", exc_info=True)
        return False
    
    try:
        username_field = wait(5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="João da Silva"]'))
        )
        username_field.send_keys(USER_NAME)
        logger.info("Entered confirmation code")
    except Exception as e:
        logger.error(f"Error when entering confirmation code: {e}", exc_info=True)
        return False
    
    try:
        wait(10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Selecione a data"]'))
        ).click()
        
        wait(10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'td[title]:not(.ant-picker-cell-disabled)'))
        ).click()

    except Exception as e:
        logger.error(f"Error when selecting date: {e}", exc_info=True)
        return False

    try:
        final_button = wait(10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Finalizar Cadastro')]"))
    )
        final_button.click()
        logger.info("Clicked 'Finalizar Cadastro' on final step")    
    except Exception as e:
        logger.error(f"Error when clicking 'Finalizar Cadastro' on final step: {e}", exc_info=True)
        return False
    
    time.sleep(200)

    return True


def novo_atestado(target_car: str)->bool:
    try:
        atestados_link = wait(30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Atestados')]"))
        )
        atestados_link.click()
        logger.info("Navigating to 'Atestados' page, from the sidebar")
    except Exception as e:
        logger.error(f"Error when trying to navigate to the Atestados page: {e}", exc_info=True)
        return False

    try:
        novo_atestado_button = wait(10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Novo atestado')]"))
        )
        novo_atestado_button.click()
        logger.info("Clicked 'Novo Atestado' button")
    except Exception as e:
        logger.error(f"Couldn't click this icon: {e}", exc_info=True)
        return False

    try:
        button = wait(20).until(EC.element_to_be_clickable((
            By.XPATH,
            f"//h3[text()='{target_car}']/following::button[1]"
        )))
        button.click()
        logger.info(f"Clicked button associated with CAR: {target_car}")
    except Exception as e:
        logger.error(f"Error when trying to click button {target_car}: {e}", exc_info=True)
        return False
    
    try:
        container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.ant-checkbox-group")))
        checkboxes = container.find_elements(By.CSS_SELECTOR, "input.ant-checkbox-input[type='checkbox']")
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                checkbox.click()
        logger.info(f"Checked all talhões for CAR {target_car}")
    except Exception as e:
        logger.error(f"Error when checking talhão boxes: {e}", exc_info=True)
        return False
    
    return True



register_status = register(USER_EMAIL, USER_PASSWORD)

if not register_status:
    logger.error("Login process was unsuccessful. Exiting with code 1")
    time.sleep(200)
    sys.exit(1)
    
# novo_atestado_status = novo_atestado("RS-4301107-1712C200BC5741109F2A04C3F5BE040F")
# if not novo_atestado_status:
#     logger.error("Novo atestado process was unsuccessful. Exiting with code 1")
#     sys.exit(2)

time.sleep(100)







    # # Step 11: Click "RS-4306767-E99CD070343A47A286122795F179BD3C" (another instance)
    # specific_id_link2 = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'RS-4306767-E99CD070343A47A286122795F179BD3C')]"))
    # )
    # specific_id_link2.click()
    # print("Clicked specific ID link 2.")
    # time.sleep(2)

    # # Step 12: Click "Talhão 2"
    # talhao_link = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Talhão 2')]"))
    # )
    # talhao_link.click()
    # print("Clicked Talhão 2.")
    # time.sleep(2)

    # # Step 13: Click "Continuar"
    # continuar_button_1 = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    # )
    # continuar_button_1.click()
    # print("Clicked Continuar 1.")
    # time.sleep(2)

    # # Step 14: Click here. (Ambiguous)
    # # This step is highly ambiguous. You will need to provide a specific locator.
    # try:
    #     click_here_ambiguous = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'here')] | //button[contains(., 'Click')] | //div[@class='some-specific-class-for-this-click']"))
    #     )
    #     click_here_ambiguous.click()
    #     print("Clicked ambiguous 'Click here' (locator needs refinement).")
    # except:
    #     print("Could not find or click the ambiguous 'Click here' in Step 14. Please provide a specific locator.")
    # time.sleep(2)

    # # Step 15: Click "Arroz"
    # arroz_option = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Arroz')]"))
    # )
    # arroz_option.click()
    # print("Clicked Arroz.")
    # time.sleep(2)

    # # Step 16: Click the "Selecione a data" field.
    # date_field = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Selecione a data']"))
    # )
    # date_field.click()
    # print("Clicked date selection field.")
    # time.sleep(2)

    # # Step 17: Click "5" (Assuming it's a day in a calendar picker)
    # day_5 = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'day') and text()='5'] | //span[text()='5']"))
    # )
    # day_5.click()
    # print("Clicked day 5.")
    # time.sleep(2)

    # # Step 18: Click "Continuar"
    # continuar_button_2 = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    # )
    # continuar_button_2.click()
    # print("Clicked Continuar 2.")
    # time.sleep(2)

    # # Step 19 & 20: Click the "Ex: Banco do Brasil S.A." field and Type "Banrisul"
    # bank_field = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Ex: Banco do Brasil S.A.']"))
    # )
    # bank_field.send_keys("Banrisul")
    # print("Entered bank name.")
    # time.sleep(1)

    # # Step 21: Click here. (Ambiguous)
    # # This step is highly ambiguous. You will need to provide a specific locator.
    # try:
    #     click_here_ambiguous_2 = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'here')] | //button[contains(., 'Click')] | //div[@class='another-specific-class-for-this-click']"))
    #     )
    #     click_here_ambiguous_2.click()
    #     print("Clicked ambiguous 'Click here' 2 (locator needs refinement).")
    # except:
    #     print("Could not find or click the ambiguous 'Click here' in Step 21. Please provide a specific locator.")
    # time.sleep(2)

    # # Step 22: Click "AP"
    # ap_option = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'AP')]"))
    # )
    # ap_option.click()
    # print("Clicked AP.")
    # time.sleep(2)

    # # Step 23: Click here. (Ambiguous)
    # # This step is highly ambiguous. You will need to provide a specific locator.
    # try:
    #     click_here_ambiguous_3 = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'here')] | //button[contains(., 'Click')] | //div[@class='yet-another-specific-class-for-this-click']"))
    #     )
    #     click_here_ambiguous_3.click()
    #     print("Clicked ambiguous 'Click here' 3 (locator needs refinement).")
    # except:
    #     print("Could not find or click the ambiguous 'Click here' in Step 23. Please provide a specific locator.")
    # time.sleep(2)

    # # Step 24: Click "Ferreira Gomes"
    # ferreira_gomes_option = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Ferreira Gomes')]"))
    # )
    # ferreira_gomes_option.click()
    # print("Clicked Ferreira Gomes.")
    # time.sleep(2)

    # # Step 25 & 26: Click the "0,00" field and Type "1111111"
    # value_field = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0,00']"))
    # )
    # value_field.send_keys("1111111")
    # print("Entered value.")
    # time.sleep(1)

    # # Step 27: Click "Continuar"
    # continuar_button_3 = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    # )
    # continuar_button_3.click()
    # print("Clicked Continuar 3.")
    # time.sleep(2)

    # # Step 28: Click "Estou de acordo com as informações e desejo requisitar meu atestado"
    # agree_checkbox = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Estou de acordo com as informações e desejo requisitar meu atestado')] | //input[@type='checkbox' and @id='agree_checkbox_id']"))
    # )
    # agree_checkbox.click()
    # print("Clicked agreement checkbox.")
    # time.sleep(2)

    # # Step 29: Click "Pagamento"
    # pagamento_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Pagamento')] | //a[contains(., 'Pagamento')]"))
    # )
    # pagamento_button.click()
    # print("Clicked Pagamento.")
    # time.sleep(2)

    # # Step 30: Click "RS-4306767-E99CD070343A47A286122795F179BD3C" (final instance)
    # specific_id_link3 = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'RS-4306767-E99CD070343A47A286122795F179BD3C')]"))
    # )
    # specific_id_link3.click()
    # print("Clicked specific ID link 3.")
    # time.sleep(2)

    # # Step 31: Click here. (Ambiguous - likely a final confirmation or download trigger)
    # # This step is highly ambiguous. You will need to provide a specific locator.
    # try:
    #     click_here_ambiguous_4 = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'here')] | //button[contains(., 'Click')] | //div[@class='final-click-element']"))
    #     )
    #     click_here_ambiguous_4.click()
    #     print("Clicked ambiguous 'Click here' 4 (locator needs refinement).")
    # except:
    #     print("Could not find or click the ambiguous 'Click here' in Step 31. Please provide a specific locator.")
    # time.sleep(5)

# finally:
#     driver.quit()
#     print("Browser closed.")


