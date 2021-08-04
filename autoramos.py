import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.select import Select

class AutoRamos:

    # Esta clase de va a encargar de navegar a la pagina web e inscribir los ramos
    # El schedule se debe hacer fuera de la clase llamando el metodo start() a cierta hora
    # Se debe instanciar la clase con los argumentos requeridos y no pedir ningun input dentro de ella
    # Si las credenciales son incorrectas va a saltar una exception que se debe manejar fuera de la clase

    # TODO: Implementar un metodo que verifique que las credenciales sean correctas antes de hacer schedule
    
    drivers = {
            'nt': os.path.join('drivers','geckodriver.exe'),
            'posix': os.path.join('drivers','geckodriver'),
            }

    def __init__(self, ramos: list, usuario: str, clave: str) -> None:
        self.usuario = usuario
        self.clave = clave
        self.ramos = ramos

        self.os = os.name
        self.driver = None

        self.get_driver()

    def start(self) -> None:
        self.login()
        self.agregar_ramos()
    

    def get_driver(self) -> None:
        try:
            driver_path = AutoRamos.drivers[self.os]
            self.driver = webdriver.Firefox(executable_path=driver_path)

        except KeyError as err:
            print('SISTEMA OPERATIVO NO SOPORTADO')
            print(err)

    def login(self) -> None:
        if self.driver:
            usuariobox = self.driver.find_element_by_xpath('//*[@id="UserID"]')
            passwordbox = self.driver.find_element_by_xpath('/html/body/div[3]/form/table/tbody/tr[2]/td[2]/input')
            loginbutton = self.driver.find_element_by_xpath('/html/body/div[3]/form/p/input')

            usuariobox.send_keys(self.usuario)
            passwordbox.send_keys(self.clave)
            loginbutton.click()

            sleep(1)

    def agregar_ramos(self) -> None:
        if self.driver:
            agregarbutton = self.driver.find_element_by_xpath('/html/body/div[3]/table[2]/tbody/tr[2]/td[2]/a')

            agregarbutton.click()
            sleep(1)

            enviarbutton = self.driver.find_element_by_xpath('/html/body/div[3]/form/input')
            enviarbutton.click()
            sleep(1)

            seleccionarlist = self.driver.find_element_by_xpath('//*[@id="st_path_id"]')
            seleccionarlist = Select(seleccionarlist)
            seleccionarlist.select_by_index(1)

            enviarplan = self.driver.find_element_by_xpath('/html/body/div[3]/form/input[19]')
            enviarplan.click()
            sleep(1)


            # Encuentro todos los bloques de NRC y hago zip para enviar cada uno a su correspondiente bloque
            nrc_blocks = []
            nrc_blocks.append(self.driver.find_element_by_xpath('//*[@id="crn_id1"]'))
            nrc_blocks.append(self.driver.find_element_by_xpath('//*[@id="crn_id2"]'))
            nrc_blocks.append(self.driver.find_element_by_xpath('//*[@id="crn_id3"]'))

            for nrc, nrc_block in zip(self.ramos, nrc_blocks):
                nrc_block.send_keys(nrc)

            enviarcambios = self.driver.find_element_by_xpath('/html/body/div[3]/form/input[19]')
            enviarcambios.click()
            print('¡Ramos tomados!')
            


if __name__ == "__main__":
    pass