#!/usr/bin/env python2.7
# coding=utf-8

import sqlite3

from time import localtime, mktime, strftime, strptime, tzset
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from functools import wraps
from hashlib import sha512, md5
from json import dumps
from os import path, urandom

__author__ = 'Kevin D.'
__version__ = '1.0.0'
__license__ = 'WTFPL'

# Configuration
DATABASE = path.join(path.dirname(__file__), 'tippspiel.db')
DEBUG = False
SECRET_KEY = 'Some very secret key here. Of course, this is not the one that I used in the running version.'


# Correct timezone for the app
def set_timezone():
	from os import environ
	environ['TZ'] = 'Europe/Berlin'
	tzset()

# Gives current timestamp
def now():
	return int(mktime(localtime()))

# Method for connecting an sqlite3 database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

# Easier queries - save some loc
def query_db(query, args=(), one=False):
	cur = g.db.execute(query, args)
	rv = [dict((cur.description[idx][0], value) for idx, value in enumerate(row)) for row in cur.fetchall()]
	return (rv[0] if rv else None) if one else rv

# Check if user is logged in
def logged_in():
	if not g.user:
		return False
	return True

def require_login(f):
	@wraps(f)
	def decorated_f(*args, **kwargs):
		if not logged_in():
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_f

# Check if a tipp is still possible or if time's up
def tipp_legal(time):
	return time > g.time

# Calculate points for a tipp
def calc_points(sh, sv, th, tv):
	if -1 in [sh, sv, th, tv]:
		return 0
	sgn = lambda x: 0 if x==0 else x/abs(x)
	points = 0
	ds = sh-sv
	dt = th-tv
	if sgn(ds)==sgn(dt):
		# correct tendency
		points += 1
		if ds==dt:
			# correct difference
			points += 1
			if sh==th:
				# correct result
				points += 1
	return points

# ---- Password related stuff ----
def hash_sha512(pw, salt=0):
	if salt == 0:
		salt = int(urandom(16).encode('hex'), 16)
	return (salt, sha512(`salt` + pw).hexdigest())

def check_pw(attempt, secret):
	salt, hashed_secret = secret.split(":")
	hashed_attempt = hash_sha512(attempt, int(salt))[1]
	if hashed_attempt == hashed_secret:
		return True
	return False

def generate_pw(length=12):
	import string as s
	chars = s.ascii_letters + s.digits + s.punctuation
	pw = ''.join([chars[int(urandom(16).encode('hex'), 16)%len(chars)] for i in range(0, length)])
	return {
		'clear': pw,
		'hashed': "%s:%s" % hash_sha512(pw)
	}
# --------------------------------


# Create the app
app = Flask(__name__)
app.config.from_object(__name__)
set_timezone()


# Connect to the database and do other stuff before everything else.
@app.before_request
def before_request():
	if not app.debug:
		# Logging into file...
		import logging
		file_handler = logging.FileHandler(path.join(path.dirname(__file__), 'tippspiel_errors.txt'))
		file_handler.setLevel(logging.WARNING)
		app.logger.addHandler(file_handler)
	g.db = connect_db()
	g.time = now()
	# check for login
	g.user = None
	if 'tipp_user_id' in session:
		u = query_db('select user_id, user_name, user_score, user_rank, user_role from users where user_id = ?', [session['tipp_user_id']], one=True)
		if not u:
			flash(u'Da war wohl ein nicht-existenter Benutzer eingeloggt. Sowas sollte nicht passieren!', 'error')
			return redirect(url_for('logout'))
		g.user = {
			'id': u['user_id'],
			'name': u['user_name'],
			'is_admin': bool(u['user_role']),
			'score': u['user_score'],
			'rank': u['user_rank']
		}

# Always close the database when finished.
@app.teardown_request
def teardown_request(exception):
	g.db.close()


