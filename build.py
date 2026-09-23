#!/usr/bin/env python3
"""Genera la pagina web delle fiabe di Nina dai file .md della cartella.

Il markdown delle fiabe usa solo quattro costrutti: '# titolo', una riga di
sottotitolo in corsivo, il separatore '---' e paragrafi con *enfasi*.
Quattro regole bastano: nessuna libreria.
"""
import datetime
import glob
import html
import json
import math
import os
import re

SRC = os.path.dirname(os.path.abspath(__file__))
STORIE = os.path.join(SRC, "stories")
SITO = "https://fiabe.vercel.app"
SPECIALI = {"prologo", "prologue", "epilogo", "epilogue"}

# Persone dietro il progetto (nomi d'arte). Finiscono nei metadati della
# pagina (autore, dati strutturati) perché aiutano la ricerca ad associare
# il sito a chi lo fa, non perché servano a un lettore umano.
AUTORE = "Fausto Chiantera"
VOCE_E_SITO = "Deckard"

# Mappa lingua -> locale nel formato che Open Graph vuole (con underscore).
OG_LOCALE = {"it": "it_IT", "en-GB": "en_GB"}

# Una lingua per cartella. "uscita" è il file generato, "base" il prefisso
# degli URL. L'italiano sta alla radice perché era lì da prima.
# Un libro per cartella. L'ordine è quello dello scaffale.
LIBRI = [
    {
        "cartella": "nina",
        "copertina": "meadow",
        "it": {
            "titolo": "Le fiabe di Nina",
            "nome_breve": "Nina",
            "occhiello": "Libro primo",
            "riassunto": ("Una lucciola che impara ad accendersi, a spegnersi e a lasciare "
                          "che sia un&rsquo;altra ad accendersi da sola."),
            "descrizione": "{n} fiabe della buonanotte su Nina, la lucciola del prato ai piedi della collina.",
        },
        "en-GB": {
            "titolo": "Nina&rsquo;s stories",
            "nome_breve": "Nina",
            "occhiello": "Book one",
            "riassunto": ("A firefly who learns to light up, to put herself out, and to let "
                          "someone else come to it on her own."),
            "descrizione": "{n} bedtime stories about Nina, the firefly of the meadow at the foot of the hill.",
        },
    },
    {
        "cartella": "tilde",
        "copertina": "burrow",
        "it": {
            "titolo": "Le fiabe di Tilde",
            "nome_breve": "Tilde",
            "occhiello": "Libro secondo",
            "riassunto": ("La vecchia talpa del prato, quella che non trovava mai la porta di "
                          "casa. Vista da sotto, dove la porta la trova benissimo."),
            "descrizione": "{n} fiabe della buonanotte su Tilde, la vecchia talpa del prato ai piedi della collina.",
        },
        "en-GB": {
            "titolo": "Tilde&rsquo;s stories",
            "nome_breve": "Tilde",
            "occhiello": "Book two",
            "riassunto": ("The old mole from the meadow, the one who could never find her own "
                          "front door. Seen from below, where she finds it perfectly well."),
            "descrizione": "{n} bedtime stories about Tilde, the old mole of the meadow at the foot of the hill.",
        },
    },
    {
        "cartella": "ugo",
        "copertina": "attic",
        "it": {
            "titolo": "Le fiabe di Ugo",
            "nome_breve": "Ugo",
            "occhiello": "Libro terzo",
            "riassunto": ("Il pipistrello che abita sotto il tetto della casa in cima alla "
                          "collina. Vede con la voce, e la sua voce non la sente nessuno."),
            "descrizione": "{n} fiabe della buonanotte su Ugo, il pipistrello sotto il tetto della casa in cima alla collina.",
        },
        "en-GB": {
            "titolo": "Ugo&rsquo;s stories",
            "nome_breve": "Ugo",
            "occhiello": "Book three",
            "riassunto": ("The bat who lives under the roof of the house at the top of the hill. "
                          "He sees with his voice, and nobody can hear it."),
            "descrizione": "{n} bedtime stories about Ugo, the bat under the roof of the house at the top of the hill.",
        },
    },
]

