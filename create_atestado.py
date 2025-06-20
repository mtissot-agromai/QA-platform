import selenium
from dotenv import load_dotenv
import os
import geopandas as gpd
import random

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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Initialize the WebDriver (assuming Chrome is installed and chromedriver is in PATH)

driver = webdriver.Chrome()

def login(USER_EMAIL, USER_PASSWORD)->bool:
    driver.maximize_window()
    try:
        driver.get("https://dev.agromai.com.br/mapa/login")
        logger.info("Navigated to login page.")
    except Exception as e:
        logger.error(f"Error when going to the login page: {e}")
        return False

    try:
        email_field = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
        email_field.send_keys(USER_EMAIL)
        logger.info("Entered email.")
    except Exception as e:
        logger.error(f"Error when entering email: {e}")
        return False

    try:
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.send_keys(USER_PASSWORD)
        logger.info("Entered password")
    except Exception as e:
        logger.error(f"Error when entering password: {e}")
        return False

    try:
        login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Entrar')]"))
    )
        login_button.click()
        logger.info("Clicked Entrar.")    
    except Exception as e:
        logger.error(f"Error when clicking entrar: {e}")
        return False

    return True


def add_area(area_filepath: str)->bool:

    width = driver.execute_script("return window.innerWidth")
    height = driver.execute_script("return window.innerHeight")

    # Read GeoJSON file
    gdf = gpd.read_file(f"{area_filepath}")
    centroide = f"{gdf['geometry'][0].centroid.y}, {gdf['geometry'][0].centroid.x}"

    try:
        areas_link = wait(30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Áreas')]"))
        )
        areas_link.click()
        logger.info("Navigating to 'Áreas' page, from the sidebar")
    except Exception as e:
        logger.error(f"Error when trying to navigate to the Areas page: {e}")
        return False
    
    try:
        location_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(., 'Buscar localização')]"))
        )
        location_field.send_keys(centroide, Keys.ENTER)
        logger.info("Entered location")
    except Exception as e:
        logger.error(f"Error when entering location: {e}")
        return False
    
    time.sleep(3)

    try:
        marcar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Marcar')]"))
        )
        marcar_button.click()
        logger.info("Clicked Marcar")    
    except Exception as e:
        logger.error(f"Error when clicking Marcar: {e}")
        return False

    try:
        # Move and click at center
        actions = ActionChains(driver)
        actions.move_by_offset(width // 2, height // 2).click().perform()
        # Reset mouse position for future actions
        actions.move_by_offset(-width // 2, -height // 2).perform()
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

    try:
        car_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(., 'últimos dígitos')]"))
        )
        car_field.send_keys("11111")
        logger.info("Entered location")
    except Exception as e:
        logger.error(f"Error when entering location: {e}")
        return False
    
    try:
        sim_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Sim, é meu')]"))
        )
        sim_button.click()
        logger.info("Clicked 'Sim é meu'")    
    except Exception as e:
        logger.error(f"Error when clicking 'Sim é meu': {e}")
        return False
    
    try:
        sim_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Sim, é meu')]"))
        )
        sim_button.click()
        logger.info("Clicked 'Sim é meu'")    
    except Exception as e:
        logger.error(f"Error when clicking 'Sim é meu': {e}")
        return False
    


    return True

def wait(time: int):
    return WebDriverWait(driver, time)


