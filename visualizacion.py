import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

COLOR_EDIFICIO = (0.36, 0.60, 0.85)
COLOR_CALLE = (0.87, 0.87, 0.87)
COLOR_ISLA = (0.55, 0.30, 0.10)
COLORES_LUZ = {"ROJO": "#d62828", "VERDE": "#1b9e4b"}


# Dibujamos el mapa, los semáforos y los vehículos del modelo en su estado actual
def dibujarEstado(modelo, eje=None):
	mapa = modelo.mapa
	if eje is None:
		_, eje = plt.subplots(figsize=(8, 8))
	eje.clear()
	fondo = [[COLOR_EDIFICIO] * mapa.ancho for _ in range(mapa.alto)]
	for (columna, fila) in mapa.direccion:
		fondo[fila - 1][columna - 1] = COLOR_CALLE
	for (columna, fila) in mapa.isla:
		fondo[fila - 1][columna - 1] = COLOR_ISLA
	eje.imshow(fondo, extent=(0.5, mapa.ancho + 0.5, mapa.alto + 0.5, 0.5), zorder=1)
	xs = [c for c, f in mapa.direccion]
	ys = [f for c, f in mapa.direccion]
	us = [mapa.direccion[celda][0] for celda in mapa.direccion]
	vs = [mapa.direccion[celda][1] for celda in mapa.direccion]
	eje.quiver(xs, ys, us, vs, color="#7d878d", pivot="mid",
		angles="xy", scale=28, width=0.004, zorder=2)
	for numero, (columna, fila) in mapa.estacionamientos.items():
		eje.scatter(columna, fila, s=170, marker="s", color="#f4e04d", zorder=3)
		eje.text(columna, fila, str(numero), ha="center", va="center", fontsize=7, zorder=4)
	for semaforo in modelo.semaforos.values():
		for columna, fila in semaforo.celdas:
			eje.scatter(columna, fila, s=170, marker="s", color=COLORES_LUZ[semaforo.color],
				edgecolors="white", linewidths=0.6, zorder=5)
	paleta = matplotlib.colormaps["tab20"]
	for v in modelo.vehiculos:
		if v.estado == "FINALIZADO":
			continue
		columna, fila = v.posicion
		eje.scatter(columna, fila, s=110, color=paleta((v.codigo - 1) % 20),
			edgecolors="black", linewidths=0.8, zorder=7)
		eje.annotate(f"{v.origen}→{v.destino}", (columna, fila), xytext=(0, 9),
			textcoords="offset points", ha="center", fontsize=7, zorder=8,
			bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
	llegaron = sum(1 for v in modelo.vehiculos if v.estado == "FINALIZADO")
	eje.set_title(f"Paso {modelo.pasos} · {llegaron} de {len(modelo.vehiculos)} autos llegaron", fontsize=11)
	eje.set(xlim=(0.5, mapa.ancho + 0.5), ylim=(mapa.alto + 0.5, 0.5), aspect="equal")
	eje.set_xticks(range(1, mapa.ancho + 1))
	eje.set_yticks(range(1, mapa.alto + 1))
	eje.tick_params(labelsize=6)
	eje.legend(handles=[
		Patch(color=COLOR_EDIFICIO, label="Edificio"),
		Patch(color=COLOR_ISLA, label="Glorieta"),
		Patch(color="#f4e04d", label="Estacionamiento"),
		Patch(color=COLORES_LUZ["VERDE"], label="Semáforo verde"),
		Patch(color=COLORES_LUZ["ROJO"], label="Semáforo rojo"),
		Line2D([], [], marker="o", color="w", markerfacecolor="#888", markeredgecolor="black", label="Auto (sale→llega)")],
		loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=6, fontsize=7, frameon=False)
	return eje.figure


# Construimos una tabla con el recorrido de cada auto.
def tablaResultados(modelo):
	filas = ["| Auto | Sale del | Llega al | Estado | Movimientos | Espera | Salió | Llegó |",
		"|---|---:|---:|---|---:|---:|---:|---:|"]
	for v in modelo.vehiculos:
		salio = "-" if v.pasoSalida is None else str(v.pasoSalida)
		llego = "-" if v.pasoLlegada is None else str(v.pasoLlegada)
		filas.append(f"| V{v.codigo} | P{v.origen} | P{v.destino} | {v.estado} | "
			f"{v.movimientos} | {v.espera} | {salio} | {llego} |")
	return "\n".join(filas)