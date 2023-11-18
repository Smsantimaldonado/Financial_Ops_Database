import sqlite3
import datetime as dt
from tkinter import *


egreso_cash = 0.0
ingreso_cash = 0.0
dm_iva = 0.0
fx = 1.0
valor_operacion = 0.0
ars_acum = 0.0
mep_acum = 0.0
ccl_acum = 0.0


def crearDB():
    database = sqlite3.connect(r"C:\Users\santi\Documents\GitHub\Apps\Financial_Ops_Database\Test_DB.db")
    cursor = database.cursor()
    return database, cursor
#crearDB()


'''def crearTablas():
    database, cursor = crearDB()
    operaciones="""CREATE TABLE IF NOT EXISTS OPERACIONES(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    FechaOperación VARCHAR(12) NOT NULL,
                    Tipo VARCHAR (10) NOT NULL, Moneda VARCHAR(10) NOT NULL,
                    Clase VARCHAR(10) NOT NULL, Plazo VARCHAR(10) NOT NULL,
                    PrecioOrden VARCHAR(10) NOT NULL, Cantidad INTEGER NOT NULL,
                    Fx VARCHAR(10) NOT NULL, DmIVA VARCHAR(10) NOT NULL,
                    FechaLiquidación VARCHAR(12) NOT NULL,
                    ValorNeto VARCHAR (15) NOT NULL, Ticker VARCHAR (10) NOT NULL)"""
    diponibilidad = """CREATE TABLE IF NOT EXISTS DISPONIBILIDAD(
                       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       ARS VARCHAR(12) NOT NULL, MEP VARCHAR(10) NOT NULL,
                       CCL VARCHAR (10) NOT NULL)"""

    cursor.execute(operaciones)
    cursor.execute(diponibilidad)
    database.close()
crearTablas()'''

def insertarOperaciones(data):
    database, cursor = crearDB()
    accion = ("""
            INSERT INTO OPERACIONES (FechaOperación, Tipo, Moneda, Clase, Plazo, PrecioOrden, Cantidad, Fx, DmIVA, FechaLiquidación, ValorNeto, Ticker)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""")

    ventana = Tk()
    ventana.title('RESULTADOS DE LA OPERACIÓN')
    ventana.geometry('400x150')
    frame = Frame()
    frame.pack()

    if (cursor.execute(accion, data)):
        etiqueta = Label(frame, text='Datos guardados', font=('Arial', 14))
        etiqueta.grid(column=1, row=1)
        print('\nDatos guardados\n')
    else:
        etiqueta = Label(frame, text='Error en la carga de datos', font=('Arial', 14))
        etiqueta.grid(column=1, row=1)
        print('\nError en la carga de datos\n')

    def click():
        ventana.destroy()

    boton = Button(frame, text='Cerrar y Terminar', command=click)
    boton.grid(column=1, row=2)

    ventana.mainloop()

    database.commit()
    database.close()
    
    
def ingresar_fecha():
    global fecha_operacion
    ventana = Tk()
    ventana.title('INGRESAR FECHA')
    ventana.geometry('400x100')
    frame = Frame()
    frame.pack()
    frame.config()

    año=IntVar()
    etiqueta_año = Label(frame, text='Ingrese el año de la operación:', font=('Arial', 12))
    etiqueta_año.grid(column=1, row=1)
    entrada_año = Entry(frame, textvariable=año, width=15)
    entrada_año.grid(column=2, row=1)

    mes=IntVar()
    etiqueta_mes = Label(frame, text='Ingrese el mes de la operación:', font=('Arial', 12))
    etiqueta_mes.grid(column=1, row=2)
    entrada_mes = Entry(frame, textvariable=mes, width=15)
    entrada_mes.grid(column=2, row=2)

    dia=IntVar()
    etiqueta_dia = Label(frame, text='Ingrese el dia de la operación:', font=('Arial', 12))
    etiqueta_dia.grid(column=1, row=3)
    entrada_dia = Entry(frame, textvariable=dia, width=15)
    entrada_dia.grid(column=2, row=3)

    def click():
        ventana.destroy()

    boton = Button(frame, text='Aceptar', command=click)
    boton.grid(column=1, row=4)

    ventana.mainloop()

    fecha_operacion = dt.date(año.get(), mes.get(), dia.get())
    return fecha_operacion