def novo_atestado(target_car: str)->bool:
    car_shown = target_car[0:3] + "*"*5+target_car[-5:len(target_car)]
    print(car_shown)
    try:
        atestados_link = wait(30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Atestados')]"))
        )
        atestados_link.click()
        logger.info("Navigating to 'Atestados' page, from the sidebar")
    except Exception as e:
        logger.error(f"Error when trying to navigate to the Atestados page: {e}")
        return False

    try:
        novo_atestado_button = wait(10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Novo atestado')]"))
        )
        novo_atestado_button.click()
        logger.info("Clicked 'Novo Atestado' button")
    except Exception as e:
        logger.error(f"Couldn't click this icon: {e}")
        return False

    try:
        button = wait(20).until(EC.element_to_be_clickable((
            By.XPATH,
            f"//h3[text()='-*****']/following::button[1]"
        )))
        button.click()
        logger.info(f"Clicked button associated with first CAR:")
    except Exception as e:
        logger.error(f"Error when trying to click button for first CAR on the list: {e}")
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
        logger.error(f"Error when checking talhão boxes: {e}")
        return False

    try:
        continuar_button = wait(10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_button.click()
        logger.info("Clicked 'Continuar' button")
    except Exception as e:
        logger.error(f"Couldn't 'Continuar' button: {e}")
        return False
    
    try:
        continuar_button_again = wait(10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_button_again.click()
        logger.info("Clicked 'Continuar' button on invasion screen")
    except Exception as e:
        logger.error(f"Couldn't 'Continuar' button on invasion screen: {e}")
        return False
    
    if (len(checkboxes) > 1):
        try:
            for i in range(len(checkboxes)-1):
                next_button = wait(10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Próximo')]]"))
                )
                next_button.click()
            logger.info(f"Clicked 'Próximo' button {len(checkboxes)} times")
        except Exception as e:
            logger.error(f"Error when clicking 'Próximo' button at time {i}: {e}")
            return False
    
    try:
        finalizar_analise_button = wait(10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Finalizar análise')]]"))
        )
        finalizar_analise_button.click()
        logger.info(f"Clicked 'Finalizar análise' button")
    except Exception as e:
        logger.error(f"Error when clicking 'Finalizar análise' button {e}")
        return False
    
    try:
        list_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.ant-list-items > li"))
        )
        for li in list_items:
            chosen = random.choice(["Soja", "Milho", "Arroz", "Feijão"])
            # First dropdown
            try:
                dropdowns = li.find_elements(By.CSS_SELECTOR, ".ant-select")
                dropdowns[0].click()
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-select-dropdown")))
                driver.find_element(By.XPATH, f"//div[@class='rc-virtual-list']//div[contains(text(), '{chosen}')]").click()
            except Exception as e:
                logger.error(f"Error when selecting crop: {chosen} -> {e}")
                return False

            try:
                wait(40).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Selecione a data"]'))
                ).click()
                
                wait(40).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'td[title]:not(.ant-picker-cell-disabled)'))
                ).click()

            except Exception as e:
                logger.error(f"Error when selecting date crop: {e}", exc_info=True)
                return False
            
        try:
            continuar_button = wait(10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
            )
            continuar_button.click()
            logger.info("Clicked 'Continuar' button")
        except Exception as e:
            logger.error(f"Couldn't 'Continuar' button: {e}")
            return False
    except Exception as e:
        logger.error(f"Error when selecting crop and date for each selected Talhão: {e}")
        return False
    
    try:
        banco_field = wait(5).until(
        EC.presence_of_element_located((By.NAME, "documents.2957.issuing_institute"))
    )
        banco_field.send_keys("Banrisul")
        logger.info("Entered issuing institute")
    except Exception as e:
        logger.error(f"Error when entering issuing institute: {e}")
        return False
    
    try:
        selection_item = wait(10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.ant-select-selection-item"))
        )
        selection_item.click()
        selection_item.send_keys(Keys.ENTER)
    except Exception as e:
        logger.error(f"Error when selecting city: {e}")
        return False

    try:
        valor_field = wait(5).until(
        EC.presence_of_element_located((By.NAME, "documents.2957.requested_amount"))
    )
        valor_field.send_keys("1111111")
        logger.info("Entered requested loan amount")
    except Exception as e:
        logger.error(f"Error when entering requested loan amount: {e}")
        return False
    
    try:
        continue_button = wait(40).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    )
        continue_button.click()
        logger.info("Clicked 'Continuar'")    
    except Exception as e:
        logger.error(f"Error when clicking 'Continuar': {e}", exc_info=True)
        return False
    
    try:
        accordance_checkbox = wait(5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.ant-checkbox-input[type='checkbox']"))
        )
        accordance_checkbox.click()
        logger.info(f"Checked the 'Estou de acordo' checkbox")
    except Exception as e:
        logger.error(f"Error {e}")
        return False
    
    try:
        continue_button = wait(40).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    )
        continue_button.click()
        logger.info("Clicked 'Continuar'")    
    except Exception as e:
        logger.error(f"Error when clicking 'Continuar': {e}", exc_info=True)
        return False
    
    # CPF
    try:
        cpf_field = wait(5).until(
        EC.presence_of_element_located((By.NAME, "cpf"))
    )
        cpf_field.send_keys("81681442019")
        logger.info("Entered CPF: 816.814.420-19")
    except Exception as e:
        logger.error(f"Error when entering CPF: {e}")
        return False
    
    # Celular
    try:
        celular_field = wait(5).until(
        EC.presence_of_element_located((By.NAME, "phoneNumber"))
    )
        celular_field.send_keys("11111111111")
        logger.info("Entered phone number")
    except Exception as e:
        logger.error(f"Error when entering requested loan amount: {e}")
        return False
    
    try:
        novo_endereco = wait(5).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Novo endereço de cobrança')]"))
        )
        novo_endereco.click()
        logger.info("Entered phone number")
    except Exception as e:
        logger.error(f"Error when entering requested loan amount: {e}")
        return False
    
    try:
        cep_field = wait(5).until(
        EC.presence_of_element_located((By.NAME, "postal_code"))
    )
        cep_field.send_keys("90620001", Keys.ENTER)
        logger.info("Entered CEP")
    except Exception as e:
        logger.error(f"Error when entering requested loan amount: {e}")
        return False
    
    try:
        number_field = wait(5).until(
        EC.presence_of_element_located((By.NAME, "number"))
    )
        number_field.send_keys("1")
        logger.info("Entered CEP")
    except Exception as e:
        logger.error(f"Error when entering requested loan amount: {e}")
        return False
    
    try:
        continue_button = wait(40).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    )
        continue_button.click()
        logger.info("Clicked 'Continuar'")    
    except Exception as e:
        logger.error(f"Error when clicking 'Continuar': {e}", exc_info=True)
        return False
    
    return True

