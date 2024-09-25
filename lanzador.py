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
    mylcd.lcd_display_string("conexion establecida", 1)
    return conexion, cursor
  except mysql.connector.Error as err:
    mylcd.lcd_display_string("Error a conectarse", 1)
    return none, none

def insertar_placa(cursor, placa):
  