tipo = {1: 'Compra', 2: 'Venta', 3: 'Ingreso', 4: 'Egreso', 5: 'Renta/Dividendos', 6:'Caucion'}
def elegir_tipo():
    global valor_tipo

    ventana = Tk()
    ventana.title('ELEGIR EL TIPO DE OPERACIÓN A REALIZAR')
    ventana.geometry('400x280')
    frame = Frame()
    frame.pack()

    etiqueta = Label(frame, text='Selecciona el tipo de operación\nsegún el siguiente menú', font=('Arial', 14))
    etiqueta.grid(column=1, row=2)

    opcion = IntVar()
    op_1 = Radiobutton(frame, text='[1] Compra', variable=opcion, value=1)
    op_1.grid(column=1, row=3)
    op_2 = Radiobutton(frame, text='[2] Venta', variable=opcion, value=2)
    op_2.grid(column=1, row=4)
    op_3 = Radiobutton(frame, text='[3] Ingreso', variable=opcion, value=3)
    op_3.grid(column=1, row=5)
    op_4 = Radiobutton(frame, text='[4] Egreso', variable=opcion, value=4)
    op_4.grid(column=1, row=6)
    op_5 = Radiobutton(frame, text='[5] Renta/Dividendos', variable=opcion, value=5)
    op_5.grid(column=1, row=7)
    op_6 = Radiobutton(frame, text='[6] Caucion', variable=opcion, value=6)
    op_6.grid(column=1, row=8)

    def click():
        ventana.destroy()

    boton = Button(frame, text='Aceptar', command=click)
    boton.grid(column=1, row=9)

    ventana.mainloop()

    valor_tipo = opcion.get()
    return valor_tipo


moneda = {1: 'ARS', 2: 'USD', 3: 'USD CCL'}
def elegir_moneda():
    global valor_moneda

    ventana = Tk()
    ventana.title('ELEGIR LA MONEDA DE LA OPERACIÓN')
    ventana.geometry('400x200')
    frame = Frame()
    frame.pack()

    etiqueta = Label(frame, text='Selecciona la moneda de operación\nsegún el siguiente menú', font=('Arial', 14))
    etiqueta.grid(column=1, row=2)

    opcion = IntVar()
    op_1 = Radiobutton(frame, text='[1] ARS', variable=opcion, value=1)
    op_1.grid(column=1, row=3)
    op_2 = Radiobutton(frame, text='[2] USD', variable=opcion, value=2)
    op_2.grid(column=1, row=4)
    op_3 = Radiobutton(frame, text='[3] USD CCL', variable=opcion, value=3)
    op_3.grid(column=1, row=5)

    def click():
        ventana.destroy()

    boton = Button(frame, text='Aceptar', command=click)
    boton.grid(column=1, row=6)

    ventana.mainloop()

    valor_moneda = opcion.get()
    return valor_moneda


def ingresar_cantidad():
    global cantidad

    ventana = Tk()
    ventana.title('INGRESAR CANTIDAD')
    ventana.geometry('400x100')
    frame = Frame()
    frame.pack()
    frame.config()

    cantidad=IntVar()
    etiqueta_cantidad = Label(frame, text='Ingrese la cantidad operada:', font=('Arial', 12))
    etiqueta_cantidad.grid(column=1, row=1)
    entrada_cantidad = Entry(frame, textvariable=cantidad, width=15)
    entrada_cantidad.grid(column=2, row=1)

    def click():
        ventana.destroy()

    boton = Button(frame, text='Aceptar', command=click)
    boton.grid(column=1, row=2)

    ventana.mainloop()

    cantidad = cantidad.get()
    return cantidad


clase = {1: 'Bonos', 2: 'ONs', 3: 'Equity', 4: 'Crypto', 0: ''}
def elegir_clase():
    global valor_clase

    def click():
        ventana.destroy()

    ventana = Tk()
    ventana.title('ELEGIR LA CLASE DE ACTIVO OPERADO')
    ventana.geometry('400x250')
    frame = Frame()
    frame.pack()

    etiqueta = Label(frame, text='Selecciona la clase de activo\nsegún el siguiente menú', font=('Arial', 14))
    etiqueta.grid(column=1, row=2)

    opcion = IntVar()
    op_1 = Radiobutton(frame, text='[1] Bonos', variable=opcion, value=1)
    op_1.grid(column=1, row=3)
    op_2 = Radiobutton(frame, text='[2] ONs', variable=opcion, value=2)
    op_2.grid(column=1, row=4)
    op_3 = Radiobutton(frame, text='[3] Equity', variable=opcion, value=3)
    op_3.grid(column=1, row=5)
    op_4 = Radiobutton(frame, text='[4] Crypto', variable=opcion, value=4)
    op_4.grid(column=1, row=6)
    op_5 = Radiobutton(frame, text='[5] Otro', variable=opcion, value=0)
    op_5.grid(column=1, row=7)

    boton = Button(frame, text='Aceptar', command=click)
    boton.grid(column=1, row=8)

    ventana.mainloop()

    valor_clase = opcion.get()
    return valor_clase


