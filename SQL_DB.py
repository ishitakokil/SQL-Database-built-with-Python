"""
Name: Ishita Kokil
Netid: kokilish
PID: A61398855

Sources:
1. https://www.w3schools.com/python/ref_keyword_del.asp
2. https://note.nkmk.me/en/python-dict-get/
4. https://stackoverflow.com/questions/16310015/what-does-this-mean-key-lambda-x-x1
5. https://blogboard.io/blog/knowledge/python-sorted-lambda/
6. https://docs.python.org/3/tutorial/classes.html
7. https://www.educative.io/answers/how-to-sort-a-list-of-tuples-in-python-using-lambda
8. CSE 482 Lecture Slides for SQL connection information and understanding.
9. https://docs.python.org/3/library/functions.html#enumerate
10.https://stackoverflow.com/questions/63980292/how-to-delete-all-instances-of-a-repeated-number-in-a-list
11.https://www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/
12.https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
13.https://stackoverflow.com/questions/4842956/python-how-to-remove-empty-lists-from-a-list
15. https://stackoverflow.com/questions/5893163/what-is-the-purpose-of-the-single-underscore-variable-in-python

"""
import string
import json


_ALL_DATABASES = {}


def remove_leading_whitespace(query, tokens):
    whitespace = collect_characters(query, string.whitespace)
    return query[len(whitespace):]


def collect_characters(query, allowed_characters):
    letters = []
    for letter in query:
        if letter not in allowed_characters:
            break
        letters.append(letter)
    return "".join(letters)


def remove_word(query, tokens):
    word = collect_characters(query, string.ascii_letters + "_" + string.digits + '.')
    if word == "NULL":
        tokens.append(None)
    elif '.' in word:
        tokens.append(word)
    else:
        tokens.append(word)
    return query[len(word):]


def remove_number(query, tokens):
    num = collect_characters(query, string.digits + ".")
    if '.' in num:
        a, b = num.split('.')
        if a.isalpha() and b.isalpha():
            tokens.append(num)
        else:
            tokens.append(float(num))
    else:
        tokens.append(int(num))

    return query[len(num):]


def remove_negative(query, tokens):
    assert query[0] == "-"
    query = query[1:]
    num = collect_characters(query, string.digits + ".")
    if '.' in num:
        tokens.append(-float(num))
    else:
        tokens.append(-int(num))
    return query[len(num):]


def remove_text(query, tokens):
    assert query[0] == "'"
    query = query[1:]
    end_quote_index = query.find("'")

    while end_quote_index < len(query) - 1 and query[end_quote_index + 1] == "'":
        end_quote_index = query.find("'", end_quote_index + 2)

    text = query[:end_quote_index].replace("''", "'")
    tokens.append(text)
    query = query[end_quote_index + 1:]  # Move the cursor past the closing single quote
    return query

def tokenize(query):
    tokens = []
    while query:
        if query.startswith("IS NOT"):
            tokens.append("IS NOT")
            query = query[6:]
            continue

        if query[0] in string.whitespace:
            query = remove_leading_whitespace(query, tokens)
            continue

        if query[0] in (string.ascii_letters + "_"):
            query = remove_word(query, tokens)
            continue

        if query[0] in (string.digits + "."):
            query = remove_number(query, tokens)
            continue

        if query[0] == "-":
            query = remove_negative(query, tokens)
            continue

        if query[0] in "(),;*":
            tokens.append(query[0])
            query = query[1:]
            continue

        if query[0] == "'":
            query = remove_text(query, tokens)
            continue

        if query.startswith('!='):
            tokens.append('!=')
            query = query[2:]
            continue

        if query[0] == '=':
            tokens.append('=')
            query = query[1:]
            continue

        if query[0] == '>':
            tokens.append('>')
            query = query[1:]
            continue

        if query[0] == '<':
            tokens.append('<')
            query = query[1:]
            continue

    if tokens[-1] != ";":
        raise ValueError("Invalid SQL query : must end with a ';'")
    tokens.pop()
    while ',' in tokens:
        tokens.remove(',')
    return tokens


