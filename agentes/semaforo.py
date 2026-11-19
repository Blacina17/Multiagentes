import mesa


class Semaforo(mesa.Agent):
	def __init__(self, model, nombre, celdas, colorInicial):
		super().__init__(model)
		self.nombre = nombre
		self.celdas = celdas
		self.colorInicial = colorInicial
		self.color = colorInicial

	def step(self):
		fase = ((self.model.pasos - 1) // self.model.duracionVerde) % 2
		if fase == 0:
			self.color = self.colorInicial
		else:
			self.color = "VERDE" if self.colorInicial == "ROJO" else "ROJO"


def crearSemaforos(model):
	semaforos = {}
	for nombre, datos in model.mapa.semaforos.items():
		semaforos[nombre] = Semaforo(model, nombre, datos["celdas"], datos["color"])
	return semaforos