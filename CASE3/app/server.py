import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/load_data")
async def load_data(request: Request):
    raw = str(await request.body())
    print(request.client.host, raw)

    data = await request.json()
    if (
        r'"\\u8fd9\\u662f\\u52a0\\u5bc6token"' not in raw
        and data.get("token") == "这是加密token"
    ):
        return "success"
    else:
        return "spider out!"


@app.get("/")
def view():
    return HTMLResponse(
        content="""<!DOCTYPE html>
<html lang="en">

<head>
    <title>json反爬</title>
</head>

<body>
    <p id="text"></p>
    <script>
        fetch('/load_data', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "token": "这是加密token" })
        }).then(resp => resp.text()).then(resp => document.getElementById('text').innerText=resp)
    </script>
</body>

</html>"""
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9242)
