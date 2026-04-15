from loaders.cargador_wikipedia import CargadorWikipedia
from utilidades.reporte_basico import ReporteBasicoWikipedia


def main():
    cargador = CargadorWikipedia()
    grafo = cargador.cargar_grafo(limite=5000,limite_lineas=5000)
    reporte = ReporteBasicoWikipedia()
    archivos_reporte = reporte.generar(grafo)
    reporte.imprimir_en_consola(grafo)

    print()
    print("Archivos generados:")
    print(archivos_reporte["texto"])

    print()
    print("Siguientes pasos sugeridos:")
    print("Completar analisis de BFS y DFS.")
    print("Implementar PageRank y exportar resultados.")
    print("-------------PageRank----------")
    resultados_pr = grafo.pagerank(iteraciones= 20, damping=0.85)
    rk_ordenado = sorted(resultados_pr.items(), key= lambda x: x[1],reverse= True)
    print("Top 10 articulos PageRank:")
    for i in range(min(10, len(rk_ordenado))):
        id_art, puntaje = rk_ordenado[i]
        articulo = grafo.obtener_articulo(id_art)
        nombre= articulo.nombre if articulo else print("Id: "+id_art)
        print(f'{i+1}) {nombre} "-Score: " {puntaje}') 
if __name__ == "__main__":
    main()
