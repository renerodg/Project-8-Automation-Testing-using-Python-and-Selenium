from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from helpers import retrieve_phone_code
import data

"""REVISION 2. A partir del main.py, se creo este archivo para separar los localizadores y los metodos. en donde tambien se incorpora
#el uso de un nuevo selector mas, By.NAME, se reduce en gran medida el uso de de los selectores con indices y se estandariza al Ingles.
"""

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    # Localizadores
    from_field = (By.ID, "from")
    to_field = (By.ID, "to")
    taxi_button = (By.CLASS_NAME, "button.round")
    comfort_button = (By.XPATH, '//div[text()="Comfort"]')
    set_phone_number_button = (By.CLASS_NAME, "np-text")
    phone_number_field = (By.ID, "phone")
    next_button = (By.CLASS_NAME, "button")
    code_field = (By.ID, 'code')
    confirm_button = (By.CLASS_NAME, "button full")
    payment_method_button = (By.CLASS_NAME, "pp-text")
    add_card_button = (By.CLASS_NAME, "pp-plus")
    add_card_field = (By.ID, "number")
    add_code_card_field = (By.NAME, 'code')
    card_added_successfully = (By.ID, "card-1")
    add_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    strip_orange_yellow = (By.CLASS_NAME, "plc")
    close_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    message_for_driver = (By.ID, "comment")
    order_requirements_button = (By.CLASS_NAME, "reqs-head")
    blanket_napkins_button = (By.CLASS_NAME, "r-sw")
    ice_cream_button = (By.XPATH,
                     '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    counter_value = (By.CLASS_NAME, "counter-value")
    reserve_button = (By.CLASS_NAME, "smart-button-wrapper")
    looking_for_cab = (By.CLASS_NAME, "order-header-content")
    driver_arrives_in = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]')


class UrbanRoutesPage(BasePage):

    def wait_time(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((self.from_field))
        )

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_taxi_button(self):
        WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(self.taxi_button)
        ).click()

    def wait_for_comfort_button(self):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.comfort_button))

    def click_in_comfort(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.comfort_button)
        ).click()

    def comfort_selected(self):
        comfort_button = self.driver.find_element(*self.comfort_button)
        return "active" in comfort_button.get_attribute("class")

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def click_telephone_number(self):
        return self.driver.find_element(*self.set_phone_number_button).click()

    def add_telephone_number(self, phone_number):
        return self.driver.find_element(*self.phone_number_field).send_keys(phone_number)

    def click_next_button(self):
        return self.driver.find_element(*self.next_button).click()

    def get_code(self):
        get_phone_code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.code_field).send_keys(get_phone_code)

    def click_in_confirm_button(self):
        WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable(self.confirm_button)
        ).click()

    #Proceso de tarjeta de credito
    def click_payment_method(self):
        return self.driver.find_element(*self.payment_method_button).click()

    def click_add_card(self):
        return self.driver.find_element(*self.add_card_button).click()

    def add_card_number(self):
        return self.driver.find_element(*self.add_card_field).send_keys(data.card_number)

    def add_code_number(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'card-code-input'))
        )
        return self.driver.find_element(*self.add_code_card_field).send_keys(data.card_code)

    def click_in_any_other_element(self):
        return self.driver.find_element(*self.strip_orange_yellow).click()

    def click_in_add(self):
        return self.driver.find_element(*self.add_button).click()

    def click_in_close(self):
        return self.driver.find_element(*self.close_button).click()

    def card_added(self):
        card_checkbox = self.driver.find_element(*self.card_added_successfully)
        is_checked = card_checkbox.get_attribute("checked") is not None
        assert is_checked, "La tarjeta no se agregó correctamente."

    #Proceso de mandar mensaje
    def search_message_for_driver(self):
        message_driver = self.driver.find_element(*self.message_for_driver)
        self.driver.execute_script("arguments[0].scrollIntoView();", message_driver)

    def wait_for_message_for_driver(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.message_for_driver)
        )

    def send_message_for_driver(self):
        self.driver.find_element(*self.message_for_driver).send_keys(data.message_for_driver)

    def get_message_for_driver(self):
        return self.driver.find_element(*self.message_for_driver).get_property('value')

    #Requisitos del pedido
    def click_requisites(self):
        return self.driver.find_element(*self.order_requirements_button).click()

    def click_in_blanket_napkins(self):
        return self.driver.find_element(*self.blanket_napkins_button).click()

    def blanket_napkins_is_selected(self):
        checkbox = self.driver.find_element(*self.blanket_napkins_button)
        return checkbox.is_selected()

    def click_in_icecream(self):
        icecream_button = self.driver.find_element(*self.ice_cream_button)
        action_chains = ActionChains(self.driver)
        action_chains.double_click(icecream_button).perform()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.counter_value).text)

    #Pedir taxi
    def click_order_cab(self):
        return self.driver.find_element(*self.reserve_button).click()

    def order_cab_displayed(self):
        order_header_content = self.driver.find_element(*self.looking_for_cab)
        assert order_header_content.is_displayed(), "El elemento order-header-content no se está mostrando."

