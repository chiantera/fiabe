# Fiabe

Fiabe della buonanotte su **Nina**, la lucciola del prato ai piedi della collina.

## I libri

| | Titolo | Lettura ad alta voce |
|---|---|---|
| I | La Lucciola che Aveva Paura del Buio | 3 min |
| II | La Lucciola e la Lanterna Stanca | 5 min |
| III | La Lucciola e la Piccola che Non Voleva Accendersi | 6 min |
| IV | La Lucciola e il Grillo che Perse la Voce | 9 min |

Vanno letti in ordine: il primo accende la luce, il secondo la spegne, il terzo
scopre che la luce di un altro non si può accendere, il quarto insegna che ciò
che si è donato resta in chi ci è stato vicino.

## L'audio (voce clonata)

Oltre alla pagina web, le fiabe possono essere ascoltate ad alta voce con una
**voce clonata** (la voce dell'autore). La clonazione è fatta con **ElevenLabs
Professional Voice Cloning** (piano Creator): voce `fausto bedtime stories`,
italiano, accento romanesco.

Gli MP3 finali disponibili (`audio/11l-*.mp3`) sono versionati nel repository e
compaiono come lettori audio sulla pagina (`index.html`): ogni fiaba che ha il
suo MP3 ha un riquadro "Ascolta" subito sotto il titolo.

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

Lo script rilegge tutti i file `stories/0*.md` in ordine e ricostruisce indice,
tempi di lettura e colophon. Per aggiungere una fiaba basta creare in `stories/`
un file `NN<titolo-attaccato-minuscolo>.md` con la stessa struttura degli altri:
titolo `#`, sottotitolo in corsivo, separatore `---`, paragrafi.

I tempi di lettura sono calcolati a 130 parole al minuto — il passo di chi legge
ad alta voce a un bambino, non quello di chi legge da solo.

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
