# Fiabe

Fiabe della buonanotte su **Nina**, la lucciola del prato ai piedi della collina.

## I libri

| | Titolo | Lettura ad alta voce |
|---|---|---|
| I | La Lucciola che Aveva Paura del Buio | 3 min |
| II | La Lucciola e la Lanterna Stanca | 5 min |
| III | La Lucciola e la Piccola che Non Voleva Accendersi | 6 min |

Vanno letti in ordine: il primo accende la luce, il secondo la spegne, il terzo
scopre che la luce di un altro non si può accendere.

## L'audio (voce clonata)

Oltre alla pagina web, le tre fiabe possono essere lette ad alta voce con una
**voce clonata**: `generate.py` usa **Coqui TTS (XTTS-v2)** per sintetizzare le
fiabe in italiano a partire da un breve campione della voce da clonare.

```bash
# una tantum: venv e dipendenze
python3 -m venv ~/tts-venv
~/tts-venv/bin/pip install coqui-tts "transformers>=4.40,<5"
~/tts-venv/bin/pip install torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cpu

# mettere il campione della voce in ref/reference.wav (mono, 22050 Hz, 6-30 s)
# poi generare i tre MP3:
COQUI_TOS_AGREED=1 ~/tts-venv/bin/python generate.py
```

`generate.py` legge i file `0*.md`, pulisce il testo (toglie emoji e corsivi),
lo divide in blocchi e sintetizza ogni blocco con la voce di `ref/reference.wav`;
i blocchi vengono poi concatenati nei tre MP3 in `audio/`, con una copia sul
Desktop Windows (`fiabe-audio`). `launch.sh` fa lo stesso ma in modo sganciato
dalla sessione, per le generazioni lunghe su CPU.

Note:

- `transformers` va tenuto `<5` perché XTTS-v2 (coqui-tts 0.27) è incompatibile
  con la serie 5.x; `torch` va tenuto a 2.8 (niente `torchcodec`, che su CPU
  dà problemi di librerie native).
- Il modello XTTS-v2 è distribuito con licenza **non-commerciale** (CPML):
  va bene per l'uso personale; per un uso commerciale serve un'altra soluzione.

## La pagina

`index.html` non si modifica a mano: è generato da `build.py` a partire dai file
`.md`. Dopo aver aggiunto o corretto una fiaba:

```bash
python3 build.py
```

Lo script rilegge tutti i file `0*.md` in ordine e ricostruisce indice, tempi di
lettura e colophon. Per aggiungere il Libro quarto basta creare
`04<titolo-attaccato-minuscolo>.md` con la stessa struttura degli altri:
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
├── generate.py                             # sintesi vocale con voce clonata
├── launch.sh                               # lancia generate.py sganciato
├── 01lalucciolacheavevapauradelbuio.md     # Libro I
├── 02lalucciolaelalanternastanca.md        # Libro II
├── 03lalucciolaelapiccolachenonvolevaaccendersi.md  # Libro III
├── ref/                                    # (ignorato) campione voce di riferimento
├── audio/                                  # (ignorato) gli MP3 generati
└── chunks/                                 # (ignorato) blocchi intermedi
```

I file `.opus` (il vocale di partenza), `ref/`, `audio/` e `chunks/` contengono
la voce e gli artefatti di sintesi: restano fuori dal repository perché sono dati
personali e/o rigenerabili.
