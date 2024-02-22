
# Libgen Scraper

Libgen Scraper is a Django web application for scraping book details from the Library Genesis (Libgen) website and exporting them in various formats.

## Features

- **Scraping**: Extracts book details such as title, authors, publisher, publication year, language, pages, and more from Libgen.
- **Exporting**: Exports scraped book details in CSV, JSON, or XLS format.
- **File Download**: Downloads book images, HTML descriptions, and PDF files (if available) for each scraped book.
- **Search**: Allows users to search for books on Libgen based on keywords and page range.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/libgen-scraper.git
```
### Navigate to the project directory:
```bash
cd libgen-scraper
```
###Install the required dependencies:
```bash
pip install -r requirements.txt
```
### Apply database migrations:
```bash
python manage.py migrate
```
### Start the Django development server:
```bash
python manage.py runserver
```
##### Access the application in your web browser at http://127.0.0.1:8000/.
## Usage
Navigate to the home page of the application.
Fill out the scraping form with the desired keyword, page range, and export format.
Click the "Scrape" button to initiate the scraping process.
Once the scraping is complete, the exported files will be available for download.
Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.
