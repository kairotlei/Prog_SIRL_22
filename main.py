# Importamos varias librerías necesarias, como:
# "os.path" para que el programa localice los archivos necesarios
# "mariadb" para realizar la conexión con MaríaDB Server
# "kivy.*" y "kivymd.*", que nos crean una interfaz gráfica a partir de configuraciones .KV
# "py.*" son archivos con la programación a realizar en cada pantalla
import os.path
import mariadb
import sys
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivymd.uix.snackbar import Snackbar
from py.LoginScreen import LoginScreen
from py.UserScreen import UserScreen
from py.Database import Database
from kivymd.uix.menu import MDDropdownMenu


# Esta clase inciará el programa y sus parámetros necesarios

class MainAPP(MDApp):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Diccionario de pantallas que se utilizarán mientras se utilice el programa
        # Screen (pantalla) a utilizar = "id_de_pantalla", "título_de_ventana"
        # El "título de ventana" será lo que se mostrará al lado de "minimizar, maximizar, cerrar"
        self.list_screen = {
            LoginScreen: ("LoginScreen", "Iniciar sesión"),  
            UserScreen: ("UserScreen", "Gestión de usuarios")
}

    # Se le dice a Kivy que cargue el "ScreenManager", necesario para administrar más de una pantalla KV
    # También se le pide a Kivy que utilice el color naranja para cosas con color, y al no especificar
    # un tema oscuro el programa utilizará un tema claro/blanco
    def build(self):
        # Título de la ventana que se mosrará en el instante de ejecutar el programa   
        self.title = 'Iniciar sesión'
        # Color naranja como principal
        self.theme_cls.primary_palette = "Orange"
        # Se carga el ScreenManager
        self.root = Builder.load_file("kv/screenManager.kv")

    # Cargar los archivos KV asociados a cada pantalla de las definidas en el "def __init__"
    def on_start(self):
        for screen, details in self.list_screen.items():
            # Se lee la lista de pantallas, creada en el "def __init__"
            screen_id,text = details
            Builder.load_file(f"kv/{screen_id}.kv")
            # Se añade la pantalla a la vista (actualmente vacía) como si fuera un Widget
            self.root.ids.screen_manager.add_widget(screen(name=screen_id))


    # Cambiador de pantallas
    def change_screen(self, screen_id):
        # Se cambia la pantalla a visualizar por la determinada aquí (lo hace el programa internamente)
        self.root.ids.screen_manager.current = screen_id



# Se inicia Kivy y las distintas programaciones
if __name__ == "__main__":
    MainAPP().run()
