"""Visualizador de Mesa. Ejecutar desde esta carpeta: solara run app.py"""
import mimetypes
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("application/javascript", ".mjs")
import matplotlib.pyplot as plt
import solara
from mesa.visualization import SolaraViz
from mesa.visualization.utils import update_counter
from modelo import Ciudad
from visualizacion import dibujarEstado, tablaResultados


# Muestra el mapa y la tabla de resultados del mismo modelo que controla Mesa.
# Parámetro: modelo, Ciudad. Retorno: componente de Solara.
@solara.component
def VistaCiudad(modelo):
	update_counter.get()
	figura = dibujarEstado(modelo)
	solara.FigureMatplotlib(figura)
	plt.close(figura)
	solara.Markdown(tablaResultados(modelo))
	if modelo.motivoFin == "TODOS_LLEGARON":
		solara.Success(f"Todos los autos llegaron en {modelo.pasos} pasos.")
	elif modelo.motivoFin == "LIMITE_ALCANZADO":
		solara.Warning("Se agotó el límite. Hay autos pendientes.")


page = SolaraViz(
	Ciudad(), components=[VistaCiudad], name="Ciudad · TC2008B",
	model_params={
		"numeroVehiculos": {"type": "SliderInt", "label": "Vehículos", "value": 5, "min": 1, "max": 17},
		"duracionVerde": {"type": "SliderInt", "label": "Pasos de cada luz", "value": 4, "min": 1, "max": 15},
		"semilla": {"type": "SliderInt", "label": "Semilla (sorteo de viajes)", "value": 7, "min": 0, "max": 99},
		"limite": 800
	}, play_interval=300
)