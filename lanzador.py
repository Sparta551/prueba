import I2C_LCD_driver
from time import *
import mysql.connector

mylcd = I2C_LCD_driver.lcd()

config ={
  'user': 'raspberry',
  'password': 'Empanadas2045/',
  'host': '4.228.37.57',
  'database': 'prueba',
}

def conectar_bd():
  print('conectando a la base de datos')
  try:
    conexion = mysql.connector.connect(**config)
    cursor = conexion, cursor()
    mylcd.lcd_display_string("Conexion establecida", 1)
    print('conexion establecida')
    return conexion, cursor
  except mysql.connector.Error as err:
    mylcd.lcd_display_string("Error a conectarse", 1)
    return None, None
    print('error de conexion')

def insertar_placa(cursor, placa):
  query = ("INSERT INTO prueba.PLACAS (PLACAS) VALUES (%s)")
  cursor.execute(query, (placa,))

def main():
  conexion, cursor = conectar_bd()
  if not conexion:
    print('no se conecto')
    return 0
  while true:
    placa = mylcd.lcd_load_custom_chars("Insertar placas").strip()
    print('insertar placas')
    if placa == '0':
      print('break')
      break
    insertar_placa(cursor, placa)
    conexion.commit()

  cursor.close()
  conexion.close()
  mylcd.lcd_display_string("Conexion finalizada", 1)
  print('conexion cerrada')

if __name__ == "__main__":
  main()
