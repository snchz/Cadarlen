import sqlite3, hashlib, time, os
from random import randint
from datetime import timedelta
from dateutil.relativedelta import relativedelta #pip install --user python-dateutil
import datetime

class colores:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

class BD:
	#
	def __init__(self, nf):
		dummy=1
		#TODO
		
class Evento:
	#Se pasan los valores como string, internamente hacemos el tipado de datos
	def __init__(self,idUsuario, fechaHoraInicio, fechaHoraFin, idPeriocidad, fechaFin, descripcion):
		self.idUsuario = int(idUsuario)
		self.fechaHoraInicio = datetime.datetime.strptime(fechaHoraInicio, "%Y-%m-%d %H:%M")
		self.fechaHoraFin = datetime.datetime.strptime(fechaHoraFin, "%Y-%m-%d %H:%M")
		self.idPeriocidad = int(idPeriocidad)
		self.fechaFin = datetime.datetime.strptime(fechaFin, "%Y-%m-%d")
		self.descripcion=descripcion
		self.insert()
	#inserto en base de datos el Evento.
	def insert(self):
		nf = "datos.db"
		db = sqlite3.connect(nf)
		cu = db.cursor()
		cu.execute("INSERT INTO Eventos (idUsuario,fechaHoraInicio,fechaHoraFin,idPeriocidad,fechaFin,descripcion) VALUES(?,?,?,?,?,?)", [self.idUsuario,self.fechaHoraInicio,self.fechaHoraFin,self.idPeriocidad,self.fechaFin,self.descripcion])
		self.idEvento=cu.lastrowid
		db.commit()
		cu.close()
		db.close()
	#obtengo la configuracion de Periocidad (tipo,incremento) Ej: Semanal-> ('D',7)
	def obtenerPeriocidad(self):
		nf="datos.db"
		db=sqlite3.connect(nf)
		cu=db.cursor()
		cu.execute("SELECT tipo,incremento FROM Periocidades WHERE idPeriocidad=?",[self.idPeriocidad])
		filas=cu.fetchall()
		for fila in filas:
			return (fila[0],fila[1])
		return (None,None)

class Calendario:
	#usuario y pass sin codificar
	def __init__(self, usuario, password, crear):
		if crear==1:
			self.insertarUsuario(usuario,password)
		elif crear==0:
			self.idUsuario=self.login(usuario,password)
			if self.idUsuario==-1:
				raise Exception("Usuario o password incorrecta.")
		else:
			raise Exception("No se ha logrado login.")
	def insertarUsuario(self,usuario,password):
		hashPass=hashlib.sha224(password.encode('utf-8')).hexdigest()
		nf="datos.db"
		db=sqlite3.connect(nf)
		cu=db.cursor()
		cu.execute("INSERT INTO Usuarios (nombre, password) VALUES(?,?)",[usuario,hashPass])
		db.commit()
		cu.close()
		db.close()
		
	#Login, busca el usuario y password y si existe retorna el id de usuario
	#Si el login es incorrecto retorna -1
	def login(self,usuario,password):
		hashPass=hashlib.sha224(password.encode('utf-8')).hexdigest()
		
		nf="datos.db"
		db=sqlite3.connect(nf)
		cu=db.cursor()
		cu.execute("SELECT idUsuario FROM Usuarios WHERE nombre=? AND password=?",[usuario,hashPass])
		filas=cu.fetchall()
		for fila in filas:
			return int(fila[0])
		return -1
	#Pinta por salida de pantalla la vista VCalendario
	def pintar(self):
		#TODO
		nf="datos.db"
		db=sqlite3.connect(nf)
		cu=db.cursor()
		cu.execute("SELECT * FROM VCalendario WHERE idUsuario=?",[self.idUsuario])
		filas=cu.fetchall()
		print(colores.OKBLUE+"### CALENDARIO ####"+colores.ENDC)
		for fila in filas:
			print(fila)
		print(colores.OKBLUE+"### ### ### ### ###"+colores.ENDC)
		cu.close()
		db.close()
	#Pinta las diferentes Periocidades que existen en tabla
	def pintarPeriocidades(self):
		#TODO
		nf="datos.db"
		db=sqlite3.connect(nf)
		cu=db.cursor()
		cu.execute("SELECT idPeriocidad, descripcion FROM Periocidades ORDER BY idPeriocidad ASC")
		filas=cu.fetchall()
		print("Periocidades:")
		for fila in filas:
			print("\t{0}. {1}".format(fila[0],fila[1]))
		cu.close()
		db.close()
	#Elimina el evento de todo el calendario
	def eliminarEvento(self,idEvento):
		#TODO
		nf="datos.db"
		db=sqlite3.connect(nf)
		cu=db.cursor()
		cu.execute("DELETE FROM Eventos WHERE idEvento=?",[idEvento])
		cu.execute("DELETE FROM Calendario WHERE idEvento=?",[idEvento])
		db.commit()
		cu.close()
		db.close()
	#Elimina del calendario el evento int, pero solo para una fecha tipada determinada
	def eliminarEventoFecha(self,idEvento,fecha):
		#TODO
		nf="datos.db"
		db=sqlite3.connect(nf)
		cu=db.cursor()
		cu.execute("DELETE FROM Calendario WHERE idEvento=? AND fechaHoraInicio>=? AND fechaHoraInicio<date(?,'+1 day')",[idEvento,fecha,fecha])
		db.commit()
		cu.close()
		db.close()
	#Dado un evento, agrega al calendario en loop dependiendo de la periocidad del evento
	def agregar(self,evento):
		(tipo,incremento) = evento.obtenerPeriocidad()
		print("tipo: "+str(tipo)+" incremento: "+str(incremento))
		nf="datos.db"
		db=sqlite3.connect(nf)
		cu=db.cursor()
		fechaHoraI=evento.fechaHoraInicio
		fechaHoraF=evento.fechaHoraFin
		fechaFin=evento.fechaFin
		while fechaHoraI<=fechaFin:
			cu.execute("INSERT INTO Calendario VALUES(?,?,?)",[fechaHoraI,fechaHoraF,evento.idEvento])
			db.commit()
			if tipo=='D':
				fechaHoraI=fechaHoraI+timedelta(days=incremento)
				fechaHoraF=fechaHoraF+timedelta(days=incremento)
			elif tipo=='M':
				fechaHoraI=fechaHoraI+relativedelta(months=incremento)
				fechaHoraF=fechaHoraF+relativedelta(months=incremento)
				
		cu.close()
		db.close()

