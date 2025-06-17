# Spavkaru Person Scraper

A unified web application for searching person information across multiple countries using Spavkaru's services. The application combines a FastAPI backend with a React frontend to provide a modern and user-friendly interface for searching person details.

## Features

- Search person information across multiple countries:
  - Kazakhstan
  - Latvia
  - Moldova
  - Russia
  - Ukraine
  - Belarus
- Modern web interface with real-time search results
- Detailed person information display including:
  - Personal details (name, age, gender, etc.)
  - Contact information
  - Address history
  - Additional information
- Responsive design that works on both desktop and mobile devices

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn package manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd spavkaru-person-scraper
```

2. Install backend dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the backend server:
```bash
# From the root directory
python backend.py
```
The backend server will start on http://localhost:8000

2. Start the frontend development server:
```bash
# From the frontend directory
cd frontend
npm start
```
The frontend application will start on http://localhost:3000

## How to Search

1. Open your web browser and navigate to http://localhost:3000

2. Enter the search parameters:
   - **First Name**: Enter the person's first name
   - **Last Name**: Enter the person's last name
   - **Country**: Select the country to search in
   - **City**: Enter the city name (optional)
   - **Age**: Enter the person's age (optional)

3. Click the "Search" button to start the search

4. The results will be displayed in a table below the search form, showing:
   - Person's full name
   - Age
   - Gender
   - Address
   - Additional information

## API Endpoints

The backend provides the following API endpoint:

- `POST /api/search`
  - Request body:
    ```json
    {
      "first_name": "string",
      "last_name": "string",
      "country": "string",
      "city": "string",
      "age": "string"
    }
    ```
  - Response:
    ```json
    {
      "results": [
        {
          "name": "string",
          "age": "string",
          "gender": "string",
          "address": "string",
          "additional_info": "string"
        }
      ]
    }
    ```

## Project Structure

```
spavkaru-person-scraper/
├── backend.py              # FastAPI backend server
├── requirements.txt        # Python dependencies
├── scrapers/              # Country-specific scrapers
│   ├── kazakhstan.py
│   ├── latvia.py
│   ├── moldova.py
│   ├── russian.py
│   ├── ukraine.py
│   └── belarus.py
└── frontend/              # React frontend application
    ├── src/
    │   ├── App.tsx        # Main application component
    │   └── App.css        # Application styles
    └── package.json       # Frontend dependencies
```

## Notes

- The application uses Spavkaru's services to search for person information
- Search results may vary depending on the country and available data
- Some countries may require additional parameters for more accurate results
- The application respects rate limits and implements proper error handling

## Contributing

Feel free to submit issues and enhancement requests! 