import sqlite3, os, hashlib

nf = "datos.db"

#Si existe el fichero db, lo borro
if os.path.isfile(nf):
	os.remove(nf)

db = sqlite3.connect(nf)
cu = db.cursor()

##########################
# TABLE Usuarios
##########################
cu.execute("CREATE TABLE Usuarios (idUsuario INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, password TEXT)")

tmp=hashlib.sha224("abc123".encode('utf-8')).hexdigest()
cu.execute("INSERT INTO Usuarios (nombre,password) VALUES (?,?)",["admin",tmp])


##########################
# TABLE Periocidades
##########################
cu.execute("CREATE TABLE Periocidades (idPeriocidad INTEGER PRIMARY KEY AUTOINCREMENT, descripcion TEXT, tipo TEXT, incremento INTEGER)")

cu.execute("INSERT INTO Periocidades (descripcion,tipo,incremento) VALUES('NO','D','0')")
cu.execute("INSERT INTO Periocidades (descripcion,tipo,incremento) VALUES('DIARIA','D',1)")
cu.execute("INSERT INTO Periocidades (descripcion,tipo,incremento) VALUES('SEMANAL','D',7)")
cu.execute("INSERT INTO Periocidades (descripcion,tipo,incremento) VALUES('MENSUAL','M',1)")
cu.execute("INSERT INTO Periocidades (descripcion,tipo,incremento) VALUES('ANUAL','M',12)")
cu.execute("INSERT INTO Periocidades (descripcion,tipo,incremento) VALUES('QUINCENAL','D',15)")
cu.execute("INSERT INTO Periocidades (descripcion,tipo,incremento) VALUES('TRIMESTRAL','M',3)")
cu.execute("INSERT INTO Periocidades (descripcion,tipo,incremento) VALUES('SEMESTRAL','M',6)")


##########################
# TABLE Eventos
##########################
se = (	"CREATE TABLE Eventos "
	"(idEvento INTEGER PRIMARY KEY AUTOINCREMENT, idUsuario INTEGER, fechaHoraInicio DATETIME, fechaHoraFin DATETIME, "
	"idPeriocidad INTEGER, fechaFin DATE, descripcion TEXTO)")
cu.execute(se)

##########################
# TABLE Eventos
##########################
cu.execute("CREATE TABLE Calendario (fechaHoraInicio DATETIME, fechaHoraFin DATETIME, idEvento INTEGER)")


##########################
# VIEW VCalendario
##########################
se=(	"CREATE VIEW VCalendario AS "
	"SELECT u.idUsuario, u.nombre, c.fechaHoraInicio, c.fechaHoraFin, e.idEvento, e.descripcion "
	"FROM Calendario c "
	"INNER JOIN Eventos e ON (c.idEvento=e.idEvento) "
	"INNER JOIN Usuarios u ON (u.idUsuario=e.idUsuario) "
	"WHERE c.fechaHoraInicio>=date('now') "
	"ORDER BY c.fechaHoraInicio DESC")
cu.execute(se)

#dependiendo de la periocidad se inserta
db.commit()

cu.close()
db.close()
