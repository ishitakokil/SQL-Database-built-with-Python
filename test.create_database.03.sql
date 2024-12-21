FILENAME: test3.db
1: CREATE TABLE names (name TEXT, id INTEGER);
1: INSERT INTO names VALUES ('James', 1), ('Yaxin', 3), ('Li', 2), (NULL, 4);
1: SELECT * FROM names ORDER BY id;
1: CREATE TABLE grades (id INTEGER, grade REAL);
1: INSERT INTO grades VALUES (3, 3.0);
1: INSERT INTO grades VALUES (1, 2.0);
1: INSERT INTO grades VALUES (2, 3.5);
1: SELECT * FROM grades ORDER BY id;
1: SELECT names.name, grades.grade FROM names LEFT OUTER JOIN grades ON names.id = grades.id ORDER BY names.id;
1: CLOSE