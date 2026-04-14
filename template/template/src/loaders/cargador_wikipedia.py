from pathlib import Path

from modelos.grafo import GrafoWikipedia


class CargadorWikipedia:
    """Carga desde el dataset los datos necesarios para construir el grafo."""

    def __init__(self, ruta_dataset=None):
        if ruta_dataset is None:
            self.ruta_dataset = Path(__file__).resolve().parent.parent.parent / "dataset"
        else:
            self.ruta_dataset = Path(ruta_dataset)

    def cargar_nombres_articulos(self):
        ruta = self.ruta_dataset / "wiki-topcats_pagenames.txt"
        nombres = {}

        with open(ruta, "r", encoding="utf-8") as archivo:
            for indice, linea in enumerate(archivo, start=1):
                nombres[indice] = linea.strip()

        return nombres

    def cargar_nombres_categorias(self):
        ruta = self.ruta_dataset / "wiki-topcats_Category_names.txt"
        categorias = {}

        with open(ruta, "r", encoding="utf-8") as archivo:
            for indice, linea in enumerate(archivo, start=1):
                categorias[indice] = linea.strip()

        return categorias

    def _leer_matriz_market(self, ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()

                if not linea or linea.startswith("%"):
                    continue

                partes = linea.split()

                if len(partes) == 3:
                    continue

                if len(partes) >= 2:
                    fila = int(partes[0])
                    columna = int(partes[1])
                    yield fila, columna
#cambiar limite despues porque si no se peta
    def cargar_grafo(self,limite = 5000, limite_lineas=50000):
        grafo = GrafoWikipedia()
        print("CArgando articulos")
        nombres = self.cargar_nombres_articulos()
        nodos_c= 0
        for id_articulo, nombre in nombres.items():
            if nodos_c >= limite:
                break
            grafo.agregar_articulo(id_articulo, nombre)
            nodos_c +=1
        print("Cargando enlaces")
        ruta_enlaces = self.ruta_dataset /"wiki-topcats.mtx"
        enlaces= 0
        lineas=0
        for id_origen, id_destino in self._leer_matriz_market(ruta_enlaces):
            lineas+=1
            if lineas > limite_lineas:
                break
            if grafo.obtener_articulo(id_origen) is not None and grafo.obtener_articulo(id_destino) is not None:
                grafo.agregar_enlace(id_origen,id_destino)
                enlaces+=1
            print(f'Subconjunto: {nodos_c} articulos, {enlaces} enlaces cargados')
        return grafo