LINGUE = {
    "it": {
        "cartella": "it",
        "uscita": "index.html",
        "base": "/",
        "lang": "it",
        "nome": "Italiano",
        "audio": "audio",
        "sito": "Le fiabe di Nina",
        "occhiello": "Fiabe della buonanotte",
        "intro": ("{n} storie di una lucciola che impara ad accendersi, a spegnersi e a "
                  "lasciare che sia un&rsquo;altra ad accendersi da sola. Da leggere ad alta "
                  "voce, una per sera, nell&rsquo;ordine in cui sono scritte."),
        "indice": "Indice",
        "in_tutto": "{m} minuti in tutto",
        "minuti_lettura": "{m} minuti di lettura",
        "ascolta": "Ascolta",
        "no_audio": "Il tuo browser non supporta la riproduzione audio.",
        "libro": "Libro",
        "da_libro": "dal Libro {r}",
        "da_prologo": "dal Prologo",
        "da_epilogo": "dall&rsquo;Epilogo",
        "colophon": "Colophon",
        "colophon_testo": ("{n} fiabe{coda}, {p} parole. I tempi di lettura sono calcolati a {wpm} "
                           "parole al minuto: il passo di chi legge ad alta voce, non di chi legge da solo."),
        "extra_nome": {"prologo": "un prologo", "epilogo": "un epilogo"},
        "extra_giunzione": " e ",
        "spegni": "Spegni la luce",
        "accendi": "Accendi la luce",
        "tema_chiaro": "Passa al tema chiaro",
        "tema_scuro": "Passa al tema scuro",
        "riprendi": "Riprendi",
        "chiudi": "Chiudi",
        "chiudi_aria": "Nascondi la ripresa",
        "testo_meno": "Testo pi&ugrave; piccolo",
        "testo_piu": "Testo pi&ugrave; grande",
        "cambia_tema": "Cambia tema",
        "altra_lingua": "English",
        "scaffale": "Le fiabe della buonanotte",
        "scaffale_intro": ("Storie da leggere ad alta voce, una per sera. Ogni libro si legge "
                           "nell&rsquo;ordine in cui &egrave; scritto."),
        "tutti_i_libri": "Tutti i libri",
        "torna_scaffale": "&#9664;&nbsp;I libri",
        "quante": "{n} fiabe &middot; {m} minuti",
        "una_fiaba": "1 fiaba &middot; {m} minuti",
        "in_preparazione": "In preparazione",
        "sei_a": "Riprendi {d}",
        "apri": "Apri",
    },
    "en-GB": {
        "cartella": "en-GB",
        "uscita": os.path.join("en", "index.html"),
        "base": "/en/",
        "lang": "en-GB",
        "nome": "English",
        "audio": os.path.join("audio", "en-GB"),
        "sito": "Nina&rsquo;s Bedtime Stories",
        "occhiello": "Bedtime stories",
        "intro": ("{n} stories about a firefly who learns to light up, to put herself out, and "
                  "to let someone else come to it on her own. To be read aloud, one a night, "
                  "in the order they were written."),
        "indice": "Contents",
        "in_tutto": "{m} minutes in all",
        "minuti_lettura": "{m} minutes to read aloud",
        "ascolta": "Listen",
        "no_audio": "Your browser cannot play this audio.",
        "libro": "Book",
        "da_libro": "from Book {r}",
        "da_prologo": "from the Prologue",
        "da_epilogo": "from the Epilogue",
        "colophon": "Colophon",
        "colophon_testo": ("{n} stories{coda}, {p} words. Reading times are worked out at {wpm} words a "
                           "minute: the pace of someone reading aloud, not of someone reading alone."),
        "extra_nome": {"prologue": "a prologue", "epilogue": "an epilogue"},
        "extra_giunzione": " and ",
        "spegni": "Turn the light off",
        "accendi": "Turn the light on",
        "tema_chiaro": "Switch to the light theme",
        "tema_scuro": "Switch to the dark theme",
        "riprendi": "Resume",
        "chiudi": "Close",
        "chiudi_aria": "Hide the resume prompt",
        "testo_meno": "Smaller text",
        "testo_piu": "Larger text",
        "cambia_tema": "Change theme",
        "altra_lingua": "Italiano",
        "scaffale": "Bedtime stories",
        "scaffale_intro": ("Stories to be read aloud, one a night. Each book reads in the order "
                           "it was written."),
        "tutti_i_libri": "All the books",
        "torna_scaffale": "&#9664;&nbsp;The books",
        "quante": "{n} stories &middot; {m} minutes",
        "una_fiaba": "1 story &middot; {m} minutes",
        "in_preparazione": "In preparation",
        "sei_a": "Resume {d}",
        "apri": "Open",
    },
}
LINGUE["it"].update({
    "inizia": "Comincia a leggere", "prossima": "La prossima storia", "fine": "Buonanotte, a domani",
    "hero": "Le storie belle.<br><em>Le sere insieme.</em>", "scopri": "Scegli una storia",
    "biblioteca": "Il nostro piccolo scaffale",
    "scaffale_nota": "Un prato, tante storie", "firma": "Dal prato ai piedi della collina. Con amore.",
    "leggi_libro": "Entra nella storia",
})
LINGUE["en-GB"].update({
    "inizia": "Start reading", "prossima": "The next story", "fine": "Goodnight, see you tomorrow",
    "hero": "Little stories.<br><em>Evenings together.</em>", "scopri": "Choose a story",
    "biblioteca": "Our little bookshelf",
    "scaffale_nota": "One meadow, many stories", "firma": "From the meadow at the foot of the hill. With love.",
    "leggi_libro": "Step into the story",
})

