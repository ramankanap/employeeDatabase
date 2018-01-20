# employeeDatabase
A simple program for manipulating data about employees to show how to use PostgreSQL with Python.


## Requirements:
 - postgresql
 - python3-psycopg2

## Installation for Ubuntu:
### 1. Install required packages:
`sudo apt install postgresql python3 python3-psycopg2`
### 2. Add the role and the database to postgresql:
`sudo su -l postgres`  
`psql`  
`CREATE ROLE yourrole WITH LOGIN PASSWORD 'yourpassword';`  
`CREATE DATABASE employees;`
### 3. Change authentication method for local roles:
`sudo nano /etc/postgresql/9.6/main/pg_hba.conf`  
Overwrite `local all all peer` with `local all all md5`  
`service postgresql reload`
### 4. Change user and password in the program:
In employeeDatabase.py overwrite `user='yourrole', password='yourpassword'` with your values.
### 5. Execute the program:
`python3 employeeDatabase.py`
