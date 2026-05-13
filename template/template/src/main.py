from loaders.cargador_wikipedia import CargadorWikipedia
from utilidades.reporte_basico import ReporteBasicoWikipedia


def imprimir_analisis_bfs_dfs(grafo):
    componentes = grafo.componentes_conectadas()

    print()
    print("Analisis de Componentes Conectadas (usando BFS)\n")
    print(f"Numero total de componentes conectadas: {len(componentes)}")

    if componentes:
        tamanos = [len(comp) for comp in componentes]
        tam_max = max(tamanos)
        tam_min = min(tamanos)
        tam_prom = sum(tamanos) / len(tamanos)

        print(f"Tamaño componente mas grande: {tam_max}")
        print(f"Tamaño componente mas pequena: {tam_min}")
        print(f"Tamaño promedio de componentes: {tam_prom:.2f}")

        print()
        print("Top 5 componentes por tamano:")
        componentes_ordenadas = sorted(componentes, key=len, reverse=True)
        for i, comp in enumerate(componentes_ordenadas[:5], start=1):
            print(f"{i}. Componente con {len(comp)} articulos")
            # Muestra algunos ejemplo
            for j, id_art in enumerate(comp[:3]):
                articulo = grafo.obtener_articulo(id_art)
                nombre = articulo.nombre if articulo else "<desconocido>"
                print(f"   - {id_art}: {nombre}")
            if len(comp) > 3:
                print(f"   ... y {len(comp) - 3} mas")
    else:
        print("No se encontraron componentes.")


def main():
    cargador = CargadorWikipedia()
    grafo = cargador.cargar_grafo(limite=5000,limite_lineas=5000)
    reporte = ReporteBasicoWikipedia()
    archivos_reporte = reporte.generar(grafo)
    reporte.imprimir_en_consola(grafo)

    # Elegimos un articulo inicial valido para los recorridos.
    id_inicio = 1
    if id_inicio not in grafo.articulos:
        id_inicio = next(iter(grafo.articulos), None)

    if id_inicio is not None:
        imprimir_analisis_bfs_dfs(grafo)
    else:
        print("No hay articulos disponibles para el analisis BFS/DFS.")

    print()
    print(f"Categorias cargadas: {grafo.cantidad_categorias()}")
    print("Top 10 categorias por articulos:")
    for i, (nombre, cantidad) in enumerate(grafo.top_categorias_por_articulos(10), start=1):
        print(f"{i}) {nombre} - {cantidad} articulos")

    print()
    print("Archivos generados:")
    print(archivos_reporte["texto"])

    print()
    print("Siguientes pasos sugeridos:")
    print("BFS y DFS completados.")
    print("Implementar PageRank y exportar resultados.")
    print("-------------PageRank----------")
    resultados_pr = grafo.pagerank(iteraciones=20, damping=0.85)
    rk_ordenado = sorted(resultados_pr.items(), key=lambda x: x[1], reverse=True)
    print("Top 10 articulos PageRank:")
    for i in range(min(10, len(rk_ordenado))):
        id_art, puntaje = rk_ordenado[i]
        articulo = grafo.obtener_articulo(id_art)
        nombre = articulo.nombre if articulo else f"Id: {id_art}"
        categorias = grafo.obtener_categorias_articulo(id_art)
        categorias_texto = ", ".join(sorted(categorias)) if categorias else "Sin categorias"
        print(f"{i+1}) {nombre} - Score: {puntaje:.8f}")
        print(f"    Categorias: {categorias_texto}")

    print()
    print("Analisis de PageRank por categorias:")
    pr_por_cat = grafo.pagerank_por_categoria(resultados_pr)
    print("Top 10 categorias por PageRank promedio:")
    for i, (categoria, promedio, cantidad) in enumerate(pr_por_cat[:10], start=1):
        print(f"{i}) {categoria} - Promedio PR: {promedio:.8f} ({cantidad} articulos)")

    # Analisis de PageRank (pr) categoria especifica (ej: la primera del top)
    if pr_por_cat:
        categoria_ejemplo = pr_por_cat[0][0]
        print(f"\nTop 5 articulos en categoria '{categoria_ejemplo}' por PageRank:")
        top_en_cat = grafo.top_articulos_por_pagerank_en_categoria(resultados_pr, categoria_ejemplo, 5)
        for i, (id_art, pr) in enumerate(top_en_cat, start=1):
            articulo = grafo.obtener_articulo(id_art)
            nombre = articulo.nombre if articulo else f"Id: {id_art}"
            print(f"{i}) {nombre} - Score: {pr:.8f}")

if __name__ == "__main__":
    main()