"""
	#!      --  Что-то критическое
	#?      --  Нужен ли этот код
	#//     --  Тестовый блок
	#TODO:  --  То, что нужно сделать в первую очередь
	#*      --  Выделение очень важного

	#! Продумать момент с выдачей пользователям логинов и паролей

	#TODO: 1) Доделать дату дедлайна задачи


	#* Тестовые SQL-запросы:

		INSERT INTO RolePermissions(name, create_tasks, join_tasks, inviting) VALUES ("Капитан", 1, 1, 1);

		--DELETE FROM Tasks WHERE id == 1;
		--INSERT INTO Tasks(task, is_done, deadline, team_id) VALUES ("Сделать проект 1", 0, "2021-04-20 00:00:00", 1);
		--INSERT INTO Tasks(task, is_done, deadline, team_id) VALUES ("Сделать проект 2", 1, "2021-04-19 00:00:00", 1);

		INSERT INTO TaskUsers VALUES (1, 1);
		INSERT INTO TaskUsers VALUES (1, 2);
		INSERT INTO TaskUsers VALUES (2, 1);


		INSERT INTO Teams(name) VALUES ('TeamWorker')

		INSERT INTO RolePermissions(create_tasks, join_tasks, inviting) VALUES ('True', 'True', 'True')
		INSERT INTO Users(login, password, name, role, team_id, role_id) VALUES ('admin', '12345', 'Tolya', 'Capitan', 1, 1)

		INSERT INTO RolePermissions(create_tasks, join_tasks, inviting) VALUES ('True', 'True', 'True')
		INSERT INTO Users(login, password, name, role, team_id, role_id) VALUES ('someLogin', '12345', 'Dima', 'Programmer', 1, 2)

		INSERT INTO RolePermissions(create_tasks, join_tasks, inviting) VALUES ('True', 'True', 'True')
		INSERT INTO Users(login, password, name, role, team_id, role_id) VALUES ('otherLogin', '12345', 'Liza', 'Designer', 1, 3)

		INSERT INTO RolePermissions(create_tasks, join_tasks, inviting) VALUES ('True', 'True', 'True')
		INSERT INTO Users(login, password, name, role, team_id, role_id) VALUES ('thirdLogin', '12345', 'Vitaly', 'Analyzer', 1, 4)



		DELETE FROM Users;
		DELETE FROM RolePermissions;
		DELETE FROM Teams;

		-- INSERT INTO Teams(name) VALUES ("Capitans");
		-- INSERT INTO RolePermissions(create_tasks, join_tasks, inviting, team_id) VALUES ("True", "True", "True", 0); 
"""
from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


from . import controllers
db.create_all()  # Создаёт файл базы данных с таблицами, если его нет
from .models import User, Task, Team, RolePermission


if __name__ == '__main__':
	manager.run(
		host='127.0.0.1',
		port=5000,
		debug=True
	)
