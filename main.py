import data
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(5)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    # Localizadores
    from_field = (By.ID, "from")
    to_field = (By.ID, "to")
    taxi_button = (By.CLASS_NAME, "button.round")
    comfort_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]/div[2]')
    set_phone_number_button = (By.CLASS_NAME, "np-text")
    phone_number_field = (By.ID, "phone")
    siguiente_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
    code_field = (By.ID, 'code')
    confirmar_button = (By.CLASS_NAME, "button full")
    metodo_de_pago_button = (By.CLASS_NAME, "pp-text")
    add_card_button = (By.CLASS_NAME, "pp-plus")
    add_card_field = (By.ID, "number")
    add_code_card_field = (By.CLASS_NAME, "card-code")
    agregar_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    strip_orange_yellow = (By.CLASS_NAME, "plc")
    cerrar_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    message_for_driver = (By.ID, "comment")
    requisitos_del_pedido_button = (By.CLASS_NAME, "reqs-head")
    manta_y_panuelos_button = (
    By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    helado_button = (By.XPATH,
                     '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    reservar_button = (By.CLASS_NAME, "smart-button-wrapper")
    buscando_automovil = (By.XPATH, "//div[text()='Buscar automóvil']")
    driver_arrives_in = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]')


class UrbanRoutesPage(BasePage):
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

    def comfort_button_is_selected(self):
        return self.driver.find_element(*self.comfort_button).is_selected()

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def click_telephone_number(self):
        return self.driver.find_element(*self.set_phone_number_button).click()

    def add_telephone_number(self, phone_number):
        return self.driver.find_element(*self.phone_number_field).send_keys(phone_number)

    def click_siguiente_button(self):
        return self.driver.find_element(*self.siguiente_button).click()

    def get_code(self):
        get_phone_code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.code_field).send_keys(get_phone_code)

    def click_in_confirmar_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.confirmar_button)
        ).click()

    #Proceso de tarjeta de credito
    def click_metodo_de_pago(self):
        return self.driver.find_element(*self.metodo_de_pago_button).click()

    def click_add_card(self):
        return self.driver.find_element(*self.add_card_button).click()

    def add_card_number(self):
        return self.driver.find_element(*self.add_card_field).send_keys(data.card_number)

    def add_code_number(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/div[2]/div[2]'))
        )
        return self.driver.find_element(*self.add_code_card_field).send_keys(data.card_code)

    def click_in_any_other_element(self):
        return self.driver.find_element(*self.strip_orange_yellow).click()

    def click_in_agregar(self):
        return self.driver.find_element(*self.agregar_button).click()

    def click_in_cerrar(self):
        return self.driver.find_element(*self.cerrar_button).click()

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
        return self.driver.find_element(*self.message_for_driver).text

    #Requisitos del pedido
    def click_requisitos_del_pedido(self):
        return self.driver.find_element(*self.requisitos_del_pedido_button).click()

    def click_in_manta_y_panuelos(self):
        return self.driver.find_element(*self.manta_y_panuelos_button).click()

    def click_in_icecream(self):
        icecream_button = self.driver.find_element(*self.helado_button)
        action_chains = ActionChains(self.driver)
        action_chains.double_click(icecream_button).perform()

    #Pedir taxi
    def click_order_cab(self):
        return self.driver.find_element(*self.reservar_button).click()

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

#Prueba 1: Configurar la direccion
    def test_from_to(self):
        self.driver.get(data.urban_routes_url)  # Usamos la URL desde el archivo data.py
        page = UrbanRoutesPage(self.driver)
        time.sleep(1)
        page.set_from(data.address_from)  # Usamos la dirección desde el archivo data.py
        page.set_to(data.address_to)  # Usamos la dirección desde el archivo data.py
        assert page.get_from() == data.address_from
        assert page.get_to() == data.address_to

   #Prueba 2: Seleccionar la tarifa Comfort
    def test_comfort_button_is_selected(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        time.sleep(1)
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        comfort_is_selected = page.comfort_button_is_selected()
        assert comfort_is_selected is True

    #Prueba 3: Rellenar el número de teléfono.
    def test_cell_number_field(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        time.sleep(1)
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        page.click_telephone_number()
        page.add_telephone_number(data.phone_number)
        page.click_siguiente_button()
        page.get_code()
        page.click_in_confirmar_button()

    #Prueba 4 Agregar una tarjeta de crédito.
    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        time.sleep(1)
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        page.click_metodo_de_pago()
        page.click_add_card()
        page.add_card_number()
        page.add_code_number()
        page.click_in_any_other_element()
        page.click_in_agregar()
        page.click_in_cerrar()

    #Prueba 5 Escribir un mensaje para el controlador.
    def test_send_message(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        time.sleep(1)
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        page.search_message_for_driver()
        page.wait_for_message_for_driver()
        page.send_message_for_driver()
        page.get_message_for_driver()
        time.sleep(3)
        text_message_for_driver = page.get_message_for_driver()
        assert text_message_for_driver == data.message_for_driver

    #Prueba 6 Pedir una manta y pañuelos.
    def test_blanket_napkins(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        time.sleep(1)
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        page.search_message_for_driver()
        page.wait_for_message_for_driver()
        page.send_message_for_driver()
        page.click_in_manta_y_panuelos()

    #Prueba 7 Pedir 2 helados.
    def test_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        time.sleep(1)
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        page.search_message_for_driver()
        page.wait_for_message_for_driver()
        page.send_message_for_driver()
        page.click_in_manta_y_panuelos()
        page.click_in_icecream()

    #Prueba 8 Aparece el modal para buscar un taxi.
    def test_looking_for_taxi(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        time.sleep(1)
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        page.search_message_for_driver()
        page.wait_for_message_for_driver()
        page.send_message_for_driver()
        page.click_in_manta_y_panuelos()
        page.click_in_icecream()
        page.click_order_cab()
        time.sleep(3)


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
