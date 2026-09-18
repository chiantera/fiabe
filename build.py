#!/usr/bin/env python3
"""Genera la pagina web delle fiabe di Nina dai file .md della cartella.

Il markdown delle fiabe usa solo quattro costrutti: '# titolo', una riga di
sottotitolo in corsivo, il separatore '---' e paragrafi con *enfasi*.
Quattro regole bastano: nessuna libreria.
"""
import glob
import html
import math
import os
import re

SRC = os.path.dirname(os.path.abspath(__file__))
STORIE = os.path.join(SRC, "stories")
ROMANI = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
PAROLE_AL_MINUTO = 130  # ritmo di lettura ad alta voce, non di lettura silenziosa


def inline(testo):
    """Escape + *enfasi* -> <em> + virgolette dritte -> virgolette curve."""
    t = html.escape(testo, quote=False)
    t = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)
    parti = t.split('"')
    if len(parti) > 1:
        t = parti[0]
        for i, p in enumerate(parti[1:]):
            t += ("“" if i % 2 == 0 else "”") + p
    return t


def leggi(percorso):
    titolo = sottotitolo = ""
    paragrafi = []
    for riga in open(percorso, encoding="utf-8"):
        riga = riga.strip()
        if not riga or riga == "---":
            continue
        if riga.startswith("# "):
            titolo = riga[2:]
        elif not paragrafi and riga.startswith("*") and riga.endswith("*"):
            sottotitolo = riga[1:-1]
        else:
            paragrafi.append(riga)
    parole = sum(len(p.split()) for p in paragrafi)
    nome = os.path.basename(percorso)
    numero = nome[:2]
    chiave = os.path.splitext(nome)[0][2:]
    speciale = chiave in ("prologo", "epilogo")
    return {
        "numero": numero,
        "speciale": speciale,
        "chiave": chiave,
        "titolo": titolo,
        "sottotitolo": sottotitolo,
        "paragrafi": paragrafi,
        "minuti": max(1, math.ceil(parole / PAROLE_AL_MINUTO)),
        "parole": parole,
    }


def lucciole(n=3):
    return '<span class="lucciole" aria-hidden="true">' + "".join(
        f'<span class="lucciola" style="--ritardo:{i * 1.3:.1f}s"></span>' for i in range(n)
    ) + "</span>"


def audio_per(numero):
    """Restituisce il percorso (relativo al sito) dell'audio della fiaba, se c'è."""
    candidati = sorted(glob.glob(os.path.join(SRC, "audio", f"11l-{numero}-*.mp3")))
    if candidati:
        return os.path.relpath(candidati[0], SRC)
    return None


fiabe = [leggi(p) for p in sorted(glob.glob(os.path.join(STORIE, "[0-9][0-9]*.md")))]