class Connection(object):
    def __init__(self, db):
        """
        Takes a filename, but doesn't do anything with it.
        (The filename will be used in a future project).
        """
        self.db = db

    def execute(self, statement):
        """
        Takes a SQL statement.
        Returns a list of tuples (empty unless select statement
        with rows to return).
        """
        tokens = tokenize(statement)  # takes the SQL Query and creates tokens in it

        if tokens[0] == "CREATE" and tokens[1] == "TABLE":
            return create(tokens,self.db.tables)

        elif tokens[0] == "INSERT" and tokens[1] == "INTO":
            return insert(tokens,self.db.tables)

        elif tokens[0] == "SELECT":
            return select(tokens,self.db.tables)

        elif tokens[0] == "DELETE" and tokens[1] == "FROM":
            return delete(tokens,self.db.tables)

        if tokens[0] == "UPDATE":
            return update(tokens,self.db.tables)

        else:
            return None

    def close(self):
        """
        Empty method that will be used in future projects
        """
        self.db.save()
        self.db = None


def connect(filename):
    """
    Creates a Connection object with the given filename
    """
    if filename not in _ALL_DATABASES:
        db = Database(filename)
        _ALL_DATABASES[filename] = db
        db.load()
    else:
        db = _ALL_DATABASES[filename]
    return Connection(db)

class Database(object):
    def __init__(self, filename):
        self.filename = filename
        self.tables = {}

    def save(self):
        """
        Saves the current state of the database to a JSON file.
        """
        data = {}
        for table_name, table in self.tables.items():
            data[table_name] = {
                'columns': table.columns,
                'rows': table.rows
            }

        with open(self.filename, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)

            for table_name, table_data in data.items():
                columns = table_data['columns']
                rows = table_data['rows']
                table = Table(table_name, columns)
                table.rows = rows
                self.tables[table_name] = table


        except FileNotFoundError:
            pass

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.rows = []


    def append(self, row):
        self.rows.append(row)

    def remove(self, row):
        self.rows.remove(row)


def order(tokens, my_rows, my_table):
    sort_columns = []
    by_index = tokens.index('BY')
    sort_columns_str = tokens[by_index + 1:]
    sort_columns_str = split(sort_columns_str)
    for sort_column_str in sort_columns_str:
        for i, col_name in enumerate(my_table.columns):
            if col_name[0] == sort_column_str:
                sort_columns.append(i)
                break
    if len(sort_columns) > 0:
        my_rows.sort(key=lambda x: [x[i] for i in sort_columns])
    return my_rows


def column_index(columns, col_name):
    for i, col_tuple in enumerate(columns):
        col_type = col_tuple[1]
        if col_tuple[0] == col_name:
            index = i
            break
    return index, col_type

def where(tokens, my_rows, my_table):
    where_index = tokens.index('WHERE')
    col_name = tokens[where_index + 1]
    operator = tokens[where_index + 2]
    value = tokens[where_index + 3]

    if '.' in col_name:
        table_name, col_name = col_name.split('.')

    column_idx= None
    for i, col_tuple in enumerate(my_table.columns):
        col_type = col_tuple[1]
        if col_tuple[0] == col_name:
            column_idx = i
            break

    all_rows = []
    if operator == '>':
        for row in my_rows:
            to_compare = row[column_idx]
            if to_compare is None:
                to_compare = False  # Set the default value to false
            if value is None:
                value = False  # Set the default value to false
            if to_compare > value:
                all_rows.append(row)

    elif operator == '<':
        for row in my_rows:
            to_compare = row[column_idx]
            if to_compare is None:
                #to_compare = False  # Set the default value to false
                continue
            if value is None:
                value = False  # Set the default value to false
            if to_compare < value:
                all_rows.append(row)
    elif operator == '=':
        for row in my_rows:
            to_compare = row[column_idx]
            if to_compare is None:
                to_compare = False  # Set the default value to false
            if value is None:
                value = False  # Set the default value to false
            if to_compare == value:
                all_rows.append(row)
    elif operator == '!=':
        for row in my_rows:
            to_compare = row[column_idx]
            if to_compare is None:
                to_compare = False  # Set the default value to false
            if value is None:
                value = False  # Set the default value to false
            if to_compare != value:
                all_rows.append(row)
    elif operator == 'IS':
        for row in my_rows:
            to_compare = row[column_idx]
            if to_compare is None:
                to_compare = False  # Set the default value to false
            if value is None:
                value = False  # Set the default value to false
            if to_compare is value:
                all_rows.append(row)
    elif operator == 'IS NOT':
        for row in my_rows:
            to_compare = row[column_idx]
            if to_compare is None:
                to_compare = False  # Set the default value to false
            if value is None:
                value = False  # Set the default value to false
            if to_compare is not value:
                all_rows.append(row)

    return all_rows


