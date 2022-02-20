# Importar librerías

from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from py.Database import Database

class LoginScreen(Screen):
    dialog = None
    def __init__(self, **kwargs):
        super().__init__()  
        self.app = MDApp.get_running_app()

    # Esto se ejecutará en el momento en que se cargue y visualice la pantalla
    def on_pre_enter(self):
        # Se hará un "auto-focus" al campo de escribir usuario
         self.ids.user_login.focus = True

    # Iniciar sesión
    def login(self, USER, PASSWORD):
        # Llamar a la base de datos
        conn = Database.do_login(USER, PASSWORD)

        # Si la comprobación de contraseña es exitosa, se cambia de pantalla.
        # En caso contrario, no se hace nada y se avisa al usuario
        if conn == True:
            self.app.change_screen("UserScreen")
            Snackbar(text="Login correcto!").open()
        if conn == False:
            Snackbar(text="Usuario o contraseña erróneos.").open()
            pass
    
    # Registrar usuario
    def signup(self, USER, PASSWORD):
        # Llamar a la base de datos
        conn = Database.do_signup(USER, PASSWORD)

        if conn == True:
            Snackbar(text="Registro correcto!").open()
        if conn == False:
            Snackbar(text="Error interno al registrar.").open()
            pass

    

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Información software",
                text="""Programa hecho para SIRL 2021-22
Escrito en Python3 con Wing Python IDE y Visual Studio Code.
Complementos: KivyMD (GUI) y MaríaDB (base datos)

Kivy  ©  2010-2022 Kivy Team and other contributors
KivyMD  ©  2015-2021 Andrés Rodríguez, KivyMD Team and other contributors
MariaDB  ©  2009 - 2022 Michael "Monty" Widenius, MariaDB
Python  ©  2001-2022 Python Software Foundation 
Visual Studio Code  ©  2015-2022 Microsoft Corporation
Wing Python IDE  ©  1999-2022 Wingware

Kevin.
"""
            )
        self.dialog.open()