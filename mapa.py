from collections import deque

CUADRICULA = [
	"<<<<<<<<<<<<<<<<<<<<<<<<",  # 1
	"<<<<<<<<<<<<<<<<<<<<<<<<",  # 2
	"vv####^^####vv^^######^^",   # 3
	"vv####^^####vv^^######^^",   # 4
	"vv####^^####vv^^######^^",   # 5
	"vv####^^<<<<vv^^######^^",   # 6
	"vv####^^<<<<vv^^<<<<<<^^",   # 7
	"vv####^^####vv^^<<<<<<^^",   # 8
	"vv####^^####vv^^######^^",   # 9
	"vv####^^####vv^^######^^",   # 10
	"vv####^^####vv^^######^^",   # 11
	"vv####^^####vv^^######^^",   # 12
	"vv<<<<<<<<<<v<<<<<<<<<^^",  # 13
	"vv<<<<<<<<<<vGG^<<<<<<^^",   # 14
	"vv>>>>>>>>>>vGG^>>>>>>^^",   # 15
	"vv>>>>>>>>>>>>>^>>>>>>^^",   # 16
	"vv####vv####vv^^##^^##^^",   # 17
	"vv####vv####vv^^##^^##^^",   # 18
	"vv<<<<vv>>>>vv^^##^^##^^",   # 19
	"vv<<<<vv>>>>vv^^##^^##^^",   # 20
	"vv####vv####vv^^##^^##^^",   # 21
	"vv####vv####vv^^##^^##^^",   # 22
	">>>>>>>>>>>>>>>>>>>>>>>>",  # 23
	">>>>>>>>>>>>>>>>>>>>>>>>",  # 24
]

DIRECCIONES = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}

ESTACIONAMIENTOS = {
	1: ((3, 10), (2, 10)),   2: ((4, 3), (4, 2)),     3: ((4, 18), (4, 19)),
	4: ((5, 12), (5, 13)),   5: ((5, 21), (5, 20)),   6: ((6, 7), (7, 7)),
	7: ((9, 9), (8, 9)),     8: ((10, 22), (10, 23)), 9: ((11, 5), (11, 6)),
	10: ((11, 12), (11, 13)), 11: ((11, 17), (11, 16)), 12: ((18, 3), (18, 2)),
	13: ((18, 18), (19, 18)), 14: ((18, 20), (19, 20)), 15: ((21, 6), (21, 7)),
	16: ((21, 9), (21, 8)),  17: ((21, 20), (20, 20)),
}

SEMAFOROS = {
	"S1": {"celdas": [(9, 1), (9, 2)], "color": "ROJO"},
	"S2": {"celdas": [(7, 3), (8, 3)], "color": "VERDE"},
	"S3": {"celdas": [(7, 8), (8, 8)], "color": "VERDE"},
	"S4": {"celdas": [(9, 6), (9, 7)], "color": "ROJO"},
	"S5": {"celdas": [(18, 15), (18, 16)], "color": "ROJO"},
	"S6": {"celdas": [(19, 17), (20, 17)], "color": "VERDE"},
	"S7": {"celdas": [(1, 18), (2, 18)], "color": "VERDE"},
	"S8": {"celdas": [(3, 19), (3, 20)], "color": "ROJO"},
	"S9": {"celdas": [(7, 22), (8, 22)], "color": "VERDE"},
	"S10": {"celdas": [(6, 23), (6, 24)], "color": "ROJO"},
}

PARES = [("S1", "S2"), ("S3", "S4"), ("S5", "S6"), ("S7", "S8"), ("S9", "S10")]


def opuesto(vector):
	return (-vector[0], -vector[1])


class MapaCiudad:
	def __init__(self):
		self.ancho = self.alto = 24
		if len(CUADRICULA) != 24 or any(len(f) != 24 for f in CUADRICULA):
			raise ValueError("La cuadrícula debe medir 24 por 24.")
		self.direccion = {}     
		self.edificios = set()
		self.isla = set()
		for fila, texto in enumerate(CUADRICULA, start=1):
			for columna, simbolo in enumerate(texto, start=1):
				if simbolo in DIRECCIONES:
					self.direccion[(columna, fila)] = DIRECCIONES[simbolo]
				elif simbolo == "G":
					self.isla.add((columna, fila))
				else:
					self.edificios.add((columna, fila))
		self.estacionamientos = {n: datos[0] for n, datos in ESTACIONAMIENTOS.items()}
		self.accesos = {n: datos[1] for n, datos in ESTACIONAMIENTOS.items()}
		self.semaforos = SEMAFOROS
		self.pares = PARES
		self.semaforoEn = {}
		for nombre, datos in SEMAFOROS.items():
			for celda in datos["celdas"]:
				if celda not in self.direccion:
					raise ValueError(f"{nombre}: la celda {celda} no es calle.")
				self.semaforoEn[celda] = nombre
		self.grafo = self.construirGrafo()

	def construirGrafo(self):
		grafo = {}
		for celda, sentido in self.direccion.items():
			grafo[celda] = []
			for movimiento in DIRECCIONES.values():
				if movimiento == opuesto(sentido):
					continue
				vecina = (celda[0] + movimiento[0], celda[1] + movimiento[1])
				if vecina not in self.direccion:
					continue
				sentidoVecina = self.direccion[vecina]
				if sentidoVecina == opuesto(movimiento) or sentidoVecina == opuesto(sentido):
					continue
				grafo[celda].append(vecina)
		for numero, celdaP in self.estacionamientos.items():
			acceso = self.accesos[numero]
			if acceso not in self.direccion:
				raise ValueError(f"El acceso del estacionamiento {numero} no es calle.")
			grafo[acceso].append(celdaP)
			grafo[celdaP] = [acceso]
		return grafo

	def calcularRuta(self, origen, destino):
		if origen not in self.estacionamientos or destino not in self.estacionamientos:
			raise ValueError("El estacionamiento debe estar entre 1 y 17.")
		if origen == destino:
			raise ValueError("El origen y el destino deben ser distintos.")
		inicio, meta = self.estacionamientos[origen], self.estacionamientos[destino]
		pendientes = deque([[inicio]])
		visitadas = {inicio}
		while pendientes:
			ruta = pendientes.popleft()
			if ruta[-1] == meta:
				return ruta
			for siguiente in self.grafo[ruta[-1]]:
				if siguiente not in visitadas:
					visitadas.add(siguiente)
					pendientes.append(ruta + [siguiente])
		raise ValueError(f"No existe ruta de P{origen} a P{destino}.")

	def aXY(self, celda):
		return celda[0], self.alto + 1 - celda[1]
