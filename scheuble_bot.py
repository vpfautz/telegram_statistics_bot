import telepot
from telepot.loop import MessageLoop
import time
# from pprint import pprint
import sys


"""
$ python scheuble_bot.py <token>

Counts messages from users and can display who sent how many.
"""

counts = {}

def handle(msg):
	# print ""
	# print "#"*40
	# pprint(msg)

	chat_id = msg["chat"]["id"]

	if not chat_id in counts:
		counts[chat_id] = {}

	sender_id = msg["from"]["id"]

	if not sender_id in counts[chat_id]:
		counts[chat_id][sender_id] = {}
		counts[chat_id][sender_id]["count"] = 0
		counts[chat_id][sender_id]["username"] =  msg["from"]["first_name"]

	counts[chat_id][sender_id]["count"] += 1

	if not "text" in msg:
		return

	text = msg["text"]

	if text == "/mystats" or text == "/mystats@scheuble_bot":
		bot.sendMessage(chat_id, "You sent %s messages in this channel." % counts[chat_id][sender_id]["count"])
		return

	if text == "/top" or text == "/top@scheuble_bot":
		out = ""
		print  sorted(counts[chat_id].values(), key=lambda x:x["count"], reverse=True)
		for user in sorted(counts[chat_id].values(), key=lambda x:x["count"], reverse=True):
			out += "%s (%s)\n" % (user["username"], user["count"])
		bot.sendMessage(chat_id, out)
		return


TOKEN = sys.argv[1]

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()

print "Listening..."
while True:
	time.sleep(10)
