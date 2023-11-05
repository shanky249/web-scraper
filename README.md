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
git clone https://github.com/shanky249/web-scraper.git
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


## Viewing Downloaded Content Locally

After running the web scraper, you can view the downloaded content locally. By default, the starting page for your scraped website is located in the output directory specified in `config.py`. The main HTML page that serves as the starting point for your locally saved website is typically named `index.html`.

Follow these steps to view the downloaded content:

1. Open a web browser on your local machine.

2. Navigate to the file path of the `index.html` file in your browser. This can typically be done by opening the browser and then dragging and dropping the `index.html` file onto the browser's window.

   Alternatively, you can use the browser's "Open File" option to select the `index.html` file from the output directory.

3. The `index.html` file will serve as the starting point for your locally saved website. You can navigate through the website by clicking links and exploring the content, just like you would with any other website.

4. If the website contains images or other assets, they will be loaded from the local directory, providing you with a complete offline browsing experience.

**Note**: The locally downloaded content does not include external CSS stylesheets. Web pages often rely on external CSS stylesheets for their layout and design. Since these stylesheets are typically hosted on external servers, they are not downloaded as part of the scraping process.

As a result, the appearance of the locally saved website may not precisely match the original website. While the website's structure and content will be preserved, the styling may be different or, in some cases, missing.



## Contributing
If you want to contribute to this project, please fork the repository, create a new branch, and make your changes. Once done, submit a pull request.
