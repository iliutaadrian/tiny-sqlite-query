TinySQLiteQuery
A lightweight, command-line tool for exploring and querying SQLite databases with ease.
🔍 Explore SQLite databases effortlessly
📊 Query tables with custom WHERE clauses
🔢 Paginate through large datasets
🔀 Sort results by any column
🗑️ Delete table contents (with confirmation)
TinySQLiteQuery is perfect for developers, data analysts, and SQLite enthusiasts who need a quick and simple way to interact with their databases directly from the command line.
Features

View table schemas and database statistics
Browse table contents with customizable pagination
Execute custom queries with WHERE clauses
Sort results by any column in ascending or descending order
Delete table contents (with safeguards)
Simple and intuitive command-line interface

Get started with TinySQLiteQuery and simplify your SQLite database exploration today!
This description:

Starts with a brief, catchy tagline
Uses emojis to visually highlight key features
Includes a short paragraph explaining the tool's purpose and target audience
Lists main features in a bulleted format for easy reading
Ends with a call-to-action to encourage users to try the tool

You can adjust any part of this description to better fit your vision for the project or to emphasize particular aspects of the tool.

# TinySQLiteQuery

A lightweight, command-line tool for exploring and querying SQLite databases with ease.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/TinySQLiteQuery.git
   ```

2. Navigate to the project directory:
   ```
   cd TinySQLiteQuery
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run TinySQLiteQuery, use the following command:

```
python tinysqlitequery.py --db path/to/your/database.db
```

Replace `path/to/your/database.db` with the actual path to your SQLite database file.

## Example Usage and Output

Here's an example of how to use TinySQLiteQuery and what the output might look like:

1. Start the tool:

```
$ python tinysqlitequery.py --db example.db

Database Statistics:
--------------------
Tables: users, orders, products
Total rows in database: 1500
Database size: 256.45 MB

Table: users
-------------
  id (INTEGER)
  name (TEXT)
  email (TEXT)
  created_at (DATETIME)

Table: orders
--------------
  id (INTEGER)
  user_id (INTEGER)
  total_amount (REAL)
  order_date (DATETIME)

Table: products
---------------
  id (INTEGER)
  name (TEXT)
  price (REAL)
  stock (INTEGER)

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

Enter your choice (0-5): 1

id  | name           | email                      | created_at          
152 | Zoe Young      | zoe.young@example.com      | 2023-05-02 16:30:00 
98  | Zachary Wilson | zachary.wilson@example.com | 2023-03-10 11:20:00 
...

Total rows: 20

Enter number of rows to move (positive or negative), or press Enter to return to menu: 

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
