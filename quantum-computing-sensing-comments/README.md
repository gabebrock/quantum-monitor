# Quantum Computing Sensing Comments

This project retrieves comments related to "quantum computing sensing" from the regulations.gov API and exports the data to CSV files.

## Project Structure

- `src/main.py`: Entry point of the application.
- `src/api/regulations_api.py`: Contains functions to interact with the regulations.gov API.
- `src/export/csv_exporter.py`: Provides functionality to export data to CSV files.
- `src/utils/env_loader.py`: Responsible for loading environment variables from the `.env.reg` file.
- `.env.reg`: Contains the API key required for authentication with the regulations.gov API.
- `requirements.txt`: Lists the dependencies required for the project.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd quantum-computing-sensing-comments
   ```

2. Create a `.env.reg` file in the root directory and add your API key:
   ```
   API_KEY=your_api_key_here
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application using the following command:
```
python src/main.py
```

This will retrieve comments containing "quantum computing sensing", export the data to a CSV file, and fetch detailed information for each comment ID to export to another CSV file.

## License

This project is licensed under the MIT License.