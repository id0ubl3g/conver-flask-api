# Conver Flask API

## Overview
The Conver Flask API is a web application developed with Flask, designed to facilitate the conversion of documents into various formats. It provides a practical solution for users needing efficient file conversion.

## Docker Prerequisites

### Build and Run the Docker Container

```sh
docker build -t conver-flask-api .
docker run -p 5000:5000 conver-flask-api
```
## API Documentation

The Conver Flask API includes interactive documentation powered by Flasgger. You can explore each endpoint, view parameter details, and test API requests directly from the browser.

**Interactive API Documentation**: [http://127.0.0.1:5000/apidocs](127.0.0.1:5000/apidocs)

## API Endpoints

### 1. Home Endpoint

- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns the home page of the API.

### 2. Convert File Endpoint

- **URL**: `/converter`
- **Method**: `POST`
- **Description**: Converts the uploaded document to the specified format.


#### Request Body:

- **Content-Type**: `multipart/form-data`
- **Form Fields**:
    - `file`: The document file to be converted (required).
      - Type: `File`
      - **Accepted Input Formats**: `doc`, `docx`, `odt`, `txt`, `rtf` (not accepting `pdf`)
    - `extension`: The desired output format (required).
      - Type: `String` 
      - **Supported Output Formats**: `pdf`, `doc`, `docx`, `odt`, `txt`, `rtf`

### Successful Response

- **Successful Response**:
    - **Status Code**: `200 OK`
    - **Content-Type**: `application/octet-stream`
    - **Description**: `Returns the converted file as a downloadable attachment.`
    - **Headers**:
    ```json
    {
        "Content-Disposition": "attachment; filename=\"Conver - filename.pdf\""
    }
    ```

### Error Responses

- **Bad Request**:
    - **Status Code**: `400 Bad Request`
    - **Content-Type**: `application/json`
    - **Description**: `Returned when an unsupported file extension is provided.`
    - **Example**:
    ```json
    {
        "error": "Unsupported file extension: xlsx"
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

### Example Request

```sh
curl -X POST "http://127.0.0.1:5000/converter" \
-H "accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "file=@testfile.txt;type=text/plain" \
-F "extension=pdf"
```

## Example Use Case

### Frontend Integration

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

#### Acknowledgments

This project was developed in collaboration with [@Francine02](https://github.com/Francine02), who contributed to the frontend part. Her collaboration was essential in integrating the API with a user-friendly interface, providing an optimized user experience.

For a live demonstration of the API in action, visit [Conver](https://conver-taupe.vercel.app/), where the API has been fully integrated into an interactive platform.
