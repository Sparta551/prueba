import I2C_LCD_driver
from time import sleep
import mysql.connector
import sys
import termios
import tty

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

def getch():
    """
    Captura un solo carácter del teclado sin esperar un Enter.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def leer_placa():
    """
    Lee la placa carácter por carácter, mostrando lo ingresado en el LCD en tiempo real.
    """
    placa = ""
    while True:
        mylcd.lcd_display_string("Escriba placa:", 1)
        char = getch()

        if char == '\n' or char == '\r':  # Terminar cuando se presiona Enter
            break
        elif char == '\x7f':  # Manejo del carácter de retroceso (backspace)
            if len(placa) > 0:
                placa = placa[:-1]  # Eliminar el último carácter
                mylcd.lcd_display_string(" " * 16, 2)  # Limpiar línea 2 del LCD
                mylcd.lcd_display_string(placa, 2)  # Mostrar la placa actualizada
        else:
            placa += char
            mylcd.lcd_display_string(placa, 2)  # Mostrar lo que se ha escrito en la línea 2 del LCD

    return placa.strip()

def main():
    # Conectar a la base de datos
    conexion, cursor = conectar_bd()
    if not conexion:
        print('No se pudo conectar a la base de datos')
        return 0
    
    while True:
        # Leer la placa en tiempo real y mostrarla en el LCD
        mylcd.lcd_clear()
        placa = leer_placa()
        
        # Mostrar la placa ingresada en el LCD
        mylcd.lcd_clear()
        mylcd.lcd_display_string(f"Placa: {placa}", 1)

        if placa == '0':
            mylcd.lcd_display_string("Fin del programa", 1)
            print('Fin del programa')
            break
        
        # Insertar la placa en la base de datos
        try:
            insertar_placa(cursor, placa)
            conexion.commit()
            
            # Mostrar confirmación en el LCD
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Placa insertada!", 1)
            sleep(2)  # Pausa para mostrar el mensaje en el LCD antes de continuar
        except mysql.connector.Error as err:
            # Mostrar mensaje de error en el LCD
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Error al insertar", 1)
            print(f"Error al insertar la placa: {err}")
            sleep(2)
    
    # Cerrar la conexión
    cursor.close()
    conexion.close()
    mylcd.lcd_display_string("Conexion finalizada", 1)
    print('Conexión cerrada')

if __name__ == "__main__":
    main()
