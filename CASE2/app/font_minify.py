import random
from io import BytesIO
from fontTools.ttLib import TTFont
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

def font_minify(base_font_path:str, export_glyph_names:list, codes:list=None) -> [bytes, dict]:
    """
    为字体文件重设编码
    
    @params base_font: 旧字体文件
    @params export_glyph_names: 要导出的字体 glyph_names
        获取方法: 
        ==============================================
        TTFont('xx.ttf').getGlyphNames()
    @params codes: 映射到的 unicode code, 默认随机映射到 #E000-F8FF 私用区
    
    return: [字体文件, 映射关系]
    """

    ttf_data = BytesIO()
    # https://github.com/fonttools/fonttools/blob/3.41.2/Lib/fontTools/fontBuilder.py#L28
    
    base_font = TTFont(base_font_path)
    
    nameStrings = {
        'familyName': 'webfont',
        'styleName': 'Regular',
        'psName': 'webfont-Regular',
        'copyright': 'Created by Python',
        'version': 'Version 1.0',
        'vendorURL': 'https://fuck-spider.com',
    }
    
    hhea = {
        'ascent': base_font['hhea'].ascent,
        'descent': base_font['hhea'].descent,
    }

    if codes is None:
        # 随机映射到 #E000-F8FF 私用区
        codes = random.sample(range(0xE000, 0xF8FF), len(export_glyph_names))
    
    glyphs, metrics, cmap = {}, {}, {}
    glyph_set = base_font.getGlyphSet()
    pen = TTGlyphPen(glyph_set)
    for i, rn in enumerate(export_glyph_names):
        glyph_set[rn].draw(pen)
        glyphs[rn] = pen.glyph()
        metrics[rn] = base_font['hmtx'][rn]
        cmap[codes[i]] = rn

    fb = FontBuilder(base_font['head'].unitsPerEm, isTTF=True)
    fb.setupGlyphOrder(export_glyph_names)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(**hhea)
    fb.setupNameTable(nameStrings)
    fb.setupOS2()
    fb.setupPost()
    fb.save(ttf_data)
    ttf_data.seek(0)
    return ttf_data, cmap


if __name__ == "__main__":
    export_glyph_names = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    ttf, cmap = font_minify("enfont.ttf", export_glyph_names)

    with open('webfont.ttf', 'wb') as f:
        f.write(ttf.read())