indice = []
articoli = []
conta = 0
for i, f in enumerate(fiabe):
    if f["speciale"]:
        slug = f["chiave"]
        etichetta_numero = f["titolo"]
        # "dal Prologo" ma "dall'Epilogo": la preposizione la sa il Python,
        # non il JavaScript.
        ripresa = "dall&rsquo;Epilogo" if f["chiave"] == "epilogo" else "dal Prologo"
    else:
        slug = f"libro-{conta + 1}"
        etichetta_numero = ROMANI[conta]
        ripresa = f"dal Libro {ROMANI[conta]}"
        conta += 1
    f["slug"] = slug
    f["etichetta_numero"] = etichetta_numero
    indice.append(
        f'<li><a href="#{slug}"><span class="numero">{etichetta_numero}</span>'
        f'<span class="voce-titolo">{inline(f["titolo"])}</span>'
        f'<span class="voce-durata">{f["minuti"]} min</span></a></li>'
    )
    corpo = []
    for j, p in enumerate(f["paragrafi"]):
        classi = []
        if j == 0:
            classi.append("apertura")
        if p.startswith("Buonanotte."):
            classi.append("congedo")
        attr = f' class="{" ".join(classi)}"' if classi else ""
        corpo.append(f"      <p{attr}>{inline(p)}</p>")

    # lettore audio della fiaba, se l'MP3 è presente
    audio = audio_per(f["numero"])
    if audio:
        lettore = (
            f'        <figure class="lettura">\n'
            f'          <figcaption>Ascolta</figcaption>\n'
            f'          <audio controls preload="none" src="{audio}">\n'
            f'            Il tuo browser non supporta la riproduzione audio.\n'
            f'          </audio>\n'
            f'        </figure>\n'
        )
    else:
        lettore = ""

    articoli.append(
        f'    <article class="fiaba" id="{slug}" data-ripresa="{ripresa}">\n'
        f'      <header class="fiaba-testata">\n'
        f'        <p class="etichetta">{etichetta_numero} &middot; {f["minuti"]} minuti di lettura</p>\n'
        f'        <h2>{inline(f["titolo"])}</h2>\n'
        f'        <p class="sottotitolo">{inline(f["sottotitolo"])}</p>\n'
        f"      </header>\n" + lettore + "\n".join(corpo) + "\n"
        f'      <div class="divisorio">{lucciole()}</div>\n'
        f"    </article>"
    )

