# Taller01_PrograCientifica
**AUTORES**
Marianela Díaz R.
Inti Bautista


**DESCRIPCIÓN DEL PROYECTO**
Este sistema modela un subconjunto de la red de artículos de Wikipedia utilizando programación orientada a objetos y grafos dirigidos. El código permite explorar la conectividad de la red (mediante BFS y DFS), analizar métricas estructurales (grados de entrada/salida) e implementar un algoritmo de PageRank simplificado para descubrir los artículos y categorías más relevantes.


**REQUISITOS ANTES DE EJECUTAR**
- Python 3 instalado.
- Descargar el dataset de Wikipedia desde Kaggle y colocar los siguientes 4 archivos dentro de la carpeta `dataset/`:
  - `wiki-topcats.mtx`
  - `wiki-topcats_pagenames.txt`
  - `wiki-topcats_Categories.mtx`
  - `wiki-topcats_Category_names.txt`

**iNSTRUCCIONES**
1. Abrir una terminal y navegar hasta la carpeta donde se encuentra el código fuente (main).
2. Ejecutar el archivo principal con el siguiente comando:
   ```bash
   python main.py
EL Sistema importa los resultados en un txt dentro de la carpeta results/
   
