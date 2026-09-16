# Genome Editing

Interactive, single-file web tool for simulating genome edits. Pick a genome, import FASTA,
configure editing rules, find CRISPR guides, apply an edit, and compare protein translation
before vs. after.

No build step, no backend, no dependencies. Just open the page in a browser.

## Open the tool

- **Local:** open `index.html` in a browser (double-click works, fully offline except NCBI fetch).
- **GitHub Pages:** this repo publishes from the root, so `index.html` is the entry point.
  `index.html` is a copy of `frontend/genome_editing.html` — edit only the frontend file,
  then sync (see below).

## Typical workflow

1. **Select a genome** (left panel, section a)
   - Dropdown: Human BRCA1 / TP53 fragments, Mouse Trp53 / Brca1 fragments,
     E. coli lacZ fragment, Python sample (48 bp), or Random DNA.
   - Click **Load selected**.
   - Or fetch a real record from NCBI: enter an accession (e.g. `NM_007294.4`) and
     click **Fetch** (requires internet; uses NCBI E-utilities `efetch`, `db=nucleotide`,
     `rettype=fasta`).
2. **Import FASTA** (section b)
   - **File** tab: upload a `.fa` / `.fasta` / `.fna` / `.txt` file.
   - **Paste** tab: paste `>header` + sequence lines, click **Parse pasted FASTA**.
   - Multi-record FASTAs are supported; switch records via the records dropdown.
3. **Configure rules** (section c)
   - **PAM / system:** SpCas9 NGG (default), NAG, SaCas9 NNGRRT, Cas12a TTTV,
     SpCas9-VQR NGA, or a custom PAM regex.
   - **Guide length** (default 20) and **cut offset upstream of PAM** (default 3,
     i.e. cut = start + 17 as in the Python version).
   - **Strand scan:** both strands (default), forward only (matches the Python script),
     or reverse only. Reverse hits are reverse-complemented and mapped to forward coords.
   - **Edit type + parameters** (see table below).
   - Click **Rescan guides** after changing PAM / guide / strand settings.
4. **Pick a guide** — click a row in the guides table. gRNA is shown 5′→3′ with U.
   The sequence view highlights the selected guide, PAM, and cut site (`|`).
5. **Apply the edit** — click **Apply edit at selected guide** (or **Reset** to clear).
   - Stats show WT → edited length, Δ bp, frameshift vs. in-frame, likely-knockout flag.
   - Alignment window shows WT vs. edited sequence around the cut.
   - Full edited sequence is shown below.
6. **Compare translation** (section e)
   - Choose Frame 1 / 2 / 3 or **Longest ORF (ATG→stop)** auto mode.
   - WT vs. edited protein boxes use alignment-based highlighting (Needleman-Wunsch
     global alignment, so frameshifts don't produce false mismatches):
     - normal text = identical residue
     - **yellow** = substitution
     - **grey** = gap / indel-shifted position
     - **red `*`** = stop codon
   - The note line reports % identity and flags premature stops; the stats row shows
     WT / edited lengths and Δ aa.

## Edit types

| Type | What it does | Parameters |
|---|---|---|
| NHEJ knockout — deletion | Deletes N bp at the cut (ports `simulate_nhej_knockout()`) | Deletion length |
| NHEJ — insertion | Inserts sequence at the cut | Inserted sequence |
| Substitution | Replaces N bp at the cut | Length + replacement |
| HDR template | Replaces ± flank bp around the cut with a donor | Donor template + flank |
| Base edit CBE | C→T within the guide window (+ strand; G→A on −) | Window from–to (1-indexed, default 4–8) |
| Base edit ABE | A→G within the guide window (+ strand; T→C on −) | Window from–to |

View options: **window ± bp around cut** and **wrap every N bases** control the sequence display.
Long sequences show a window around the cut; the edited-sequence box caps at 4000 bp display.

## Project structure

```
index.html                  # GitHub Pages entry point (copy of frontend file — do not edit directly)
frontend/genome_editing.html # Source of truth for the app
backend/gene_editing.py      # Original Python logic (guide scan + NHEJ knockout)
scripts/sync.sh              # Keeps index.html and frontend/genome_editing.html in sync
```

## Syncing after edits

```sh
sh scripts/sync.sh           # frontend -> index.html (normal flow)
sh scripts/sync.sh --reverse # index.html -> frontend (if you edited the root copy)
sh scripts/sync.sh --check   # exit 1 if the two files differ (useful in CI)
```

## Notes & limitations

- Demo "genomes" are short gene fragments, not full genomes (a full human genome is ~3 GB
  and can't ship in a static page). Use NCBI fetch or FASTA import for real sequences.
- Simulations are educational models (PAM match, fixed cut offset, simple repair outcomes),
  not predictions of real editing efficiency. Not for clinical use.