STILE = """
  :root {
    --ground: #edf0e6;
    --paper: #f8faf3;
    --ink: #1c241b;
    --muted: #5f6a56;
    --rule: #d5dbc8;
    --accent: #6b7a1c;
    --glow: #8c9e22;
    --alone: rgba(140, 158, 34, 0.22);
    --ombra: 0 1px 2px rgba(28, 36, 27, 0.05), 0 12px 32px -20px rgba(28, 36, 27, 0.35);
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --ground: #0c1310;
      --paper: #111a15;
      --ink: #e4e9dc;
      --muted: #8d9b86;
      --rule: #22302a;
      --accent: #c3d75f;
      --glow: #d8ec6b;
      --alone: rgba(216, 236, 107, 0.3);
      --ombra: 0 1px 2px rgba(0, 0, 0, 0.4), 0 18px 40px -24px rgba(0, 0, 0, 0.8);
    }
  }
  :root[data-theme="dark"] {
    --ground: #0c1310;
    --paper: #111a15;
    --ink: #e4e9dc;
    --muted: #8d9b86;
    --rule: #22302a;
    --accent: #c3d75f;
    --glow: #d8ec6b;
    --alone: rgba(216, 236, 107, 0.3);
    --ombra: 0 1px 2px rgba(0, 0, 0, 0.4), 0 18px 40px -24px rgba(0, 0, 0, 0.8);
  }

  * { box-sizing: border-box; }

  body {
    margin: 0;
    background: var(--ground);
    color: var(--ink);
    font-family: "Newsreader", Georgia, "Times New Roman", serif;
    font-size: 1.1875rem;
    line-height: 1.75;
    font-optical-sizing: auto;
    -webkit-font-smoothing: antialiased;
  }

  .pagina {
    display: flex;
    flex-direction: column;
    gap: 3.5rem;
    max-width: 42rem;
    margin: 0 auto;
    padding: 2.5rem 1.5rem 5rem;
  }

  .etichetta {
    margin: 0;
    font-family: "Karla", system-ui, sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
  }

  /* --- testata ------------------------------------------------------ */
  .testata { display: flex; flex-direction: column; gap: 1rem; }
  .testata-alto {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
  }
  .testata h1 {
    margin: 0;
    font-family: "Young Serif", Georgia, serif;
    font-weight: 400;
    font-size: clamp(2.5rem, 9vw, 3.75rem);
    line-height: 1.05;
    letter-spacing: -0.01em;
    text-wrap: balance;
  }
  .occhiello { display: flex; align-items: center; gap: 0.6rem; }
  .testata .intro {
    margin: 0;
    max-width: 32rem;
    color: var(--muted);
    font-size: 1.0625rem;
  }

  .interruttore {
    flex: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 0.85rem;
    border: 1px solid var(--rule);
    border-radius: 999px;
    background: var(--paper);
    color: var(--muted);
    font-family: "Karla", system-ui, sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    cursor: pointer;
    transition: color 0.2s ease, border-color 0.2s ease;
  }
  .interruttore:hover { color: var(--accent); border-color: var(--accent); }
  .interruttore::before {
    content: "";
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 50%;
    background: var(--glow);
    box-shadow: 0 0 0 4px var(--alone);
  }

  /* --- indice ------------------------------------------------------- */
  .indice { display: flex; flex-direction: column; gap: 0.75rem; }
  .indice ol { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; }
  .indice li + li { border-top: 1px solid var(--rule); }
  .indice a {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    padding: 0.7rem 0;
    color: inherit;
    text-decoration: none;
  }
  .indice a:hover .voce-titolo { color: var(--accent); }
  .numero {
    flex: none;
    width: 1.75rem;
    font-family: "Karla", system-ui, sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    color: var(--glow);
  }
  .voce-titolo { flex: 1; font-size: 1.0625rem; transition: color 0.2s ease; }
  .voce-durata {
    flex: none;
    font-family: "Karla", system-ui, sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    color: var(--muted);
    font-variant-numeric: tabular-nums;
  }

  /* --- fiabe -------------------------------------------------------- */
  .fiaba {
    background: var(--paper);
    border: 1px solid var(--rule);
    border-radius: 3px;
    box-shadow: var(--ombra);
    padding: clamp(1.75rem, 6vw, 3.25rem);
    scroll-margin-top: 1.5rem;
  }
  .fiaba-testata { display: flex; flex-direction: column; gap: 0.65rem; margin-bottom: 2.25rem; }
  .fiaba h2 {
    margin: 0;
    font-family: "Young Serif", Georgia, serif;
    font-weight: 400;
    font-size: clamp(1.75rem, 5.5vw, 2.25rem);
    line-height: 1.15;
    text-wrap: balance;
  }
  .sottotitolo { margin: 0; color: var(--muted); font-style: italic; font-size: 1rem; }
  .fiaba p { margin: 0 0 1.35em; }
  .fiaba p:last-of-type { margin-bottom: 0; }

  /* --- lettore audio ------------------------------------------------- */
  .lettura {
    margin: 0 0 2.25rem;
    padding: 1rem 1.15rem;
    border: 1px solid var(--rule);
    border-radius: 3px;
    background: var(--ground);
  }
  .lettura figcaption {
    margin-bottom: 0.6rem;
    font-family: "Karla", system-ui, sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
  }
  .lettura audio {
    display: block;
    width: 100%;
    height: 2.4rem;
  }
  .lettura audio::-webkit-media-controls-panel {
    background: transparent;
  }

  .apertura::first-letter {
    float: left;
    font-family: "Young Serif", Georgia, serif;
    font-size: 3.6em;
    line-height: 0.82;
    padding: 0.06em 0.09em 0 0;
    color: var(--accent);
  }

  .congedo {
    font-family: "Young Serif", Georgia, serif;
    font-size: 1.25rem;
    color: var(--accent);
  }

  .divisorio { display: flex; justify-content: center; padding-top: 2.5rem; }
  .lucciole { display: inline-flex; gap: 0.9rem; }
  .lucciola {
    width: 0.4rem;
    height: 0.4rem;
    border-radius: 50%;
    background: var(--glow);
    box-shadow: 0 0 0 5px var(--alone);
    animation: respiro 4.4s ease-in-out infinite;
    animation-delay: var(--ritardo);
  }
  @keyframes respiro {
    0%, 100% { opacity: 0.22; transform: scale(0.85); }
    45% { opacity: 1; transform: scale(1); }
  }

  .colophon {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    color: var(--muted);
    font-size: 0.9375rem;
  }
  .colophon p { margin: 0; }

  a:focus-visible, button:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 3px;
    border-radius: 2px;
  }

  /* --- scala del testo: si legge ad alta voce, spesso al buio -------- */
  :root { --scala: 1; }
  body { font-size: calc(1.1875rem * var(--scala)); }

  /* --- barra di servizio: compare quando si è dentro una fiaba ------- */
  .barra {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 20;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem max(1.5rem, calc(50vw - 21rem + 1.5rem));
    background: var(--ground);
    background: color-mix(in srgb, var(--ground) 97%, transparent);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--rule);
    transform: translateY(-105%);
    transition: transform 0.22s ease;
  }
  .barra[data-visibile="si"] { transform: none; }
  .barra .dove {
    flex: 1 1 auto;
    min-width: 0;
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    font-family: "Karla", system-ui, sans-serif;
    font-size: 0.8125rem;
    color: var(--muted);
  }
  .barra .dove-numero { font-weight: 600; color: var(--accent); flex: none; }
  .barra .dove-titolo {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .barra-azioni { display: flex; align-items: center; gap: 0.25rem; flex: none; }

  .tasto {
    appearance: none;
    border: 1px solid transparent;
    background: none;
    color: var(--muted);
    font-family: "Karla", system-ui, sans-serif;
    font-size: 0.8125rem;
    font-weight: 600;
    line-height: 1;
    padding: 0.5rem 0.6rem;
    border-radius: 999px;
    cursor: pointer;
    min-height: 2.5rem;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
  }
  .tasto:hover { color: var(--accent); border-color: var(--rule); }
  .tasto:focus-visible,
  .interruttore:focus-visible,
  .indice a:focus-visible,
  .riprendi a:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
    border-radius: 6px;
  }
  .tasto .aa-piccola { font-size: 0.7em; }

  /* --- riprendi da dove si era rimasti ------------------------------- */
  .riprendi {
    display: none;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    border: 1px solid var(--rule);
    border-radius: 12px;
    background: var(--paper);
    box-shadow: var(--ombra);
  }
  .riprendi[data-visibile="si"] { display: flex; }
  .riprendi a {
    font-family: "Karla", system-ui, sans-serif;
    font-size: 0.9375rem;
    font-weight: 600;
    color: var(--accent);
    text-decoration: none;
    flex: 1 1 auto;
  }
  .riprendi a:hover { text-decoration: underline; }

  /* --- segno sulle fiabe già raggiunte ------------------------------- */
  .indice li[data-letta="si"] .numero::after {
    content: "";
    display: inline-block;
    width: 0.3rem;
    height: 0.3rem;
    margin-left: 0.35rem;
    border-radius: 50%;
    background: var(--accent);
    vertical-align: 0.15em;
  }
  .indice li[data-letta="si"] .voce-titolo { color: var(--muted); }

  /* --- ancore: non finire sotto la barra ----------------------------- */
  .fiaba { scroll-margin-top: 4.25rem; }
  .indice { scroll-margin-top: 4.25rem; }

  /* --- il lettore audio è il comando più usato al buio --------------- */
  .lettura audio { width: 100%; min-height: 2.75rem; }

  @media (max-width: 30rem) {
    .barra { padding-left: 1rem; padding-right: 1rem; gap: 0.5rem; }
    .barra .dove-titolo { display: none; }
  }
  @media (prefers-reduced-motion: reduce) {
    .barra { transition: none; }
  }

  @media (prefers-reduced-motion: reduce) {
    .lucciola { animation: none; opacity: 0.9; }
    * { transition-duration: 0.01ms !important; }
  }
"""

