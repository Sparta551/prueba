import I2C_LCD_driver
from time import *
import mysql.connector

# Inicializar el LCD
mylcd = I2C_LCD_driver.lcd()

# Configuración de conexión a la base de datos MySQL
config = {
    'user': 'raspberry',
    'password': 'Empanadas2045/',
    'host': 'parkease-ur.brazilsouth.cloudapp.azure.com',
    'database': 'prueba',
}

def conectar_bd():
    print('Conectando a la base de datos...')
    mylcd.lcd_display_string("Conectando a BD...", 1)
    
    try:
        # Establecer conexión a MySQL
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()
        
        # Mostrar en el LCD si la conexión fue exitosa
        mylcd.lcd_display_string("Conexion establecida", 1)
        print('Conexión establecida')
        return conexion, cursor
    except mysql.connector.Error as err:
        # Mostrar error en el LCD y en la consola
        mylcd.lcd_display_string("Error al", 1)
        mylcd.lcd_display_string("conectarse", 2)
        print(f"Error de conexión: {err}")
        return None, None

def insertar_placa(cursor, placa):
    # Consulta SQL para insertar una placa
    query = "INSERT INTO prueba.PLACAS (PLACAS) VALUES (%s)"
    cursor.execute(query, (placa,))

def main():
    # Conectar a la base de datos
    conexion, cursor = conectar_bd()
    if not conexion:
        print('No se pudo conectar a la base de datos')
        return 0
    
    while True:
        # Mostrar mensaje en el LCD para ingresar una placa
        mylcd.lcd_display_string("Insertar placa:", 1)
        placa = mylcd.lcd_load_custom_chars("Insertar placas").strip()
        # Capturar entrada del usuario (simulando por consola)
        placa = input("Ingresa la placa (o 0 para salir): ").strip()  # Simulación del input por consola
        
        if placa == '0':
            mylcd.lcd_display_string("Fin del programa", 1)
            print('Fin del programa')
            break
        
        # Insertar la placa en la base de datos
        insertar_placa(cursor, placa)
        conexion.commit()
        
        # Mostrar confirmación en el LCD
        mylcd.lcd_display_string("Placa insertada!", 1)
        sleep(2)  # Pausa para mostrar el mensaje en el LCD antes de continuar
    
    # Cerrar la conexión
    cursor.close()
    conexion.close()
    mylcd.lcd_display_string("Conexion finalizada", 1)
    print('Conexión cerrada')

if __name__ == "__main__":
    main()
