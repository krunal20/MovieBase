# MovieBase

MovieBase is a web application that allows users to search for movies from a database of the top 1000 movies on IMDb. Users can filter search results by genre, release year, IMDb rating, and certificate. The application also provides recommendations based on user preferences.

## Features

- **Search Movies**: Search for movies by title.
- **Filter Results**: Filter search results by genre, release year, IMDb rating, and certificate.
- **Sort Results**: Sort search results by rating.
- **View Details**: View detailed information about each movie, including the poster, genre, year, and certificate.

## Setup

### Prerequisites

- Node.js (v14 or higher)
- Python (v3.6 or higher)
- Elasticsearch (v7.10 or higher)

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/krunal20/MovieBase.git
    cd MovieBase
    ```

2. **Set up the backend**:
    - Create a virtual environment and activate it:
        ```sh
        python -m venv venv
        source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
        ```
    - Install the required Python packages:
        ```sh
        pip install -r requirements.txt
        ```

3. **Set up the frontend**:
    - Navigate to the frontend directory:
        ```sh
        cd frontend
        ```
    - Install the required Node.js packages:
        ```sh
        npm install
        ```

4. **Configure Elasticsearch**:
    - Ensure Elasticsearch is running and accessible.
    - Update the `config.py` file with your Elasticsearch configuration.

5. **Populate Elasticsearch with data**:
    - Run the data population script:
        ```sh
        python populate_data.py
        ```

## Running the Project

1. **Start the backend server**:
    ```sh
    python run.py
    ```

2. **Start the frontend development server**:
    ```sh
    cd frontend
    npm start
    ```

3. **Access the application**:
    - Open your web browser and navigate to `http://localhost:3000`.

## Project Structure

- **backend**: Flask application and Elasticsearch setup scripts.
- **frontend**: React application.
- **data**: CSV file with IMDB top 1000 movies data.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.