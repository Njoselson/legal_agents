# Legal Crew

A crewai based LLM systemf for answering legal questions about rental law cases

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

```
poetry install
poetry shell
```

## Usage

Make sure you have secrets for [openai](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key) and [serper-dev](https://serper.dev/) saved in the file `/.streamlit/secrets.toml` in the app's main directory.

```
streamlit agents.py
```

## Contributing

To update the streamlit app in deployments use 
```
poetry export -f requirements.txt --output requirements.txt
```

## License

Information about the license under which your project is distributed.