COPERTINE = {l["cartella"]: l["copertina"] for l in LIBRI}

ROMANI = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
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
    speciale = chiave in SPECIALI
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


def audio_per(cartella_audio, numero):
    """Percorso dell'audio della fiaba, relativo alla radice del sito."""
    candidati = sorted(glob.glob(os.path.join(SRC, cartella_audio, f"11l-{numero}-*.mp3")))
    if candidati:
        return "/" + os.path.relpath(candidati[0], SRC).replace(os.sep, "/")
    return None


def raccogli(lingua, libro):
    """Legge le fiabe di un libro in una lingua e prepara indice e articoli."""
    cartella = os.path.join(STORIE, lingua["cartella"], libro["cartella"])
    fiabe = [leggi(f) for f in sorted(glob.glob(os.path.join(cartella, "[0-9][0-9]*.md")))]

    indice, articoli = [], []
    conta = 0
    for f in fiabe:
        if f["speciale"]:
            # l'ancora non cambia con la lingua: #prologo e #epilogo sono gli
            # stessi ovunque, così i link restano validi e un domani si può
            # cambiare lingua restando sulla stessa fiaba.
            epilogo = "epilog" in f["chiave"]
            slug = "epilogo" if epilogo else "prologo"
            etichetta_numero = f["titolo"]
            numero_indice = "&mdash;"
            ripresa = lingua["da_epilogo" if epilogo else "da_prologo"]
        else:
            slug = f"libro-{conta + 1}"
            etichetta_numero = ROMANI[conta]
            numero_indice = ROMANI[conta]
            ripresa = lingua["da_libro"].format(r=ROMANI[conta])
            conta += 1

        f["slug"] = slug
        minuti = lingua["minuti_lettura"].format(m=f["minuti"])
        indice.append(
            f'<li><a href="#{slug}"><span class="numero">{numero_indice}</span>'
            f'<span class="voce-titolo">{inline(f["titolo"])}</span>'
            f'<span class="voce-durata">{f["minuti"]} min</span></a></li>'
        )

        corpo = []
        for j, par in enumerate(f["paragrafi"]):
            classi = []
            if j == 0:
                classi.append("apertura")
            if par.startswith("Buonanotte.") or par.startswith("Goodnight."):
                classi.append("congedo")
            attr = f' class="{" ".join(classi)}"' if classi else ""
            corpo.append(f"      <p{attr}>{inline(par)}</p>")

        audio = audio_per(os.path.join(lingua["audio"], libro["cartella"]), f["numero"])
        lettore = ""
        if audio:
            lettore = (
                f'        <figure class="lettura">\n'
                f'          <figcaption>{lingua["ascolta"]}</figcaption>\n'
                f'          <audio controls preload="none" src="{audio}">\n'
                f'            {lingua["no_audio"]}\n'
                f'          </audio>\n'
                f'        </figure>\n'
            )

        illustrazione = ""
        disegno = f'assets/chapters/{libro["cartella"]}/{f["numero"]}.svg'
        if os.path.isfile(os.path.join(SRC, disegno)):
            illustrazione = (f'      <img class="illustrazione-capitolo" src="/{disegno}" '
                             f'width="800" height="560" alt="" loading="lazy" decoding="async">\n')

        articoli.append(
            f'    <article class="fiaba" id="{slug}" data-ripresa="{ripresa}">\n'
            f'      <header class="fiaba-testata">\n'
            f'        <p class="etichetta">{etichetta_numero} &middot; {minuti}</p>\n'
            f'        <h2>{inline(f["titolo"])}</h2>\n'
            f'        <p class="sottotitolo">{inline(f["sottotitolo"])}</p>\n'
            f"      </header>\n" + illustrazione + lettore + "\n".join(corpo) + "\n"
            f'      <div class="divisorio">{lucciole()}</div>\n'
            f"    </article>"
        )
    for i, articolo in enumerate(articoli):
        if i + 1 < len(articoli):
            destinazione = "#" + fiabe[i + 1]["slug"]
            titolo = inline(fiabe[i + 1]["titolo"])
            testo = lingua["prossima"]
        else:
            destinazione = lingua["base"]
            titolo = lingua["tutti_i_libri"]
            testo = lingua["fine"]
        navigazione = (f'<nav class="prossima" aria-label="{testo}">'
                       f'<span class="etichetta">{testo}</span>'
                       f'<a href="{destinazione}">{titolo} <span aria-hidden="true">&rarr;</span></a></nav>')
        articoli[i] = articolo.replace('    </article>', navigazione + '\n    </article>')
    return fiabe, indice, articoli


