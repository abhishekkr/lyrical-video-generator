from PIL import Image, ImageDraw, ImageFont

freesans = '/usr/share/fonts/gnu-free/FreeSans.ttf'

unicode_text = u"Hello World!"
font = ImageFont.truetype(freesans, 28, encoding="unic")
text_width, text_height = font.getsize(unicode_text)
canvas = Image.new('RGB', (text_width + 100, text_height + 100), "orange")
draw = ImageDraw.Draw(canvas)
draw.text((5, 5), u'Hello World!', 'blue', font)
canvas.save("unicode-text-1.png", "PNG")
draw.text((25, 25), u'Hola World!', 'green', font)
canvas.save("unicode-text-2.png", "PNG")
draw.text((45, 45), u'Ahoy World!', 'red', font)
canvas.save("unicode-text-3.png", "PNG")
#canvas.show()