plazo = {0: 'CI', 24: '24hs', 48: '48hs', 9: ''}
def elegir_plazo():
    global valor_plazo

    def click():
        ventana.destroy()

    ventana = Tk()
    ventana.title('ELEGIR EL PLAZO')
    ventana.geometry('400x250')
    frame = Frame()
    frame.pack()

    etiqueta = Label(frame, text='Selecciona el plazo de la operación\nsegún el siguiente menú', font=('Arial', 14))
    etiqueta.grid(column=1, row=2)

    opcion = IntVar()
    op_1 = Radiobutton(frame, text='[1] CI', variable=opcion, value=0)
    op_1.grid(column=1, row=3)
    op_2 = Radiobutton(frame, text='[2] 24hs', variable=opcion, value=24)
    op_2.grid(column=1, row=4)
    op_3 = Radiobutton(frame, text='[3] 48hs', variable=opcion, value=48)
    op_3.grid(column=1, row=5)
    op_4 = Radiobutton(frame, text='[4] Otro', variable=opcion, value=9)
    op_4.grid(column=1, row=6)

    boton = Button(frame, text='Aceptar', command=click)
    boton.grid(column=1, row=7)

    ventana.mainloop()

    valor_plazo = opcion.get()
    return valor_plazo


def ingresar_precio_orden():
    global precio_orden

    ventana = Tk()
    ventana.title('INGRESAR PRECIO DE LA ORDEN')
    ventana.geometry('400x100')
    frame = Frame()
    frame.pack()
    frame.config()

    if tipo[valor_tipo] == 'Caucion' or tipo[valor_tipo] == 'Renta/Dividendos':
        etiqueta_precio_orden = Label(frame, text='Ingrese la cantidad ganada:', font=('Arial', 12))
    elif tipo[valor_tipo] == 'Egreso':
        etiqueta_precio_orden = Label(frame, text='Ingrese la cantidad retirada:', font=('Arial', 12))
    elif tipo[valor_tipo] == 'Ingreso':
        etiqueta_precio_orden = Label(frame, text='Ingrese la cantidad enviada:', font=('Arial', 12))
    elif tipo[valor_tipo] == 'Compra' or tipo[valor_tipo] == 'Venta':
        etiqueta_precio_orden = Label(frame, text='Ingrese el precio de la orden:', font=('Arial', 12))
    
    etiqueta_precio_orden.grid(column=1, row=1)

    precio_orden = DoubleVar()
    entrada_precio_orden = Entry(frame, textvariable=precio_orden, width=15)
    entrada_precio_orden.grid(column=2, row=1)

    def click():
        ventana.destroy()

    boton = Button(frame, text='Aceptar', command=click)
    boton.grid(column=1, row=2)

    ventana.mainloop()

    precio_orden = precio_orden.get()
    return precio_orden


def ingresar_ticker():
    global ticker

    ventana = Tk()
    ventana.title('INGRESAR TICKER')
    ventana.geometry('400x100')
    frame = Frame()
    frame.pack()
    frame.config()

    ticker = StringVar()
    etiqueta_ticker = Label(frame, text='Ingrese el ticker:', font=('Arial', 12))
    etiqueta_ticker.grid(column=1, row=1)
    entrada_ticker = Entry(frame, textvariable=ticker, width=15)
    entrada_ticker.grid(column=2, row=1)

    def click():
        ventana.destroy()

    boton = Button(frame, text='Aceptar', command=click)
    boton.grid(column=1, row=2)

    ventana.mainloop()

    ticker = ticker.get()
    ticker = ticker.upper()
    return ticker


def duracion_caucion():
    global dias_duracion

    ventana = Tk()
    ventana.title('INGRESAR DURACION CAUCION')
    ventana.geometry('400x100')
    frame = Frame()
    frame.pack()
    frame.config()

    dias_duracion=IntVar()
    etiqueta_dias_duracion = Label(frame, text='Ingrese los dias de duracion:', font=('Arial', 12))
    etiqueta_dias_duracion.grid(column=1, row=1)
    entrada_dias_duracion = Entry(frame, textvariable=dias_duracion, width=15)
    entrada_dias_duracion.grid(column=2, row=1)

    def click():
        ventana.destroy()

    boton = Button(frame, text='Aceptar', command=click)
    boton.grid(column=1, row=2)

    ventana.mainloop()

    dias_duracion = dias_duracion.get()
    return dias_duracion


