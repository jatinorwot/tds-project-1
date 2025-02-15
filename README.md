# tds-project-1


## Setup

### Prerequisites

- Python 3.9
- Docker

### Installation

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add your environment variables:

    ```sh
    touch .env
    echo "AIPROXY_TOKEN=your_token_here" >> .env
    ```

### Running the Application

1. Start the FastAPI server:

    ```sh
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```

2. The application will be available at `http://localhost:8000`.

### Using Docker

1. Build the Docker image:

    ```sh
    docker build -t llm-automation-agent .
    ```

2. Run the Docker container:

    ```sh
    docker run -p 8000:8000 llm-automation-agent
    ```

## API Endpoints

### `/run`

- **Method:** `POST`
- **Description:** Placeholder for task execution.

### `/read`

- **Method:** `GET`
- **Description:** Reads the content of a specified file.
- **Query Parameters:**
  - `path` (string): File path to read.

## Tasks

### Task A

- **A1:** Run a Python script from a given URL, passing an email as the argument.
- **A2:** Format a markdown file using a specified version of Prettier.
- **A3:** Count the number of occurrences of a specific weekday in a date file.
- **A4:** Sort a JSON contacts file and save the sorted version to a target file.
- **A5:** Retrieve the most recent log files from a directory and save their content to an output file.
- **A6:** Generate an index of documents from a directory and save it as a JSON file.
- **A7:** Extract the sender's email address from a text file and save it to an output file.
- **A8:** Generate an image representation of credit card details from a text file.
- **A9:** Find similar comments from a text file and save them to an output file.
- **A10:** Identify high-value (gold) ticket sales from a database and save them to a text file.

### Task B

- **B3:** Download content from a URL and save it to the specified path.
- **B4:** Clone a Git repository and make a commit.
- **B5:** Execute a SQL query on a specified database file and save the result to an output file.
- **B6:** Fetch content from a URL and save it to the specified output file.
- **B7:** Process an image by optionally resizing it and saving the result to an output path.
- **B8:** Transcribe audio using OpenAI's Whisper model.
- **B9:** Convert a Markdown file to another format and save the result to the specified output path.
- **B12:** Check if a filepath starts with `/data`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