def distinct(my_rows):
    my_dict = {}
    d_rows = []
    for row in my_rows:
        if row not in my_dict:
            d_rows.append(row)
            my_dict[row] = True
    return d_rows


def split(my_list):
    new_list = []
    for i in my_list:
        if '.' in i:
            table_name, col_name = i.split('.')
            new_list.append(col_name)
        else:
            new_list.append(i)
    for i in new_list:
        if i == '':
            new_list.remove(i)
    return new_list


def asterisk(tokens,tables):
    from_index = tokens.index('FROM')
    table_name = tokens[from_index + 1]
    my_table = tables.get(table_name)
    my_rows = []
    for row in my_table.rows:
        my_rows.append(tuple(row))

    if 'WHERE' in tokens:
        my_rows = where(tokens, my_rows, my_table)
    if 'ORDER' in tokens:
        my_rows = order(tokens, my_rows, my_table)
    if 'DISTINCT' in tokens:
        my_rows = distinct(my_rows)
    return my_rows



def remove_duplicates(my_list):
    count = {}
    ans = []

    for el in my_list:
        datatype = type(el)
        if datatype not in count:
            count[datatype] = {el: 1}
        else:
            if el not in count[datatype]:
                count[datatype][el] = 1
            else:
                count[datatype][el] += 1

    for el in my_list:
        datatype = type(el)
        if count[datatype][el] == 1:
            ans.append(el)

    return ans

def create_table_join(table_name, columns,tables):
    if table_name in tables:
        del tables[table_name]
    columns = []  # empty list to hold columns
    my_table = Table(table_name, columns)
    tables[table_name] = my_table


def join_columns(columns, new_cols):
    for i in new_cols:
        columns.append(i)
    return columns

def create(tokens,tables):
    table_name = tokens[2]
    if "IF" in tokens and "NOT" in tokens and "EXISTS" in tokens:
        if table_name in tables:
            return
    elif table_name in tables:
        raise ValueError("Table already exists")

    columns = []
    col_tokens = tokens[4:-1]
    for i in range(0, len(col_tokens) - 1, 2):
        col_name = col_tokens[i]
        col_type = col_tokens[i + 1]
        columns.append((col_name, col_type))

    my_table = Table(table_name, columns)
    tables[table_name] = my_table

def insert(tokens,tables):
    table_name = tokens[2]
    if table_name in tables:
        my_table = tables.get(table_name)

        value_index = tokens.index('VALUES')
        column_names = tokens[4:value_index - 1]

        values = tokens[value_index + 2:]

        sublists = []
        curr = []
        for val in values:
            if val == '(':
                curr = []
            elif val == ')':
                sublists.append(curr)
                curr = []
            else:
                curr.append(val)

        values = [x for x in sublists if x]
        columns = my_table.columns

        if len(column_names) > 0:
            index_values = []
            for k in column_names:
                for i, j in enumerate(my_table.columns):
                    if k in j:
                        index_values.append(i)

            for value in values:
                row = [None] * len(columns)
                for i, index in enumerate(index_values):
                    if i < len(value):
                        row[index] = value[i]
                my_table.append(row)

        else:
            for value in values:
                row = []
                for i in value:
                    row.append(i)
                my_table.append(row)
    else:
        return None

def delete(tokens,tables):
    table_name = tokens[2]
    if table_name in tables:
        my_table = tables.get(table_name)

        if 'WHERE' in tokens:
            my_rows = where(tokens, my_table.rows, my_table)
        else:
            my_rows = []
            for row in my_table.rows:
                my_rows.append(list(row))
        for row in my_rows:
            my_table.remove(row)

