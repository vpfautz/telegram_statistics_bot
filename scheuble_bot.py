import telepot
from telepot.loop import MessageLoop
import time
# from pprint import pprint
import sys
import sqlite3


"""
$ python scheuble_bot.py <token>

Counts messages from users and can display who sent how many.
"""



def init_db():
	conn = sqlite3.connect('stats.db')
	c = conn.cursor()

	# Create table
	c.execute('CREATE TABLE IF NOT EXISTS counts (chat_id int, sender_id int, username text, count int)')

def inc_count(chat_id, sender_id, username):
	conn = sqlite3.connect('stats.db')
	c = conn.cursor()

	c.execute('SELECT count FROM counts where chat_id=? and sender_id=?', (chat_id, sender_id))
	r = c.fetchone()

	if not r:
		c.execute("INSERT INTO counts VALUES (?, ?, ?, ?)", (chat_id, sender_id, username, 1))
		conn.commit()
		return

	count = r[0] + 1

	c.execute("UPDATE counts set count=? where chat_id=? and sender_id=?", (count, chat_id, sender_id))
	conn.commit()

def get_count(chat_id, sender_id):
	conn = sqlite3.connect('stats.db')
	c = conn.cursor()

	c.execute('SELECT count FROM counts where chat_id=? and sender_id=?', (chat_id, sender_id))
	r = c.fetchone()

	if not r:
		return 0
	else:
		return r[0]

def get_top(chat_id):
	conn = sqlite3.connect('stats.db')
	c = conn.cursor()

	r = c.execute('SELECT username, count FROM counts where chat_id=? order by count desc', (chat_id,))
	return r.fetchall()

def reset_count(chat_id, sender_id):
	conn = sqlite3.connect('stats.db')
	c = conn.cursor()

	c.execute('DELETE FROM counts where chat_id=? and sender_id=?', (chat_id, sender_id))
	conn.commit()


counts = {}

def handle(msg):
	# print ""
	# print "#"*40
	# pprint(msg)

	chat_id   = msg["chat"]["id"]
	sender_id = msg["from"]["id"]
	username  = msg["from"]["first_name"]

	inc_count(chat_id, sender_id, username)

	if not "text" in msg:
		return

	text = msg["text"]

	if text == "/mystats" or text == "/mystats@scheuble_bot":
		bot.sendMessage(chat_id, "You sent %s messages in this channel." % get_count(chat_id, sender_id))
		return

	if text == "/top" or text == "/top@scheuble_bot":
		out = ""
		for user in get_top(chat_id):
			out += "%s (%s)\n" % user
		bot.sendMessage(chat_id, out)
		return


TOKEN = sys.argv[1]

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()

print "Listening..."
while True:
	time.sleep(10)
