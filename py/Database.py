from dataclasses import fields
from locale import D_FMT
import mariadb
import sys
import os.path
from kivymd.uix.snackbar import Snackbar
import json


# ============================ Config de María DB ==========================

# Se carga la configuración de base de datos desde un archivo json para facilitar la configuración.
try:
    # Por precaución, se carga el archivo en modo solo lectura.
    with open('config/mariadb_config.json', 'r') as json_file:
        # El archivo .json se convierte a diccionario de Python
        mdb_JSONCONFIG = json.load(json_file)

        # Se pasan los datos del diccionario a las variables que utilizarán los comandos de MaríaDB
        mdb_HOST = mdb_JSONCONFIG[0]["mariadb-HOST"]
        mdb_PORT = mdb_JSONCONFIG[0]["mariadb-PORT"]
        mdb_USER = mdb_JSONCONFIG[0]["mariadb-USER"]
        mdb_PASSWORD = mdb_JSONCONFIG[0]["mariadb-PASS"]
        mdb_DB = mdb_JSONCONFIG[0]["mariadb-BASE"]
        


# La base de datos es fundamental. Si no fuera posible cargar su configuración, se detiene el programa.
except Exception as e:
    print(" >> Se necesita una base de datos válida para que el programa pueda funcionar.")
    print(" >> Revise el contenido o existencia del archivo ./config/mariadb_config.json")
    print(" >> El programa se cerrará.")
    print(f" >> Error: {e}")
    exit()




################################################################################
################################################################################

class Database():
    # Función que realizará el proceso de verificar usario/contraseña para iniciar sesión.
    def do_login(USER, PASSWORD):
        # Se da por hecho que va a fallar.
        ps_ok = False
        try:
            # Se conecta con MaríaDB
            connection = mariadb.connect(host=mdb_HOST,port=mdb_PORT,user=mdb_USER,passwd=mdb_PASSWORD,db=mdb_DB)
            # Se crea un cursor
            cursor = connection.cursor()
            # Se le pide a base de datos la contraseña de lusario que hemos introducido
            cursor.execute(f"SELECT Pass FROM login WHERE User = '{USER}'")
            # Si la contraseña está y es igual a lo que hemos escrito,
            # se concederá acceso a la pantalla de gestión de alumnado.
            for (db_pass) in cursor:
                if db_pass[0] == PASSWORD:
                    print("Pass ok")
                    ps_ok = True
                else:
                    print("Pass fail")
                    ps_ok = False

        # Visión en consola del error, en caso de producirse
        except mariadb.Error as e:
            print(f"Error al conectar con MaríaDB: {e}")
            sys.exit(1)
        
        # Se devuelve False si algo falla, y únicamente True si la comprobación es exitosa.
        return ps_ok





################################################################################
################################################################################

    # Función que realizará el registro de un nuevo usuario en la base de datos
    def do_signup(USER, PASSWORD):
        # Se da por hecho que va a fallar.
        sn_ok = False
        try:
            # Se conecta con MaríaDB
            connection = mariadb.connect(host=mdb_HOST,port=mdb_PORT,user=mdb_USER,passwd=mdb_PASSWORD,db=mdb_DB)
            # Se crea un cursor
            cursor = connection.cursor()
            # Pedir a base de datos
            try:
                #Predefinir futura variable (se explica abajo)
                user_in_db = "?"


                # Si la longitud es demasiado larga (según la VARCHAR 25 establecida en MaríaDB), notificar y no hacer nada.
                if len(USER) >25 and len(PASSWORD) >25:
                    Snackbar(text="Longitud máxima de nombre y contraseña: 25 caracteres").open()
                    sn_ok: False



                # Si las inputs tienen longitud correcta, ejecutar...            
                elif len(USER) >2 and len(PASSWORD) >2:
                    # Buscar si ya existe el usuario a registrar
                    cursor.execute(f"SELECT User FROM login WHERE User = '{USER}'")

                    # Si el CURSOR.EXECUTE no falla y se entra al FOR,
                    # definir variable a modo de indicador de que no se ha entrado en el FOR
                    user_in_db = "!"

                    # Si existe entrará en el FOR y se notifica mediante Snackbar,
                    # si no entra al FOR será porque no hay user y al no entrar al FOR hará lo presente en el siguiente ELIF
                    for (db_user) in cursor:
                        user_in_db = db_user[0]
                        print(user_in_db)
                        if user_in_db == USER:
                            print("User already exists!")
                            Snackbar(text="El usuario introducido ya existe!").open()
                            sn_ok = False
                            user_in_db = "exists"
                            
                    # Se registra al usuario porque cumple el mínimo de longitud
                    # y el usuario no existe/ía en la DB
                    if user_in_db == "!":
                        print("Proceed")
                        cursor.execute(f"INSERT INTO login(User, Pass) VALUES ('{USER}', '{PASSWORD}')")
                        connection.commit()
                        sn_ok = True
                        print("Done!")
                

                # Si la longitud es demasiado corta (porque ni es muy larga ni es adecuada), se notifica y no se hace nada.
                else:
                    Snackbar(text="Longitud mínima de nombre y contraseña: 3 caracteres").open()
                    sn_ok: False

            except mariadb.Error as e:
                print(f"Error al registrar en MaríaDB: {e}")
                sn_ok = False


        # Visión en consola del error, en caso de producirse
        except mariadb.Error as e:
            print(f"Error al conectar con MaríaDB: {e}")
            sys.exit(1)

        # Se devuelve False si algo falla, y únicamente True si el registro es exitoso.
        return sn_ok




