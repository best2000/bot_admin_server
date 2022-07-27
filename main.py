from cProfile import label
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from configparser import ConfigParser
import matplotlib.pyplot as plt
import json
import sqlite3

# uvicorn main:app --host 0.0.0.0 --port 5055 --reload
# api docs => http://127.0.0.1:8000/docs

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

# templates = Jinja2Templates(directory="templates")

# @app.get("/dashboard/{id}")
# async def dashboard(req: Request, id: str):
#     return templates.TemplateResponse("template.html", {"request": req, "id": id})


# @app.post("/config/{id}")
# async def update_config(up_config: dict, id: str):
#     config = ConfigParser()
#     config.read("./stash/config.ini")
#     # check config key exist
#     # update config value
#     # config.set('SETTINGS', 'value', '15')
#     # with open('settings.ini', 'w') as configfile:
#     #     config.write(configfile)
#     return config._sections


@app.get("/status/{id}")
async def get_status(id: str):
    data = {}
    # instance
    with open("./public/{}/instance.json".format(id)) as file:
        data['instance'] = json.load(file)
    # config
    config = ConfigParser()
    config.read("./public/{}/config.ini".format(id))
    data['config'] = config._sections
    return data


@app.get("/trade-logs/{id}")
async def get_trade_logs(id: str, limit: int = 100):
    # get data from db
    conn = sqlite3.connect("./public/{}/log.db".format(id))
    c = conn.cursor()
    c.execute(
        "SELECT * FROM trade_logs ORDER BY datetime DESC LIMIT {}".format(limit))
    data = c.fetchall()
    data.reverse()  # old...new
    conn.commit()
    conn.close()
    # plot
    file_path = "./public/{}/trade_logs.svg".format(id)
    time = [i[0] for i in data]
    #price = [i[1] for i in data]
    price_chg_pct = [i[2] for i in data]
    #nav = [i[3] for i in data]
    nav_chg_pct = [i[4] for i in data]
    base_ratio = [i[5] for i in data]
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    ax1.plot(time, price_chg_pct, color="r", marker=".", label="price%")
    ax1.plot(time, nav_chg_pct, color="g", marker=".", label='nav%')
    #ax1.set_ylim(0, 500)
    ax1.legend()
    ax2.plot(time, base_ratio, marker=".", label='asset ratio%')
    ax2.set_ylim(0,100)
    ax2.legend()
    fig.savefig(file_path)
    return FileResponse(file_path)
