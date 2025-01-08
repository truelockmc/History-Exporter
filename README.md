# History Exporter

History Exporter is a Python tool that allows you to export browsing history from popular browsers like **Chrome**, **Firefox**, **Edge**, and **Opera**. The exported history is saved in a CSV format containing URLs, titles, and the last visit time.

## Supported Browsers

- **Google Chrome**
- **Mozilla Firefox**
- **Microsoft Edge**
- **Opera**

## Features

- Export browsing history to CSV format.
- Supports multiple operating systems: **Windows**, **macOS**, and **Linux**.
- Handles browser-specific SQLite databases.
- Easy to use, command-line interface (CLI) for browser selection.

## Installation

1. **Clone the Repository / or download Exporter.py**

    ```bash
    git clone https://github.com/truelockmc/History-Exporter.git
    ```

2. **Navigate to the Directory**

    ```bash
    cd History-Exporter
    ```

3. **Install Dependencies**

   There are no external dependencies other than Python 3.x, so you can directly use the script.

## Usage

1. **Run the Script**:

3. **Choose the Browser**:  
   You will be prompted to select the browser from which you want to export the history. Choose from the following options:

    - **chrome**
    - **firefox**
    - **edge**
    - **opera**

   Example:

    ```text
    Which browser's history do you want to export? (chrome/firefox/edge/opera): edge
    ```

4. **CSV File Output**:  
   After running the script, a CSV file will be created in the same directory as the script, with the exported history of the selected browser.

   The CSV file will contain the following columns:

    - **URL**: The web address visited.
    - **Title**: The title of the webpage (if available).
    - **Last Visit Time**: The timestamp of the last visit in the browser.

    Example CSV:

    ```csv
    URL,Title,Last Visit Time
    "https://www.example.com","Example Website","2025-01-01 12:00:00"
    ```

## How it Works

- The script locates the browser's history database, which is an SQLite file stored in the browser's data folder.
- For **Chrome**, **Edge**, and **Opera**, the script connects to the SQLite database, queries the history tables, and exports the data.
- For **Firefox**, it queries the `moz_places` and `moz_historyvisits` tables to extract URLs and visit timestamps.

## Contributing

Contributions are welcome! If you have any improvements or bug fixes, feel free to submit a pull request. Make sure to follow the coding style and include tests for your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [True_Lock](https://github.com/truelockmc) : )
