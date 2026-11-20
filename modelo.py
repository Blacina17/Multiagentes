"""Modelo de la ciudad: crea el mapa, los semáforos, los vehículos y el coordinador."""
import mesa
from mapa import MapaCiudad
from agentes.semaforo import crearSemaforos
from agentes.vehiculo import Vehiculo
from agentes.coordinador import Coordinador


class Ciudad(mesa.Model):
	def __init__(self, *, numeroVehiculos=5, duracionVerde=4, limite=800, semilla=7, viajes=None):
		super().__init__(rng=semilla)
		for valor in (duracionVerde, limite):
			if type(valor) is not int or valor < 1:
				raise ValueError("La duración y el límite deben ser enteros positivos.")
		self.mapa = MapaCiudad()
		self.pasos = 0
		self.duracionVerde = duracionVerde
		self.limite = limite
		self.motivoFin = "EN_CURSO"
		if viajes is None:
			viajes = self.sortearViajes(numeroVehiculos, semilla)
		self.validarViajes(viajes)
		self.semaforos = crearSemaforos(self)
		self.vehiculos = [Vehiculo(self, i + 1, o, d) for i, (o, d) in enumerate(viajes)]
		self.control = Coordinador(self)

	def sortearViajes(self, cantidad, semilla):
		if type(cantidad) is not int or not 1 <= cantidad <= len(self.mapa.estacionamientos):
			raise ValueError("Usa entre 1 y 17 vehículos.")
		numeros = list(self.mapa.estacionamientos)
		origenes = self.random.sample(numeros, cantidad)
		return [(o, self.random.choice([p for p in numeros if p != o])) for o in origenes]

	def validarViajes(self, viajes):
		if not viajes:
			raise ValueError("Debe haber al menos un viaje.")
		origenes = [o for o, d in viajes]
		if len(origenes) != len(set(origenes)):
			raise ValueError("Dos autos no pueden salir del mismo estacionamiento.")
		for o, d in viajes:
			if o not in self.mapa.estacionamientos or d not in self.mapa.estacionamientos:
				raise ValueError("Los estacionamientos deben estar entre 1 y 17.")
			if o == d:
				raise ValueError("El origen y el destino deben ser distintos.")

	def haTerminado(self):
		return all(v.estado == "FINALIZADO" for v in self.vehiculos)

	def step(self):
		if self.motivoFin != "EN_CURSO":
			return
		self.pasos += 1
		for semaforo in self.semaforos.values():
			semaforo.step()
		self.control.step()
		if self.haTerminado():
			self.motivoFin = "TODOS_LLEGARON"
		elif self.pasos >= self.limite:
			self.motivoFin = "LIMITE_ALCANZADO"
		self.running = self.motivoFin == "EN_CURSO"
