import uvicorn
from base64 import b64encode
from faker import Faker
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from font_minify import font_minify

app = FastAPI()

fd = Faker(locale='en')

number_map = {'zero': '0',
            'one': '1',
            'two': '2',
            'three': '3',
            'four': '4',
            'five': '5',
            'six': '6',
            'seven': '7',
            'eight': '8',
            'nine': '9'}

@app.get("/")
def view(req:Request):
    

    export_glyph_names = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    ttf, font_map = font_minify("./base_font.ttf", export_glyph_names)
    font_map_new = {}
    for k, v in font_map.items():
        font_map_new[number_map.get(v, v)] = f"&#x{hex(k)[2:]};"

    # 生成数据
    fake_data = []
    for _ in range(10):
        row = f"{fd.name()} ### {fd.phone_number()} ### {fd.address()}"
        fake_data.append("<p>" + "".join(font_map_new.get(chr, chr) for chr in row) + "</p>")

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSS字体反爬</title>
        <style>
            @font-face {font-family: "webfont";
                src: url(data:font/truetype;charset=utf-8;base64,%(font)s)format('truetype');
            }
        </style>
    </head>
    <body>
        <div style="font-family: webfont">
            %(content)s
        </table>
        
    </body>
    </html>
    """ % ({'font': b64encode(ttf.read()).decode(), 'content': "".join(fake_data)})

    return HTMLResponse(content=html_content, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9242)