with open(os.path.join(SRC, "assets", "fiabe.css"), encoding="utf-8") as fp:
    STILE = fp.read()

SCAFFALE_SCRIPT = """
  (function () {
    var T = /*TRADUZIONI*/;
    var radice = document.documentElement;
    var sistemaScuro = window.matchMedia("(prefers-color-scheme: dark)");
    var interruttore = document.getElementById("interruttore");

    function leggi(chiave) {
      try { return window.localStorage.getItem(chiave); } catch (e) { return null; }
    }
    function scrivi(chiave, valore) {
      try { window.localStorage.setItem(chiave, valore); } catch (e) { /* pazienza */ }
    }

    function scuroAdesso() {
      var scelta = radice.getAttribute("data-theme");
      return scelta ? scelta === "dark" : sistemaScuro.matches;
    }
    function aggiornaEtichetta() {
      var scuro = scuroAdesso();
      interruttore.textContent = scuro ? T.accendi : T.spegni;
      interruttore.setAttribute("aria-label", scuro ? T.temaChiaro : T.temaScuro);
    }
    interruttore.addEventListener("click", function () {
      var prossimo = scuroAdesso() ? "light" : "dark";
      radice.setAttribute("data-theme", prossimo);
      scrivi("fiabe:tema", prossimo);
      aggiornaEtichetta();
    });
    sistemaScuro.addEventListener("change", aggiornaEtichetta);
    aggiornaEtichetta();

    // per ogni libro, dove si era arrivati
    var righe = document.querySelectorAll(".ripresa-libro");
    Array.prototype.forEach.call(righe, function (riga) {
      var ancora = leggi(riga.getAttribute("data-libro") + ":ultima");
      if (!ancora) { return; }
      var a = document.createElement("a");
      a.setAttribute("href", riga.getAttribute("data-base") + "#" + ancora);
      var etichette = {};
      try { etichette = JSON.parse(riga.getAttribute("data-etichette") || "{}"); } catch (e) { etichette = {}; }
      var dove = etichette[ancora];
      if (!dove) { return; }
      a.textContent = riga.getAttribute("data-testo").replace("{d}", dove);
      riga.appendChild(a);
      riga.setAttribute("data-visibile", "si");
    });
  })();
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
    var T = /*TRADUZIONI*/;
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
      interruttore.textContent = scuro ? T.accendi : T.spegni;
      interruttore.setAttribute("aria-label", scuro ? T.temaChiaro : T.temaScuro);
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

    var arrivata = parseInt(leggi(T.memoria + ":arrivata"), 10);
    if (isNaN(arrivata) || arrivata < 0) { arrivata = 0; }
    segnaLette(arrivata);

    // ripresa: solo se si era andati oltre la prima fiaba e si riparte dall'alto
    var ultima = leggi(T.memoria + ":ultima");
    if (ultima) {
      var bersaglio = document.getElementById(ultima);
      if (bersaglio && window.scrollY < 40 && fiabe.indexOf(bersaglio) > 0) {
        var d = datiFiaba(bersaglio);
        riquadroLink.textContent = (d.titolo === d.numero)
          ? T.riprendi + " " + d.ripresa
          : T.riprendi + " " + d.ripresa + " \u2014 " + d.titolo;
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
        // nel Prologo e nell'Epilogo il titolo e' gia' il numero: non ripeterlo
        doveTitolo.textContent = (d.titolo === d.numero) ? "" : d.titolo;
        scrivi(T.memoria + ":ultima", d.id);

        var indice = fiabe.indexOf(attiva);
        if (indice > arrivata) {
          arrivata = indice;
          scrivi(T.memoria + ":arrivata", String(arrivata));
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
    function aggiornaBarra() {
      var dentro = fiabe.length && fiabe[0].getBoundingClientRect().top <= 80;
      var visibile = !!(dentro && corrente);
      barra.setAttribute("data-visibile", visibile ? "si" : "no");
      barra.inert = !visibile;
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



def guscio(lingua, titolo_tab, descrizione, url, corpo, script, jsonld=None):
    """Mette insieme una pagina completa."""
    alternative = "\n".join(
        f'<link rel="alternate" hreflang="{l["lang"]}" href="{SITO}{l["base"]}{url}">'
        for l in LINGUE.values()
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITO}/{url}">'
    canonico = f'{SITO}{lingua["base"]}{url}'
    cartella = url.rstrip("/")
    libro_pagina = cartella in {l["cartella"] for l in LIBRI}
    immagine = (f"{SITO}/assets/og-{cartella}.png" if libro_pagina
                else f"{SITO}/assets/og-default.png")
    tipo_og = "book" if libro_pagina else "website"
    locale_alternative = "\n".join(
        f'<meta property="og:locale:alternate" content="{OG_LOCALE.get(l["lang"], l["lang"])}">'
        for l in LINGUE.values() if l["lang"] != lingua["lang"]
    )
    dati_strutturati = (
        f'\n<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>'
        if jsonld else ""
    )
    return f"""<!doctype html>
