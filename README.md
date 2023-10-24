# Media Link Checker with Customizable Parameters

## Overview

This Python script scans articles on a website to identify missing media links. It's designed for flexibility, allowing users to customize key parameters through command-line arguments.

## Prerequisites

- Python 3.x
- Required Python packages: `aiohttp`, `beautifulsoup4`

  Install the necessary packages with:
  ```bash
  pip3 install aiohttp beautifulsoup4
  ```

## Usage

1. **Clone this repository**:
   ```bash
   git clone https://github.com/docvinum/wp-check-media/
   cd wp-check-media
   ```

2. **Run the script with default settings**:
   ```bash
   python3 check_media.py
   ```

3. **Run the script with custom settings**:
   ```bash
   python3 check_media.py --base-url [YOUR_BASE_URL] --start [STARTING_ARTICLE_NUMBER] --end [ENDING_ARTICLE_NUMBER] --output-file [OUTPUT_FILENAME] --id-url [TARGET_URL_ID]
   ```

## Command-Line Arguments

- `--base-url`: Specifies the base URL of the articles. (Default: `https://ives-openscience.eu/`)
- `--start`: Designates the starting article number. (Default: `1`)
- `--end`: Defines the ending article number. (Default: `40197`)
- `--output-file`: Names the output CSV file. (Default: `missing_media.csv`)
- `--id-url`: Provides the ID of the target URL to check within each article. (Default: `target-pdf-id`)

## Features

- Scans a designated range of articles to identify missing media links.
- Supports customization of key parameters through command-line arguments.
- Uses multiprocessing and asynchronous programming to enhance performance.

## Contributing

Contributions via pull requests are welcome. For major changes, please open an issue first to discuss the desired changes.

## License

Released under the [MIT License](https://choosealicense.com/licenses/mit/).
