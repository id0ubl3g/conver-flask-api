<div align="center">
    <img src=".github/document-logo.png" alt="Document Logo" width="130">
    <h1><b>Conver Flask API</b></h1>
    <p>Flask API for document conversion </p>
    <p>
        <img src="https://img.shields.io/github/last-commit/id0ubl3g/conver-flask-api?style=flat&logo=git&logoColor=white&color=0080ff" alt="Last Commit">
        <img src="https://img.shields.io/github/languages/top/id0ubl3g/conver-flask-api?style=flat&color=0080ff" alt="Top Language">
        <img src="https://img.shields.io/github/languages/count/id0ubl3g/conver-flask-api?style=flat&color=0080ff" alt="Languages Count">
    </p>
</div>

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)  
    - [Steps to Set Up `Docker`](#steps-to-set-up-docker)  
- [Build and Run Container](#build-and-run-container)
- [API Documentation](#api-documentation)
    - [API Endpoints](#api-endpoints)
        - [1. Convert File Endpoint](#1-convert-file-endpoint)
            - [Request Body](#request-body)
                - [Example Request](#example-request)
            - [Successful Response](#successful-response)
            - [Error Responses](#error-responses)
    - [Example Use Case](#example-use-case)
        - [Frontend Integration](#frontend-integration)
- [Acknowledgments](#acknowledgments)


## Overview
The Conver Flask API is a web application developed with Flask, designed to facilitate the conversion of documents into various formats. It provides a practical solution for users needing efficient file conversion.

## Project Structure

```plaintext
└── conver-flask-api/
    ├── .github/
    │   ├── document-logo.png
    ├── src/
    │   ├── api/
    │   │   └── app.py
    │   ├── modules/
    │   │   └── conver.py
    │   ├── utils/
    │   │   └── system_utils.py
    ├── config/
    │   ├── base_converter.py
    │   └── path_config.py
    ├── docs/
    │   └── flasgger.py
    ├── requirements.txt
    ├── .dockerignore
    ├── .gitignore
    ├── Dockerfile
    ├── README.md
    └── run.py
```

## Prerequisites

To use Docker for containerizing the Conver Flask API, follow these steps to install Docker on your system.

### Steps to Set Up `Docker`

Update your system and install Docker with the following commands:

```sh
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y
```

Add your user to the Docker group:

```sh
sudo usermod -aG docker $USER
```

Run the test container to confirm Docker is working:

```sh
docker run hello-world
```

For additional information on how to install Docker on your system, visit the official Docker documentation: [Download Docker](https://docs.docker.com/get-docker/)

## Build and Run Container

```sh
docker build -t conver-flask-api .
docker run -p 5000:5000 conver-flask-api
```

## API Documentation

The Conver Flask API includes interactive documentation powered by Flasgger. You can explore each endpoint, view parameter details, and test API requests directly from the browser.

Interactive API Documentation: [http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/)

### API Endpoints

#### 1. Convert File Endpoint

- **URL**: `/converter`
- **Method**: `POST`
- **Description**: Converts the uploaded document to the specified format.


##### Request Body:

- **Content-Type**: `multipart/form-data`
- **Form Fields**:
    - `file`: The document file to be converted (required).
      - Type: `File`
      - **Accepted Input Formats**: `doc`, `docx`, `odt`, `txt`, `rtf` (not accepting `pdf`)
    - `extension`: The desired output format (required).
      - Type: `String` 
      - **Supported Output Formats**: `pdf`, `doc`, `docx`, `odt`, `txt`, `rtf`

###### Example Request

```sh
curl -X POST "http://127.0.0.1:5000/converter" \
-H "accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "file=@testfile.txt;type=text/plain" \
-F "extension=pdf"
```

##### Successful Response

- **Successful Response**:
    - **Status Code**: `200 OK`
    - **Content-Type**: `application/octet-stream`
    - **Description**: `Returns the converted file as a downloadable attachment.`
    - **Headers**:
    ```json
    {
        "..."
        "content-disposition": "attachment; filename=\"Conver - filename.pdf\""
        "..."
    }
    ```

##### Error Responses

- **Bad Request**:
    - **Status Code**: `400 Bad Request`
    - **Content-Type**: `application/json`
    - **Description**: `Returned when an unsupported file extension is provided.`
    - **Example**:
    ```json
    {
        "error": "Unsupported file extension: octet-stream"
    }
    ```
- **413 Payload Too Large**: 
    - **Status Code**: `413`
    - **Content-Type**:`application/json`
    - **Description**: `Returned when the uploaded file size exceeds 50 MB.`
    - **Example**:
    ```json
    {
        "error": "File size exceeds the maximum limit of 50 MB."
    }
    ```

- **500 Internal Server Error**:
    - **Status Code**: `500`
    - **Content-Type**:`application/json`
    - **Description**: `Returned when an internal error occurs during conversion.`
    - **Example**:
    ```json
    {
        "error": "Conversion failed, output file not found"
    }
    ```

### Example Use Case

#### Frontend Integration

Integrating the Conver Flask API can be done easily in a frontend application. Here’s a simple example using JavaScript and fetch to send a file to the API.

```js
const convertRequest = async (formData: FormData) => {
    try {
        const response = await fetch('http://127.0.0.1:5000/converter', {
            method: 'POST',
            body: formData,
        })

        const blob = await response.blob(); 
        const downloadUrl = URL.createObjectURL(blob);

        return downloadUrl;

    } catch (e) {
        return "Conversion failed!";
    }
}
```

## Acknowledgments

This project was developed in collaboration with [Francine Cruz](https://github.com/Francine02), who contributed to the frontend part. Her collaboration was essential in integrating the API with a user-friendly interface, providing an optimized user experience.

For a live demonstration of the API in action, visit [Conver](https://conver-taupe.vercel.app/), where the API has been fully integrated into an interactive platform.