c=None

##################################
#TODO Opcion login o crear usuario
##################################
logado=0
while logado==0:
	print("".rjust(100,"#"))
	login=int(input("[1] Login o [2] Crear Usuario: "))
	if login==2:
		usuario=input("Nuevo usuario: ")
		password=input("Password: ")
		password2=input("Repetir password: ")
		if password!=password2:
			print("Password Incorrecta.")
		else:
			c=Calendario(usuario, password,1)
			print("Usuario Creado.")
			time.sleep(2)
	else:
		usuario=input("Usuario: ")
		password=input("Password: ")
		try:
			c=Calendario(usuario, password,0)
			logado=1
			print("Login correcto. Hola "+usuario)
		except:
			print("Usuario o password incorrecto.")
time.sleep(2)



##################################
#Mientras mostramos lo siguiente podemos hacer calculos
##################################
a=1
salto=1
while a<50:
	#Limpiar pantalla
	if os.name=='posix':
		os.system('clear')
	elif os.name =='nt':
		os.system('cls')
	inc=randint(0,salto)
	salto=salto*2
	a=a+inc
	if a>50:
		a=50
	print("["+"".rjust(a,'*')+"".rjust(50-a,' ')+"] "+str(a*2)+"%")
	time.sleep(0.5)

##################################
#Si logado entonces opciones
##################################

while logado!=0:
	c.pintar()
	print("1. Agregar")
	print("2. Eliminar evento")
	print("3. Eliminar evento de una fecha")
	opcion=int(input("Seleccione opcion: "))
	if opcion==1:
		fhi=None
		try:
			fhi=input("Fecha hora inicio (YYYY-MM-DD HH:MM): ")
			datetime.datetime.strptime(fhi, "%Y-%m-%d %H:%M")
			fhf=input("Fecha hora fin (YYYY-MM-DD HH:MM): ")
			datetime.datetime.strptime(fhf, "%Y-%m-%d %H:%M")
			ff=input("Fecha fin (YYYY-MM-DD): ")
			datetime.datetime.strptime(ff, "%Y-%m-%d")
			c.pintarPeriocidades()
			p=input("Periocidad: ")
			d=input("Descripcion: ")
			e=Evento(c.idUsuario,fhi,fhf,p,ff,d)
			c.agregar(e)
		except:
			print("Formato incorrecto. Vuelva a intentarlo.")
	elif opcion==2:
		idEvento=int(input("Introduce idEvento: "))
		c.eliminarEvento(idEvento)
	elif opcion==3:
		idEvento=int(input("Introduce idEvento: "))
		fecha=input("Fecha (YYYY-MM-DD): ")
		fecha=datetime.datetime.strptime(fecha, "%Y-%m-%d")
		c.eliminarEventoFecha(idEvento,fecha)
	else:
		print("Opcion inexistente.")
