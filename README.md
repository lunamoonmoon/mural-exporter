# Mural Exporter

This is a tool for exporting Mural boards as PDFs.

## Features

- Retrieves a list of all Mural boards in json format by a workspace ID
- Saves the list of Mural boards id, name, and export id to a CSV file
- Exports Mural boards as high res PDFs

## Requirements

- python3

## Installation

1. Clone the repository
2. Install the required Python packages:

```bash
python3 -m venv venv
```

3. Activate the virtual environment:

```bash
source venv/bin/activate
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Create a .env file using the .env.template file and enter your mural access token and workspace id

1. To export a Mural board, run the following command:

```bash
python3 export_mural.py
```

2. Then allow time for all the export links to be created by the mural server

```bash
python3 pdf_download.py
```

## License

This project is licensed under the MIT License.
