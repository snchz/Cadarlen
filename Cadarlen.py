import sqlite3
from datetime import timedelta
import datetime

class Evento:
	def __init__(self,idUsuario, fechaHoraInicio, fechaHoraFin, idPeriocidad, fechaFin, descripcion):
		self.idUsuario = idUsuario
		self.fechaHoraInicio = datetime.datetime.strptime(fechaHoraInicio, "%Y-%m-%d %H:%M")
		self.fechaHoraFin = datetime.datetime.strptime(fechaHoraFin, "%Y-%m-%d %H:%M")
		self.idPeriocidad = idPeriocidad
		self.fechaFin = datetime.datetime.strptime(fechaFin, "%Y-%m-%d")
		self.descripcion=descripcion
		self.insert()
	def insert(self):
		nf = "datos.db"
		db = sqlite3.connect(nf)
		cu = db.cursor()
		cu.execute("INSERT INTO Evento (idUsuario,fechaHoraInicio,fechaHoraFin,idPeriocidad,fechaFin,descripcion) VALUES(?,?,?,?,?,?)", [self.idUsuario,self.fechaHoraInicio,self.fechaHoraFin,self.idPeriocidad,self.fechaFin,self.descripcion])
		self.idEvento=cu.lastrowid
		db.commit()
		cu.close()
		db.close()
class Calendario:
	def __init__(self):
		a=1
	def agregar(self,e):
		i=e.idEvento
		if e.idPeriocidad==1:
			#NA
			self.insertar(0,i)
		elif e.idPeriocidad==2:
			#Diario
			self.insertar(1,i)
		elif e.idPeriocidad==3:
			#Semanal
			self.insertar(7,i)
	def insertar(self,dias,idEvento):
		nf="datos.db"
		db=sqlite3.connect(nf)
		cu=db.cursor()
		fechaHoraI=e.fechaHoraInicio
		fechaHoraF=e.fechaHoraFin
		fechaFin=e.fechaFin
		while fechaHoraI<=fechaFin:
			cu.execute("INSERT INTO Calendario VALUES(?,?,?)",[fechaHoraI,fechaHoraF,e.idEvento])
			db.commit()
			fechaHoraI=fechaHoraI+timedelta(days=dias)
			fechaHoraF=fechaHoraF+timedelta(days=dias)
		cu.close()
		db.close()
c=Calendario()

while 1==1:
	fhi=raw_input("Fecha hora inicio (YYYY-MM-DD HH:MM): ")
	fhf=raw_input("Fecha hora fin (YYYY-MM-DD HH:MM): ")
	ff=raw_input("Fecha fin (YYYY-MM-DD): ")
	p=raw_input("Periocidad: ")
	d=raw_input("Descripcion: ")
	e=Evento(1,fhi,fhf,p,ff,d)
	c.agregar(e)