################################################################################
################################################################################
    # Esto se encarga de buscar un alumno en la base de datos en base a su nombre.
    def do_read_this(NAME):
        try:
            # Conectar con MaríaDB
            connection = mariadb.connect(host=mdb_HOST,port=mdb_PORT,user=mdb_USER,passwd=mdb_PASSWORD,db=mdb_DB)
            # Crear cursor
            cursor = connection.cursor()

            # Pedir a base de datos los datos del alumno que coincida el nombre 
            try:
                cursor.execute(f"SELECT Name,Surname,Course,Email,Telegram FROM aln WHERE Name = '{NAME}'")

                # Marcar que aún no se ha entrado en al FOR
                # si se entra es sobreescrito
                fields_of_user_db = "!"

                # Extraer datos de usuario de la tabla
                for (db_out) in cursor:
                    print(db_out)
                    fields_of_user_db = db_out
                    Snackbar(text="¡Datos de usuario leídos!").open()

            except:
                print("Error!!")
                Snackbar(text="Error al solicitar datos.").open()

        # Visión en consola del error, en caso de producirse
        except mariadb.Error as e:
            print(f"Error al conectar con MaríaDB: {e}")
            sys.exit(1)
        
        # Finalizar y enviar datos
        return fields_of_user_db


################################################################################
################################################################################

    # Permite añadir datos de alumnos a la tabla de alumnos en la base de datos
    def do_save_alumn(NAME, SURNAME, COURSE, EMAIL, TELEGRAM):
        # Se da por hecho que podría fallar
        sd_ok = False
        try:
            # Conexión con MaríaDB
            connection = mariadb.connect(host=mdb_HOST,port=mdb_PORT,user=mdb_USER,passwd=mdb_PASSWORD,db=mdb_DB)
            # Crear cursor
            cursor = connection.cursor()
            # Registrar a base de datos
            try:
                cursor.execute(f"INSERT INTO aln(Name,Surname,Course,Email,Telegram) VALUES ('{NAME}', '{SURNAME}','{COURSE}','{EMAIL}','{TELEGRAM}')")
                connection.commit()
                print("Aln. registered!")
                sd_ok = True


            except mariadb.Error as e:
                print(f"Error al registrar en MaríaDB: {e}")
                sd_ok = False


        # Visión en pantalla del error    
        except mariadb.Error as e:
            print(f"Error al conectar con MaríaDB: {e}")
            sys.exit(1)
        
        return sd_ok

################################################################################
################################################################################

    # Recoge los nombres de todos los alumnos de la base de datos, principalmente para el buscador
    def get_names():
        try:
            # Conexión con MaríaDB
            connection = mariadb.connect(host=mdb_HOST,port=mdb_PORT,user=mdb_USER,passwd=mdb_PASSWORD,db=mdb_DB)
            # Crear cursor
            cursor = connection.cursor()

            # Pedir a base de datos
            try:
                cursor.execute(f"SELECT Name FROM aln")
                # Extraer datos de usuario de la tabla
                all_alnames = cursor.fetchall()
                print(all_alnames)
                alumns_list = []

                for alumn in all_alnames:
                    all_alnames = cursor.fetchone()
                    alumns_list.append(alumn[0])


            except:
                print("Error!!")
                Snackbar(text="Error al solicitar datos.").open()

        # Visión en pantalla del error    
        except mariadb.Error as e:
            print(f"Error al conectar con MaríaDB: {e}")
            sys.exit(1)
        
        # Finalizar y enviar datos
        return alumns_list
