# Mural Exporter

This is a tool for exporting Mural boards as PDFs.

## Features

- Retrieves a list of all Mural boards in json format by a workspace ID
- Saves the list of Mural boards to a JSON file
- Exports Mural boards as PDFs
- Batch exports multiple boards

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

To export a Mural board, run the following command:

```bash
python3 export_mural.py
```

## License

This project is licensed under the MIT License.