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


class Pantalla:	
	##################################
	#Mientras mostramos lo siguiente podemos hacer calculos
	##################################
	def cargando(self):
		a=1
		salto=1
		while a<50:
			self.limpiar()
			inc=randint(0,salto)
			salto=salto*2
			a=a+inc
			if a>50:
				a=50
			print("["+"".rjust(a,'*')+"".rjust(50-a,' ')+"] "+str(a*2)+"%")
			time.sleep(0.5)
	def limpiar(self):
		#Limpiar pantalla
		if os.name=='posix':
			os.system('clear')
		elif os.name =='nt':
			os.system('cls')

	
class BD:
	def __init__(self, nf):
		self.nf=nf
	#Retorna el lastrowid
	def insert(self, query, arrayParametros):
		print("Dentroooo")
		db = sqlite3.connect(self.nf)
		cu = db.cursor()
		cu.execute(query,arrayParametros)
		lastId=cu.lastrowid
		print("last "+str(lastId))
		db.commit()
		cu.close()
		db.close()
		return lastId
	def select(self, query, arrayParametros):
		db=sqlite3.connect(self.nf)
		cu=db.cursor()
		cu.execute(query, arrayParametros)
		filas=cu.fetchall()
		cu.close() #Eliminar si no funciona el select
		db.close() #Eliminar si no funciona el select
		return filas
		
		
		
class Evento(BD):
	#Se pasan los valores como string, internamente hacemos el tipado de datos
	def __init__(self,idUsuario, fechaHoraInicio, fechaHoraFin, idPeriocidad, fechaFin, descripcion):
		BD.__init__(self,"datos.db")
		self.idUsuario = int(idUsuario)
		self.fechaHoraInicio = datetime.datetime.strptime(fechaHoraInicio, "%Y-%m-%d %H:%M")
		self.fechaHoraFin = datetime.datetime.strptime(fechaHoraFin, "%Y-%m-%d %H:%M")
		self.idPeriocidad = int(idPeriocidad)
		self.fechaFin = datetime.datetime.strptime(fechaFin, "%Y-%m-%d")
		self.descripcion=descripcion
		#inserto en base de datos el Evento.
		#print("Insertando en la la tabla Eventos")
		self.idEvento=self.insert("INSERT INTO Eventos (idUsuario,fechaHoraInicio,fechaHoraFin,idPeriocidad,fechaFin,descripcion) VALUES(?,?,?,?,?,?)", [self.idUsuario,self.fechaHoraInicio,self.fechaHoraFin,self.idPeriocidad,self.fechaFin,self.descripcion])
		#print("Evento "+str(self.idEvento)+" insertado")
	#obtengo la configuracion de Periocidad (tipo,incremento) Ej: Semanal-> ('D',7)
	def obtenerPeriocidad(self):
		filas=self.select("SELECT tipo,incremento FROM Periocidades WHERE idPeriocidad=?",[self.idPeriocidad])
		for fila in filas:
			return (fila[0],fila[1])
		return (None,None)

class Calendario(BD):
	#usuario y pass sin codificar
	def __init__(self, usuario, password, crear):
		BD.__init__(self,"datos.db")
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
		self.insert("INSERT INTO Usuarios (nombre, password) VALUES(?,?)",[usuario,hashPass])
		
	#Login, busca el usuario y password y si existe retorna el id de usuario
	#Si el login es incorrecto retorna -1
	def login(self,usuario,password):
		hashPass=hashlib.sha224(password.encode('utf-8')).hexdigest()
		filas=self.select("SELECT idUsuario FROM Usuarios WHERE nombre=? AND password=?",[usuario,hashPass])
		for fila in filas:
			return int(fila[0])
		return -1
	#Pinta por salida de pantalla la vista VCalendario
	def pintar(self):
		#TODO
		filas=self.select("SELECT * FROM VCalendario WHERE idUsuario=?",[self.idUsuario])
		print(colores.OKBLUE+"### CALENDARIO ####"+colores.ENDC)
		for fila in filas:
			print(fila)
		print(colores.OKBLUE+"### ### ### ### ###"+colores.ENDC)
	#Pinta las diferentes Periocidades que existen en tabla
	def pintarPeriocidades(self):
		#TODO
		filas=self.select("SELECT idPeriocidad, descripcion FROM Periocidades ORDER BY idPeriocidad ASC",[])
		print("Periocidades:")
		for fila in filas:
			print("\t{0}. {1}".format(fila[0],fila[1]))
	#Elimina el evento de todo el calendario
	def eliminarEvento(self,idEvento):
		#TODO
		self.insert("DELETE FROM Eventos WHERE idEvento=?",[idEvento])
		self.insert("DELETE FROM Calendario WHERE idEvento=?",[idEvento])
	#Elimina del calendario el evento int, pero solo para una fecha tipada determinada
	def eliminarEventoFecha(self,idEvento,fecha):
		#TODO
		self.insert("DELETE FROM Calendario WHERE idEvento=? AND fechaHoraInicio>=? AND fechaHoraInicio<date(?,'+1 day')",[idEvento,fecha,fecha])
	#Dado un evento, agrega al calendario en loop dependiendo de la periocidad del evento
	def agregar(self,evento):
		(tipo,incremento) = evento.obtenerPeriocidad()
		fechaHoraI=evento.fechaHoraInicio
		fechaHoraF=evento.fechaHoraFin
		fechaF=evento.fechaFin
		while (fechaHoraI<=fechaF):
			self.insert("INSERT INTO Calendario (fechaHoraInicio, fechaHoraFin, idEvento) VALUES(?,?,?)",[fechaHoraI,fechaHoraF,evento.idEvento])
			if tipo=='D':
				fechaHoraI=fechaHoraI+timedelta(days=incremento)
				fechaHoraF=fechaHoraF+timedelta(days=incremento)
			elif tipo=='M':
				fechaHoraI=fechaHoraI+relativedelta(months=incremento)
				fechaHoraF=fechaHoraF+relativedelta(months=incremento)
c=None

##################################
#TODO Opcion login o crear usuario
##################################
logado=0
while logado==0:
	print(colores.HEADER+"".rjust(100,"#")+colores.ENDC)
	login=0
	try:
		login=int(input("[1] Login o [2] Crear Usuario: "))
	except:
		login=0
	if login==2: #Crear usuario
		usuario=input("Nuevo usuario: ")
		password=input("Password: ")
		password2=input("Repetir password: ")
		if password!=password2:
			print("Password Incorrecta.")
		else:
			c=Calendario(usuario, password,1)
			print("Usuario Creado.")
			time.sleep(2)
	elif login==1:
		usuario=input("Usuario: ")
		password=input("Password: ")
		try:
			c=Calendario(usuario, password,0)
			logado=1
			print("Login correcto. Hola "+usuario)
		except:
			Pantalla().limpiar()
			print("Usuario o password incorrecto.")
	else:
		Pantalla().limpiar()
		print("OpciÃ³n incorrecta.")
time.sleep(2)

Pantalla().cargando()

##################################
#Si logado entonces opciones
##################################

while logado!=0:
	c.pintar()
	print("1. Agregar")
	print("2. Eliminar evento")
	print("3. Eliminar evento de una fecha")
	opcion=0
	try:
		opcion=int(input("Seleccione opcion: "))
	except:
		opcion=0
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
