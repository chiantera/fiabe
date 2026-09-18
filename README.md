# Fiabe

Fiabe della buonanotte su **Nina**, la lucciola del prato ai piedi della collina.

## I libri

| | Titolo | Lettura ad alta voce |
|---|---|---|
| — | Prologo | 4 min |
| I | La lucciola che aveva paura del buio | 3 min |
| II | La lucciola e la lanterna stanca | 5 min |
| III | La lucciola e la piccola che non voleva accendersi | 6 min |
| IV | La lucciola e il grillo che perse la voce | 9 min |
| V | La lucciola e la luce nella finestra | 6 min |
| VI | La lucciola e chi scese dalla collina | 6 min |
| VII | La lucciola e il grillo che volò | 7 min |
| VIII | La lucciola che restò sulla radice | 7 min |
| IX | La lucciola che raccontava | 7 min |
| X | La lucciola che ascoltò la sua storia | 8 min |
| — | Epilogo | 4 min |

Vanno letti in ordine: il primo accende la luce, il secondo la spegne, il terzo
scopre che la luce di un altro non si può accendere, il quarto insegna che ciò
che si è donato resta in chi ci è stato vicino. Il quinto porta Nina fuori dal
prato per la prima volta, e le fa scoprire chi c'è dall'altra parte; nel sesto
è l'altra parte che scende nel prato, e deve imparare da capo la lezione del
terzo — che certe cose non si vanno a prendere, si aspettano. Il settimo chiude
la storia di Rocco, e riprende la promessa fatta nel quarto: la canzone resta
in chi l'ha sentita. L'ottavo rifà il secondo con i ruoli scambiati: stavolta
è Bea a spegnersi, e Nina a dire le parole che una volta le aveva detto Rocco.
Nel nono le ali non la portano più, e le lucciole nuove — che Rocco non l'hanno
mai conosciuto — vanno da lei a farsi raccontare le otto fiabe di prima. Nel
decimo è Bea che racconta, e chi ascolta è Nina.

Il **Prologo** si legge per primo ed è scritto per ultimo: non racconta il prato,
racconta chi lo guardava dalla finestra. È quella persona a dire «amore mio»
nella chiusa di tutte e dieci le fiabe.

L'**Epilogo** si legge alla fine e risponde all'unica domanda che i bambini
fanno sempre — *ma è vera?* — separando quello che è vero davvero (il prato, la
quercia, le lucciole, i grilli, il buio, la paura del buio) da quello che è
stato aggiunto: il nome di Nina. Poi smette di raccontare e porta chi ascolta
alla finestra, al buio, ad aspettare. La serie finisce facendo fare la cosa di
cui ha parlato per dieci sere.

Prologo ed Epilogo prendono i numeri `00` e `11` e non consumano un numero
romano: nell'indice sono «Prologo» ed «Epilogo», e le loro ancore sono
`#prologo` e `#epilogo`.

Il settimo è l'unico in cui muore qualcuno. Muore di vecchiaia, nel sonno, dopo
aver avuto quello che voleva, e la fiaba non finisce lì — ma è bene saperlo
prima di leggerlo ad alta voce a qualcuno che si è affezionato a Rocco.

## Come ci si rivolge a chi ascolta

Ogni fiaba si chiude parlando direttamente a chi ascolta. La formula è
**«amore mio»**, scelta perché non ha genere: chi ascolta può essere chiunque.

Fino al Libro quinto la formula era «piccolo mio», sostituita ovunque nei testi.

## L'audio (voce clonata)

