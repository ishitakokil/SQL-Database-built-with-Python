OPEN: test3.db
1: SELECT names.name, grades.grade FROM names LEFT OUTER JOIN grades ON names.id = grades.id ORDER BY names.id;
1: UPDATE names SET name = 'James Jr.' WHERE name = 'James';
1: SELECT * FROM names ORDER BY id;
1: SELECT names.name, grades.grade FROM names LEFT OUTER JOIN grades ON names.id = grades.id ORDER BY names.id;
1: ENDTEST