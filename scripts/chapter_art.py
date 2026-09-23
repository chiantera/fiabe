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

def foundation():
    b=earth(80)+path('M479 0H620V323H479Z','#92947b')
    b+=path('M479 80H620M479 153H620M479 226H620M535 0V80M572 80V153M524 153V226M571 226V323','none','#737866',4)
    b+=tunnel('M0 470Q250 480 382 316H447',86)+mole(399,341,1.25)
    b+=path('M689 0V560','none','#696e62',42)+path('M689 0V560','none','#304e43',20)
    b+=path('M708 510Q770 456 800 476','none','#73938a',24)
    b+=path('M654 363Q670 347 676 334M646 390Q665 378 676 362','none','#8d9e87',3)
    return b

def lost_room():
    b=earth()+tunnel('M0 265H350Q397 265 432 360H700',87)+room(620,387,130,101)
    b+=path('M494 369Q548 361 600 373 651 387 749 368C768 510 492 532 494 369Z','#73938a')
    b+=path('M531 411Q590 401 641 413M642 446H695','none','#b1bfa1',3)
    b+=path('M402 401 414 352 407 302 434 283 459 306 478 296 493 328 481 365 491 399Z','#b99b73')
    b+=mole(326,289,1.2)+shrew(215,296,.9)
    return b

def dry_corner():
    b=earth(130)+path('M480 0Q433 168 494 261 544 315 721 317','none','#6f5940',37)
    b+=tunnel('M0 444H346Q432 444 477 346',80)+room(556,351,114,65)
    b+=path('M507 387 539 377 526 393 563 382 548 397 587 387 574 400 612 389','none','#af965f',4)
    b+=mole(471,389,1.25)
    b+=path('M652 170Q684 243 728 250','none','#927651',5)
    return b

SCENES['tilde:06'] = ('Tilde scopre le fondamenta e il pozzo della casa', foundation)
SCENES['tilde:07'] = ('Pino resta vicino a Tilde mentre chiudono le stanze allagate', lost_room)
SCENES['tilde:08'] = ('Tilde prepara in segreto un angolino asciutto per Rocco', dry_corner)

def digging():
    b=earth()+tunnel('M0 443Q273 443 509 300',96)
    b+=mole(456,350,1.3)+shrew(310,414,1)
    b+=path('M509 254 524 273 511 290 535 304 514 322','none','#9e7d54',4)
    for x,y,r in [(547,287,8),(562,316,5),(530,354,7),(401,422,6)]: b+=circle(x,y,r,'#97764d')
    b+=path('M73 402 93 399M133 397 152 393M193 386 211 382M253 369 272 361','none','#d4b781',3)
    return b

def old_city():
    b=earth(70)
    b+=tunnel('M0 335H800',76)+tunnel('M387 173V500',72)
    b+=tunnel('M126 335V211H665V335M178 335V473H614V335',49)
    for x,y,rx,ry in [(128,213,57,37),(665,213,53,38),(614,473,66,36),(181,473,61,37)]: b+=room(x,y,rx,ry)
    b+=ellipse(524,335,28,22,'#a49c81')+tunnel('M476 334Q515 276 570 331',30)
    b+=mole(362,353,1)+shrew(270,356,.75)
    return b

def cicada(x,y,s=1):
    b=path('M-3 8Q-92-73-94-16-93 42-4 36Z','#b5c3a0')+path('M3 8Q92-73 94-16 93 42 4 36Z','#cbd3ad')
    b+=path('M-8 25-77-20M-8 25-62 19M8 25 77-20M8 25 62 19','none','#8b9c77',2)
    b+=ellipse(0,21,13,33,'#9b9e6e')+ellipse(0,-10,20,15,'#bac18a')
    b+=circle(-16,-12,4,'#596c4a')+circle(16,-12,4,'#596c4a')
    return group(b,x,y,s)

def emergence():
    b=meadow()+path('M507 560Q541 411 516 188','none','#657d55',10)
    b+=path('M522 317Q601 245 611 286 612 317 524 328Z','#6e8861')
    b+=mole(337,493,1.8)+nymph(518,405,.62)+cicada(514,246,1.3)
    for x,y in [(173,357),(647,376),(231,255)]: b+=glow(x,y,22)+circle(x,y,3,'#edd88e')
    return b+grass()

SCENES['tilde:09'] = ('Una talpa al giorno: Tilde e Pino ricostruiscono in salita', digging)
SCENES['tilde:10'] = ('Le strade larghe e le stanze della città antica', old_city)
SCENES['tilde:11'] = ('Sette asciuga le ali nuove, Tilde resta al suo fianco', emergence)

def front_door():
    b=meadow()+tree(445,-185,1.6)
    b+=ellipse(447,462,63,35,'#172d25')+path('M390 459Q405 397 449 410 493 405 509 460','none','#7f7957',12)
    b+=mole(368,464,1.4)+shrew(227,481,1.15)
    return b+grass()

