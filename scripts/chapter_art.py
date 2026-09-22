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

def root_scene():
    return meadow(False)+tree(410,-195,1.65)+path('M196 505Q394 375 615 506Z','#50694e')

def girl(x,y,s=1):
    b=path('M-32-35Q-47-91 0-100 47-95 34-35Z','#4b4938')
    b+=ellipse(0,-61,27,31,'#c9aa80')+path('M-29-68Q-26-105 17-91L32-66Q4-70-7-86-15-68-29-68Z','#4b4938')
    b+=path('M-25-30Q-43 3-36 42H40Q45 0 23-30Z','#8f9a78')
    b+=path('M-28 2Q-65 36-96 29','none','#c9aa80',12)
    b+=path('M-30 41Q-53 68-78 63M31 40Q57 70 81 64','none','#64755a',19)
    return group(b,x,y,s)

def nina_window():
    b=sky(False)+path('M170 0H800V560H170Z','#536450')
    b+=path('M280 70H694V473H280Z','#a99b73')+path('M299 90H675V450H299Z','#d4bd88')
    b+=girl(540,343,1.25)+path('M302 381Q440 327 675 390V451H302Z','#7f9478')
    b+=path('M481 87V453M300 254H678','none','#8d815f',13)
    b+=path('M256 456H717V484H256Z','#b6a27a')+fly(411,281,1.4)
    return b+clover(106,590,1.2)

SCENES['nina:03'] = ('Nina e Bea si tengono compagnia sotto il trifoglio', lambda: meadow(False)+clover(411,510,2.4)+fly(333,445,1.1,False)+fly(423,455,.75,False,True)+grass())
SCENES['nina:04'] = ('Rocco ascolta la canzone delle nuove lucciole', lambda: root_scene()+cricket(395,433,1.5,True)+fly(215,369,.8)+fly(547,351,.8,True,True)+fly(493,270,.65)+fly(299,291,.65)+fly(609,416,.6,True,True)+grass())
SCENES['nina:05'] = ('Nina incontra la bambina dietro la finestra', nina_window)

def nina_hand():
    b=meadow()+house(670,250,.7,False)+girl(478,357,1.6)
    b+=fly(326,353,.65)+fly(200,428,.5,True,True)
    for x,y in [(119,400),(641,431),(601,351),(246,294),(541,495)]: b+=glow(x,y,20)+circle(x,y,3,'#edd88e')
    return b+grass()

def rocco_flight():
    b=meadow()+creek()+tree(164,286,.42)+house(680,273,.4)
    # Forty small carriers form a soft cloud under the old cricket.
    for row in range(4):
        for col in range(10):
            b+=fly(266+col*28,256+row*15+(col%3)*3,.3,True,(row+col)%4==0)
    b+=cricket(403,250,1.9,True)
    return b+grass()

SCENES['nina:06'] = ('Una mano aperta, una lucciola, il prato acceso', nina_hand)
SCENES['nina:07'] = ('Quaranta lucciole portano Rocco sopra il prato', rocco_flight)
SCENES['nina:08'] = ('Nina veglia dalla radice mentre Bea torna a brillare', lambda: root_scene()+fly(325,427,1.35,False)+fly(538,339,1.2,True,True)+clover(650,539,.85)+grass())

def nina_story():
    b=root_scene()+fly(390,416,1.25,False)
    for x,y,s in [(202,476,.7),(274,505,.65),(361,516,.55),(456,505,.7),(538,469,.6),(572,410,.65)]: b+=fly(x,y,s)
    return b+fly(620,480,.9,True,True)+grass()

def nina_departure():
    b=sky()+path('M0 350Q260 259 800 390V560H0Z','#a9a17e')
    b+=path('M0 363Q171 315 335 390L439 560H0Z','#365f4c')
    b+=path('M296 560Q352 478 289 422 268 391 321 374 372 343 369 302','none','#234d3d',54)
    b+=fly(302,348,.85,True,True)+fly(484,279,.6)
    b+=glow(606,248,22)+circle(606,248,2,'#edd88e')
    return b+grass()

def nina_epilogue():
    b=window_scene()
    # A smaller observer and an adult share the window, looking outward.
    b+=path('M196 560V410Q196 381 233 381 270 381 270 416V560Z','#294538')+circle(233,359,28,'#294538')
    b+=path('M301 560V447Q301 420 331 420 361 420 361 447V560Z','#365641')+circle(331,401,22,'#365641')
    b+=path('M260 439Q289 459 308 444','none','#294538',16)
    return b

SCENES['nina:09'] = ('Le giovani lucciole ascoltano Nina raccontare', nina_story)
SCENES['nina:10'] = ('Nina passa la siepe, Bea resta a cantare', nina_departure)
SCENES['nina:11'] = ('Insieme alla finestra, senza accendere la luce', nina_epilogue)

def earth(surface=100):
    b=path('M0 0H800V560H0Z','#b99b73')
    b+=path(f'M0 0H800V{surface}C597 {surface-41} 279 {surface+63} 0 {surface-16}Z','#607258')
    b+=path(f'M0 {surface-10}C279 {surface+69} 597 {surface-25} 800 {surface}V{surface+22}C570 {surface-9} 252 {surface+84} 0 {surface+18}Z','#899571')
    b+=path(f'M146 {surface+27}l16 53-22 36m18-48 41 25m378-51-21 57 13 33m-10-49-26 18M311 {surface+38}l9 30','none','#927651',5)
    for x,y in [(96,321),(628,255),(557,491),(105,481),(694,462),(298,204),(730,202),(74,224)]: b+=ellipse(x,y,7,3,'#9d7e56')
    return b

