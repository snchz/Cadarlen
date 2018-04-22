import sqlite3, os

nf = "datos.db"

if os.path.isfile(nf):
	os.remove(nf)

db = sqlite3.connect(nf)
cu = db.cursor()

se = "CREATE TABLE Usuarios (id TEXT, nombre TEXT, password TEXT, PRIMARY KEY(id))"
cu.execute(se)
se = "CREATE TABLE Periocidad (id INTEGER PRIMARY KEY AUTOINCREMENT, descripcion TEXT)"
cu.execute(se)

se = "INSERT INTO Periocidad VALUES(1,'NO')"
cu.execute(se)
se = "INSERT INTO Periocidad VALUES(2,'DIARIA')"
cu.execute(se)
se = "INSERT INTO Periocidad VALUES(3,'SEMANAL')"
cu.execute(se)
se = "INSERT INTO Periocidad VALUES(5,'MENSUAL')"
cu.execute(se)
se = "INSERT INTO Periocidad VALUES(6,'ANUAL')"
cu.execute(se)
se = "INSERT INTO Periocidad VALUES(1,'QUINCENAL')"
cu.execute(se)
se = "INSERT INTO Periocidad VALUES(1,'DIARIA')"
cu.execute(se)

se = "CREATE TABLE Evento (idEvento INTEGER PRIMARY KEY AUTOINCREMENT, idUsuario INTEGER, fechaHoraInicio DATETIME, fechaHoraFin DATETIME, idPeriocidad INTEGER, fechaFin DATE, descripcion TEXTO)"
cu.execute(se)

se = "CREATE TABLE Calendario (fechaHoraInicio DATETIME, fechaHoraFin DATETIME, idEvento INTEGER)"
cu.execute(se)

se="CREATE VIEW VCalendario AS SELECT c.fechaHoraInicio, c.fechaHoraFin, e.descripcion FROM Calendario c INNER JOIN Evento e ON (c.idEvento=e.idEvento)"
cu.execute(se)

#dependiendo de la periocidad se inserta
db.commit()

cu.close()
db.close()

