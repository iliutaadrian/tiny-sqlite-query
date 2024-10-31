import sqlite3
import readline
import sys
import os
import argparse
import re

def truncate_value(value, max_length=50):
    # Convert to string and replace newlines and tabs with spaces
    str_value = str(value).replace('\n', ' ').replace('\t', ' ')
    # Remove multiple spaces
    str_value = re.sub(r'\s+', ' ', str_value).strip()
    if len(str_value) > max_length:
        return str_value[:max_length - 3] + "..."
    return str_value

def execute_query(db_file, query):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(query)
        
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            if results:
                # Get column names
                column_names = [description[0] for description in cursor.description]
                
                # Truncate and calculate column widths
                truncated_results = [[truncate_value(value) for value in row] for row in results]
                col_widths = [min(100, max(len(str(row[i])) for row in truncated_results + [column_names])) for i in range(len(column_names))]

                # Print header
                print("-" * (sum(col_widths) + 3 * (len(col_widths) - 1)))
                print(" | ".join(name.ljust(width) for name, width in zip(column_names, col_widths)))
                print("-" * (sum(col_widths) + 3 * (len(col_widths) - 1)))
                
                # Print rows
                for row in truncated_results:
                    print(" | ".join(str(value).ljust(width) for value, width in zip(row, col_widths)))
                
                # Print footer with column names
                print("-" * (sum(col_widths) + 3 * (len(col_widths) - 1)))
                print(" | ".join(name.ljust(width) for name, width in zip(column_names, col_widths)))
            
            print(f"\nTotal rows: {len(results)}")
        elif query.strip().upper().startswith("DELETE"):
            conn.commit()
            print(f"Deleted {cursor.rowcount} rows")
        else:
            conn.commit()
            print("Query executed successfully")
        
        cursor.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def get_schema_and_stats(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
        tables = cursor.fetchall()
        
        print("\nDatabase Statistics:")
        print("-" * 20)
        
        total_rows = 0
        table_info = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            total_rows += row_count
            table_info[table_name] = {"row_count": row_count, "schema": []}
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for column in columns:
                table_info[table_name]["schema"].append((column[1], column[2]))
        
        print(f"Tables: {', '.join(table_info.keys())}")
        print(f"Total rows in database: {total_rows}")
        
        # Get database size
        db_size_bytes = os.path.getsize(db_file)
        db_size_mb = db_size_bytes / (1024 * 1024)
        print(f"Database size: {db_size_mb:.2f} MB")
        
        cursor.close()
        return table_info
    except sqlite3.Error as e:
        print(f"An error occurred while fetching schema and stats: {e}")
        return {}
    finally:
        if conn:
            conn.close()

def display_all_schemas(table_info):
    for table_name, info in table_info.items():
        print(f"\nTable: {table_name} - Row Count: {info['row_count']}")
        print("-" * (len(table_name) + 7))
        for column, data_type in info["schema"]:
            print(f"  {column} ({data_type})")

def select_rows_with_offset(db_file, table_name, offset=0, limit=20, sort_column=None, sort_order="ASC"):
    query = f"SELECT * FROM {table_name}"
    if sort_column:
        query += f" ORDER BY {sort_column} {sort_order}"
    query += f" LIMIT {limit} OFFSET {offset}"
    execute_query(db_file, query)

def prompt_where_clause(db_file, table_name):
    where_clause = input(f"Enter a WHERE clause for {table_name} (or press Enter to skip): ")
    if where_clause:
        query = f"SELECT * FROM {table_name} WHERE {where_clause} LIMIT 20"
    else:
        query = f"SELECT * FROM {table_name} LIMIT 20"
    execute_query(db_file, query)

def delete_all_from_table(db_file, table_name):
    confirm = input(f"Are you sure you want to delete all content from {table_name}? (yes/no): ")
    if confirm.lower() == 'yes':
        query = f"DELETE FROM {table_name}"
        execute_query(db_file, query)
    else:
        print("Delete operation cancelled.")

def get_sort_options(table_info, table_name):
    columns = [col[0] for col in table_info[table_name]["schema"]]
    print("\nAvailable columns for sorting:")
    for i, column in enumerate(columns, 1):
        print(f"{i}. {column}")
    
    while True:
        column_choice = input("Enter the number of the column to sort by (or press Enter to skip sorting): ")
        if column_choice == "":
            return None, None
        try:
            column_index = int(column_choice) - 1
            if 0 <= column_index < len(columns):
                sort_column = columns[column_index]
                sort_order = input("Enter sort order (ASC/DESC, default is ASC): ").upper()
                if sort_order not in ["ASC", "DESC"]:
                    sort_order = "ASC"
                return sort_column, sort_order
            else:
                print("Invalid column number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or press Enter to skip sorting.")


def setup_readline():
    try:
        # Create a valid history file path
        histfile = os.path.join(os.path.expanduser("~"), ".sqlite_query_tool_history")
        histfile = os.path.abspath(histfile)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(histfile), exist_ok=True)
        
        try:
            readline.read_history_file(histfile)
        except (FileNotFoundError, OSError):
            # Create new history file
            try:
                with open(histfile, 'w') as f:
                    pass
            except (IOError, OSError) as e:
                print(f"Warning: Could not create history file: {e}")
                histfile = None
        
        if histfile:
            # Set history length
            readline.set_history_length(1000)
            
            # Configure key bindings if supported
            try:
                readline.parse_and_bind('"\e[A": history-search-backward')
                readline.parse_and_bind('"\e[B": history-search-forward')
            except (AttributeError, TypeError):
                # Some readline implementations might not support these bindings
                print("Note: Command history navigation might be limited")
    
    except Exception as e:
        print(f"Warning: History file functionality disabled: {e}")
        histfile = None
    
    return histfile


