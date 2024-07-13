import data
from selenium import webdriver
from urban_routes_page import UrbanRoutesPage

"""
REVISION 2: Siguiendo las recomendaciones proporcionadas, el archivo main.py se ha dividido en 3 diferentes archivos para un mejor
acomodo del proyecto. Aquí en main.py solo se encuentran las pruebas realizadas, a las que se les agregaron métodos assert como comprobación
de que la prueba es un éxito, o bien, una leyenda de AssertionError que diga la razón por la cual sale en Error. A su vez, también
quito el uso del time.sleep(), cambiándose por un método de espera inteligente.
"""
"""
REVISION 3: Se agregan metodos assert en todas las pruebas y se quitan las excepciones de las aserciones
"""

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
        page.wait_time()
        page.set_from(data.address_from)  # Usamos la dirección desde el archivo data.py
        page.set_to(data.address_to)  # Usamos la dirección desde el archivo data.py
        assert page.get_from() == data.address_from
        assert page.get_to() == data.address_to

   #Prueba 2: Seleccionar la tarifa Comfort
    def test_comfort_button_is_selected(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.wait_time()
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        comfort_button = page.find_comfort_button()
        assert "active" in comfort_button.get_attribute("class"), "Comfort no seleccionado"

    #Prueba 3: Rellenar el número de teléfono.
    def test_cell_number_field(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.wait_time()
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        page.click_telephone_number()
        page.add_telephone_number(data.phone_number)
        page.click_next_button()
        page.get_code()
        assert page.click_in_confirm_button(), "No es posible clickear el botón 'Confirmar'"

    #Prueba 4 Agregar una tarjeta de crédito.
    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.wait_time()
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        page.click_payment_method()
        page.click_add_card()
        page.add_card_number()
        page.add_code_number()
        page.click_in_any_other_element()
        page.click_in_add()
        page.click_in_close()
        assert page.card_added(), "La tarjeta no se agregó correctamente."


    #Prueba 5 Escribir un mensaje para el controlador.
    def test_send_message(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.wait_time()
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        page.search_message_for_driver()
        page.wait_for_message_for_driver()
        page.send_message_for_driver()
        page.get_message_for_driver()
        text_message_for_driver = page.get_message_for_driver()
        assert text_message_for_driver == data.message_for_driver

    #Prueba 6 Pedir una manta y pañuelos.
    def test_blanket_napkins(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.wait_time()
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        page.search_message_for_driver()
        page.wait_for_message_for_driver()
        page.send_message_for_driver()
        page.click_in_blanket_napkins()
        manta_y_panuelos_is_selected = page.blanket_napkins_is_selected()
        assert manta_y_panuelos_is_selected, "Expected manta y panuelos to be selected but it was not."

    #Prueba 7 Pedir 2 helados.
    def test_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.wait_time()
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        page.search_message_for_driver()
        page.wait_for_message_for_driver()
        page.send_message_for_driver()
        page.click_in_blanket_napkins()
        page.click_in_icecream()
        ice_cream_count = page.get_ice_cream_count()
        assert ice_cream_count == 2, f"Expected 2 ice creams but found {ice_cream_count}"

    #Prueba 8 Aparece el modal para buscar un taxi.
    def test_looking_for_taxi(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.wait_time()
        page.set_route(data.address_from, data.address_to)
        page.click_taxi_button()
        page.wait_for_comfort_button()
        page.click_in_comfort()
        page.search_message_for_driver()
        page.wait_for_message_for_driver()
        page.send_message_for_driver()
        page.click_in_blanket_napkins()
        page.click_in_icecream()
        page.click_order_cab()
        order_header_content = page.looking_for_cab_screen()
        assert order_header_content.is_displayed(), "El elemento order-header-content no se está mostrando."

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
