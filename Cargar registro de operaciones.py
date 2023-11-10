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
    database = sqlite3.connect(r"C:\Users\santi\Documents\GitHub\Financial_Ops_Database\Test_DB.db")
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


def nuevaOperacion():

    global ars_acum, mep_acum, ccl_acum, egreso_cash, ingreso_cash, valor_neto, ticker, fecha_liquidacion, dias_duracion
    tipo = {1: 'Compra', 2: 'Venta', 3: 'Ingreso', 4: 'Egreso', 5: 'Renta/Dividendos', 6:'Caucion'}
    moneda = {1: 'ARS', 2: 'USD', 3: 'USD CCL'}
    clase = {1: 'Bonos', 2: 'ONs', 3: 'Equity', 4: 'Crypto', 0: ''}
    plazo = {0: 'CI', 24: '24hs', 48: '48hs', 9: ''}

    año = int(input('\nIngrese el año de la operación: '))
    mes = int(input('\nIngrese el mes de la operación: '))
    dia = int(input('\nIngrese el dia de la operación: '))
    global fecha_operacion
    fecha_operacion = dt.date(año, mes, dia)

    valor_tipo = int(input(f'\n{tipo}\nIngrese el tipo de operación según el menu anterior: '))

    valor_moneda = int(input(f'\n{moneda}\nIngrese la moneda según el menu anterior: '))

    if tipo[valor_tipo] == 'Compra' or tipo[valor_tipo] == 'Venta':
        cantidad = float(input('\nIngrese la cantidad de la orden: '))
        valor_clase = int(input(f'\n{clase}\nIngrese la clase según el menu anterior: '))
        valor_plazo = int(input(f'\n{plazo}\nIngrese el plazo según el menu anterior: '))
        if plazo[valor_plazo] == 'CI':
            fecha_liquidacion = fecha_operacion
        elif plazo[valor_plazo] == '24hs':
            fecha_liquidacion = fecha_operacion + dt.timedelta(days=1)
        elif plazo[valor_plazo] == '48hs':
            fecha_liquidacion = fecha_operacion + dt.timedelta(days=2)
    elif tipo[valor_tipo] == 'Renta/Dividendos':
        valor_clase = int(input(f'\n{clase}\nIngrese la clase según el menu anterior: '))
        cantidad = 1
        fecha_liquidacion = fecha_operacion
        valor_plazo = 9
    elif tipo[valor_tipo] == 'Caucion':
        cantidad = 1
        dias_duracion = int(input('\nIngrese el plazo de la caución en dias: '))
        fecha_liquidacion = fecha_operacion + dt.timedelta(days=dias_duracion)
        valor_clase = 0
        valor_plazo = 9
        ticker = 'Caucion'
        ticker = ticker.upper()        
    else:
        cantidad = 1
        fecha_liquidacion = fecha_operacion
        valor_clase = 0
        valor_plazo = 9
        ticker = ''
        ticker = ticker.upper()

    if fecha_liquidacion.weekday() == 5:
        fecha_liquidacion = fecha_liquidacion + dt.timedelta(days=2)
    elif fecha_liquidacion.weekday() == 6:
        fecha_liquidacion = fecha_liquidacion + dt.timedelta(days=1)

    if tipo[valor_tipo] == 'Caucion' or tipo[valor_tipo] == 'Renta/Dividendos':
        precio_orden = float(input('\nIngrese la cantidad ganada: '))
    elif tipo[valor_tipo] == 'Egreso':
        precio_orden = float(input('\nIngrese la cantidad retirada: '))
    elif tipo[valor_tipo] == 'Ingreso':
        precio_orden = float(input('\nIngrese la cantidad enviada: '))
    elif tipo[valor_tipo] == 'Compra' or tipo[valor_tipo] == 'Venta':
        precio_orden = float(input('\nIngrese el precio de la orden: '))
    
    valor_operacion = float(precio_orden * cantidad)

    if (clase[valor_clase] == 'Bonos' and tipo[valor_tipo] != 'Renta/Dividendos') or (clase[valor_clase] == 'ONs' and tipo[valor_tipo] != 'Renta/Dividendos'):
        valor_operacion = float(precio_orden * cantidad / 100)
    else:
        valor_operacion = float(precio_orden * cantidad)

    if tipo[valor_tipo] == 'Compra' or tipo[valor_tipo] == 'Venta':
    #or tipo[valor_tipo] == 'Renta/Dividendos'
        if clase[valor_clase] == 'Equity':
            dm_iva = float((cantidad * precio_orden) * 0.0008 * 1.21)
            dm_iva = round(dm_iva, 2)
        elif clase[valor_clase] == 'Bonos' or clase[valor_clase] == 'ONs':
            dm_iva = (cantidad * precio_orden / 100) * 0.0001
            dm_iva = round(dm_iva, 2)
        elif clase[valor_clase] == 'Crypto':
            dm_iva = 0.0
        elif clase[valor_clase] == 'Bonos' and moneda[valor_moneda] == 'USD':
            dm_iva = 0.0
        else:
            dm_iva = 0.0
    else:
        dm_iva = 0.0
    # En el caso de ser Equity, la variable 'dm_iva' incluye el IVA

    if tipo[valor_tipo] == 'Compra' or tipo[valor_tipo] == 'Egreso':
        #egreso_cash = float(valor_operacion + dm_iva)
        valor_neto = float(valor_operacion + dm_iva)
    elif tipo[valor_tipo] == 'Venta' or tipo[valor_tipo] == 'Ingreso' or tipo[valor_tipo] == 'Renta/Dividendos':
        #ingreso_cash = float(valor_operacion - dm_iva)
        valor_neto = float(valor_operacion - dm_iva)
    elif tipo[valor_tipo] == 'Caucion':
        #ingreso_cash = float(valor_operacion - dm_iva)
        valor_neto = float(valor_operacion - dm_iva)

    if moneda[valor_moneda] == 'ARS':
        fx = float(input('\nIngrese el tipo de cambio en ARS: '))
    else:
        fx = 1
    
    if tipo[valor_tipo] == 'Compra' or tipo[valor_tipo] == 'Venta' or tipo[valor_tipo] == 'Renta/Dividendos':
        ticker = str(input('\nIngrese el ticker: '))
        ticker = ticker.upper()

    '''nuevo = ingreso_cash - egreso_cash
    if moneda[valor_moneda] == 'ARS':
        ars_acum += nuevo
    elif moneda[valor_moneda] == 'USD':
        mep_acum += nuevo
    elif moneda[valor_moneda] == 'USD CCL':
        ccl_acum += nuevo'''
        
    datos = (fecha_operacion, tipo[valor_tipo], moneda[valor_moneda],
            clase[valor_clase], plazo[valor_plazo], precio_orden, cantidad, fx,
            dm_iva, fecha_liquidacion, valor_neto, ticker)
    
    insertarOperaciones(data=datos)


nuevaOperacion()