<html lang="{lingua["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titolo_tab}</title>
<meta name="description" content="{descrizione}">
<meta name="author" content="{AUTORE}">
<link rel="canonical" href="{canonico}">
{alternative}
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="{lingua["base"]}manifest.json">
<meta name="theme-color" content="#14241e">
<meta property="og:type" content="{tipo_og}">
<meta property="og:site_name" content="Fiabe">
<meta property="og:title" content="{titolo_tab}">
<meta property="og:description" content="{descrizione}">
<meta property="og:url" content="{canonico}">
<meta property="og:image" content="{immagine}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{OG_LOCALE.get(lingua["lang"], lingua["lang"])}">
{locale_alternative}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titolo_tab}">
<meta name="twitter:description" content="{descrizione}">
<meta name="twitter:image" content="{immagine}">{dati_strutturati}
{FONTS}
<link rel="stylesheet" href="/assets/fiabe.css">
<script>{PRESCRIPT}</script>
</head>
<body>
{corpo}
<script>{script}</script>
</body>
</html>
"""


def traduzioni_js(lingua, extra=None):
    d = {
        "accendi": lingua["accendi"],
        "spegni": lingua["spegni"],
        "temaChiaro": lingua["tema_chiaro"],
        "temaScuro": lingua["tema_scuro"],
        "riprendi": lingua["riprendi"],
    }
    if extra:
        d.update(extra)
    return json.dumps(d, ensure_ascii=False)


def scrivi(lingua, url, html_pagina):
    destinazione = os.path.join(SRC, lingua["base"].strip("/").replace("/", os.sep), url, "index.html")
    destinazione = os.path.normpath(destinazione)
    os.makedirs(os.path.dirname(destinazione), exist_ok=True)
    with open(destinazione, "w", encoding="utf-8") as fp:
        fp.write(html_pagina)
    return os.path.relpath(destinazione, SRC)


def pagina(codice, lingua, libro):
    fiabe, indice, articoli = raccogli(lingua, libro)
    if not fiabe:
        return None
    voce = libro[codice]

    totale_minuti = sum(f["minuti"] for f in fiabe)
    numero_fiabe = sum(1 for f in fiabe if not f["speciale"])
    parole = sum(f["parole"] for f in fiabe)

    # "un prologo e un epilogo": l'articolo cambia con la parola e con la
    # lingua ("a prologue" ma "an epilogue"), quindi sta scritto per esteso.
    pezzi = [lingua["extra_nome"][f["chiave"]] for f in fiabe
             if f["speciale"] and f["chiave"] in lingua["extra_nome"]]
    coda = ", " + lingua["extra_giunzione"].join(pezzi) if pezzi else ""

    scambio = cambio_lingua(codice, libro["cartella"] + "/")
    titolo_sito = voce["titolo"]
    corpo = f'''<a class="skip-link" href="#indice">{lingua["indice"]}</a>
  <div class="barra" id="barra" data-visibile="no" inert>
    <a class="tasto" href="#indice">&#9650;&nbsp;{lingua["indice"]}</a>
    <p class="dove" id="dove">
      <a class="dove-libro" href="{lingua["base"]}" title="{lingua["tutti_i_libri"]}">{voce["nome_breve"]}</a>
      <span class="dove-numero" id="dove-numero"></span>
      <span class="dove-titolo" id="dove-titolo"></span>
    </p>
    <span class="barra-azioni">
      <button class="tasto" id="testo-meno" type="button" aria-label="{lingua["testo_meno"]}"><span class="aa-piccola">A</span>&minus;</button>
      <button class="tasto" id="testo-piu" type="button" aria-label="{lingua["testo_piu"]}">A&plus;</button>
      <button class="tasto" id="tema-barra" type="button" aria-label="{lingua["cambia_tema"]}">&#9681;</button>
    </span>
  </div>

  <main class="pagina">
    <header class="testata">
      <div class="testata-alto">
        <a class="marchio" href="{lingua["base"]}" aria-label="{lingua["tutti_i_libri"]}">fiabe</a>
        <span class="testata-azioni">
          {scambio}
          <button class="interruttore" id="interruttore" type="button">{lingua["spegni"]}</button>
        </span>
      </div>
      <p class="briciola"><a href="{lingua["base"]}">{lingua["torna_scaffale"]}</a></p>
      <h1>{titolo_sito}</h1>
      <p class="intro">{voce["riassunto"]}</p>
      <div class="libro-azioni">
        <a class="bottone" href="#{fiabe[0]['slug']}">{lingua["inizia"]} <span aria-hidden="true">&rarr;</span></a>
        <p class="quante">{lingua["in_tutto"].format(m=totale_minuti)}</p>
      </div>
    </header>

    <p class="riprendi" id="riprendi" data-visibile="no">
      <a href="#" id="riprendi-link">{lingua["riprendi"]}</a>
      <button class="tasto" id="riprendi-chiudi" type="button" aria-label="{lingua["chiudi_aria"]}">{lingua["chiudi"]}</button>
    </p>

    <nav class="indice" id="indice" aria-label="{lingua["indice"]}">
      <p class="etichetta">{lingua["indice"]} &middot; {lingua["in_tutto"].format(m=totale_minuti)}</p>
      <ol>
{chr(10).join("        " + v for v in indice)}
      </ol>
    </nav>

{chr(10).join(articoli)}

    <footer class="colophon">
      <p class="etichetta">{lingua["colophon"]}</p>
      <p>{lingua["colophon_testo"].format(n=numero_fiabe, coda=coda, p=parole, wpm=PAROLE_AL_MINUTO)}</p>
    </footer>
  </main>'''

    script = SCRIPT.replace("/*TRADUZIONI*/",
                            traduzioni_js(lingua, {"memoria": "fiabe:" + libro["cartella"]}))

    titolo_pulito = voce["titolo"].replace("&rsquo;", "\u2019")
    descrizione = voce["descrizione"].format(n=numero_fiabe)
    jsonld_libro = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": titolo_pulito,
        "description": descrizione,
        "url": f'{SITO}{lingua["base"]}{libro["cartella"]}/',
        "inLanguage": lingua["lang"],
        "image": f'{SITO}/assets/og-{libro["cartella"]}.png',
        "audience": {"@type": "PeopleAudience", "suggestedMinAge": 3, "suggestedMaxAge": 8},
        "author": {"@type": "Person", "name": AUTORE},
        "contributor": {"@type": "Person", "name": VOCE_E_SITO,
                        "description": "Voce narrante e sviluppo del sito"},
    }

    html_pagina = guscio(
        lingua,
        titolo_pulito,
        descrizione,
        libro["cartella"] + "/",
        corpo,
        script,
        jsonld=jsonld_libro,
    )
    uscita = scrivi(lingua, libro["cartella"], html_pagina)

    fuori = os.environ.get("SCRATCH")
    if fuori and codice == "it" and libro["cartella"] == "nina":
        with open(os.path.join(fuori, "fiabe-di-nina.html"), "w", encoding="utf-8") as fp:
            fp.write(f"<title>{voce['titolo']}</title>\n{FONTS}\n<style>{STILE}</style>\n"
                     f"<script>{PRESCRIPT}</script>\n{corpo}\n<script>{script}</script>\n")

    etichette = {}
    conta2 = 0
    for f in fiabe:
        if f["speciale"]:
            ep = "epilog" in f["chiave"]
            etichette["epilogo" if ep else "prologo"] = lingua["da_epilogo" if ep else "da_prologo"]
        else:
            etichette[f"libro-{conta2 + 1}"] = lingua["da_libro"].format(r=ROMANI[conta2])
            conta2 += 1

    return {"fiabe": fiabe, "uscita": uscita, "minuti": totale_minuti, "etichette": etichette,
            "quante": numero_fiabe, "titolo": voce["titolo"],
            "riassunto": voce["riassunto"], "occhiello": voce["occhiello"],
            "cartella": libro["cartella"]}


def cambio_lingua(codice, url):
    return "".join(
        f'<a class="lingua" href="{l["base"]}{url}" hreflang="{l["lang"]}" lang="{l["lang"]}">{l["nome"]}</a>'
        for c, l in LINGUE.items() if c != codice
    )


def scaffale(codice, lingua, schede):
    """La pagina che elenca i libri."""
    righe = []
    for s in schede:
        if s["pronto"]:
            quante = (lingua["una_fiaba"] if s["quante"] == 1 else lingua["quante"]).format(
                n=s["quante"], m=s["minuti"])
            righe.append(
                f'      <li class="scheda">\n'
                f'        <a class="copertina" href="{lingua["base"]}{s["cartella"]}/" tabindex="-1" aria-hidden="true">'
                f'<img src="/assets/{COPERTINE[s["cartella"]]}.svg" width="800" height="560" alt="" loading="lazy"></a>\n'
                f'        <div class="scheda-corpo"><p class="etichetta">{s["occhiello"]}</p>\n'
                f'        <h2><a href="{lingua["base"]}{s["cartella"]}/">{s["titolo"]}</a></h2>\n'
                f'        <p class="riassunto">{s["riassunto"]}</p>\n'
                f'        <p class="quante">{quante}</p>\n'
                f'        <p class="ripresa-libro" data-libro="fiabe:{s["cartella"]}"'
                f' data-base="{lingua["base"]}{s["cartella"]}/" data-testo="{lingua["sei_a"]}"'
                f' data-etichette="{html.escape(json.dumps(s["etichette"], ensure_ascii=False), quote=True)}"></p>\n'
                f'        <a class="scheda-link" href="{lingua["base"]}{s["cartella"]}/">{lingua["leggi_libro"]} <span aria-hidden="true">&rarr;</span></a></div>\n'
                f'      </li>'
            )
        else:
            righe.append(
                f'      <li class="scheda scheda-attesa"><div class="scheda-corpo">\n'
                f'        <p class="etichetta">{s["occhiello"]}</p>\n'
                f'        <h2>{s["titolo"]}</h2>\n'
                f'        <p class="riassunto">{s["riassunto"]}</p>\n'
                f'        <p class="quante">{lingua["in_preparazione"]}</p></div>\n'
                f'      </li>'
            )

    corpo = f"""<a class="skip-link" href="#scaffale">{lingua["tutti_i_libri"]}</a>
  <main class="pagina pagina-scaffale">
    <header class="testata">
      <div class="testata-alto">
        <a class="marchio" href="{lingua["base"]}" aria-label="{lingua["tutti_i_libri"]}">fiabe</a>
        <span class="testata-azioni">
          {cambio_lingua(codice, "")}
          <button class="interruttore" id="interruttore" type="button">{lingua["spegni"]}</button>
        </span>
      </div>
      <div class="hero">
        <div class="hero-copy">
          <p class="etichetta">{lingua["occhiello"]}</p>
          <h1>{lingua["hero"]}</h1>
          <p class="intro">{lingua["scaffale_intro"]}</p>
          <a class="bottone" href="#scaffale">{lingua["scopri"]} <span aria-hidden="true">&darr;</span></a>
        </div>
      </div>
    </header>

    <nav id="scaffale" aria-label="{lingua["tutti_i_libri"]}">
      <div class="sezione-titolo"><h2>{lingua["biblioteca"]}</h2><span>{lingua["scaffale_nota"]}</span></div>
      <ol class="scaffale">
{chr(10).join(righe)}
      </ol>
    </nav>
    <footer class="scaffale-footer"><p>{lingua["firma"]}</p>{lucciole()}</footer>
  </main>"""

    titolo_sito = lingua["scaffale"].replace("&rsquo;", "\u2019")
    descrizione_sito = lingua["scaffale_intro"].replace("&rsquo;", "\u2019").replace("&egrave;", "\u00e8")
    jsonld_sito = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": titolo_sito,
        "description": descrizione_sito,
        "url": f'{SITO}{lingua["base"]}',
        "inLanguage": lingua["lang"],
        "author": {"@type": "Person", "name": AUTORE},
        "contributor": {"@type": "Person", "name": VOCE_E_SITO,
                        "description": "Voce narrante e sviluppo del sito"},
        "hasPart": [
            {"@type": "Book", "name": s["titolo"].replace("&rsquo;", "\u2019"),
             "url": f'{SITO}{lingua["base"]}{s["cartella"]}/'}
            for s in schede if s["pronto"]
        ],
    }

    script = SCAFFALE_SCRIPT.replace("/*TRADUZIONI*/", traduzioni_js(lingua))
    html_pagina = guscio(lingua, titolo_sito, descrizione_sito, "", corpo, script, jsonld=jsonld_sito)
    return scrivi(lingua, "", html_pagina)


fatte = []
for codice, lingua in LINGUE.items():
    schede = []
    for libro in LIBRI:
        esito = pagina(codice, lingua, libro)
        if esito is None:
            schede.append({"pronto": False, "cartella": libro["cartella"],
                           "titolo": libro[codice]["titolo"],
                           "riassunto": libro[codice]["riassunto"],
                           "occhiello": libro[codice]["occhiello"]})
            print(f"[{codice}/{libro['cartella']}] nessuna fiaba: scheda in preparazione")
            continue
        esito["pronto"] = True
        schede.append(esito)
        fatte.append(esito["uscita"])
        print(f"[{codice}/{libro['cartella']}] -> {esito['uscita']}")
        for f in esito["fiabe"]:
            print(f"    {f['titolo']}: {f['parole']} parole, {f['minuti']} min")

    if not any(s["pronto"] for s in schede):
        print(f"[{codice}] nessun libro: pagina saltata")
        continue
    fatte.append(scaffale(codice, lingua, schede))

# sitemap: scaffale e libri di ogni lingua, con le alternative di lingua
# scritte per esteso (xhtml:link) invece che lasciate solo al <link> nella
# <head> di ogni pagina: è il formato che Google raccomanda per l'hreflang
# e riduce il rischio che una lingua venga indicizzata e l'altra no.
oggi = datetime.date.today().isoformat()
percorsi = [""] + [libro["cartella"] + "/" for libro in LIBRI]
voci = []
for percorso in percorsi:
    presenti = [
        (codice, lingua) for codice, lingua in LINGUE.items()
        if os.path.exists(os.path.join(
            SRC, lingua["base"].strip("/").replace("/", os.sep), percorso, "index.html"))
    ]
    if not presenti:
        continue
    alternative = "\n".join(
        f'    <xhtml:link rel="alternate" hreflang="{lingua["lang"]}" '
        f'href="{SITO}{lingua["base"]}{percorso}"/>'
        for _, lingua in presenti
    )
    for codice, lingua in presenti:
        voci.append(
            f"  <url>\n"
            f"    <loc>{SITO}{lingua['base']}{percorso}</loc>\n"
            f"    <lastmod>{oggi}</lastmod>\n"
            f"{alternative}\n"
            f"  </url>"
        )

with open(os.path.join(SRC, "sitemap.xml"), "w", encoding="utf-8") as fp:
    fp.write('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
             + "\n".join(voci) + "\n</urlset>\n")

# manifest.json: non serve a essere installato come app, ma dà al sito
# un'icona coerente su Android/Chrome e nella scheda "aggiungi alla
# schermata Home", ed è un segnale in più di sito curato per i motori.
# Uno per lingua, con lo start_url giusto: un manifest solo, condiviso da
# tutte le pagine, avrebbe fatto aprire lo scaffale italiano anche a chi
# installa il sito da /en/.
manifesti = []
for codice, lingua in LINGUE.items():
    manifesto = {
        "name": lingua["scaffale"].replace("&rsquo;", "’"),
        "short_name": "Fiabe",
        "description": lingua["scaffale_intro"].replace("&rsquo;", "’").replace("&egrave;", "è"),
        "start_url": lingua["base"],
        "scope": lingua["base"],
        "display": "standalone",
        "background_color": "#14241e",
        "theme_color": "#14241e",
        "lang": lingua["lang"],
        "icons": [
            {"src": "/assets/favicon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
            {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/assets/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
        ],
    }
    percorso = os.path.join(SRC, lingua["base"].strip("/").replace("/", os.sep), "manifest.json")
    percorso = os.path.normpath(percorso)
    with open(percorso, "w", encoding="utf-8") as fp:
        json.dump(manifesto, fp, ensure_ascii=False, indent=2)
        fp.write("\n")
    manifesti.append(os.path.relpath(percorso, SRC))

print("scritte: " + ", ".join(fatte) + ", sitemap.xml, " + ", ".join(manifesti))
