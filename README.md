# ReSequel [arXiv:2606.20853]
### Robust LLM-assisted Query Rewriting and Optimization using Templatization and Sampling

- **Paper:** [Robust LLM-assisted Query Rewriting and Optimization using Templatization and Sampling](https://arxiv.org/pdf/2606.20853)
- **Source:** [CoDS-GCS/ReSequel](https://github.com/CoDS-GCS/ReSequel)

This workspace contains the Python implementation of the LLM-assisted query rewriter, which templatizes workloads, samples candidate rewrites, and verifies them against the database catalog.

---

## Command Line Usage

Use `uv` to automatically manage the virtual environment and run the entry-point script. All commands are executed from `src/main/python`, and `--dataset-name` is always required.

### Basic CLI Commands

#### 1. Prepare the Database Catalog
Builds the database catalog used for verification:
```bash
uv run python main.py --dataset-name imdb --prepare-data-catalog --catalog-path ./catalog.json
```

#### 2. Templatize & Reconstruct a Workload
Extract templates from a workload, then reconstruct rewritten candidates per query:
```bash
uv run python main.py --dataset-name imdb --templatization --workload-path /path/to/workload.sql --workload-output /tmp/
uv run python main.py --dataset-name imdb --reconstruct --workload-path /path/to/workload.sql \
  --template-path /tmp/templates.json --template-rewrite-path /tmp/rewrites.json --workload-output /tmp/
```

#### 3. Verify Rewrites & Custom Parameters
Verify LLM-generated rewrites (`--judge`), optionally downsampling the database, specifying the LLM model and DBMS:
```bash
uv run python main.py --dataset-name imdb --judge --catalog-path ./catalog.json \
  --template-path /tmp/templates.json --template-rewrite-path /tmp/rewrites.json \
  --llm-model gpt-4o --dbms postgresql
```

---

## CLI Options

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--dataset-name` | `str` | `None` | **Required.** Name of the dataset to load configuration/catalog for. |
| `--prepare-data-catalog` | `flag` | `False` | Build the database data catalog. |
| `--implement` | `flag` | `False` | Implement database functions via the LLM. |
| `--templatization` | `flag` | `False` | Extract query templates from the workload. |
| `--query-list` | `flag` | `False` | Generate a list of candidate rewritten queries. |
| `--reconstruct` | `flag` | `False` | Reconstruct workload queries from template rewrites. |
| `--judge` | `flag` | `False` | Verify LLM-generated queries. |
| `--downsampling` | `flag` | `False` | Downsample the database for verification. |
| `--db-schema` | `str` | `schema.json` | Path to the database schema file. |
| `--list-size` | `int` | `10` | Number of candidate queries to generate per template. |
| `--llm-model` | `str` | `None` | LLM model to use (e.g., GPT, Gemini, Groq, LLaMa). |
| `--catalog-path` | `str` | `None` | Path to read/write the database catalog. |
| `--system-log` | `str` | `/tmp/cat-system-log.dat` | Path to the system log file. |
| `--output-path` | `str` | `/tmp/results.csv` | Path to write results output. |
| `--result-log-path` | `str` | `/tmp/results-log.csv` | Path to the result log file. |
| `--workload-path` | `str` | `None` | Path to the input SQL workload file. |
| `--template-path` | `str` | `None` | Path to extracted query templates. |
| `--template-rewrite-path` | `str` | `None` | Path to template rewrites. |
| `--query-ID` | `str` | `None` | Specific query ID to process. |
| `--workload-output` | `str` | `/tmp/` | Directory to write generated workload files. |
| `--dbms` | `str` | `postgresql` | Target DBMS. |
| `--sample-fraction` | `int` | `1` | Sampling fraction for database downsampling. |
