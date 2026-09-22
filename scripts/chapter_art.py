"""Original vector illustrations for Fiabe. Run with explicit book:NN keys.

Shared shapes and the palettes of meadow.svg / burrow.svg keep the two books
visually consistent. Scenes are composed individually, not randomly generated.
"""
from pathlib import Path
from html import escape
import sys

ROOT = Path(__file__).resolve().parents[1]
SCENES = {}

def path(d, fill, stroke=None, width=4):
    return f'<path d="{d}" fill="{fill}"' + (f' stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"' if stroke else '') + '/>'

def ellipse(x,y,rx,ry,fill):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}"/>'

def circle(x,y,r,fill):
    return ellipse(x,y,r,r,fill)

def group(body,x=0,y=0,s=1,flip=False):
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})">{body}</g>'

def glow(x,y,r=70,color='#edd88e'):
    return f'<g opacity=".09">{circle(x,y,r,color)}{circle(x,y,r*.6,color)}</g>'

def fly(x,y,s=1,on=True,bea=False):
    light = '#cbd99b' if bea else '#edd88e'
    b = (glow(0,10,45,light) if on else '')
    b += ellipse(-9,-5,13,7,'#8d9f87')+ellipse(9,-5,13,7,'#b4bea0')
    b += ellipse(0,9,10,16,light if on else '#788571')+circle(0,-9,9,'#344c3d')
    b += path('M-4-16-9-24M4-16 9-24','none','#344c3d',2)
    return group(b,x,y,s)

def cricket(x,y,s=1,old=False):
    b=ellipse(0,0,26,13,'#87906a' if old else '#657d53')
    b+=circle(23,-10,13,'#9a9e77' if old else '#839565')+circle(28,-13,2,'#253e31')
    b+=path('M-19 5-34-16-43 18M-3 7-18-13-27 20M14-2 26 18 42 18M28-21 43-42M20-22 21-46','none','#5b714b',4)
    return group(b,x,y,s)

def clover(x,y,s=1):
    b=path('M0 0Q4-45 0-104','none','#64816a',6)
    for xx,yy in [(-26,-109),(26,-109),(0,-134)]: b+=ellipse(xx,yy,35,25,'#4c7357')
    b+=path('M0-103-26-113M0-103 27-113M0-103 0-136','none','#78916b',2)
    return group(b,x,y,s)

def grass():
    return path('M61 560 70 459M66 510 40 480M68 492 93 457M724 560 716 460M720 510 746 479M718 494 695 471M118 560 112 520M682 560 692 521','none','#66856a',3)

def sky(moon=True):
    b=path('M0 0H800V560H0Z','url(#sky)')
    for x,y,r in [(83,91,2),(209,56,2),(359,134,2),(710,79,2),(461,48,1.5),(686,231,1.5),(292,199,1.5),(117,246,2)]: b+=circle(x,y,r,'#d9d2a5')
    if moon: b+=glow(595,117,92)+path('M605 65a52 52 0 1 0 16 92 56 56 0 0 1-16-92Z','#f5e5b5')
    return b

def meadow(moon=True):
    return sky(moon)+path('M0 341C124 238 231 262 364 320 519 388 641 209 800 226V560H0Z','#64816a')+path('M0 398C137 382 219 313 341 340 539 384 643 394 800 333V560H0Z','#365f4c')+path('M0 470C165 396 286 502 449 460 599 421 686 448 800 477V560H0Z','#214739')

def tree(x=180,y=0,s=1):
    b=path('M0 440Q21 285 0 180M8 309-45 266M9 272 50 224','none','#233f33',24)
    b+=path('M-110 249C-140 210-116 165-80 160-84 115-35 85 4 111 42 82 95 107 91 150 150 165 155 220 115 249 100 299 42 300 10 277-35 309-93 290-110 249Z','#234d3d')
    b+=path('M-92 222Q-104 180-65 175-60 128-20 131','none','#39604a',7)
    b+=path('M0 431Q-38 456-93 449M0 430Q35 461 90 462','none','#233f33',16)
    return group(b,x,y,s)

def stone(x=380,y=465,s=1):
    return group(path('M-117 0Q-100-58-57-51-30-83 22-63 83-66 112-7 35 21-117 0Z','#869080')+path('M-83-27Q-39-56 4-47','none','#a5ac93',4),x,y,s)

def creek():
    return path('M480 330C321 374 623 408 437 458 367 483 318 514 358 560H509C459 523 489 498 554 472 753 396 439 380 521 333Z','#73938a')+path('M453 380 490 381M487 436 540 432M425 501 468 495','none','#bec5a3',3)

def house(x=610,y=230,s=1,lit=True):
    b=path('M-52 0V-69L0-112 54-69V0Z','#25483c')+path('M-67-67 0-124 69-67Z','#1a392f')
    b+=path('M-17-63H17V-24H-17Z','#efdaa0' if lit else '#142c25')
    return group(b,x,y,s)

def window_scene():
    b=meadow()+tree(175,100,.7)
    for x,y in [(180,375),(270,430),(340,380),(470,440),(590,370),(645,445)]: b+=glow(x,y,22)+circle(x,y,3,'#edd88e')
    b+=path('M0 0H800V560H0ZM106 52V474H694V52Z','#716a51')
    b+=path('M400 52V474M106 259H694','none','#a49470',15)
    b+=path('M69 475H731V503H69Z','#c0aa7c')
    b+=fly(398,241,.8)
    return b

SCENES['nina:00'] = ('La finestra e il prato', window_scene)
SCENES['nina:01'] = ('Nina accompagna Rocco lungo il ruscello', lambda: meadow()+creek()+tree(675,80,.65)+clover(150,485,1.3)+fly(320,350,1.5)+cricket(395,438,1.2)+grass())
SCENES['nina:02'] = ('Due amici guardano le stelle, sul sasso', lambda: meadow()+creek()+stone(335,459,1.4)+fly(289,361,1.25,False)+cricket(382,371,1.25)+grass())

def render(key):
    title, draw = SCENES[key]
    book, number = key.split(':')
    output = ROOT / 'assets' / 'chapters' / book / (number+'.svg')
    output.parent.mkdir(parents=True,exist_ok=True)
    defs='<defs><linearGradient id="sky" x2="0" y2="560" gradientUnits="userSpaceOnUse"><stop stop-color="#153e38"/><stop offset="1" stop-color="#587761"/></linearGradient></defs>'
    output.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560" fill="none">\n<title>'+escape(title)+'</title>\n'+defs+'\n'+draw()+'\n</svg>\n',encoding='utf-8')
    print(output.relative_to(ROOT))

if __name__=='__main__':
    if len(sys.argv)<2: raise SystemExit('Specify chapter keys, e.g. nina:00 nina:01 nina:02')
    for key in sys.argv[1:]: render(key)