PRESCRIPT = """
  (function () {
    try {
      var tema = localStorage.getItem("fiabe:tema");
      if (tema === "dark" || tema === "light") {
        document.documentElement.setAttribute("data-theme", tema);
      }
      var SCALE = [0.92, 1, 1.12, 1.26];
      var passo = parseInt(localStorage.getItem("fiabe:scala"), 10);
      if (!isNaN(passo) && passo >= 0 && passo < SCALE.length) {
        document.documentElement.style.setProperty("--scala", String(SCALE[passo]));
      }
    } catch (e) { /* senza memoria si parte dai valori di partenza */ }
  })();
"""

SCRIPT = """
  (function () {
    var radice = document.documentElement;
    var sistemaScuro = window.matchMedia("(prefers-color-scheme: dark)");
    var lento = window.matchMedia("(prefers-reduced-motion: reduce)");
    var SCALE = [0.92, 1, 1.12, 1.26];

    // localStorage puo' mancare (navigazione privata, cookie bloccati):
    // la pagina deve funzionare comunque, solo senza memoria.
    function leggi(chiave) {
      try { return window.localStorage.getItem(chiave); } catch (e) { return null; }
    }
    function scrivi(chiave, valore) {
      try { window.localStorage.setItem(chiave, valore); } catch (e) { /* pazienza */ }
    }

    /* ---------- tema ---------- */
    var interruttore = document.getElementById("interruttore");
    var temaBarra = document.getElementById("tema-barra");

    function scuroAdesso() {
      var scelta = radice.getAttribute("data-theme");
      return scelta ? scelta === "dark" : sistemaScuro.matches;
    }
    function aggiornaEtichetta() {
      var scuro = scuroAdesso();
      interruttore.textContent = scuro ? "Accendi la luce" : "Spegni la luce";
      interruttore.setAttribute("aria-label", scuro ? "Passa al tema chiaro" : "Passa al tema scuro");
    }
    function cambiaTema() {
      var prossimo = scuroAdesso() ? "light" : "dark";
      radice.setAttribute("data-theme", prossimo);
      scrivi("fiabe:tema", prossimo);
      aggiornaEtichetta();
    }
    interruttore.addEventListener("click", cambiaTema);
    temaBarra.addEventListener("click", cambiaTema);
    sistemaScuro.addEventListener("change", aggiornaEtichetta);
    aggiornaEtichetta();

    /* ---------- dimensione del testo ---------- */
    var passo = parseInt(leggi("fiabe:scala"), 10);
    if (isNaN(passo) || passo < 0 || passo >= SCALE.length) { passo = 1; }

    function applicaScala() {
      radice.style.setProperty("--scala", String(SCALE[passo]));
      document.getElementById("testo-meno").disabled = (passo === 0);
      document.getElementById("testo-piu").disabled = (passo === SCALE.length - 1);
      scrivi("fiabe:scala", String(passo));
    }
    document.getElementById("testo-meno").addEventListener("click", function () {
      if (passo > 0) { passo--; applicaScala(); }
    });
    document.getElementById("testo-piu").addEventListener("click", function () {
      if (passo < SCALE.length - 1) { passo++; applicaScala(); }
    });
    applicaScala();

    /* ---------- dove siamo, e dove eravamo rimasti ---------- */
    var fiabe = Array.prototype.slice.call(document.querySelectorAll(".fiaba"));
    var vociIndice = Array.prototype.slice.call(document.querySelectorAll(".indice li"));
    var barra = document.getElementById("barra");
    var doveNumero = document.getElementById("dove-numero");
    var doveTitolo = document.getElementById("dove-titolo");
    var riquadro = document.getElementById("riprendi");
    var riquadroLink = document.getElementById("riprendi-link");

    function datiFiaba(articolo) {
      var testata = articolo.querySelector(".fiaba-testata");
      var numero = testata.querySelector(".etichetta").textContent.split("\u00b7")[0].trim();
      return {
        id: articolo.id,
        numero: numero,
        titolo: testata.querySelector("h2").textContent,
        ripresa: (articolo.getAttribute("data-ripresa") || ("dal Libro " + numero))
                   .replace(/&rsquo;/g, "\u2019")
      };
    }

    var corrente = null;

    function segnaLette(fino) {
      vociIndice.forEach(function (li, i) {
        li.setAttribute("data-letta", i < fino ? "si" : "no");
      });
    }

    var arrivata = parseInt(leggi("fiabe:arrivata"), 10);
    if (isNaN(arrivata) || arrivata < 0) { arrivata = 0; }
    segnaLette(arrivata);

    // ripresa: solo se si era andati oltre la prima fiaba e si riparte dall'alto
    var ultima = leggi("fiabe:ultima");
    if (ultima) {
      var bersaglio = document.getElementById(ultima);
      if (bersaglio && window.scrollY < 40 && fiabe.indexOf(bersaglio) > 0) {
        var d = datiFiaba(bersaglio);
        riquadroLink.textContent = (d.titolo === d.numero)
          ? "Riprendi " + d.ripresa
          : "Riprendi " + d.ripresa + " \u2014 " + d.titolo;
        riquadroLink.setAttribute("href", "#" + d.id);
        riquadro.setAttribute("data-visibile", "si");
      }
    }
    document.getElementById("riprendi-chiudi").addEventListener("click", function () {
      riquadro.setAttribute("data-visibile", "no");
    });
    riquadroLink.addEventListener("click", function () {
      riquadro.setAttribute("data-visibile", "no");
    });

    if ("IntersectionObserver" in window) {
      var visibili = {};
      var osservatore = new IntersectionObserver(function (voci) {
        voci.forEach(function (v) { visibili[v.target.id] = v.isIntersecting; });

        var attiva = null;
        for (var i = 0; i < fiabe.length; i++) {
          if (visibili[fiabe[i].id]) { attiva = fiabe[i]; break; }
        }
        if (!attiva || attiva === corrente) { return; }
        corrente = attiva;

        var d = datiFiaba(attiva);
        doveNumero.textContent = d.numero;
        doveTitolo.textContent = d.titolo;
        scrivi("fiabe:ultima", d.id);

        var indice = fiabe.indexOf(attiva);
        if (indice > arrivata) {
          arrivata = indice;
          scrivi("fiabe:arrivata", String(arrivata));
          segnaLette(arrivata);
        }

        // l'osservatore arriva dopo l'ultimo evento di scroll: senza questa
        // riga la barra compare solo al movimento successivo, e saltando
        // dall'indice a una fiaba non compare affatto.
        aggiornaBarra();
      }, { rootMargin: "-45% 0px -45% 0px" });
      fiabe.forEach(function (f) { osservatore.observe(f); });
    }

    // la barra serve dentro le fiabe, non in cima alla pagina
    var soglia = document.querySelector(".indice");
    function aggiornaBarra() {
      var dentro = soglia.getBoundingClientRect().bottom < 0;
      barra.setAttribute("data-visibile", dentro && corrente ? "si" : "no");
    }
    window.addEventListener("scroll", aggiornaBarra, { passive: true });
    aggiornaBarra();

    /* ---------- un lettore audio alla volta ---------- */
    var lettori = Array.prototype.slice.call(document.querySelectorAll("audio"));
    lettori.forEach(function (a) {
      a.addEventListener("play", function () {
        lettori.forEach(function (altro) { if (altro !== a) { altro.pause(); } });
      });
    });

    if (lento.matches) { radice.style.scrollBehavior = "auto"; }
  })();
"""

