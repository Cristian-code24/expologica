# Compuertas lógicas y Álgebra de Boole

Presentación web en Python y Streamlit para exponer los fundamentos, las compuertas y los ejercicios 5.11a–5.13. Incluye explicaciones de apoyo para la exposición, fórmulas renderizadas en LaTeX, tablas de verdad con resaltado de la combinación seleccionada y circuitos Canvas que transportan paquetes animados con el valor actual de cada señal.

## Ejecutar localmente

Requiere Python 3.10 o posterior.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

En Windows también puedes instalar las dependencias con `python -m pip install -r requirements.txt` y ejecutar `python -m streamlit run app.py`.

La app busca documentos opcionales en `libros/` y en `libros-materiales-de-referencia/`. No es necesario que esas carpetas existan para iniciar la presentación. Los PDF y PPTX aparecen en la diapositiva «Material de consulta» y se extraen solo cuando se solicita la vista previa.

## Imágenes opcionales de portada

La app busca imágenes dentro de `assets/`, `images/` y `fotos/` (también en subcarpetas). No necesitas renombrar las imágenes que ya están en `fotos/`; se reconocen nombres relacionados con universidad/campus, logo/escuela y Boole/guía. Si quieres usar nombres previsibles, coloca:

```text
assets/fondo-universidad.jpg
assets/logo-escuela-estadistica-informatica.png
assets/guia-boole.jpg
```

Si falta alguno, la portada usa su gradiente, un monograma o una ilustración de respaldo. Ninguna imagen es obligatoria para iniciar la app.

Los archivos de referencia pesados o sujetos a las condiciones del curso se mantienen locales y están excluidos de Git; el repositorio conserva el código, las pruebas, las imágenes de `fotos/` y la guía de `libros/`.

## Estructura

```text
app.py                  Navegación, contenido y controles de Streamlit
boolean_logic.py        Operaciones, evaluación de redes y tablas de verdad
exercises.py            Expresiones, pasos resueltos y definición de circuitos
circuit_canvas.py       Renderizador Canvas, señales y partículas animadas
course_references.py    Detección y lectura opcional de PDF, PPTX y texto
visual_assets.py       Búsqueda flexible de imágenes locales opcionales
libros/                 Material local opcional del curso
requirements.txt        Dependencias mínimas
```

## Ajustar o añadir un circuito

1. Define la lista `variables`, la expresión para mostrar, la lista ordenada de `gates` y el nombre de la señal de `output` en `exercises.py`.
2. Cada compuerta indica `kind` (`NOT`, `AND`, `OR`, `NAND`, `NOR`, `XOR` o `XNOR`), `inputs`, `output` y coordenadas `x`, `y` en un lienzo de 960 × 500.
3. Las entradas de una compuerta pueden tomar señales de entrada o salidas de compuertas anteriores. El renderizador calcula las rutas entre ellas automáticamente.
4. Añade la nueva sección al arreglo `SLIDES` y conéctala a la vista adecuada en `app.py`. `render_circuit()` calcula la salida para la tabla/control manual y el Canvas anima las mismas señales.

Las entradas manuales se eligen con 0/1. La fila resaltada de cada tabla corresponde a esa combinación. La reproducción automática recorre las combinaciones binarias dentro del Canvas; desactívala para fijar una combinación manual.

La presentación hace referencia al ejercicio 5.14, pero no incluye una resolución inventada: consulta el enunciado en el material oficial del curso y añade el archivo a `libros/` para revisarlo.

## Extender el diseño

El CSS principal vive en `app.py`; los colores, el dibujo de compuertas, las rutas y las partículas están en `circuit_canvas.py`. Para una siguiente iteración se pueden incorporar diagramas SVG específicos, atajos de teclado, transiciones entre diapositivas o una paleta de colores del curso sin tocar las funciones booleanas.
