from collections import deque, defaultdict

from modelos.articulo import ArticuloWikipedia


class GrafoWikipedia:
    """Representa un grafo dirigido de articulos de Wikipedia y sus enlaces."""

    def __init__(self):
        self.articulos = {}
        self.categorias = {}
        self.articulos_por_categoria = defaultdict(set)

    def agregar_articulo(self, id_articulo, nombre):
        if id_articulo not in self.articulos:
            self.articulos[id_articulo] = ArticuloWikipedia(id_articulo,nombre)

    def obtener_articulo(self, id_articulo):
        return self.articulos.get(id_articulo)

    def agregar_enlace(self, id_origen, id_destino):
        if id_origen in self.articulos and id_destino in self.articulos:
            self.articulos[id_origen].agregar_enlace_salida(id_destino)
            self.articulos[id_destino].agregar_enlace_entrada(id_origen)

    def agregar_categoria_articulo(self, id_articulo, id_categoria, nombre_categoria):
        if id_articulo in self.articulos:
            self.categorias[id_categoria] = nombre_categoria
            self.articulos[id_articulo].agregar_categoria(nombre_categoria)
            self.articulos_por_categoria[id_categoria].add(id_articulo)

    def obtener_categorias_articulo(self, id_articulo):
        articulo = self.obtener_articulo(id_articulo)
        return articulo.categorias if articulo else set()

    def cantidad_articulos(self):
        return len(self.articulos)

    def cantidad_categorias(self):
        return len(self.categorias)

    def cantidad_enlaces(self):
        return sum(articulo.grado_salida() for articulo in self.articulos.values())

    def top_categorias_por_articulos(self, cantidad=10):
        lista = [
            (self.categorias[id_categoria], len(articulos))
            for id_categoria, articulos in self.articulos_por_categoria.items()
        ]
        lista.sort(key=lambda x: x[1], reverse=True)
        return lista[:cantidad]

    def pagerank_por_categoria(self, resultados_pr):
        """
        Calcula el PageRank promedio por categoria.
        Retorna una lista de tuplas (categoria, promedio_pr, cantidad_articulos).
        """
        pr_por_categoria = defaultdict(list)

        for id_articulo, pr in resultados_pr.items():
            categorias = self.obtener_categorias_articulo(id_articulo)
            for categoria in categorias:
                pr_por_categoria[categoria].append(pr)

        promedios = []
        for categoria, prs in pr_por_categoria.items():
            promedio = sum(prs) / len(prs) if prs else 0
            promedios.append((categoria, promedio, len(prs)))

        promedios.sort(key=lambda x: x[1], reverse=True)
        return promedios

    def top_articulos_por_pagerank_en_categoria(self, resultados_pr, nombre_categoria, cantidad=10):
        """
        Retorna los top articulos por PageRank dentro de una categoria especifica.
        """
        articulos_en_categoria = []
        for id_articulo in self.articulos:
            if nombre_categoria in self.obtener_categorias_articulo(id_articulo):
                pr = resultados_pr.get(id_articulo, 0)
                articulos_en_categoria.append((id_articulo, pr))

        articulos_en_categoria.sort(key=lambda x: x[1], reverse=True)
        return articulos_en_categoria[:cantidad]

#sort
    def top_por_grado_entrada(self, cantidad=10):
        lista = list(self.articulos.values())
        lista.sort(key=lambda a: a.grado_entrada(), reverse=True)
        return lista[:cantidad]

    def top_por_grado_salida(self, cantidad=10):
        lista = list(self.articulos.values())
        lista.sort(key=lambda a: a.grado_salida(), reverse = True)
        return lista[:cantidad]

    def resumen(self):
        return {
            "articulos": self.cantidad_articulos(),
            "enlaces": self.cantidad_enlaces(),
            "categorias": self.cantidad_categorias(),
        }

    def bfs(self, id_inicio):
        """
        TODO:
        Implementar recorrido BFS.

        Sugerencia:
        - usar una cola (`deque`);
        - marcar visitados;
        - retornar el orden de visita.
        """
        if id_inicio not in self.articulos:
            return []

        visitados = set([id_inicio])
        cola = deque([id_inicio])
        recorrido = []

        while cola:
            actual = cola.popleft()
            recorrido.append(actual)

            for vecino in self.articulos[actual].enlaces_salida:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)

        return recorrido

    def componentes_conectadas(self):
        """
        Encuentra todas las componentes conectadas del grafo usando BFS.
        Retorna una lista de listas, donde cada sublista es una componente.
        """
        visitados = set()
        componentes = []

        for id_articulo in self.articulos:
            if id_articulo not in visitados:
                componente = self.bfs(id_articulo)
                componentes.append(componente)
                visitados.update(componente)

        return componentes

    def dfs(self, id_inicio):
        """
        TODO:
        Completar o reescribir este método usando una pila o recursión.
        """
        if id_inicio not in self.articulos:
            return []

        visitados = set()
        pila = [id_inicio]
        recorrido = []

        while pila:
            actual = pila.pop()

            if actual in visitados:
                continue

            visitados.add(actual)
            recorrido.append(actual)

            vecinos = list(self.articulos[actual].enlaces_salida)
            vecinos.reverse()

            for vecino in vecinos:
                if vecino not in visitados:
                    pila.append(vecino)

        return recorrido

    def encontrar_camino_simple(self, id_origen, id_destino):
        """
        TODO:
        Mejorar esta búsqueda para encontrar caminos más interesantes.
        Por ahora retorna un camino simple usando BFS.
        """
        if id_origen not in self.articulos or id_destino not in self.articulos:
            return []

        cola = deque([id_origen])
        padres = {id_origen: None}

        while cola:
            actual = cola.popleft()

            if actual == id_destino:
                break

            for vecino in self.articulos[actual].enlaces_salida:
                if vecino not in padres:
                    padres[vecino] = actual
                    cola.append(vecino)

        if id_destino not in padres:
            return []

        camino = []
        actual = id_destino

        while actual is not None:
            camino.append(actual)
            actual = padres[actual]

        camino.reverse()
        return camino

    def pagerank(self, iteraciones=20, damping=0.85):
        """
        TODO:
        Este método puede servir como base para la versión final.
        Puede validarlo, modificarlo o reimplementarlo.
        """
        cantidad_nodos = self.cantidad_articulos()
        if cantidad_nodos == 0:
            return {}

        puntajes = {}
        valor_inicial = 1.0 / cantidad_nodos

        for id_articulo in self.articulos:
            puntajes[id_articulo] = valor_inicial

        for _ in range(iteraciones):
            nuevos_puntajes = {}

            for id_articulo in self.articulos:
                nuevos_puntajes[id_articulo] = (1.0 - damping) / cantidad_nodos

            for id_articulo, articulo in self.articulos.items():
                if articulo.grado_salida() == 0:
                    continue

                aporte = puntajes[id_articulo] / articulo.grado_salida()

                for vecino in articulo.enlaces_salida:
                    nuevos_puntajes[vecino] += aporte

            puntajes = nuevos_puntajes

        return puntajes