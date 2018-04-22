import sqlite3, os, hashlib

nf = "datos.db"

if os.path.isfile(nf):
	os.remove(nf)

db = sqlite3.connect(nf)
cu = db.cursor()

se = "CREATE TABLE Usuarios (idUsuario INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, password TEXT)"
cu.execute(se)

tmp=hashlib.sha224("abc123").hexdigest()
cu.execute("INSERT INTO Usuarios (nombre,password) VALUES (?,?)",["admin",tmp])

se = "CREATE TABLE Periocidad (idPeriocidad INTEGER PRIMARY KEY AUTOINCREMENT, descripcion TEXT)"
cu.execute(se)

se = "INSERT INTO Periocidad (descripcion) VALUES('NO')"
cu.execute(se)
se = "INSERT INTO Periocidad (descripcion) VALUES('DIARIA')"
cu.execute(se)
se = "INSERT INTO Periocidad (descripcion) VALUES('SEMANAL')"
cu.execute(se)
se = "INSERT INTO Periocidad (descripcion) VALUES('MENSUAL')"
cu.execute(se)
se = "INSERT INTO Periocidad (descripcion) VALUES('ANUAL')"
cu.execute(se)
se = "INSERT INTO Periocidad (descripcion) VALUES('QUINCENAL')"
cu.execute(se)
se = "INSERT INTO Periocidad (descripcion) VALUES('DIARIA')"
cu.execute(se)

se = (	"CREATE TABLE Evento "
	"(idEvento INTEGER PRIMARY KEY AUTOINCREMENT, idUsuario INTEGER, fechaHoraInicio DATETIME, fechaHoraFin DATETIME, "
	"idPeriocidad INTEGER, fechaFin DATE, descripcion TEXTO)")
cu.execute(se)

se = "CREATE TABLE Calendario (fechaHoraInicio DATETIME, fechaHoraFin DATETIME, idEvento INTEGER)"
cu.execute(se)

se=(	"CREATE VIEW VCalendario AS "
	"SELECT u.nombre, c.fechaHoraInicio, c.fechaHoraFin, e.descripcion "
	"FROM Calendario c "
	"INNER JOIN Evento e ON (c.idEvento=e.idEvento) "
	"INNER JOIN Usuarios u ON (u.idUsuario=e.idUsuario)")
cu.execute(se)

#dependiendo de la periocidad se inserta
db.commit()

cu.close()
db.close()

