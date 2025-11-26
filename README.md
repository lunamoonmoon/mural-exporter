# Mural Exporter

This is a tool for exporting Mural boards as PDFs.

## Features

- Retrieves a list of all Mural boards in json format by a workspace ID
- Saves the list of Mural boards id, name, and export id to a CSV file
- Exports Mural boards as high res PDFs

## Requirements

- python3

## How to get the Access Token and Workspace Id

1. Login to Mural
2. Under progile go to my apps and click new app
3. For redirect URL use https://oauth.pstmn.io/v1/callback
4. Mural provides a client id and secret
5. Your workspace ID is in the center of your URL when you navigate to one of your mural boards, save to .env
6. In postman create a get request to https://app.mural.co/api/public/v1/authorization/oauth2/token using your mural client id and secret. For scope use murals:read murals:write rooms:read rooms:write
7. Send your request in postman to get your mural access token
8. In the .env file paste your workspace id and mural access token

If you have trouble check the helpful mural API documents
[Mural API Docs Testing with Postman](https://developers.mural.co/public/docs/testing-with-postman)

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
Get your mural access token through an application like postman and 
[follow these steps](https://developers.mural.co/public/docs/testing-with-postman)

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
