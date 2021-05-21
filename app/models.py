from app import db


task_users = db.Table('TaskUsers',
	db.Column('user_id', db.Integer, db.ForeignKey('Users.id')),
	db.Column('task_id', db.Integer, db.ForeignKey('Tasks.id'))
)


'''
	#* user.executors
	#* task.users
	included_members = db.relationship('Member', secondary=bot_members, backref='members')
	Из одного обращался по included_members , в другом - members
'''


class User(db.Model):
	__tablename__ = 'Users'

	id = db.Column(db.Integer(), primary_key=True)
	login = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(100), nullable=False)  # Хэш пароля после регистрации
	name = db.Column(db.String(50), nullable=False)
	role = db.Column(db.String(50), nullable=False, default="Капитан")

	# Связь с <Teams>
	team_id = db.Column(db.Integer(), db.ForeignKey('Teams.id'))
	# Связь с <RolePermission>
	role_id = db.Column(db.Integer(), db.ForeignKey('RolePermissions.id'))

	#? tasks = db.relationship('Task', secondary=task_users, backref=db.backref('executors', lazy='dynamic'))  # 'lazy'

	def __repr__(self) -> str:
		return f'<object Users(\n\tid: {self.id},\n\tlogin: {self.login},\n\tpassword: {self.password},\n\tname: {self.name},\n\trole: {self.role},\n\n\tteam_id: {self.team_id},\n\trole_id: {self.role_id}\n)>'


class Task(db.Model):
	__tablename__ = 'Tasks'

	id = db.Column(db.Integer(), primary_key=True)
	task = db.Column(db.String(100), nullable=False)
	is_done = db.Column(db.Boolean(), default=False, nullable=False)
	deadline = db.Column(db.DateTime())  # TODO: Доделать дату дедлайна задачи

	team_id = db.Column(db.Integer(), db.ForeignKey('Teams.id'))

	users = db.relationship('User', secondary=task_users, backref=db.backref('executors', lazy='dynamic'))  # 'lazy' - Данные подгружаются только в момент обращения

	def __repr__(self) -> str:
		return f'<object Tasks(\n\tid: {self.id},\n\ttask : {self.task},\n\tis_done: {self.is_done},\n\tdeadline: {self.deadline}\n\n\tteam_id: {self.team_id}\n)>'


'''
	class TaskUser(db.Model):
		"""
			Является промежуточной таблицей между Users и Tasks.
			Обеспечивает связь Многие ко многим (М:М)
		"""
		__tablename__ = 'TaskUsers'

		id = db.Column(db.Integer(), primary_key=True)  # Нужно, чтобы sqlalchemy воспринимал

		# Связь с <Task>
		task_id = db.Column(db.Integer(), db.ForeignKey('Tasks.id'))
		# Связь с <User>
		user_id = db.Column(db.Integer(), db.ForeignKey('Users.id'))

		def __repr__(self) -> str:
			return f'<object TaskUsers(id: {self.id}, task_id: {self.task_id}, user_id: {self.user_id})>'
'''

class Team(db.Model):
	__tablename__ = 'Teams'

	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), nullable=False, unique=True)

	def __repr__(self) -> str:
		return f'<object Teams(id: {self.id}, name: {self.name})>'


class RolePermission(db.Model):
	__tablename__ = 'RolePermissions'

	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), nullable=False)  #?
	create_tasks = db.Column(db.Boolean(), default=False, nullable=False)
	join_tasks = db.Column(db.Boolean(), default=False, nullable=False)
	inviting = db.Column(db.Boolean(), default=False, nullable=False)

	def __repr__(self) -> str:
		return f'<object RolePermissions(\n\tid: {self.id},\n\tname: {self.name},\n\tcreate_tasks: {self.create_tasks},\n\tjoin_tasks: {self.join_tasks},\n\tinviting: {self.inviting}\n)>'


"""
	from flask.ext.sqlalchemy import SQLAlchemy
	from werkzeug import generate_password_hash, check_password_hash

	db = SQLAlchemy()

	class User(db.Model):
		__tablename__ = 'users'
		uid = db.Column(db.Integer, primary_key = True)
		firstname = db.Column(db.String(100))
		lastname = db.Column(db.String(100))
		email = db.Column(db.String(120), unique = True)
		pwdhash = db.Column(db.String(54))    

		def __init__(self, firstname, lastname, email, password):
			self.firstname = firstname.title()
			self.lastname = lastname.title()
			self.email = email.lower()
			self.set_password(password)

		def set_password(self, password):
			self.pwdhash = generate_password_hash(password)

		def check_password(self, password):
			return check_password_hash(self.pwdhash, password)
"""
