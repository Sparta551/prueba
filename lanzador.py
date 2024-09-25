import I2C_LCD_driver
from time import *
import mysql.connector

config ={
  'user': 'raspberry',
  'password': 'Empanadas2045/',
  'host': '4.228.37.57',
  'database': 'prueba',
}

def conectar_bd():
  try:
    conexion = mysql.connector.connect(**config)
    cursor = conexion, cursor()
    mylcd.lcd_display_string("Conexion establecida", 1)
    return conexion, cursor
  except mysql.connector.Error as err:
    mylcd.lcd_display_string("Error a conectarse", 1)
    return none, none

def insertar_placa(cursor, placa):
  query = ("INSERT INTO preuba.PLACAS (PLACAS) VALUES (%s)")
  cursor.execute(query, (placa,))

def main():
  conexion, cursor = conectar_bd()
  if not conexion:
    return 0
  while true:
    placa = mylcd.lcd_load_custom_chars("Insertar placas").strip()
    if placa == '0':
      break
    insertar_placa(cursor, placa)
    conexion.commit()

  cursor.close()
  conexion.close()
  mylcd.lcd_display_string("Conexion finalizada", 1)

if __name__ == "__main__":
  main()
