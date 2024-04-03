import uvicorn
import random
from fastapi import FastAPI, Request, Response

app = FastAPI()


user = {
    "127.0.0.1": {"port": 0, "need_changed": False}
}


@app.get("/")
def view(req:Request):
    ip = req.client.host
    port = req.client.port

    content = "success"

    # 初始化
    if ip in user:
        # 检测爬虫
        if (user[ip]["need_changed"]==True and user[ip]["port"] == port) or \
           (user[ip]["need_changed"]==False and user[ip]["port"] != port):
                content = "failed"
    else:
        user[ip] = {"port": port, "need_changed": False}


    print(ip, port, user[ip]["port"], user[ip]["need_changed"])


    connection = "keep-alive" if random.randint(1, 10) > 5 else "close"
    if connection == "keep-alive":
        user[ip]["need_changed"] = False
    else:
        user[ip]["need_changed"] = True

    # 更新 port
    user[ip]["port"] = port

    return Response(
        content=content,
        headers={
            "connection": connection
        }
    )


# uvicorn.run(app, host='0.0.0.0', port=9242)