def input_with_history(prompt):
    try:
        return input(prompt)
    finally:
        readline.write_history_file(histfile)

def main():
    parser = argparse.ArgumentParser(
        description="SQLite Database Query Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python %(prog)s -db my_database.db

This tool allows you to interact with SQLite databases. You can:
- View database statistics and table schemas
- Select and view data from tables
- Perform custom queries with WHERE clauses
- Delete data from tables

For more information, visit:
https://github.com/your-repo/sqlite-query-tool
        """
    )
    parser.add_argument("-db", "--database", required=True, help="Path to the SQLite database file")

    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        sys.exit(1)

    db_file = args.database

    if not os.path.exists(db_file):
        print(f"Error: Database file '{db_file}' does not exist.")
        parser.print_help()
        sys.exit(1)

    print("\nWelcome to the SQLite Database Query Tool!")
    print("=" * 40)
    print("Use up and down arrow keys to navigate command history.")
    
    global histfile
    histfile = setup_readline()
    
    table_info = get_schema_and_stats(db_file)
    
    
    while True:
        display_all_schemas(table_info)
        print("\nAvailable tables:")
        for i, table_name in enumerate(table_info.keys(), 1):
            print(f"{i}. {table_name}")
        
        table_choice = input_with_history("\nSelect a table (enter number or table name, or 'q' to quit): ")
        
        if table_choice.lower() == 'q':
            print("Thank you for using the SQLite Database Query Tool. Goodbye!")
            break
        
        try:
            if table_choice.isdigit():
                table_name = list(table_info.keys())[int(table_choice) - 1]
            else:
                table_name = table_choice
            
            if table_name not in table_info:
                raise ValueError
        except (IndexError, ValueError):
            print("Invalid table selection. Please try again.")
            continue
        
        offset = 0
        sort_column, sort_order = None, "ASC"
        while True:
            print(f"\nCurrent table: {table_name} - Row Count: {table_info[table_name]['row_count']}")
            print("Options:")
            print("0. Exit")
            print(f"1. Select 20 rows (current offset: {offset})")
            print("2. Select with custom WHERE clause")
            print("3. Delete all content from table")
            print("4. Choose another table")
            print("5. Change sort options")
            
            choice = input_with_history("Enter your choice (0-5): ")
            
            if choice == '0':
                print("Returning to table selection...")
                break
            elif choice == '1':
                while True:
                    select_rows_with_offset(db_file, table_name, offset, sort_column=sort_column, sort_order=sort_order)
                    offset_change = input_with_history("Enter number of rows to move (positive or negative), or press Enter to return to menu: ")
                    if offset_change == "":
                        break
                    try:
                        offset = max(0, offset + int(offset_change))
                    except ValueError:
                        print("Invalid input. Please enter a number or press Enter.")
            elif choice == '2':
                where_clause = input_with_history(f"Enter a WHERE clause for {table_name} (or press Enter to skip): ")
                if where_clause:
                    query = f"SELECT * FROM {table_name} WHERE {where_clause} LIMIT 20"
                else:
                    query = f"SELECT * FROM {table_name} LIMIT 20"
                execute_query(db_file, query)
            elif choice == '3':
                delete_all_from_table(db_file, table_name)
            elif choice == '4':
                break
            elif choice == '5':
                sort_column, sort_order = get_sort_options(table_info, table_name)
                print(f"Sorting by: {sort_column or 'None'} {sort_order}")
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
