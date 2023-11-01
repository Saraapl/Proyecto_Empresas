from typing import Annotated
from fastapi import Body, FastAPI, Form
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from motor import motor_asyncio


CONNECTION_STRING = 'mongodb://localhost:27017'
client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING)
db = client['Empresas']

Empresas_nacionales = db["empresas nacionales"]
Empresas_extranjeras = db["empresas internacionales"]

#comando para iniciar el servidor: uvicorn main:app --reloads
#inciar app:
#crear entorno virtual de conda
#primer_entorno
app = FastAPI()
#crear ruta (con decorador):


class EmpresaLocal(BaseModel):
    nombre: str
    ubicacion: str
    correo: str
    numero : str

class EmpresaExtranjera(BaseModel):
    nombre: str
    ubicacion: str
    correo: str
    numero : str


def index():
    return "Hola usuario, bienvenido a la base de datos de empresas"

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def principal(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/agregarInternacional", response_class=HTMLResponse)
async def agregar_internacional(request: Request):
    return templates.TemplateResponse("agregarInternacional.html", {"request": request})


@app.get("/agregarNacional", response_class=HTMLResponse)
async def agregar_nacional(request: Request):
    return templates.TemplateResponse("agregarNacional.html", {"request": request})


#post para página que recibe datos y los procesa. Petición al formulario html
@app.post("/agregarNacionalCrear", response_class=HTMLResponse)
async def agregar_nacional_crear(request: Request, empresa_nombre:Annotated[str,Form()], empresa_correo:Annotated[str,Form()], empresa_ubicacion:Annotated[str,Form()], empresa_descripcion:Annotated[str,Form()]):
    print(empresa_nombre, empresa_correo, empresa_ubicacion, empresa_descripcion)
    await Empresas_nacionales.insert_one({"nombre": empresa_nombre, "correo": empresa_correo, "ubicacion": empresa_ubicacion, "descripcion": empresa_descripcion})
    return templates.TemplateResponse("agregarNacional.html", {"request": request})

@app.post("/agregarInternacionalCrear", response_class=HTMLResponse)
async def agregar_internacional_crear(request: Request, empresa_nombre:Annotated[str,Form()], empresa_correo:Annotated[str,Form()], empresa_ubicacion:Annotated[str,Form()], empresa_descripcion:Annotated[str,Form()]):
    print(empresa_nombre, empresa_correo, empresa_ubicacion, empresa_descripcion)
    await Empresas_extranjeras.insert_one({"nombre": empresa_nombre, "correo": empresa_correo, "ubicacion": empresa_ubicacion, "descripcion": empresa_descripcion})
    return templates.TemplateResponse("agregarInternacional.html", {"request": request})


@app.post("/consultarNacionalPedir", response_class=HTMLResponse)
async def consultar_nacional_pedir(request: Request, nombre: str = Form(...)):
    empresa = await Empresas_nacionales.find_one({"nombre": nombre})
    return templates.TemplateResponse("consultarNacional.html", {"request": request, "empresa": empresa})

@app.post("/consultarInternacionalPedir", response_class=HTMLResponse)
async def consultar_internacional_pedir(request: Request, nombre: str = Form(...)):
    empresa = await Empresas_extranjeras.find_one({"nombre": nombre})
    return templates.TemplateResponse("consultarInternacional.html", {"request": request, "empresa": empresa})

@app.get("/consultarNacional", response_class=HTMLResponse)
async def consultar_nacional(request: Request):
    return templates.TemplateResponse("consultarNacional.html", {"request": request})


@app.get("/consultarInternacional", response_class=HTMLResponse)
async def consultar_internacional(request: Request):
    return templates.TemplateResponse("consultarInternacional.html", {"request": request})


@app.get("/consultarTodas", response_class=HTMLResponse)
async def consultar_todas(request: Request):
    nacionales = await Empresas_nacionales.find().to_list(100000)
    internacionales = await Empresas_extranjeras.find().to_list(100000)
    return templates.TemplateResponse("consultarTodas.html", {"request": request, "nacionales" : nacionales, "internacionales" : internacionales})


#poner rutas post y get con el mismo response html.