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
