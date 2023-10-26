from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import schema
import mook

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIS
@app.get("/api/")
def root():
    return {
        "Servicio": "Estructura de datos",
        "Lista para la busqueda": mook.my_documents
    }

# Buscador de palabra en los indices invertirdos
@app.post("/api/indices-invertidos", response_model=schema.ResultadoBusqueda)
def indices_invertidos(palabra: schema.PalabraBuscar):
    """
    Endpoint que recibe una palabra y devuelve el documento si existe en la caché.

    Args:
        palabra (schema.PalabraBuscar): Objeto que contiene la palabra a buscar.

    Returns:
        str: El/Los documentos de la palabra si se encuentra en la caché, de lo contrario "No se encontro".
    """

    return {"resultado": mook.cache.get(palabra.palabra, ["No se encontro"])}


# Devuelve un repetido de una lista
@app.post("/api/numero-repetido", response_model=schema.NumeroRepetido)
def numeros_repetidos(lista: schema.ListaNumeros):
    """
    Detecta el primer número repetido en una lista.

    El array contiene números en el rango de 1 a n, donde n es la longitud del array.

    Args:
        lista (dict): Un diccionario que contiene una lista de enteros bajo la clave 'lista'.

    Returns:
        dict: Un diccionario que contiene el primer número repetido bajo la clave 'repetido'.
    """
    return {"repetido": mook.detectar_primer_repetido(lista.lista)}


@app.post("/api/merge-sort", response_model=schema.ResultadoMergeSort)
def merge_sort(lista: schema.ListaMergeSort):
    """
    Ordena una lista de cadenas de texto utilizando el algoritmo de ordenamiento merge sort.

    Args:
        lista (dict): Un diccionario que contiene una lista de cadenas de texto bajo la clave 'lista'.

    Returns:
        dict: Un diccionario que contiene la lista de cadenas de texto ordenada bajo la clave 'organizado'.
    """
    return {"organizado": mook.merge_sort(lista.lista)}

# Templates


@app.get('/indices-invertidos')
def indices_invertidos(request: Request):
    return templates.TemplateResponse("indices-invertidos.html", {"request": request})
