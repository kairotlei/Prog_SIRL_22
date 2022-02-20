# Importar librerías

from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from py.Database import Database
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivy.metrics import dp
from kivy.properties import StringProperty

import os.path


class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class UserScreen(Screen):
    def __init__(self,**kw):
        super().__init__()
        # Diccionario de pantallas
        # Pantalla = (id, nombre a mostrar)
        self.app = MDApp.get_running_app()


        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(35),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": UserScreen.read_data_this(self,x)
            } for i in Database.get_names()]


        self.menu = MDDropdownMenu(
            caller=self.ids.search_button,
            items=menu_items,
            position="bottom",
            width_mult=3,
        )
    
    def on_pre_enter(self):
        self.app.title = "Gestión de usuarios"
    

    def set_item(self, text__item):
        self.ids.user_name.text = text__item
        self.menu.dismiss()
        UserScreen.update_dropdown(self)

    def update_dropdown(self):
        UserScreen.__init__.menu_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(35),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": UserScreen.read_data_this(self,x)
            } for i in Database.get_names()]


    # BUSCAR INFO DE ALUMNO A PARTIR DE SU NOMBRE
    def read_data_this(self, NAME):
        rd = Database.do_read_this(NAME)
        

        if rd == "!":
            Snackbar(text="¡El alumno solicitado no existe!").open()
        else:
            self.ids.user_name.text = rd[0]
            self.ids.user_surname.text = rd[1]
            self.ids.user_course.text = rd[2]
            self.ids.user_telegram.text = rd[4]
            if "@" in rd[3]:
                email_user = rd[3].split("@")[0]
                email_domain = rd[3].split("@")[1]
                self.ids.user_email_domain.text = email_domain
            else:
                email_user = rd[3]
            self.ids.user_email.text = email_user




    # GUARDAR NUEVO ALUMNO
    # Se pasan los datos de los TextField mediante argumentos de función
    def save_data(self, NAME, SURNAME, COURSE, EMAIL, EDOMAIN, TELEGRAM):
        if NAME == "":
            Snackbar(text="¡El nombre no puede estar vacío!").open()
            return
        
        # Esto hará que la primera letra de nombre y apellidos sea siempre mayúscula
        NAME = NAME.title()
        SURNAME = SURNAME.title()

        # Si no se escribe nada ni en correo ni en dominio, se da por hecho que el usuario no tiene o no quiere
        # anotar un email, así que se almacena en blanco
        if EMAIL == "" and EDOMAIN == "":
            Snackbar(text="No se ha proporcionado email - se guardará vacío").open()

        # Si el correo es "ASDF@", notificar y abortar guardado.
        elif EDOMAIN == "":
            Snackbar(text="Email incompleto:  falta 'servicio.com'").open()
            return
            

        # Si el correo es "@EMAIL.COM", notificar y abortar guardado.
        elif EMAIL == "":
            Snackbar(text="Email incompleto:  falta dirección personal").open()
            return

        # Si el correo es "ASDF@EMAILCOM", notificar y abortar guardado.    
        elif EDOMAIN != "" and "." not in EDOMAIN:
            Snackbar(text="Email incompleto:  'servicio.com' no válido").open()
            return

        # Se supone entonces que el correo es "ASDF@EMAIL.COM", así que se guarda en la variable "email"
        # Si está todo vacío, se guarda en blanco.
        elif EMAIL != "" and EDOMAIN != "":
            EMAIL = str(EMAIL+"@"+EDOMAIN)
        else:
            EMAIL = ""
        

        saved = Database.do_save_alumn(NAME, SURNAME, COURSE, EMAIL, TELEGRAM)

        if saved == True:
            Snackbar(text="¡Alumno registrado!").open()
        else:
            Snackbar(text="Error al guardar alumno: {e}").open()
        
        UserScreen.update_dropdown(self)

        self.ids.user_name.text = ""
        self.ids.user_surname.text =  ""
        self.ids.user_course.text =  ""
        self.ids.user_telegram.text =  ""
        self.ids.user_email.text =  ""
        self.ids.user_email_domain.text =  ""
        


    def exit_app(self):
        exit()