def tilde_epilogue():
    b=earth(226)+path('M0 0H800V176Q529 138 342 192 163 222 0 172Z','#a9b497')
    b+=circle(592,83,39,'#e8d6a0')+tree(164,-72,.65)
    for x,y,s in [(300,226,1),(442,209,.7),(642,209,.9)]:
        b+=group(path('M-37 0Q-20-32 0-23 23-33 42 0Z','#806d4e'),x,y,s)
    b+=tunnel('M296 239V352H644V234',47)+tunnel('M449 351V459H268',45)+room(267,446,77,50)
    b+=mole(270,465,.85)
    b+=path('M204 471 233 461 225 475 254 463 248 478 282 468 278 480 310 470','none','#b29a65',3)
    return b

SCENES['tilde:12'] = ('La porta scelta da Tilde, vicino al ricordo di Rocco', front_door)
SCENES['tilde:13'] = ('I mucchietti nel prato rivelano una città nascosta', tilde_epilogue)

# --- Ugo --------------------------------------------------------------------
# Il pipistrello è più chiaro del cielo, e caldo: sul verde scuro deve leggersi.
BAT_WING, BAT_BODY = '#5b4f45', '#75675a'

def bat(x,y,s=1,flip=False):
    b=path('M0-4C-14-20-36-25-62-15-53-8-49 1-53 10-42 3-31 5-25 14-18 7-9 7 0 7Z',BAT_WING)
    b+=path('M0-4C14-20 36-25 62-15 53-8 49 1 53 10 42 3 31 5 25 14 18 7 9 7 0 7Z',BAT_WING)
    b+=ellipse(0,3,9,13,BAT_BODY)+circle(0,-11,8,BAT_BODY)
    b+=path('M-7-15-9-27-1-18Z',BAT_BODY)+path('M7-15 9-27 1-18Z',BAT_BODY)
    b+=circle(-3,-12,1.6,'#edd88e')+circle(3,-12,1.6,'#edd88e')
    return group(b,x,y,s,flip)

def bat_hanging(x,y,s=1):
    b=path('M-4-24-5-36M4-24 5-36','none',BAT_BODY,3)
    b+=ellipse(0,0,15,25,BAT_WING)+path('M0-22V20','none','#4a4038',2)
    b+=circle(0,22,8,BAT_BODY)+path('M-7 26-9 38-1 29Z',BAT_BODY)+path('M7 26 9 38 1 29Z',BAT_BODY)
    return group(b,x,y,s)

def echo(x,y,s=1,flip=False,n=3):
    # La voce di Ugo: archi che vanno avanti e tornano indietro.
    b=''.join(path(f'M{72+i*16} {-14-i*9}Q{84+i*20} 0 {72+i*16} {14+i*9}','none','#d9d2a5',2) for i in range(n))
    return f'<g opacity=".45">{group(b,x,y,s,flip)}</g>'

def big_house(lit=True, gap=True):
    # La casa in cima alla collina, vista da vicino: il tetto è il protagonista.
    b=path('M150 300H650V560H150Z','#25483c')
    b+=path('M92 318 400 118 708 318Z','#1a392f')
    for y in [170,205,240,275,305]:
        half=(y-118)*308/200
        b+=path(f'M{400-half+6:.0f} {y}H{400+half-6:.0f}','none','#2c5044',3)
    b+=path('M86 318H714V332H86Z','#142c25')
    if gap: b+=path('M608 332Q624 348 640 332Z','#0b1a16')
    if lit: b+=glow(340,420,70)
    b+=path('M300 380H380V460H300Z','#efdaa0' if lit else '#142c25')+path('M340 380V460M300 420H380','none','#25483c',5)
    b+=path('M470 400H540V560H470Z','#1d3c32')
    return b

def attic_cover():
    ground=path('M0 470C180 430 320 455 460 440 600 426 700 450 800 440V560H0Z','#214739')
    return sky()+ground+big_house()+bat(700,380,.9)+echo(700,380,.9)

def ugo_01():
    b=meadow()+tree(170,90,.7)+house(610,262,1,False)
    return b+bat(410,175,1.2)+echo(410,175,1)+grass()

SCENES['ugo:01'] = ('Ugo sente per la prima volta una cosa dritta: la casa nuova', ugo_01)

def mosquito(x,y,s=1):
    b=path('M-6-3-1 0M6-3 1 0','none','#9aa38c',1.5)+ellipse(0,0,3,1.6,'#2a3a31')
    return group(b,x,y,s)

def ugo_02():
    b=sky()+path('M0 470C180 430 320 455 460 440 600 426 700 450 800 440V560H0Z','#214739')+big_house()
    for x,y in [(262,372),(288,352),(398,366),(412,398),(245,440),(420,452),(395,340)]: b+=mosquito(x,y,1.8)
    return b+bat(195,345,.95)+echo(195,345,.8)

SCENES['ugo:02'] = ('La finestra accesa del Respiro, le zanzare, e Ugo che fa la guardia', ugo_02)

