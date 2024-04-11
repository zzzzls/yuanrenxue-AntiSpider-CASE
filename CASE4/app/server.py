import time
import uvicorn
from uuid import uuid1
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user = {}


@app.get("/")
async def view(request: Request):
    cookies = request.cookies

    device = "mobile" if "mobile" in request.headers.get("user-agent", "").lower() else "pc"

    if cookies == {}:
        response = RedirectResponse(url="/")
        sign = str(uuid1())
        user[request.client.host] = sign
        response.set_cookie("sign", "default")
        response.set_cookie("ts", int(time.time()))
        response.set_cookie("sign", sign)
    else:
        # 防重放
        if user.get(request.client.host) != cookies.get("sign"):
            content = "已过期"
        else:
            if "sign" in cookies and "ts" in cookies:
                cookie_keys = list(cookies)
                # 检测 cookie 顺序, sign 在 ts 之后
                if cookie_keys.index("sign") > cookie_keys.index("ts"):
                    content = "success"
                else:
                    content = "spider out!"
            else:
                content = "cookie错误"

        response = PlainTextResponse(content=content)
        print(request.client.host, device, content, cookies, sep=" -- ")

        # 清空cookie
        response.delete_cookie("sign")
        response.delete_cookie("ts")

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9242)
