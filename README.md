# ALPHA – ERP Technology Classification

Python project for assigning ERP technology categories to text excerpts with an LLM and a ChromaDB retrieval index. It also includes an inter-rater agreement analysis using exact agreement, Jaccard distance and Krippendorff's alpha.

## Project structure

```text
ALPHA-GitHub-Projekt/
├── data/                  # Local Excel input files (not tracked by Git)
│   ├── data.xlsx
│   └── ALPHA.xlsx
├── results/               # Generated Excel outputs (not tracked by Git)
├── src/
│   ├── alpha_cal.py       # Inter-rater agreement analysis
│   ├── classify.py        # Classifies one coding unit
│   ├── classify_all.py    # Runs classification for test data
│   ├── index_setup.py     # Builds the ChromaDB index
│   └── load_data.py       # Reads and prepares Excel worksheets
├── tests/
├── models/
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python version compatible with the packages in `requirements.txt`
- Ollama installed and running
- Ollama models `nomic-embed-text` and `qwen3:14b`

Download the Ollama models:

```bash
ollama pull nomic-embed-text
ollama pull qwen3:14b
```

## Setup

Run these commands from the project root.

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Add the input workbooks

Place the two Excel files in the `data/` folder:

- `data/data.xlsx` – category system, training data and test data
- `data/ALPHA.xlsx` – ratings from Rater1 and Rater2

The workbooks are deliberately excluded from Git by `.gitignore`. Only commit them if you have checked that the research data may be shared and that the repository's access level is appropriate.

## Run the project

Run commands from the repository root.

### Build the ChromaDB index

Run once initially, and again if the training examples change:

```bash
python -m src.index_setup
```

The index is stored locally in `chroma_db/`. To rebuild it from scratch, delete that folder and run the command again.

### Classify one example

```bash
python -m src.classify
```

### Classify the test data

```bash
python -m src.classify_all
```

**Important:** `src/classify_all.py` currently uses `.head(1)`, matching the original script's one-row test setting. Remove `.head(1)` in that file to process all rows in the `test_1` worksheet.

### Calculate inter-rater agreement

```bash
python -m src.alpha_cal
```

## Outputs

Generated Excel files are saved in `results/`:

- `result.xlsx` – LLM classification output
- `ALPHA_Result_Kripp.xlsx` – inter-rater agreement details and Jaccard distances

## Notes

- The classification scripts expect the ChromaDB index to exist before classification.
- The embedding model used by ChromaDB is `nomic-embed-text`.
- The chat model is `qwen3:14b`, with temperature set to `0`.
- The maximum accepted retrieval distance is `0.230`.
- The category system contains 20 categories, including `X` for cases where no technology is apparent.
