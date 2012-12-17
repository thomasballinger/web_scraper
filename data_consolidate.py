from database_static import static_data
from database_matches import get_player_match_stats, get_calendar_for_player
from pymongo import Connection
from urlparse import urlsplit
import sys, os

def set_perm_scores(name):
	return static_data(name)

def set_calendar_stats(name):
	calendar = get_calendar_for_player(name)
	for day in calendar:
		url = day['url']
		day.update(get_player_match_stats(url,name))
	return calendar

def make_database():
	db.footballparser.remove()
	db.footballpermanent.remove()
	for name in ['Moussa Dembele', 'Marouane Fellaini', 'Romelu Lukaku', 'Simon Mignolet', 'Thomas Vermaelen', 'Jan Vertonghen']:
		db.footballparser.insert(set_calendar_stats(name))
		db.footballpermanent.insert(set_perm_scores(name))

if __name__ == '__main__':
#	url = 'mongodb://heroku_app9943363:ltoo03cli1dnufi04kepkljv4l@ds045147.mongolab.com:45147/heroku_app9943363'
	url=os.environ.get('MONGOLAB_URI', 'mongodb://localhost:27017')
	if url == 'mongodb://localhost:27017':
		db_name = 'test'
		db = Connection(url)[db_name]
	else:
		port_number = int(os.environ.get('PORT', 5000))
		parsed = urlsplit(url)
		db_name = parsed.path[1:]
		db = Connection(url)[db_name]
#		user_pass = parsed.netloc.split('@')[0].split(':')
	make_database()