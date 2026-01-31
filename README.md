# Wiki-QA CLI

Intelligent Document Q&A System with hybrid vector + graph search.

## Phase 1: Foundation (Complete)

### Completed Features

- Project structure with Python packages
- Configuration management (YAML + environment variables)
- CLI skeleton with Rich interface
- Unit tests for configuration and CLI

### Project Structure

```
wiki-qa-cli/
├── cli/
│   ├── __init__.py
│   └── app.py              # Main CLI application
├── config/
│   ├── __init__.py
│   ├── settings.py         # Configuration models
│   └── settings.yaml       # Default configuration
├── pipeline/
│   ├── __init__.py
├── storage/
│   ├── __init__.py
├── query/
│   ├── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   └── test_cli.py
├── pyproject.toml
├── requirements.txt
└── .gitignore
```

### Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run CLI
python -m cli.app
```

### Next Steps

Phase 2: Data Ingestion
- Wikipedia streaming
- Document chunking
- State persistence

## Quick Links

- [Phase Plan](WIKI_QA_PHASE_PLAN.md)
- [GitHub Repository](https://github.com/akgitrepos/wiki-qa-cli)