# Routes
@app.route('/')
@require_login
def index():
	return render_template('landing.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if logged_in():
		return redirect(url_for('index'))
	if request.method == 'POST':
		err = False
		user_name = request.form['user']
		pw_attempt = request.form['pass']
		if user_name == '':
			flash(u'Es wurde kein Benutzername angegeben.', 'error')
			err = True
		if pw_attempt == '':
			flash(u'Es wurde kein Passwort angegeben.', 'error')
			err = True
		if not err:
			user = query_db('select user_id, user_name, user_pass, user_score, user_role from users where user_name = ?', [user_name], one=True)
			if not user:
				flash(u'Es wurde kein Benutzer gefunden.', 'error')
				err = True
			else:
				if not check_pw(pw_attempt, user['user_pass']):
					flash(u'Das eigegebene Passwort ist ungültig.', 'error')
					err = True
				else:
					session['tipp_user_id'] = user['user_id']
					flash(u'Du wurdest erfolgreich eingeloggt. Viel Spaß beim Tippen!', 'success')
		if not err:
			return redirect(url_for('index'))
	return render_template('login.html')


@app.route('/logout')
@require_login
def logout():
	session.pop('tipp_user_id', None)
	flash(u'Du wurdest ausgeloggt. Bis bald.', 'success')
	return redirect(url_for('index'))


@app.route('/schedule')
@require_login
def schedule():
	matches = query_db('select match_id, match_time, match_group, match_team_home, match_team_visitor, match_score_home, match_score_visitor from matches order by match_time asc')
	tipps = query_db('select * from tipps where tipp_user = ?', [g.user['id']])
	tipps_by_match = dict([(t['tipp_match'], t) for t in tipps])
	for match in matches:
		match['time'] = strftime('%d.%m %H:%M', localtime(match['match_time']))
		match['tipp_legal'] = tipp_legal(match['match_time'])
		if match['match_id'] in tipps_by_match:
			match['tipp'] = tipps_by_match[match['match_id']]
			if not match['tipp_legal']:
				match['tipp_points'] = calc_points(
					match['match_score_home'],
					match['match_score_visitor'],
					match['tipp']['tipp_score_home'],
					match['tipp']['tipp_score_visitor']
				)
	return render_template('schedule.html', active='schedule', matches=matches)


@app.route('/match/<match_id>')
@require_login
def match(match_id):
	match = query_db('select * from matches where match_id = ? and match_time<?', [match_id, g.time], one=True)
	tipps = query_db('select * from tipps left join users on tipp_user=user_id where tipp_match = ? order by user_name', [match_id])
	if not match:
		flash(u'Für dieses Spiel können noch Tipps abgegeben werden.')
		return redirect(url_for('schedule'))
	if match['match_score_home'] != -1 and match['match_score_visitor'] != -1:
		for tipp in tipps:
			tipp['points'] = calc_points(match['match_score_home'], match['match_score_visitor'], tipp['tipp_score_home'], tipp['tipp_score_visitor'])
	return render_template('match.html', match=match, tipps=tipps)


@app.route('/tipp/<match_id>', methods=['GET', 'POST'])
@require_login
def tipp(match_id):
	match = query_db('select * from matches where match_id = ?', [match_id], one=True)
	tipp = query_db('select * from tipps where tipp_match = ? and tipp_user = ?', [match_id, g.user['id']], one=True)

	if not match:
		flash(u'Dieses Spiel konnte nicht gefunden werden.', 'error')
		return redirect(url_for('schedule'))
	if not tipp_legal(match['match_time']):
		flash(u'Für dieses Spiel kannst du keinen Tipp mehr abgeben.', 'error')
		return redirect(url_for('schedule'))

	if request.method == 'POST':
		# check input
		tipp_home = int(request.form['inputTippHome'])
		tipp_visitor = int(request.form['inputTippVisitor'])
		if tipp_home < 0 or tipp_visitor < 0:
			flash('Kein gültiger Tipp!', 'error')
			return redirect(url_for('tipp', match_id=match_id))
		if not tipp:
			# create new tipp
			g.db.execute(
				'insert into tipps (tipp_time, tipp_match, tipp_user, tipp_score_home, tipp_score_visitor) values (?, ?, ?, ?, ?)',
				[
					g.time,
					match_id,
					g.user['id'],
					tipp_home,
					tipp_visitor,
				]
			)
		else:
			# edit existing
			g.db.execute('update tipps set tipp_time = ?, tipp_score_home = ?, tipp_score_visitor = ? where tipp_id = ?',
				[
					g.time,
					tipp_home,
					tipp_visitor,
					tipp['tipp_id']
				]
			)
		try:
			g.db.commit()
		except:
			flash('Es ist ein Fehler aufgetreten! Bitte versuche es erneut.', 'error')
			return redirect(url_for('tipp', match_id=match_id))
		flash('Dein Tipp wurde gespeichert.', 'success')
		return redirect(url_for('schedule'))

	return render_template('tipp.html', match=match, tipp=tipp)


@app.route('/ranking')
@require_login
def ranking():
	users = query_db('select user_id, user_name, user_rank, user_score from users order by user_score desc, user_name')
	return render_template('ranking.html', active='ranking', users=users)


@app.route('/user/<userid>')
@require_login
def user(userid):
	if userid==g.user['id']:
		return redirect(url_for('schedule'))
	user = query_db('select user_name, user_mail, user_score, user_rank from users where user_id=?', [userid], one=True)
	if not user:
		flash(u'Es wurde kein Benutzer gefunden.', 'error')
		return redirect(url_for('ranking'))
	tipps = query_db('select * from tipps left join matches on tipp_match=match_id where tipp_user=? and match_time<?', [userid, g.time])
	for tipp in tipps:
		tipp['tipp_points'] = calc_points(tipp['match_score_home'], tipp['match_score_visitor'], tipp['tipp_score_home'], tipp['tipp_score_visitor'])
	user['gravatar'] = md5(user['user_mail']).hexdigest()
	return render_template('user.html', user=user, tipps=tipps)


@app.route('/settings', methods=['GET', 'POST'])
@require_login
def settings():
	if request.method == 'POST':
		npw = request.form['pass_new']
		npwc = request.form['pass_new_confirm']
		if npw == '':
			flash(u'Es wurde kein neues Passwort eingegeben.', 'error')
		elif npw != npwc:
			flash(u'Die eingegeben Passwörter stimmen nicht überein.', 'error')
		elif len(npw) < 8:
			flash(u'Also mindestens acht Zeichen lang sollte das Passwort schon sein...', 'error')
		else:
			try:
				new_hash = "%s:%s" % hash_sha512(npw)
				g.db.execute('update users set user_pass = ? where user_id = ?', [new_hash, g.user['id']])
				g.db.commit()
				flash(u'Dein Passwort wurde erfolgreich geändert.', 'success')
			except Exception, e:
				flash(u'Es ist ein Fehler aufgetreten. Dein Passwort wurde nicht geändert.', 'error')
	return render_template('settings.html')


# purely experimental not for release /* okay, I leave it in here, so you can laugh... */
@app.route('/feedback', methods=['GET', 'POST'])
@require_login
def feedback():
	filename = path.join(path.dirname(__file__), 'feedback/%s.mdown' % g.user['name'])
	if request.method == 'POST':
		text = request.form['inputText']
		try:
			with open(filename, mode='w+') as f:
				f.write(text)
			flash(u'Dein Feedback wurde gespeichert. Vielen Dank!', 'success')
		except:
			text = None
			flash(u'Das Feedback konnte nicht gespeichert werden.', 'error')
	else:
		try:
			with open(filename) as f:
				text = f.read()
		except:
			text = None
	return render_template('feedback.html', text=text)


@app.route('/admin', methods=['GET', 'POST'])
@require_login
def admin():
	if not g.user['is_admin']:
		return redirect(url_for('index'))
	res = None
	q = None
	if request.method == 'POST':
		q = request.form['query']
		try:
			if q.lower().startswith('select'):
				res = dumps(query_db(q), indent=2)
			else:
				g.db.execute(q)
				g.db.commit()
				flash('Query successfull!', 'success')
		except Exception, e:
				flash('Error in your query: %s' % e, 'error')
	return render_template('admin.html', active='admin', q=q, res=res)


@app.route('/admin/randompw')
@require_login
def admin_randompw():
	if not g.user['is_admin']:
		return redirect(url_for('index'))
	return dumps(generate_pw())


@app.route('/admin/recalc')
@require_login
def admin_recalc():
	if not g.user['is_admin']:
		return redirect(url_for('index'))
	# Recalculate scores
	tipps_and_matches = query_db('select * from tipps left join matches on tipp_match=match_id where match_time<?', [g.time])
	tam_by_users = {}
	for tam in tipps_and_matches:
		if not tam['tipp_user'] in tam_by_users:
			tam_by_users[tam['tipp_user']] = []
		tam_by_users[tam['tipp_user']].append(tam)
	for userid, tam in tam_by_users.iteritems():
		points = sum(calc_points(x['match_score_home'], x['match_score_visitor'], x['tipp_score_home'], x['tipp_score_visitor']) for x in tam)
		try:
			g.db.execute('update users set user_score=? where user_id=?', [points, userid])
			g.db.commit()
		except Exception, e:
			flash('Could not update score for user %d: %s' % (userid, e), 'error')
	# Recalculate ranking
	users = query_db('select user_id, user_score, user_rank from users order by user_score desc')
	rank, tick, score = 1, 0, users[0]['user_score']
	for user in users:
		if user['user_score'] < score:
			rank += tick
			tick = 1
			score = user['user_score']
		else:
			tick += 1
		if user['user_rank'] != rank:
			try:
				g.db.execute('update users set user_rank=? where user_id=?', [rank, user['user_id']])
				g.db.commit()
			except Exception, e:
				flash('Could not update rank for user %d: %s' % (user['user_id'], e), 'errror')
	return render_template('admin.html', active='admin')


@app.route('/admin/backupdb')
@require_login
def admin_backupdb():
	if not g.user['is_admin']:
		return redirect(url_for('index'))
	g.db.close()
	from shutil import copy2
	src = app.config['DATABASE']
	dst = path.join(path.dirname(__file__), 'db_backup', '%s.db' % g.time)
	try:
		copy2(src, dst)
		flash('Backup successfull. Saved as %s' % dst, 'success')
	except Exception, e:
		flash('%s' % e, 'error')
	return render_template('admin.html', active='admin')


@app.route('/admin/time')
@require_login
def admin_time():
	if not g.user['is_admin']:
		return redirect(url_for('index'))
	return "%s" % strftime('%d.%m %H:%M', localtime(g.time))


@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404



# Starting point for running the app locally.
if __name__ == '__main__':
	set_timezone()
	#app.run(host='0.0.0.0')
	app.run()



# --- Method for installing the app ---
# Only to be used from console.
def setup():
	print('[Setup tippspiel]')
	if raw_input('Continue? ') != 'yes':
		print('Setup borted.')
		return
	with closing(connect_db()) as db:
		db.text_factory = str
		# Import schema
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		# Load match plan
		with app.open_resource('schedule.txt') as schedule:
			for line in schedule.read().split('\n'):
				data = line.split(';')
				match = [
					int(mktime(strptime(data[1], '%d.%m.%Y %H:%M'))),
					data[0],
					data[2],
					data[3]
				]
				db.execute('insert into matches (match_time, match_group, match_team_home, match_team_visitor, match_score_home, match_score_visitor) values (?, ?, ?, ?, -1, -1)', match)
		# Add user for testing
		db.execute('insert into users (user_name, user_mail, user_pass, user_score, user_rank, user_role) values (?, ?, ?, 235, 1, 1)', ['Admin', 'your@mail.com', "%s:%s" % hash_sha512('default')])
		db.commit()
		print('Done!')
# -------------------------------------