def update(tokens,tables):
    table_name = tokens[1]
    set_index = tokens.index('SET')
    my_table = tables.get(table_name)
    my_rows = my_table.rows
    to_set = []

    if 'WHERE' in tokens:
        where_index = tokens.index('WHERE')
        to_set = tokens[set_index + 1: where_index]
        matching_rows = where(tokens, my_rows, my_table)  # Get the rows that match the WHERE condition
    else:
        to_set = tokens[set_index + 1:]
        matching_rows = my_rows  # If there's no WHERE condition, update all rows

    set_columns = []
    set_values = []

    for i in range(0, len(to_set), 3):
        if (i + 1) < len(to_set) and to_set[i + 1] == '=':
            set_columns.append(to_set[i])
            set_values.append(to_set[i + 2])

    updated_rows = []  # Create a separate list to store updated rows

    for row in my_rows:
        if row in matching_rows:  # Only update the rows that match the WHERE condition
            row_list = list(row)
            for i in range(len(set_columns)):
                column = set_columns[i]
                value = set_values[i]
                col_index, _ = column_index(my_table.columns, column)
                row_list[col_index] = value  # Evaluate the value without checking col_type

            updated_row = tuple(row_list)
        else:
            updated_row = row  # Keep the original row if it doesn't match the WHERE condition

        updated_rows.append(updated_row)  # Add the updated row to the updated_rows list

    my_table.rows = updated_rows  # Replace the original rows with the updated ones

def select(tokens,tables):
    if tokens[1] == '*':
        my_rows = asterisk(tokens,tables)
        return my_rows

    else:
        from_index = tokens.index('FROM')  # gets the 'from' index
        to_select_old = tokens[1:from_index]  # the column names to be selected
        to_select = split(to_select_old)
        table_name = tokens[from_index + 1]  # gets the table name.
        my_table = tables.get(table_name)  # gets the table.

        all_rows = []
        for row in my_table.rows:
            all_rows.append(tuple(row))

        if 'JOIN' in tokens and 'OUTER' in tokens and 'LEFT' in tokens:
            join_index = tokens.index('JOIN')
            left_table_name, left_col = tokens[join_index + 3].split('.')
            right_table_name, right_col = tokens[join_index + 5].split('.')
            left_table = tables.get(left_table_name)
            right_table = tables.get(right_table_name)

            all_rows = []
            none_rows = []
            left_columns = left_table.columns
            right_columns = right_table.columns

            left_col_idx, left_col_type = column_index(left_columns, left_col)
            right_col_idx, right_col_type = column_index(right_columns, right_col)

            for left_row in left_table.rows:
                issame = False
                for right_row in right_table.rows:
                    if left_row[left_col_idx] == right_row[right_col_idx]:
                        combined = left_row + right_row
                        all_rows.append(tuple(combined))
                        issame = True
                if not issame:
                    none_rows.append(tuple([None] * len(left_columns)))
            columns = []
            new_left_cols = left_columns
            new_right_cols = right_columns

            columns = join_columns(columns, new_left_cols)
            columns = join_columns(columns, new_right_cols)

            new_table_name = 'join'
            new_table = Table(new_table_name, columns)

            new_rows = all_rows
            if 'WHERE' in tokens:
                new_rows = where(tokens, all_rows, new_table)

            if 'ORDER' in tokens:
                new_rows = order(tokens, all_rows, new_table)

            my_rows = []
            for i in new_rows:
                row = remove_duplicates((i))
                my_rows.append(tuple(row))

            my_rows_f = my_rows + none_rows

            if 'DISTINCT' in tokens:
                my_rows_f = distinct(my_rows_f)

            return my_rows_f

        if 'WHERE' in tokens:
            all_rows = where(tokens, all_rows, my_table)

        if 'ORDER' in tokens:
            all_rows = order(tokens, all_rows, my_table)

        index_values = []
        for k in to_select:
            if k == '*':
                for i, j in enumerate(my_table.columns):
                    index_values.append(i)
            else:
                for i, j in enumerate(my_table.columns):
                    if k in j:
                        index_values.append(i)
                        break
        my_rows = []  # Rows to be returned
        for row in all_rows:
            selected_row = []
            for i in index_values:
                selected_row.append(row[i])
            if selected_row:
                my_rows.append(tuple(selected_row))

        if 'DISTINCT' in tokens:
            my_rows = distinct(my_rows)

        return my_rows