def tunnel(d,w=70):
    return path(d,'none','#6b553f',w)

def room(x,y,rx=130,ry=100):
    return ellipse(x,y,rx+17,ry+15,'#69533f')+ellipse(x,y,rx,ry,'#d4b781')

def mole(x,y,s=1,flip=False):
    b=path('M-27 14C-46 8-48-15-40-36-34-57-13-65 2-53 21-42 27-22 28-7L47 1 29 14Z','#756451')
    b+=path('M29-7 47 1 29 8Z','#c9947b')+circle(21,-18,2.5,'#332f29')
    b+=path('M-30 14H-44M9 14H27','none','#4f463a',6)
    b+=f'<g stroke="#d3bf8d" stroke-width="2.5">{circle(8,-20,9,"none")}{circle(27,-20,8,"none")}{path("M16-22H19M-1-22-15-28","none")}</g>'
    return group(b,x,y,s,flip)

def shrew(x,y,s=1,flip=False):
    b=ellipse(0,0,23,12,'#a6a292')+path('M14-9 44 1 17 8Z','#a6a292')+circle(25,-3,2,'#403e34')
    b+=circle(10,-11,6,'#9a8e7d')+path('M-22 2Q-44-14-56 2','none','#a6a292',3)+path('M-10 10-16 16M14 8 21 15','none','#756451',3)
    return group(b,x,y,s,flip)

def hedgehog(x,y,s=1):
    b=path('M-39 13-42-3-34-9-38-20-23-22-20-34-8-30 1-40 11-30 24-33 28-20 38-16 36 12Z','#67513f')
    b+=path('M20 0Q27-15 38-8L57 11H12Z','#c7ab80')+circle(40,2,2,'#332f29')
    b+=path('M-27 13H-37M25 13H36','none','#564633',5)
    return group(b,x,y,s)

def tilde_prologue():
    b=earth(180)+house(603,147,.9)+path('M677 143H722V178H677Z','#92947b')
    b+=path('M689 178V293Q661 350 701 430','none','#73938a',18)
    b+=tunnel('M0 390H318Q438 390 477 465')+room(284,383,117,82)+mole(287,417,1.25)
    b+=path('M681 312Q558 311 496 369','none','#73938a',13)
    return b

def rescue():
    b=earth()+path('M578 107 607 160 581 208 610 256 584 302 600 342','none','#69533f',26)
    b+=tunnel('M603 356Q506 421 391 374 279 328 213 135',82)
    b+=mole(400,396,1.25,True)+hedgehog(521,391,.8)
    for x in [535,583,643]: b+=fly(x,64,.55)
    return b

def roads():
    b=earth()+tunnel('M88 148V290Q88 324 147 324H665Q710 324 710 266V146')
    b+=tunnel('M333 324V441H545M510 326V215H657',60)+room(539,446,88,54)
    b+=mole(305,339,1.1)+shrew(198,344,.9)
    b+=path('M595 413 620 430 596 448M622 407 647 430 622 457','none','#bfa06b',3)
    return b

SCENES['tilde:00'] = ('La stessa casa vista da sotto: il pozzo e le strade', tilde_prologue)
SCENES['tilde:01'] = ('Tilde guida il piccolo riccio lungo la salita sicura', rescue)
SCENES['tilde:02'] = ('Tilde mostra a Pino le strade sotto il prato', roads)

def nymph(x,y,s=1):
    b=ellipse(0,2,18,26,'#a98755')+circle(0,-23,16,'#b99b68')
    b+=path('M-13-4-26-14-29-1M13-4 26-14 29-1M-14 9-28 16M14 9 28 16M-11 20-23 32M11 20 23 32M-13 6H13M-12 16H12','none','#785f3d',3)
    return group(b,x,y,s)

def seven_waits():
    b=earth()+tunnel('M0 365H467',94)+room(542,338,99,117)
    b+=path('M541 111Q505 177 552 255L548 323','none','#927651',8)+nymph(548,345,1.3)
    return b+mole(362,390,1.3)+shrew(247,397,1)

def neighbour():
    b=earth(222)+tree(393,-80,.67)+cricket(430,204,1.25)
    b+=tunnel('M0 410H367Q436 410 436 335',85)+room(424,370,92,61)+mole(431,396,1.15)
    b+=path('M385 246Q425 276 471 246M388 269Q425 297 468 269M397 292Q425 314 458 292','none','#937649',3)
    return b

def water_warning():
    b=earth()+tunnel('M0 378H481',105)
    b+=path('M555 155Q523 226 559 284 587 329 547 390 513 450 553 560','none','#73938a',23)
    b+=path('M488 284Q456 319 482 393','none','#8c9c84',11)
    b+=mole(421,409,1.55)+shrew(273,415,1.1)
    return b

SCENES['tilde:03'] = ('Sette cresce in silenzio nella cella accanto alla radice', seven_waits)
SCENES['tilde:04'] = ('Tre colpetti attraverso la terra: Tilde e Rocco', neighbour)
SCENES['tilde:05'] = ('La parete umida e la vena di acqua che cambia strada', water_warning)

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
