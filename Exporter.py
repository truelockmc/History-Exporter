import os
import sqlite3
import shutil
import platform
from datetime import datetime, timedelta  # Import timedelta

# Function to retrieve the path of the browser database based on the operating system
def get_browser_db_paths(browser_name):
    paths = []
    os_type = platform.system()

    if browser_name.lower() == "chrome":
        if os_type == "Windows":
            paths.append(os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\History")
        elif os_type == "Darwin":  # macOS
            paths.append(os.path.expanduser("~") + "/Library/Application Support/Google/Chrome/Default/History")
        elif os_type == "Linux":
            paths.append(os.path.expanduser("~") + "/.config/google-chrome/Default/History")
    
    elif browser_name.lower() == "firefox":
        if os_type == "Windows":
            paths.append(os.path.expanduser("~") + r"\AppData\Roaming\Mozilla\Firefox\Profiles")
        elif os_type == "Darwin":  # macOS
            paths.append(os.path.expanduser("~") + "/Library/Application Support/Firefox/Profiles")
        elif os_type == "Linux":
            paths.append(os.path.expanduser("~") + "/.mozilla/firefox")

    elif browser_name.lower() == "edge":
        if os_type == "Windows":
            paths.append(os.path.expanduser("~") + r"\AppData\Local\Microsoft\Edge\User Data\Default\History")
    
    elif browser_name.lower() == "opera":
        if os_type == "Windows":
            paths.append(os.path.expanduser("~") + r"\AppData\Roaming\Opera Software\Opera Stable\History")
        elif os_type == "Darwin":  # macOS
            paths.append(os.path.expanduser("~") + "/Library/Application Support/com.operasoftware.Opera/History")
        elif os_type == "Linux":
            paths.append(os.path.expanduser("~") + "/.config/opera/History")

    return paths

# Function to export browsing history from a SQLite database for Edge
def export_edge_history(db_path, output_file):
    # Ensure the database file exists
    if not os.path.exists(db_path):
        print(f"The file {db_path} was not found.")
        return False

    # Avoid access conflicts by copying the database file
    temp_db_path = db_path + "_temp"
    shutil.copyfile(db_path, temp_db_path)

    # Connect to the SQLite database
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()

    # Query the browsing history for Edge
    try:
        cursor.execute("""
            SELECT url, title, last_visit_time
            FROM urls
            ORDER BY last_visit_time DESC
            """)
    except sqlite3.OperationalError as e:
        print(f"Error retrieving data from the database: {e}")
        conn.close()
        os.remove(temp_db_path)
        return False

    # Export results to a file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("URL,Title,Last Visit Time\n")
            for row in cursor.fetchall():
                url = row[0]
                title = row[1] if row[1] else "No title"
                last_visit_time = datetime(1601, 1, 1) + timedelta(microseconds=row[2])  # Windows file time
                f.write(f'"{url}","{title}","{last_visit_time}"\n')
    except Exception as e:
        print(f"Error writing to the file: {e}")
        conn.close()
        os.remove(temp_db_path)
        return False

    # Close the connection and delete the temporary file
    conn.close()
    os.remove(temp_db_path)
    return True
    
# Function to export browsing history from a SQLite database
def export_firefox_history(db_path, output_file):
    # Ensure the database file exists
    if not os.path.exists(db_path):
        print(f"The file {db_path} was not found.")
        return False

    # Avoid access conflicts by copying the database file
    temp_db_path = db_path + "_temp"
    shutil.copyfile(db_path, temp_db_path)

    # Connect to the SQLite database
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()

    # Query the browsing history for Firefox
    try:
        cursor.execute("""
            SELECT p.url, p.title, v.visit_date
            FROM moz_places p
            JOIN moz_historyvisits v ON p.id = v.place_id
            ORDER BY v.visit_date DESC
            """)
    except sqlite3.OperationalError as e:
        print(f"Error retrieving data from the database: {e}")
        conn.close()
        os.remove(temp_db_path)
        return False

    # Export results to a file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("URL,Title,Last Visit Time\n")
            for row in cursor.fetchall():
                url = row[0]
                title = row[1] if row[1] else "No title"
                last_visit_time = datetime(1970, 1, 1) + timedelta(microseconds=row[2])  # Unix epoch
                f.write(f'"{url}","{title}","{last_visit_time}"\n')
    except Exception as e:
        print(f"Error writing to the file: {e}")
        conn.close()
        os.remove(temp_db_path)
        return False

    # Close the connection and delete the temporary file
    conn.close()
    os.remove(temp_db_path)
    return True

# Function to export browser history
def export_browser_history(browser_name):
    success_count = 0
    db_paths = get_browser_db_paths(browser_name)
    for db_path in db_paths:
        if os.path.isdir(db_path):  # For Firefox profiles
            for profile in os.listdir(db_path):
                full_path = os.path.join(db_path, profile, "places.sqlite")
                if os.path.exists(full_path):
                    output_file = f"{browser_name}_history_{profile}.csv"
                    if export_firefox_history(full_path, output_file):
                        print(f"History successfully exported to {output_file}")
                        success_count += 1
        else:
            output_file = f"{browser_name}_history.csv"
            if browser_name.lower() == "edge":
                if export_edge_history(db_path, output_file):
                    print(f"History successfully exported to {output_file}")
                    success_count += 1
            else:
                if export_firefox_history(db_path, output_file):
                    print(f"History successfully exported to {output_file}")
                    success_count += 1

    if success_count > 0:
        print(f"\nExport complete: {success_count} file(s) successfully exported.")
    else:
        print("\nNo history exported. Please check your input.")

# Example usage
if __name__ == "__main__":
    browser = input("Which browser's history do you want to export? (chrome/firefox/edge/opera): ").strip().lower()
    export_browser_history(browser)
    input("\nPress Enter to close the window.")
