from app import app, db
from .models import User, Task, Team, RolePermission

from flask import make_response, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

import json


@app.route('/')
def index():
	
	capitan_rp = RolePermission.query.filter_by(name="Капитан").first()
	if not capitan_rp:

		rp = RolePermission(
				name="Капитан",
				create_tasks=1,
				join_tasks=1,
				inviting=1
		)
		db.session.add(rp)
		db.session.commit()

		return make_response('Capitan rp', 201)

	return make_response('dima pidor', 200)


@app.route("/register", methods=["POST", "GET"])
def register():

	if request.method == "POST":

		data = request.json
		print(json.dumps(data, indent=4, ensure_ascii=False))  #// (test_block)

		team_name = data['team_name']
		users = data['users']
		roles = data['roles']

		# TODO: Проверка корректности полученых данных

		# Проверка имени команды
		if Team.query.filter_by(name=team_name).first():
			print('Название команды уже занято')
			return make_response('Название команды уже занято', 409)  # 409 - «конфликт»

		# Проверка на присутсвие хотя бы одного пользователя
		elif len(users) == 0:
			print('Отсутствуют участники команды')
			return make_response('Отсутствуют участники команды', 406)  # 406 - «неприемлемо»

		# Добавляем в 'Teams'
		t = Team(name=team_name)
		db.session.add(t)
		db.session.flush()  #* Временные изменения
		print(t)  #// (test_block)

		# Добавляем сначала 'RolePermissions', а затем в 'Users' каждого пользователя
		for role in roles:

			rp = RolePermission(
				name=role["role_name"],
				create_tasks=role["create_tasks"],
				join_tasks=role["join_tasks"],
				inviting=role["inviting"],
			)

			db.session.add(rp)
			db.session.flush()
			print(rp)  #// (test_block)

		for user in users:

			# Ищем уже переданную роль или роль Капитана, чтобы в последствии взять id
			role = RolePermission.query.filter_by(name=user['user_role']).first()

			u = User(
				login=user['user_login'],
				password=generate_password_hash(user['user_password']),  # Хэширование пароля
				name=user['user_name'],
				role=user['user_role'],

				team_id=t.id,
				role_id=role.id
			)

			# https://stackoverflow.com/questions/4201455/sqlalchemy-whats-the-difference-between-flush-and-commit
			db.session.add(u)
			db.session.flush()
			print(u)  #// (test_block)

		db.session.commit()  #* Всегда сохраняет изменения

		return make_response(f"Команда успешно зарегистрирована", 201)  # 201 - "создано"

	return make_response("register", 200)


@app.route("/enter", methods=["POST", "GET"])
def enter():

	if request.method == "POST":

		data = request.json
		login = data['login']
		password = data['password']

		#// (test_block)
		print(json.dumps(data, indent=4))

		user = User.query.filter_by(login=login).first()
		print(user)  #// (test_block)

		# Если не находит пользователя, то кидает bad response
		if not user:
			return make_response("Пользователь не найден", 404)
		
		# Если неверный пароль
		elif not check_password_hash(user.password, password):
			return make_response("Неверный пароль", 406)
		
		return make_response(f"Успешный вход пользователя {login}", 200)

	return make_response('enter', 200)


@app.route("/is-login-unique", methods=["POST", "GET"])
def is_login_unique():

	if request.method == "POST":

		print(json.dumps(request.json, indent=4))  #// (test_block)
		login = request.json['login']
		
		user = User.query.filter_by(login=login).first()
		if user:
			return make_response("Такой логин уже существует", 409)
		
		return make_response("Уникальный логин", 200)
	
	return make_response('is-login-unique', 200)


@app.route('/push_tasks_info', methods=["POST", "GET"])  #!!!
def push_tasks_info():

	from datetime import datetime
	
	if request.method == "POST":

		'''
			...
				{
					"task_text":f"Сосать бибу {i}",
					"task_users_login":["huesos1login","huesos2login"],
					"task_users":["хуесос 1", "Хуесос 2"],
					"task_deadline":"21 апреля, 2021",
					"task_is_done":0
				}
			...
		'''

		tasks = request.json
		print("tasks: ", json.dumps(tasks, ensure_ascii=False))

		for task in tasks['tasks_data']:
			
			t = Task(
				task=task['task_text'],
				is_done='task_is_done',
				deadline=...
			)
			db.session.add(t)
			db.session.flush()

	return make_response('push_tasks_info', 200)


@app.route('/get_tasks_info', methods=["POST", "GET"])
def get_tasks_info():
	
	if request.method == "POST":
		account_login = request.json['account_login']
		print("account_login", account_login)
		
		user = User.query.filter_by(login=account_login).first()

		if not user:
			return make_response("Пользователь не найден", 404)
		
		team = Team.query.filter(Team.id == user.team_id).first()
		print(team)

		tasks = Task.query.filter_by(team_id=user.team_id).all()  # Все задачи, принадлежащие команде
		print(tasks)

		tasks_data: list = []  # Список словарей

		for task in tasks:
			print("task_users: ", task.users)
			
			task_dict = {}

			task_dict["task_text"] = task.task
			task_dict["task_user_logins"] = [user.login for user in task.users]
			task_dict["task_user_names"] = [user.name for user in task.users]
			task_dict["task_deadline"] = task.deadline
			task_dict["task_is_done"] = task.is_done

			tasks_data.append(task_dict)

		return jsonify({'tasks_data': tasks_data})
		
	return make_response('get_tasks_info', 200)


@app.route('/get_team_users', methods=["POST", "GET"])
def get_team_users():

	if request.method == "POST":

		account_login = request.json['account_login']

		user = User.query.filter_by(login=account_login).first()

		if not user:
			return make_response('Пользователь не найден', 404)

		users = User.query.filter_by(team_id=user.team_id).all()

		data = {
			'user_logins': [],
			'user_names': []
		}

		for user in users:

			data['user_logins'].append(user.login)
			data['user_names'].append(user.name)

		return jsonify(data)
	
	return make_response("get_team_users", 200)


@app.route('/get_team_name', methods=["POST", "GET"])
def get_team_name():
	
	if request.method == "POST":
		
		account_login = request.json['account_login']
		user = User.query.filter_by(login=account_login).first()
		if not user:
			return make_response('Пользователь не найден', 404)

		team = Team.query.filter_by(id=user.team_id).first()

		return jsonify({'team_name': team.name})

	return make_response('get_team_name', 200)


@app.route("/drop_all", methods=["POST", "GET"])
def drop_all():
	""" Нужна лишь для ускорения разработки """
	try:

		users = User.query.all()
		for user in users:
			db.session.delete(user)

		roles = RolePermission.query.all()
		for role in roles:
			db.session.delete(role)
		
		teams = Team.query.all()
		for team in teams:
			db.session.delete(team)

		tasks = Task.query.all()
		for task in tasks:
			db.session.delete(task)
		
		# task_users = TaskUser.query.all()
		# for task_user in task_users:
		# 	db.session.delete(task_user)

		db.session.commit()

	except Exception as e:
		print(e)
		db.session.rollback()

		return make_response('drop_all', 400)

	return make_response('drop_all', 200)
