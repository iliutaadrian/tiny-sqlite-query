#!/bin/bash

# Set the path to your Python script
QUERY_SCRIPT="$HOME/.tinyquery/app.py"

# Function to select a database file using fzf
select_db_file() {
    find . -type f | sed 's|^./||' | \
    fzf --prompt="Select a database file: " \
        --preview 'file -b {}; echo; if file -b {} | grep -q "SQLite"; then echo "Tables:"; sqlite3 {} ".tables"; else echo "Not a SQLite database"; fi'
}

# Main script
main() {
    # Select the database file
    DB_FILE=$(select_db_file)
    if [ -n "$DB_FILE" ]; then
      echo "Selected: $DB_FILE"
      python3 "$QUERY_SCRIPT" -db "$DB_FILE"
    else
        echo "No database file selected."
    fi

    echo
    read -p "Press enter to close this window"
}

# Run the main function
main
