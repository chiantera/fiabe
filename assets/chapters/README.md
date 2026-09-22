# Illustrazioni dei capitoli

26 disegni SVG originali: 12 per Nina e 14 per Tilde, inclusi prologhi ed
epiloghi. Forme piatte, colori e proporzioni riprendono `assets/meadow.svg`
e `assets/burrow.svg`. Le scene seguono il testo italiano, comprese le
revisioni degli occhiali di Tilde e della bambina della collina.

Ogni file `nina/NN.svg` o `tilde/NN.svg` corrisponde al prefisso numerico del
file della storia. `build.py` lo inserisce dopo la testata del capitolo, in
entrambe le lingue, solo se il file esiste. I disegni hanno proporzioni 800 ×
560, si adattano alla larghezza della pagina e vengono caricati quando servono.

Le composizioni e le forme condivise sono in `scripts/chapter_art.py`.
Per rigenerare un gruppo specifico:

```sh
python scripts/chapter_art.py nina:00 nina:01 nina:02
python build.py
```

Le chiavi disponibili vanno da `nina:00` a `nina:11` e da `tilde:00` a
`tilde:13`. Ogni SVG contiene un titolo descrittivo della scena. Nelle pagine
le immagini sono decorative (`alt=""`): il testo completo della storia è
già presente e resta accessibile senza descrizioni duplicate.