def ingresar_fx():
    global fx

    ventana = Tk()
    ventana.title('INGRESAR FX RATE')
    ventana.geometry('400x100')
    frame = Frame()
    frame.pack()
    frame.config()
    
    etiqueta = Label(frame, text='Último paso!', font=('Arial', 14))
    etiqueta.grid(column=1, row=1)

    etiqueta_fx = Label(frame, text='Ingrese el tipo de cambio en ARS:', font=('Arial', 12))
    etiqueta_fx.grid(column=1, row=2)

    fx = DoubleVar()
    entrada_fx = Entry(frame, textvariable=fx, width=15)
    entrada_fx.grid(column=2, row=2)

    def click():
        ventana.destroy()

    boton = Button(frame, text='Aceptar', command=click)
    boton.grid(column=1, row=3)

    ventana.mainloop()

    fx = fx.get()
    return fx


def nuevaOperacion():
    global ars_acum, mep_acum, ccl_acum, egreso_cash, ingreso_cash, valor_neto, fecha_liquidacion, dias_duracion
    global fecha_operacion, valor_tipo, valor_moneda

    fecha_operacion = ingresar_fecha() # retorna fecha_operacion
    valor_tipo = elegir_tipo() # retorna valor_tipo
    valor_moneda = elegir_moneda() # retorna valor_moneda

    if tipo[valor_tipo] == 'Compra' or tipo[valor_tipo] == 'Venta':
        cantidad = ingresar_cantidad() # retorna cantidad
        valor_clase = elegir_clase() # retorna valor_clase
        valor_plazo = elegir_plazo() # retorna valor_plazo
        if plazo[valor_plazo] == 'CI':
            fecha_liquidacion = fecha_operacion
        elif plazo[valor_plazo] == '24hs':
            fecha_liquidacion = fecha_operacion + dt.timedelta(days=1)
        elif plazo[valor_plazo] == '48hs':
            fecha_liquidacion = fecha_operacion + dt.timedelta(days=2)
        else:
            fecha_liquidacion = ''
    elif tipo[valor_tipo] == 'Renta/Dividendos':
        valor_clase = elegir_clase() # retorna valor_clase
        cantidad = 1
        fecha_liquidacion = fecha_operacion
        valor_plazo = 9
    elif tipo[valor_tipo] == 'Caucion':
        cantidad = 1
        dias_duracion = duracion_caucion()
        fecha_liquidacion = fecha_operacion + dt.timedelta(days=dias_duracion)
        valor_clase = 0
        valor_plazo = 9
    else:
        cantidad = 1
        fecha_liquidacion = fecha_operacion
        valor_clase = 0
        valor_plazo = 9
        ticker = ''

    if fecha_liquidacion.weekday() == 5:
        fecha_liquidacion = fecha_liquidacion + dt.timedelta(days=2)
    elif fecha_liquidacion.weekday() == 6:
        fecha_liquidacion = fecha_liquidacion + dt.timedelta(days=1)

    precio_orden = ingresar_precio_orden()
    
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
    
    if tipo[valor_tipo] == 'Compra' or tipo[valor_tipo] == 'Venta' or tipo[valor_tipo] == 'Renta/Dividendos':
        ticker = ingresar_ticker()
    elif tipo[valor_tipo] == 'Caucion':
        ticker = 'CAUCION'
    else:
        ticker = ''

    if moneda[valor_moneda] == 'ARS':
        fx = ingresar_fx()
    else:
        fx = 1
    
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


def consultar():
    ventana = Tk()
    ventana.title('BORRAR OPERACION')
    ventana.geometry('400x100')
    frame = Frame()
    frame.pack()
    frame.config()

    etiqueta_iidd = Label(frame, text='Ingrese el ID del registro a consultar:', font=('Arial', 12))
    etiqueta_iidd.grid(column=1, row=1)
    entrada_iidd = Entry(frame, textvariable=IntVar(), width=15)
    entrada_iidd.grid(column=2, row=1)

    def click():
        database, cursor = crearDB()
        indicacion = f"""SELECT * FROM OPERACIONES WHERE ID={entrada_iidd.get()}"""
        cursor.execute(indicacion)
        for columna in cursor:
            print('\n---------------------------------------\n')
            print('Fecha de la operación:   ', columna[1])
            print('Tipo de operación:       ', columna[2])
            print('Moneda:                  ', columna[3])
            print('Clase:                   ', columna[4])
            print('Plazo:                   ', columna[5])
            print('Precio de la orden:      ', columna[6])
            print('Cantidad:                ', columna[7])
            print('Fx:                      ', columna[8])
            print('Dm + IVA:                ', columna[9])
            print('Fecha de liquidación:    ', columna[10])
            print('Valor Neto:              ', columna[11])
            print('Ticker:                  ', columna[12])
            print('\n---------------------------------------\n')
        database.close()
        database.commit()
        database.close()
        ventana.destroy()

    boton = Button(frame, text='Aceptar', command=click) #
    boton.grid(column=1, row=100)

    ventana.mainloop()


