from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from configparser import ConfigParser
import json
import sqlite3

# uvicorn main:app --reload
# api docs => http://127.0.0.1:8000/docs

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/dashboard/{id}")
async def dashboard(req: Request, id: str):
    return templates.TemplateResponse("template.html", {"request": req, "id": id})


@app.post("/config/{id}")
async def update_config(up_config: dict, id: str):
    config = ConfigParser()
    config.read("./stash/config.ini")
    # check config key exist
    # update config value
    # config.set('SETTINGS', 'value', '15')
    # with open('settings.ini', 'w') as configfile:
    #     config.write(configfile)
    return config._sections


@app.get("/status/{id}")
async def get_status(req: Request, id: str):
    data = {}
    # instance
    with open('./stash/instance.json') as file:
        data['instance'] = json.load(file)
    # config
    config = ConfigParser()
    config.read("./stash/config.ini")
    data['config'] = config._sections
    # #runtime logs
    # with open('./stash/main.log') as file:
    #     lines = file.readlines()
    #     data['logs'] = [line.rstrip() for line in lines]
    return data


@app.get("/trade-logs/{id}")
async def get_trade_logs(id: str, limit: int = 4):
    conn = sqlite3.connect("./stash/log.db")
    c = conn.cursor()
    c.execute(
        "SELECT * FROM trade_logs ORDER BY datetime DESC LIMIT {}".format(limit))
    data = c.fetchall()
    data.reverse()  # old...new
    conn.commit()
    conn.close()
    return data