def cutaway(lamp=True):
    # Sezione della casa: la soffitta sopra, la stanza del Respiro sotto.
    b=path('M0 0H800V560H0Z','url(#sky)')
    b+=path('M40 262 400 44 760 262Z','#1a392f')+path('M110 250 400 78 690 250Z','#0f231c')
    b+=path('M262 150H538','none','#3a5a4b',14)
    b+=path('M40 250H760V270H40Z','#4a3e30')
    b+=path('M40 270H760V560H40Z','#2c3f35')
    if lamp: b+=glow(600,400,110)+path('M584 470H616L608 420H592Z','#6d5f48')+path('M570 420H630L615 385H585Z','#efdaa0')
    b+=path('M150 450H470V510H150Z','#6f7d62')+ellipse(200,445,40,16,'#c9c1a0')+path('M150 510V545M470 510V545','none','#4a3e30',8)
    return b

def sleeper_standing(x,y,s=1):
    # Chi dorme sotto il tetto: una figura piccola e neutra, in pigiama, un braccio alzato.
    b=path('M-14 0V-52M14 0V-52','none','#6b7a63',16)
    b+=path('M-26-50Q-30-110 0-116 30-110 26-50Z','#8f9a78')
    b+=path('M14-104Q30-140 22-170','none','#c9aa80',11)+circle(22,-172,9,'#c9aa80')
    b+=path('M-16-104Q-34-86-36-66','none','#c9aa80',11)
    b+=circle(0,-136,21,'#c9aa80')+path('M-21-138Q-20-162 0-160 20-162 21-138Q12-150 0-148-12-150-21-138Z','#4b4938')
    return group(b,x,y,s)

def ugo_03():
    b=cutaway()+bat_hanging(400,192,1.25)
    b+=sleeper_standing(300,450)
    for i,y in enumerate([290,306,322]): b+=f'<g opacity=".5">{path(f"M{338+i*6} {y}Q{352+i*6} {y-6} {366+i*6} {y}","none","#edd88e",2)}</g>'
    for i,y in enumerate([226,236,246]): b+=f'<g opacity=".5">{path(f"M{430+i*6} {y}Q{444+i*6} {y-6} {458+i*6} {y}","none","#edd88e",2)}</g>'
    return b

SCENES['ugo:03'] = ('Tre colpi dal letto, tre colpi dalla trave', ugo_03)

def ugo_04():
    b=cutaway()
    b+=path('M40 262 400 44 760 262','none','#dfe5d6',12)
    for x,y in [(90,60),(170,140),(640,90),(720,170),(60,210),(700,40),(560,30),(250,40)]: b+=circle(x,y,4,'#dfe5d6')
    b+=bat_hanging(400,192,1.25)
    b+=path('M170 452Q230 404 300 420 360 405 430 452Z','#7f8c70')
    return b

SCENES['ugo:04'] = ('Neve sul tetto, Ugo nel sonno lungo, e sotto qualcuno che bussa lo stesso', ugo_04)

def owl(x,y,s=1):
    # La civetta in volo, ali larghe e morbide: niente spigoli, niente rumore.
    wing=path('M8-8C44-30 96-30 132-18L150-14 136-8 148-2 132 0 140 8 122 8Q80 22 8 16Z','#6f6858')
    wing+=path('M30 4Q70 10 110 4M40-6Q80-10 118-8','none','#857d6a',3)
    b=group(wing)+group(wing,flip=True)
    b+=ellipse(0,6,22,28,'#7d7563')+path('M-12 30 0 46 12 30Z','#6f6858')
    b+=circle(0,-14,20,'#8c8470')+ellipse(-8,-14,9,10,'#b9ad92')+ellipse(8,-14,9,10,'#b9ad92')
    b+=circle(-8,-14,3,'#1f2a24')+circle(8,-14,3,'#1f2a24')+path('M-2-6 0-1 2-6Z','#5a5244')
    return group(b,x,y,s)

def ugo_05():
    b=meadow(False)+tree(120,110,.55)
    b+=owl(500,345,1.05)
    b+=path('M392 492Q430 470 468 492','none','#2d5646',10)+shrew(430,488,.9)
    b+=path('M352 492 360 466M372 494 368 470M482 494 490 468M500 494 496 472','none','#66856a',3)
    return b+bat(250,170,1.05)+echo(250,170,.9)+grass()

SCENES['ugo:05'] = ('La civetta scivola senza rumore, Pino si appiattisce, Ugo grida dal cielo', ugo_05)
COVERS = {'attic': ('Il tetto della casa in cima alla collina, e Ugo che esce dal buco sotto le tegole', attic_cover)}

SKY_DEFS='<defs><linearGradient id="sky" x2="0" y2="560" gradientUnits="userSpaceOnUse"><stop stop-color="#153e38"/><stop offset="1" stop-color="#587761"/></linearGradient></defs>'

def render(key):
    if key.startswith('cover:'):
        # Le copertine dello scaffale stanno in assets/, non in assets/chapters/.
        title, draw = COVERS[key.split(':')[1]]
        output = ROOT / 'assets' / (key.split(':')[1]+'.svg')
        output.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560" fill="none">\n<title>'+escape(title)+'</title>\n'+SKY_DEFS+'\n'+draw()+'\n</svg>\n',encoding='utf-8')
        print(output.relative_to(ROOT))
        return
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
