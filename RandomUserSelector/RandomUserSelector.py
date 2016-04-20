# -*- coding: utf-8 -*-

"""
A script that selects random users and add them as approved submitters
Written by /u/SmBe19, /u/wataqo, /u/baconwiches and /u/_rya_
"""

import praw
import random
import time
import OAuth2Util

# ### USER CONFIGURATION ### #

# The bot's useragent. It should contain a short description of what it does and your username. e.g. "RSS Bot by /u/SmBe19"
USERAGENT = "Waiaas by /r/waiaas"

# The name of the subreddit to post to. e.g. "funny"
SUBREDDIT = "waiaas"

# Number of users to select -- should be dependent on the kick users section below, so no longer a constant/param
#USERS_COUNT = 33

# Number of comments from which the users are selected (max is 1000)
SAMPLE_SIZE = 1000

# Whether to check whether the selected user is already a contributor (does not work atm)
CHECK_CONTRIBUTOR = True

# Whether to add the selected users as approved submitters.
# Note that that running the script with this flag set to True is considered spam.
ADD_CONTRIBUTOR = True

# ### END USER CONFIGURATION ### #

try:
	# A file containing infos for testing.
	import bot
	USERAGENT = bot.useragent
	SUBREDDIT = bot.subreddit
except ImportError:
	pass

# main procedure
def run_bot():
	r = praw.Reddit(USERAGENT)
	if CHECK_CONTRIBUTOR or ADD_CONTRIBUTOR:
		o = OAuth2Util.OAuth2Util(r)
		o.refresh()
	sub = r.get_subreddit(SUBREDDIT)

	users_count = 0

	# kick peeps (in theory)
	contributors = list(sub.get_contributors())
	for contributor in contributors:
		contributor_comments = list(contributor.get_comments(SUBREDDIT, sort=u'new',time=u'week', limit=None))
		if not contributor_comments:
			contributor.leave_contributor(SUBREDDIT)
			users_count += 1

	print("Start bot for subreddit", SUBREDDIT)
	print("Select", users_count, "users from", SAMPLE_SIZE, "comments")
	comments = list(r.get_comments("all", limit=SAMPLE_SIZE))
	added_users = []

	for i in range(users_count):
		user = random.choice(comments).author
		while (CHECK_CONTRIBUTOR and user in contributors) or user in added_users:
			user = random.choice(comments).author
		added_users.append(user)

		print(user.name)

		if ADD_CONTRIBUTOR:
			sub.add_contributor(user)

if __name__ == "__main__":
	if not USERAGENT:
		print("missing useragent")
	elif not SUBREDDIT:
		print("missing subreddit")
	else:
		run_bot()