def register(email_address, USER_PASSWORD)->bool:
    # service = webdriver.ChromeService(log_output="browserlog.log")

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)

    driver.set_window_size(1920, 1080)

    def wait(time: int)-> WebDriverWait:
        return WebDriverWait(driver, time)
    try:
        driver.get("https://dev.agromai.com.br/mapa/login")
        logger.info("Navigated to login page.")
    except Exception as e:
        logger.error(f"{email_address}: Error when going to the login page: {e}", exc_info=True)
        return False

    try:
        register_button = wait(40).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Registre-se')]"))
    )
        register_button.click()
        logger.info("Clicked 'Registre-se'")
    except Exception as e:
        logger.error(f"{email_address}: Error when clicking 'Registre-se': {e}", exc_info=True)
        return False
    
    try:
        email_field = wait(40).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="exemplo@email.com.br"]'))
        )
        email_field.send_keys(email_address)
        logger.info("Entered email to register")
    except Exception as e:
        logger.error(f"{email_address}: Error when entering email address: {e}", exc_info=True)
        return False
    
    try:
        continue_button = wait(40).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    )
        continue_button.click()
        logger.info("Clicked 'Continuar'")    
    except Exception as e:
        logger.error(f"{email_address}: Error when clicking 'Continuar': {e}", exc_info=True)
        return False
    
    try:
        firstpassword_field = wait(40).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Insira sua senha"]'))
        )
        firstpassword_field.send_keys(USER_PASSWORD)
        logger.info("Entered password to register")
    except Exception as e:
        logger.error(f"{email_address}: Error when entering password: {e}", exc_info=True)
        return False
    
    try:
        secondpassword_field = wait(40).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Insira sua senha novamente"]'))
        )
        secondpassword_field.send_keys(USER_PASSWORD)
        logger.info("Entered password confirmation to register")
    except Exception as e:
        logger.error(f"{email_address}: Error when entering password confirmation: {e}", exc_info=True)
        return False
    
    try:
        continue_button = wait(40).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    )
        continue_button.click()
        driver.save_screenshot(f"Teste.png")
        logger.info("Clicked 'Continuar' during password setup")
    except Exception as e:
        logger.error(f"{email_address}: Error when clicking 'Continuar' during password setup: {e}", exc_info=True)
        return False

    
    try:
        driver.save_screenshot(f"Teste2.png")
        confirmationcode_field = wait(20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="_ _ _ - _ _ _"]'))
        )
        driver.save_screenshot(f"Teste3.png")
        confirmationcode_field.send_keys("111111")
        logger.info("Entered confirmation code")
    except Exception as e:
        driver.save_screenshot(f"Teste4.png")
        logger.error(f"{email_address}: Error when entering confirmation code: {e}", exc_info=True)
        return False

    
    try:
        driver.save_screenshot(f"Teste5.png")
        acessarconta_button = wait(40).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Acessar conta')]"))
    )
        driver.save_screenshot(f"Teste6.png")
        acessarconta_button.click()
        driver.save_screenshot(f"Teste7.png")
        logger.info("Clicked 'Acessar conta' after entering confirmation code")    
    except Exception as e:
        driver.save_screenshot(f"Teste8.png")
        logger.error(f"{email_address}: Error when clicking 'Acessar conta' after entering confirmation code: {e}", exc_info=True)
        return False
    
    
    try:
        username_field = wait(40).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="João da Silva"]'))
        )
        username_field.send_keys("Nome Sobrenome")
        logger.info("Entered confirmation code")
    except Exception as e:
        logger.error(f"{email_address}: Error when entering confirmation code: {e}", exc_info=True)
        return False
    
    
    try:
        wait(40).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Selecione a data"]'))
        ).click()
        
        wait(40).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'td[title]:not(.ant-picker-cell-disabled)'))
        ).click()

    except Exception as e:
        logger.error(f"{email_address}: Error when selecting date: {e}", exc_info=True)
        return False


    try:
        final_button = wait(40).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Finalizar Cadastro')]"))
    )
        final_button.click()
        logger.info("Clicked 'Finalizar Cadastro' on final step")    
    except Exception as e:
        logger.error(f"{email_address}: Error when clicking 'Finalizar Cadastro' on final step: {e}", exc_info=True)
        return False

    finally:
        with open('register_user.log', 'a') as log_file:
            log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Finished registration for email {email_address}\n")
        # print(f"Got to the final step for {USER_NAME}")
        driver.quit()

    return True


geojson_files = os.listdir("geojson")
print(geojson_files)
emails = [f"matheu{i}@email.com" for i in range(1)]
passwords = [f"#Teste123"] * len(emails)

print(emails)
print(passwords)

for i, email in enumerate(emails):
    print(f"Registering {email} with password {passwords[i]}")
    if register(email, passwords[i]):
        print(f"Successfully registered {email}")
    else:
        print(f"Failed to register {email}")

    add_area(f"geojson/{geojson_files[i]}")

    novo_atestado("")



time.sleep(100)