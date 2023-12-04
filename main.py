from fastapi import FastAPI
import httpx
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get("/")
async def root():
    with open("./index.html", "r") as f:
        html = f.read()
    return HTMLResponse(content=html, status_code=200)


@app.get("/get_data")
async def get_data(id: str):
    async with httpx.AsyncClient() as aclient:
        ruc = await get_ruc(aclient, id + '001')
        points = await get_points(aclient, id)
        ruc_v = 'Tiene RUC' if ruc['existe'] else 'No tiene RUC'
        return HTMLResponse(content=f"<h1>{id}</h1>"
                                    f"<div><h2>Nombre: {points['nombre']}</h2></div>"
                                    f"<div><h2>Puntos de licencia: {points['puntos']}</h2></div>"
                                    f"<div><h2>{ruc_v}</h2></div>", status_code=200)


async def get_ruc(aclient: httpx.AsyncClient, ruc: str):
    url = f"http://127.0.0.1:8000/ruc/{ruc}"
    response = await aclient.get(url)
    return response.json()


async def get_points(aclient: httpx.AsyncClient, id: str):
    url = f"http://127.0.0.1:8001/puntos/{id}"
    response = await aclient.get(url)
    return response.json()