def modificar():
    ventana = Tk()
    ventana.title('MODIFICAR OPERACION')
    ventana.geometry('400x100')
    frame = Frame()
    frame.pack()
    frame.config()

    etiqueta_iidd = Label(frame, text='Ingrese el ID del registro a modificar:', font=('Arial', 12))
    etiqueta_iidd.grid(column=1, row=1)
    entrada_iidd = Entry(frame, textvariable=IntVar(), width=15)
    entrada_iidd.grid(column=2, row=1)

    etiqueta_variab = Label(frame, text='Ingrese el nombre de la variable a modificar:', font=('Arial', 12))
    etiqueta_variab.grid(column=1, row=2)
    entrada_variab = Entry(frame, width=15)
    entrada_variab.grid(column=2, row=2)

    etiqueta_valor = Label(frame, text='Ingrese el nuevo valor de la variable:', font=('Arial', 12))
    etiqueta_valor.grid(column=1, row=3)
    entrada_valor = Entry(frame, width=15)
    entrada_valor.grid(column=2, row=3)

    def click():
        database, cursor = crearDB()
        indicacion= f"""UPDATE OPERACIONES
                        SET {entrada_variab.get()}='{entrada_valor.get()}'
                        WHERE ID={entrada_iidd.get()}"""
        
        if cursor.execute(indicacion):
            print('\nDatos modificados\n')
        else:
            print('\nError en la modificacion de datos\n')
        cursor.close()
        database.commit()
        database.close()
        ventana.destroy()

    boton = Button(frame, text='Aceptar', command=click)
    boton.grid(column=1, row=100)

    ventana.mainloop()


def borrar():
    ventana = Tk()
    ventana.title('BORRAR OPERACION')
    ventana.geometry('400x100')
    frame = Frame()
    frame.pack()
    frame.config()

    etiqueta_iidd = Label(frame, text='Ingrese el ID del registro a borrar:', font=('Arial', 12))
    etiqueta_iidd.grid(column=1, row=1)
    entrada_iidd = Entry(frame, textvariable=IntVar(), width=15)
    entrada_iidd.grid(column=2, row=1)

    def click():
        database, cursor = crearDB()
        indicacion = f"""DELETE
                         FROM OPERACIONES
                         WHERE ID = {int(entrada_iidd.get())}"""
        if cursor.execute(indicacion):
            print('\nDatos borrados\n')
        else:
            print('\nError en la eliminación de datos\n')
        cursor.close()
        database.commit()
        database.close()
        ventana.destroy()

    boton = Button(frame, text='Aceptar', command=click) #
    boton.grid(column=1, row=100)

    ventana.mainloop()


def elegir_operacion():
    ventana = Tk()
    ventana.title('ELEGIR LA OPERACIÓN A REALIZAR')
    ventana.geometry('400x200')
    frame = Frame()
    frame.pack()

    etiqueta = Label(frame, text='¿Qué desea hacer? \nIngrese una opción del siguiente menú', font=('Arial', 14))
    etiqueta.grid(column=1, row=2)

    opcion = IntVar()
    op_1 = Radiobutton(frame, text='[1] Cargar una nueva operación', variable=opcion, value=1)
    op_1.grid(column=1, row=3)
    op_2 = Radiobutton(frame, text='[2] Consultar un registro de la base de datos', variable=opcion, value=2)
    op_2.grid(column=1, row=4)
    op_3 = Radiobutton(frame, text='[3] Modificar un registro', variable=opcion, value=3)
    op_3.grid(column=1, row=5)
    op_4 = Radiobutton(frame, text='[4] Borrar un registro', variable=opcion, value=4)
    op_4.grid(column=1, row=6)

    def click():
        ventana.destroy()
        while opcion.get() > 0 and opcion.get() <=4:
            if opcion.get() == 1:
                nuevaOperacion()
                break
            elif opcion.get() == 2:
                consultar()
                break
            elif opcion.get() == 3:
                modificar() 
                break
            elif opcion.get() == 4:
                borrar()
                break
            else:
                print('El valor ingresado no corresponde a una opción del menu ofrecido')

    boton = Button(frame, text='Aceptar', command=click)
    boton.grid(column=1, row=7)

    ventana.mainloop()

elegir_operacion()