FONTS = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Young+Serif&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..600'
         '&family=Karla:wght@400;600&display=swap">')

totale_minuti = sum(f["minuti"] for f in fiabe)
numero_fiabe = sum(1 for f in fiabe if not f["speciale"])
extra = [f["titolo"].lower() for f in fiabe if f["speciale"]]
coda = ""
if len(extra) == 1:
    coda = f", un {extra[0]}"
elif len(extra) > 1:
    coda = ", un " + " e un ".join(extra)

CORPO = f"""<div class="barra" id="barra" data-visibile="no">
    <a class="tasto" href="#indice">&#9650;&nbsp;Indice</a>
    <p class="dove" id="dove">
      <span class="dove-numero" id="dove-numero"></span>
      <span class="dove-titolo" id="dove-titolo"></span>
    </p>
    <span class="barra-azioni">
      <button class="tasto" id="testo-meno" type="button" aria-label="Testo pi&ugrave; piccolo"><span class="aa-piccola">A</span>&minus;</button>
      <button class="tasto" id="testo-piu" type="button" aria-label="Testo pi&ugrave; grande">A&plus;</button>
      <button class="tasto" id="tema-barra" type="button" aria-label="Cambia tema">&#9681;</button>
    </span>
  </div>

  <div class="pagina">
    <header class="testata">
      <div class="testata-alto">
        <div class="occhiello">
          {lucciole()}
          <p class="etichetta">Fiabe della buonanotte</p>
        </div>
        <button class="interruttore" id="interruttore" type="button">Spegni la luce</button>
      </div>
      <h1>Le fiabe di Nina</h1>
      <p class="intro">{numero_fiabe} storie di una lucciola che impara ad accendersi, a spegnersi e a
      lasciare che sia un&rsquo;altra ad accendersi da sola. Da leggere ad alta voce, una per sera,
      nell&rsquo;ordine in cui sono scritte.</p>
    </header>

    <p class="riprendi" id="riprendi" data-visibile="no">
      <a href="#" id="riprendi-link">Riprendi dal Libro I</a>
      <button class="tasto" id="riprendi-chiudi" type="button" aria-label="Nascondi la ripresa">Chiudi</button>
    </p>

    <nav class="indice" id="indice" aria-label="Indice delle fiabe">
      <p class="etichetta">Indice &middot; {totale_minuti} minuti in tutto</p>
      <ol>
{chr(10).join("        " + v for v in indice)}
      </ol>
    </nav>

{chr(10).join(articoli)}

    <footer class="colophon">
      <p class="etichetta">Colophon</p>
      <p>{numero_fiabe} fiabe{coda}, {sum(f['parole'] for f in fiabe)} parole. I tempi di lettura sono calcolati
      a {PAROLE_AL_MINUTO} parole al minuto: il passo di chi legge ad alta voce, non di chi legge
      da solo.</p>
    </footer>
  </div>"""

