# Web Scraper

## Description
Web Scraper is a Python application for recursively scraping web pages from a target website and downloading their content, including HTML pages and images, while preserving the original website's file structure. The application also displays progress information in the console using a progress bar.

## Design and Features
- The code is organized into separate files (following `Separation of Concerns` design principle):
  - `web_scraper.py`: Contains the main logic for web scraping.
  - `utils.py`: Contains common utility functions.
  - `config.py`: Centralizes configuration constants.
  - `main.py`: Serves as the entry point to run the application.
- The code uses the `requests`, `BeautifulSoup`, and `tqdm` libraries for web scraping and progress display.
- Common operations are modularized in `utils.py` to promote code reusability.
- The application ensures that relative links within downloaded pages are converted to absolute links for local navigation.

## Installation and Usage

1. Clone this repository:
```
git clone https://github.com/yourusername/web-scraper.git
```

2. Navigate to the project directory:
```
cd web-scraper
```

3. Create a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate # On Windows, use: venv\Scripts\activate
```

4. Install the required packages:
```
pip install -r requirements.txt
```

5. Update the `BASE_URL` and `OUTPUT_DIR` in the `config.py` file as needed.

6. Run the application using the following command:
```
python main.py
```

7. The web scraper will start working and save scraped content in the specified output directory.

## Contributing
If you want to contribute to this project, please fork the repository, create a new branch, and make your changes. Once done, submit a pull request.
