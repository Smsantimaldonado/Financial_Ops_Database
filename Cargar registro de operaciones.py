# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 19:08:24 2023

FUM: Fri Nov  10 21:23:38 2023

@author: Santiago Maldonado
"""

import sqlite3
import datetime as dt

egreso_cash = 0.0
ingreso_cash = 0.0
dm_iva = 0.0
fx = 1.0
valor_operacion = 0.0
ars_acum = 0.0
mep_acum = 0.0
ccl_acum = 0.0


def crearDB():
    database = sqlite3.connect(r"C:/Users/santi/Documents/GitHub/Finance/Test_DB.db")
    cursor = database.cursor()
    return database, cursor
crearDB()


def crearTablas():

    database, cursor = crearDB()
    operaciones="""CREATE TABLE IF NOT EXISTS OPERACIONES
                    (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    FechaOperación VARCHAR(12) NOT NULL,
                    Tipo VARCHAR (10) NOT NULL, Moneda VARCHAR(10) NOT NULL,
                    Clase VARCHAR(10) NOT NULL, Plazo VARCHAR(10) NOT NULL,
                    PrecioOrden VARCHAR(10) NOT NULL, Cantidad INTEGER NOT NULL,
                    Fx VARCHAR(10) NOT NULL, DmIVA VARCHAR(10) NOT NULL,
                    FechaLiquidación VARCHAR(12) NOT NULL,
                    ValorNeto VARCHAR (15) NOT NULL, Ticker VARCHAR (10) NOT NULL
                    )
                """
    diponibilidad = """ CREATE TABLE IF NOT EXISTS DISPONIBILIDAD
                        (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        ARS VARCHAR(12) NOT NULL, MEP VARCHAR(10) NOT NULL,
                        CCL VARCHAR (10) NOT NULL
                        )
                    """

    cursor.execute(operaciones)
    cursor.execute(diponibilidad)
    database.close()
crearTablas()


def insertarOperaciones(data):

    database, cursor = crearDB()
    accion = (" \n"
              "        INSERT INTO OPERACIONES (FechaOperación, Tipo, Moneda, Clase, Plazo, PrecioOrden, Cantidad, Fx, DmIVA, FechaLiquidación, ValorNeto, Ticker) \n"
              "        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\n"
              "        ")

    if (cursor.execute(accion, data)):
        print('\nDatos guardados')
        print('\n')
    else:
        print('\nError en la carga de datos')
        print('\n')
    database.commit()
    database.close()