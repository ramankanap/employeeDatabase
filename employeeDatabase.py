'''employeeDatabase version 20180120
license: public domain'''

import psycopg2

'''fields for filling in user and password information'''
CONNECTED_DATABASE = psycopg2.connect(dbname='employees', user='yourrole', password='yourpassword')
CURSOR = CONNECTED_DATABASE.cursor()

def create_tables():
    '''if tables do not yet exist, create them'''
    CURSOR.execute('''create table if not exists employees
        (employee_id serial primary key, first_name text, surname text, role_id integer)''')
    CURSOR.execute('''create table if not exists roles
        (role_id serial primary key, role_description text unique)''')
    CONNECTED_DATABASE.commit()

def add_role_or_employee():
    '''user chooses to which table to add'''
    toWhichTableToAdd = input('Add role (insert r) or employee (insert e)?: ')
    if toWhichTableToAdd == 'r':
        add_role()
    elif toWhichTableToAdd == 'e':
        add_employee()

def add_role():
    '''add role to the roles table'''
    descriptionOfNewRole = input('Insert new role\'s description: ')
    CURSOR.execute('insert into roles (role_description) values (%s)',
                   (descriptionOfNewRole,))
    CONNECTED_DATABASE.commit()

def add_employee():
    '''add employee to the employees table'''
    firstNameToBeAdded = input('Insert employee\'s first name: ')
    surnameToBeAdded = input('Insert employee\'s surname: ')
    CURSOR.execute('insert into employees (first_name, surname) values (%s, %s)',
                   (firstNameToBeAdded, surnameToBeAdded))
    CONNECTED_DATABASE.commit()

def assign_employee_to_the_role():
    '''assigning role to the employee'''
    idOfEmployeeForAssignment = int(input('Insert employee\'s id for assignment: '))
    CURSOR.execute('select * from employees where employee_id=%s', (idOfEmployeeForAssignment,))
    row = CURSOR.fetchone()
    print('Employee\'s name: ' + row[1] + ' ' + row[2])
    print('Available roles: ')
    list_roles()
    idOfRoleForAssignment = int(input('Insert role\'s id for assignment: '))
    CURSOR.execute('update employees set role_id=%s where employee_id=%s',
                   (idOfRoleForAssignment, idOfEmployeeForAssignment))
    CONNECTED_DATABASE.commit()

def modify_role_or_employee():
    '''user chooses what record from which table to modify'''
    whichTableToModify = input('Modify role (insert r) or employee (insert e)?: ')
    if whichTableToModify == 'r':
        modify_role()
    elif whichTableToModify == 'e':
        modify_employee()

def modify_role():
    '''modify existing role'''
    idForModification = int(input('Insert role\'s id: '))
    CURSOR.execute('select * from roles where role_id=%s', (idForModification,))
    row = CURSOR.fetchone()
    print('Previous value: ' + row[1])
    print('Insert role\'s new description')
    newRoleDescription = input()
    CURSOR.execute('update roles set role_description=%s where role_id=%s',
                   (newRoleDescription, idForModification))
    CONNECTED_DATABASE.commit()

def modify_employee():
    '''modify existing employee'''
    idForModification = int(input('Insert employee\'s id: '))
    CURSOR.execute('select * from employees where employee_id=%s', (idForModification,))
    row = CURSOR.fetchone()
    print('Previous values: ' + row[1] + ' ' + row[2])
    firstName = input('Insert employee\'s new first name: ')
    surname = input('Insert employee\'s new surname: ')
    CURSOR.execute('update employees set first_name=%s, surname=%s where employee_id=%s',
                   (firstName, surname, idForModification))
    CONNECTED_DATABASE.commit()

def delete_role_or_employee():
    '''user chooses what record from which table to delete'''
    fromWhichTableToDelete = input('Delete role (insert r) or employee (insert e)?: ')
    if fromWhichTableToDelete == 'r':
        delete_role()
    elif fromWhichTableToDelete == 'e':
        delete_employee()

def delete_role():
    '''delete role'''
    idForDeletion = int(input('Insert role\'s id: '))
    CURSOR.execute('delete from roles where role_id=%s', (idForDeletion,))
    CONNECTED_DATABASE.commit()

def delete_employee():
    '''delete employee'''
    idForDeletion = int(input('Insert employee\'s id: '))
    CURSOR.execute('delete from employees where employee_id=%s', (idForDeletion,))
    CONNECTED_DATABASE.commit()

def list_roles_or_employees():
    '''user chooses which table to show'''
    whichTableToList = input('List roles (insert r) or employees (insert e)?: ')
    if whichTableToList == 'r':
        list_roles()
    elif whichTableToList == 'e':
        list_employees()

def list_roles():
    '''show all available roles'''
    print('-----------------------------------------------')
    CURSOR.execute('select * from roles')
    for record in CURSOR:
        print(str(record[0]) + ',' + ' ' + record[1])
    print('-----------------------------------------------')

def list_employees():
    '''show all employees'''
    print('-----------------------------------------------')
    CURSOR.execute('''select * from employees
                   left outer join roles on employees.role_id = roles.role_id''')
    for record in CURSOR:
        print(str(record[0]) + ',' + ' ' + record[1] + ' ' + record[2] + ',' + ' ' + str(record[5]))
    print('-----------------------------------------------')

def transfer_names():
    '''copy data from text files'''
    numberOfDesiredNames = int(input('How many persons would you like to transfer?: '))
    copyFromFirstnames = open('firstnames', 'r')
    copyFromSurnames = open('surnames', 'r')
    all_firstnames = copyFromFirstnames.read().split()
    all_surnames = copyFromSurnames.read().split()
    i = 0
    while i < numberOfDesiredNames:
        firstName = all_firstnames[i]
        surname = all_surnames[i]
        CURSOR.execute('insert into employees (first_name, surname) values (%s, %s)',
                       (firstName, surname))
        i = i + 1
    CONNECTED_DATABASE.commit()
    copyFromFirstnames.close()
    copyFromSurnames.close()

def main_menu():
    '''main menu is running in a loop'''
    try:
        typeOfAction = ''
        while typeOfAction != 'q':
            print('----------------------------------')
            print('Add (insert a)')
            print('Assign (insert s)')
            print('Modify (insert m)')
            print('Delete (insert d)')
            print('List (insert l)')
            print('Transfer names (insert t)')
            print('Quit (insert q)')
            print('----------------------------------')
            typeOfAction = input()
            if typeOfAction == 'a':
                add_role_or_employee()
            elif typeOfAction == 's':
                assign_employee_to_the_role()
            elif typeOfAction == 'm':
                modify_role_or_employee()
            elif typeOfAction == 'd':
                delete_role_or_employee()
            elif typeOfAction == 'l':
                list_roles_or_employees()
            elif typeOfAction == 't':
                transfer_names()
    except BaseException as causeOfError:
        print(causeOfError.__class__.__name__)

create_tables()
main_menu()
CURSOR.close()
CONNECTED_DATABASE.close()
