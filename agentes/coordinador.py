"""Coordinador del tráfico. Decide qué vehículos avanzan en cada paso.
Los vehículos sólo proponen su siguiente celda; aquí se aplican las reglas:
semáforo en verde, celda libre y un solo vehículo por celda.
"""
import mesa


class Coordinador(mesa.Agent):
	def __init__(self, model):
		super().__init__(model)
		self.codigo = "CONTROL"
		self.bloqueos = 0 

	def semaforoBloquea(self, actual, siguiente):
		mapa = self.model.mapa
		nombre = mapa.semaforoEn.get(siguiente)
		if nombre is None or mapa.semaforoEn.get(actual) == nombre:
			return False
		return self.model.semaforos[nombre].color != "VERDE"

	def activos(self):
		return [v for v in self.model.vehiculos if v.estado != "FINALIZADO"]

	def step(self):
		activos = sorted(self.activos(), key=lambda v: v.codigo)
		ocupadas = {v.posicion: v for v in activos}

		propuestas = {}
		for v in activos:
			siguiente = v.proponer()
			if self.semaforoBloquea(v.posicion, siguiente):
				v.esperar("ESPERANDO_ROJO")
			else:
				propuestas[v] = siguiente

		ganadores = {}
		for v, celda in propuestas.items():
			if celda not in ganadores or v.codigo < ganadores[celda].codigo:
				ganadores[celda] = v
		movimientos = {}
		for v, celda in propuestas.items():
			if ganadores[celda] is v:
				movimientos[v] = celda
			else:
				v.esperar("ESPERANDO_TURNO")

		cambio = True
		while cambio:
			cambio = False
			for v, celda in list(movimientos.items()):
				otro = ocupadas.get(celda)
				if otro is None or otro is v:
					continue
				if otro not in movimientos:
					v.esperar("ESPERANDO_OCUPACION")
					del movimientos[v]
					cambio = True

		for v, celda in movimientos.items():
			v.avanzar(celda)
		self.bloqueos += len(activos) - len(movimientos)