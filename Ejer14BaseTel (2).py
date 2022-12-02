#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Escribir un programa para gestionar un listado telefónico con los siguientes campos:
 dni, nombre y apellido, dirección, teléfonos de los clientes de una empresa. 
El programa incorpora funciones para:
- crear la base, 
- crear las tablas, 
- incorporar algunos registros a la tabla, 
- consultar el teléfono de un cliente solicitado, 
- añadir un nuevo cliente con sus datos,
- modificar el teléfono o dirección de un cliente solicitado,
- eliminar el teléfono de un cliente
- mostrar listado de todos los clientes en la tabla.
"""
import mariadb # importa la libreria
class BaseTel(object):
    def __init__(self):
        self.mydb = ""
        self.mycursor = ""
    def conectarAdmin(self):
        self.mydb = mariadb.connect(
	    host="127.0.0.1",
            user="root",
            autocommit=True
            )
        #print(self.mydb)
    def crearBase(self):
        while True:
            try:
                self.mycursor = self.mydb.cursor()
                self.mycursor.execute("CREATE DATABASE AGENDA")
                self.mycursor = self.mydb.cursor()
                self.mycursor.execute("SHOW DATABASES")
                for ind in self.mycursor:
                    print(ind)
            except mariadb.ProgrammingError:
                print("La base AGENDA ya existe")
            break
    def conectarBase(self):
        self.mydb = mariadb.connect(
	        host="127.0.0.1",
	        user="root",
	        database = "AGENDA"
	        )
    def crearTabla(self):
        while True:
            try:
                self.mycursor = self.mydb.cursor()
                self.mycursor.execute("CREATE TABLE cliente (dni INT PRIMARY KEY, nombre VARCHAR(255), direccion VARCHAR(255), telefono INT)")
            except mariadb.OperationalError:
                print("La tabla cliente ya existe")
            break
    def insertoRegis(self):
        self.mycursor = self.mydb.cursor()
        sql = "INSERT INTO cliente (dni, nombre, direccion, telefono) VALUES (%s, %d, %s, %d)"
        val = [
            (42123123,'Pedro Gomez','Santa Rosa 4',45673456),
            (11111111,'Amalia Perez','Dillon 652', 47567676),
            (22222222,'Analia Gonzalez','Aguado 21',45657676),
            (33333333,'Miguel Lopez','Muñiz 345',48569898)
            ]
        self.mycursor.executemany(sql, val)
        self.mydb.commit()
        print(self.mycursor.rowcount, "Fueron insertados.")
    def consultaTel(self):
        dni = int(input("Ingrese DNI de la persona: "))
        self.mycursor = self.mydb.cursor()
        sql = "SELECT telefono FROM cliente WHERE dni = "+str(dni)
        self.mycursor.execute(sql)
        myresultado = self.mycursor.fetchall()
        if len(myresultado) == 0:
             print("Registro no encontrado")
        else:
             print("El teléfono del cliente ", dni, " es: " ,myresultado[0][0])
    def nuevoCliente(self):
        while True:
            try:
                dni = int(input("Ingrese DNI de la persona: "))
                nombre = input("Ingrese su Nombre y Apellido: ")
                dire = input("Ingrese su dirección: ")
                tel = int(input("Ingrese su teléfono: "))
                self.mycursor = self.mydb.cursor()
                sql = "INSERT INTO cliente (dni, nombre, direccion, telefono) VALUES (%s, %d, %s, %d)"
                val = (dni,nombre,dire,tel)
                self.mycursor.execute(sql, val)
                self.mydb.commit()
                print(self.mycursor.rowcount, "Fueron insertados.")
            except mariadb.IntegrityError:
                print("DNI existente")
            break
    def modif_Tel_Dire(self):
		pass
		"""
        dni = int(input("Ingrese DNI de la persona: "))
        tel = int(input("Ingrese teléfono a cambiar: "))
        sql = "UPDATE cliente SET telefono = "+str(tel)+" WHERE dni = "+str(dni)
        print("sql ",sql)
        self.mycursor.execute(sql)
        self.mydb.commit()
        print(self.mycursor.rowcount, " registros modificados")
#       veo el registro despues del cambio------------------------------
        #sql = "SELECT * FROM cliente where dni = "+str(dni)
        #self.mycursor.execute(sql)
        #myresultado = self.mycursor.fetchall()
        #for ind in myresultado:
        #    print(ind)
        """
    def del_Telefono(self):
        pass # eliminar el teléfono de un cliente
    def listado_Clientes(self):
        pass # mostrar listado de todos los clientes en la tabla
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SELECT * FROM cliente")
        myresultado = self.mycursor.fetchall()
        if len(myresultado) == 0:
            print("No se han encontrado registros")
        else:
            print("|-------------------------------------------------------|")
            print("|  DNI   ", "Nombre y Apellido", "Dirección", "Teléfono|")
            print("|-------------------------------------------------------|")
            for ind in myresultado:
                print("|", ind[0],"|", ind[1],"|", ind[2],"|", ind[3],"|")
            print("|-------------------------------------------------------|")
# ---------------------------------- parte principal -----------------------------------
agendaTel = BaseTel()
agendaTel.conectarAdmin()
menu = """
|--------------------------------------------|
| Ingrese la opción deseada:                 |
| 0 - Crear nueva Base de Datos              |
| 1 - Crear tabla Cliente                    |
| 2 - Consulta telefono cliente              |
| 3 - Alta nuevo cliente                     |
| 4 - Modificar telefono de cliente          |
| 5 - Eliminar cliente                       |
| 6 - Listado clientes                       |
| 7 - Salir                                  |
|--------------------------------------------|
"""
while True:
    print(menu)
    opcion = int(input("Opcion: "))
    if opcion == 0:
        agendaTel.crearBase()
    elif opcion == 1:
        agendaTel.conectarBase()
        agendaTel.crearTabla()
        #agendaTel.insertoRegis()
        agendaTel.mydb.close()
    elif opcion == 2:
	    agendaTel.conectarBase()
	    agendaTel.consultaTel()
	    agendaTel.mydb.close()
    elif opcion == 3:
	    agendaTel.conectarBase()
	    agendaTel.nuevoCliente()
	    agendaTel.mydb.close()
    elif opcion == 4:
	    agendaTel.conectarBase()
	    agendaTel.modif_Tel_Dire()
	    agendaTel.mydb.close()
    elif opcion == 5:
	    agendaTel.conectarBase()
	    agendaTel.del_Telefono()
	    agendaTel.mydb.close()
    elif opcion == 6:
	    agendaTel.conectarBase()
	    agendaTel.listado_Clientes()
	    agendaTel.mydb.close()
    else:
	    break
