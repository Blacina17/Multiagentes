import mesa
class Vehiculo(mesa.Agent):
	def __init__(self, model, codigo, origen, destino):
		super().__init__(model)
		self.codigo = codigo
		self.origen = origen
		self.destino = destino
		self.ruta = model.mapa.calcularRuta(origen, destino)
		self.indice = 0
		self.posicion = self.ruta[0]
		self.estado = "EN_ORIGEN"
		self.movimientos = 0
		self.espera = 0
		self.pasoSalida = None
		self.pasoLlegada = None

	def etiqueta(self):
		return f"P{self.origen} → P{self.destino}"

	def proponer(self):
		if self.estado == "FINALIZADO":
			return None
		return self.ruta[self.indice + 1]

	def avanzar(self, celda):
		if celda != self.proponer():
			raise ValueError("Sólo puede avanzar a la celda que propuso.")
		if self.indice == 0:
			self.pasoSalida = self.model.pasos
		self.posicion = celda
		self.indice += 1
		self.movimientos += 1
		if self.indice == len(self.ruta) - 1:
			self.estado = "FINALIZADO"
			self.pasoLlegada = self.model.pasos
		else:
			self.estado = "CIRCULANDO"

	def esperar(self, motivo):
		self.estado = motivo
		self.espera += 1