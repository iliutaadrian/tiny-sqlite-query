# TinyQuery

TinyQuery is a lightning-fast, lightweight command-line tool designed for effortless exploration and querying of SQLite databases. Perfect for developers, data analysts, and SQLite enthusiasts who need a quick and powerful way to interact with their databases directly from the terminal.

![Screenshot 2024-10-19 at 12 00 05](https://github.com/user-attachments/assets/8be492ca-b662-44e3-b5b7-81e845f0b631)

## 🚀 Features
- 🔍 Explore SQLite databases with ease
- 📊 Execute custom queries with WHERE clauses
- 🔀 Sort results by any column, ascending or descending
- 🖥️ Tmux integration for quick access
- ALL FROM CLI

## 🛠 Installation

1. Clone the repository to your home directory:
   ```
   git clone https://github.com/iliutaadrian/tiny-query.git ~/.tinyquery
   ```

2. Navigate to the project directory:
   ```
   cd ~/.tinyquery
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Add the following to your `~/.zshrc` file (or `~/.bashrc` if you're using bash):
   ```
   alias query='python $HOME/.tinyquery/app.py'
   ```

5. Reload your shell configuration:
   ```
   source ~/.zshrc
   ```

6. For tmux integration, add the following line to your `.tmux.conf`:
   ```
   bind-key q run-shell 'tmux neww "cd #{pane_current_path}; ~/.tinyquery/tmux_launcher.sh"'
   ```

## 🖥 Usage

After setting up the global alias, you can run TinyQuery from anywhere using:

```
query --db path/to/your/database.db
```

Replace `path/to/your/database.db` with the actual path to your SQLite database file.

### Tmux Launcher

If you've set up the tmux integration, you can quickly launch TinyQuery in a new tmux window by pressing `prefix + q`. This will open a new window with TinyQuery, allowing you to select a database file using fzf.


![Screenshot 2024-10-19 at 13 44 23](https://github.com/user-attachments/assets/c9bc6f66-acf0-4969-86e0-254c421d88b4)



## 💡 Example Usage

Here's a quick demonstration of TinyQuery in action:

```
$ query --db example.db

Database Statistics:
--------------------
Tables: users, orders, products
Total rows in database: 1500
Database size: 256.45 MB

Available tables:
1. users
2. orders
3. products

Select a table (enter number or table name, or 'q' to quit): 1

Options:
0. Exit
1. Select 20 rows (current offset: 0)
2. Select with custom WHERE clause
3. Delete all content from table
4. Choose another table
5. Change sort options

Enter your choice (0-5): 1

id | name       | email                  | created_at          
1  | John Doe   | john.doe@example.com   | 2023-01-01 10:00:00 
2  | Jane Smith | jane.smith@example.com | 2023-01-02 11:30:00 
...

Total rows: 20

Enter number of rows to move (positive or negative), or press Enter to return to menu: 20

id  | name           | email                      | created_at          
21  | Alice Johnson  | alice.johnson@example.com  | 2023-01-21 09:15:00 
22  | Bob Williams   | bob.williams@example.com   | 2023-01-22 14:45:00 
...

Total rows: 20

Enter number of rows to move (positive or negative), or press Enter to return to menu: 

Options:
0. Exit
1. Select 20 rows (current offset: 20)
2. Select with custom WHERE clause
3. Delete all content from table
4. Choose another table
5. Change sort options

Enter your choice (0-5): 5

Available columns for sorting:
1. id
2. name
3. email
4. created_at

Enter the number of the column to sort by (or press Enter to skip sorting): 2
Enter sort order (ASC/DESC, default is ASC): DESC

Sorting by: name DESC

Options:
0. Exit
1. Select 20 rows (current offset: 0)
2. Select with custom WHERE clause
3. Delete all content from table
4. Choose another table
5. Change sort options

Enter your choice (0-5): 2

Enter a WHERE clause for users (or press Enter to skip): name LIKE 'A%'

id | name          | email                     | created_at          
3  | Alice Johnson | alice.johnson@example.com | 2023-01-03 09:15:00 
7  | Andrew Davis  | andrew.davis@example.com  | 2023-01-07 13:45:00 
...

Total rows: 15

Options:
0. Exit
1. Select 20 rows (current offset: 0)
2. Select with custom WHERE clause
3. Delete all content from table
4. Choose another table
5. Change sort options

Enter your choice (0-5): 0

Exiting...
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/iliutaadrian/TinyQuery/issues).

## 📝 License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.