Oltre alla pagina web, le fiabe possono essere ascoltate ad alta voce con una
**voce clonata** (la voce dell'autore). La clonazione è fatta con **ElevenLabs
Professional Voice Cloning** (piano Creator): voce `fiabe`
(`G9UYpVOtV3hbTUam453l`), italiano, accento romanesco.

Gli MP3 (`audio/11l-*.mp3`) sono versionati nel repository e compaiono come
lettori audio sulla pagina (`index.html`): ogni fiaba che ha il suo MP3 mostra un
riquadro "Ascolta" subito sotto il titolo.

Il numero dell'MP3 viene dal nome del file della fiaba, non dalla sua posizione:
`stories/07...md` cerca `audio/11l-07-*.mp3`. Per questo il Prologo ha potuto
prendere il numero `00` senza rinumerare niente.

Stato attuale: Prologo, Libro X ed Epilogo non hanno ancora l'audio, e i testi
di IV, VI, VII, VIII e IX sono cambiati dopo la revisione, quindi i loro MP3
vanno rifatti. I, II, III e V sono allineati. In una volta sola:

```bash
python3 generate_elevenlabs.py 00 04 06 07 08 09 10 11
```

Il vecchio percorso locale con **Coqui TTS (XTTS-v2)** resta in `generate.py` come
alternativa gratuita, ma è stato sostituito da ElevenLabs perché la qualità della
clonazione era giudicata insufficiente. `generate_elevenlabs.py` è lo script che
chiama l'API ElevenLabs (richiede `ELEVENLABS_API_KEY` in `.env`).

Note:

- La voce clonata parte da un campione pulito (non un vocale WhatsApp compresso):
  il campione va registrato con l'app Memo Vocali a 128 kbps o più.
- Il modello XTTS-v2 (usato in `generate.py`) è distribuito con licenza
  **non-commerciale** (CPML); ElevenLabs non ha questa limitazione sul piano a pagamento.

## La pagina

`index.html` non si modifica a mano: è generato da `build.py` a partire dai file
`.md`. Dopo aver aggiunto o corretto una fiaba:

```bash
python3 build.py
```

Lo script rilegge tutti i file `stories/<lingua>/[0-9][0-9]*.md` in ordine e ricostruisce indice,
tempi di lettura e colophon. Per aggiungere una fiaba basta creare in `stories/`
in `stories/<lingua>/` un file `NN<titolo-attaccato-minuscolo>.md` (`00` è il prologo) con la stessa
struttura degli altri:
titolo `#`, sottotitolo in corsivo, separatore `---`, paragrafi.

## Le lingue

Una cartella per lingua sotto `stories/`, e una pagina per lingua:

| Lingua | Testi | Pagina | URL |
| --- | --- | --- | --- |
| Italiano | `stories/it/` | `index.html` | `/` |
| English (UK) | `stories/en-GB/` | `en/index.html` | `/en/` |

`build.py` genera tutte le lingue in `LINGUE`, dove stanno anche le stringhe
dell'interfaccia. Una lingua senza file `.md` viene saltata con un avviso, quindi
per aggiungerne una basta creare la cartella, tradurre e aggiungere la voce.

Le ancore non cambiano con la lingua: `#prologo`, `#libro-1` … `#libro-10`,
`#epilogo` sono le stesse su tutte le pagine.

I titoli inglesi seguono la stessa regola di quelli italiani, maiuscola solo
sulla prima parola. In inglese si userebbe anche il maiuscolo su tutte le
parole: è una scelta, non una dimenticanza.

L'audio è per ora solo italiano. `build.py` cerca gli MP3 di ogni lingua in
`audio/` per l'italiano e in `audio/<lingua>/` per le altre: la pagina inglese
semplicemente non mostra nessun riquadro "Ascolta".

I percorsi nelle pagine sono assoluti (`/audio/…`, `/en/`), quindi per
guardarle in locale serve un server, non basta aprire il file:

```bash
python3 -m http.server 8000
```

## Come si usa la pagina

Chi legge lo fa quasi sempre di sera, col telefono in mano e la luce bassa, una
fiaba per volta. La pagina tiene conto di questo:

- **Barra in alto**: compare quando si è dentro una fiaba e dice a quale si è
  arrivati. Da lì si torna all'indice, si cambia la dimensione del testo e si
  cambia il tema, senza dover risalire.
- **Riprendi**: la pagina ricorda l'ultima fiaba raggiunta e la propone in cima
  alla visita dopo. Nell'indice le fiabe già passate hanno un pallino.
- **Tema e dimensione del testo** restano come li si è lasciati, anche
  riaprendo la pagina. Vengono applicati prima del disegno, così non si vede il
  tema chiaro lampeggiare al buio.
- **Un solo audio alla volta**: farne partire uno mette in pausa gli altri.

Se il browser non ha la memoria locale (navigazione privata, cookie bloccati)
la pagina funziona lo stesso: perde solo il ricordo fra una visita e l'altra.

I tempi di lettura sono calcolati a 130 parole al minuto — il passo di chi legge
ad alta voce a un bambino, non quello di chi legge da solo.

## Rigenerare l'audio dopo una correzione

`generate_elevenlabs.py` spezza ogni fiaba in blocchi e li tiene in cache come
`audio/chunk_<NN>_<i>_<firma>.mp3`. La firma è l'hash del testo del blocco: se
correggi una fiaba, i blocchi cambiati si rigenerano da soli e quelli intatti si
riusano, senza spendere caratteri ElevenLabs per niente. I blocchi vecchi
vengono ripuliti a fine run.

Prima questa cache era indicizzata solo per posizione, e una correzione al testo
veniva ignorata: il blocco vecchio veniva riusato e l'audio restava indietro
rispetto alla fiaba.

## Il sito

La pagina è online su **https://fiabe.vercel.app**.

Il progetto Vercel è collegato a questo repository: ogni push su `main`
pubblica una nuova versione. Ricordarsi quindi di eseguire `python3 build.py`
e committare anche `index.html` rigenerato, altrimenti il sito resta indietro
rispetto ai testi.

## Struttura del progetto

```text
fiabe/
├── .gitignore                              # esclude voce e artefatti di sintesi
├── README.md
├── build.py                                # genera index.html dai file .md
├── index.html                              # generato: non modificare a mano
├── generate.py                             # sintesi vocale locale (XTTS-v2, alternativa)
├── generate_elevenlabs.py                  # sintesi vocale via API ElevenLabs
├── launch.sh                               # lancia generate.py sganciato
├── stories/                                # testi sorgente, ordinati per libro
│   ├── 01lalucciolacheavevapauradelbuio.md # Libro I
│   ├── 02lalucciolaelalanternastanca.md    # Libro II
│   ├── 03lalucciolaelapiccolachenonvolevaaccendersi.md  # Libro III
│   └── 04lalucciolaeilgrillocheperselavoce.md  # Libro IV
├── ref/                                    # (ignorato) campione voce di riferimento
├── audio/                                  # (ignorato, tranne gli MP3 finali)
│   └── 11l-*.mp3                           # fiabe lette ad alta voce (versionate)
└── chunks/                                 # (ignorato) blocchi intermedi
```

I file `.opus` (il vocale di partenza), `ref/`, `audio/` e `chunks/` contengono
la voce e gli artefatti di sintesi: restano fuori dal repository perché sono dati
personali e/o rigenerabili.