TITOLO = "<title>Le fiabe di Nina</title>"

# 1. pagina autonoma per la cartella del progetto
autonoma = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{TITOLO}
<meta name="description" content="{numero_fiabe} fiabe della buonanotte su Nina, la lucciola del prato ai piedi della collina.">
<link rel="canonical" href="https://fiabe.vercel.app/">
{FONTS}
<style>{STILE}</style>
<script>{PRESCRIPT}</script>
</head>
<body>
{CORPO}
<script>{SCRIPT}</script>
</body>
</html>
"""
with open(os.path.join(SRC, "index.html"), "w", encoding="utf-8") as fp:
    fp.write(autonoma)

# 2. versione per l'Artifact: niente doctype/html/head/body, li aggiunge la piattaforma
artifact = f"""{TITOLO}
{FONTS}
<style>{STILE}</style>
<script>{PRESCRIPT}</script>
{CORPO}
<script>{SCRIPT}</script>
"""
fuori = os.environ.get("SCRATCH")
if fuori:
    with open(os.path.join(fuori, "fiabe-di-nina.html"), "w", encoding="utf-8") as fp:
        fp.write(artifact)

for f in fiabe:
    print(f"{f['titolo']}: {f['parole']} parole, {f['minuti']} min")
print("scritti index.html e fiabe-di-nina.html")
