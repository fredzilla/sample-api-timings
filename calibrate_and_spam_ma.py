from twython import Twython
from twython.exceptions import TwythonError
from numpy import mean, std
import time

### NOTE!!!!!! It is good to sync your machine's time before beginning this script
### On Ubuntu: sudo ntpdate -s time.nist.gov

# python 3 convenience. 'long' is not defined in Python3, so define it as int if it cannot be found.
try:
    long = long
except NameError:
    long = int

# How many past samples we should look at when
# calculating the lag time.
window_size = 3
# How many spam messages to send.
no_spam = 100
# The target millisecond. This is the middle of 
# the sample API window.
target_ms = (666 + 657) / 2

twitter_epoch = 1288834974657
def tweet_id_to_timestamp(tweet_id):
	"""
	Convert a tweet ID to the Twitter timestamp embedded within it.
	:param tweet_id:
	This is the ID of the tweet (should be passed as a string)
	:return:
	The timestamp of the tweet from the tweet ID.
	"""
	num = long(tweet_id)
	bits = '{0:064b}'.format(num)
	ts = bits[1:42]

	final_time = int(ts, 2) + twitter_epoch
	return final_time


def get_next_tweet(filePointer, file_name):
    """
    This gets pre-cooked tweets from a file.
    :param filePointer:
    The pointer object that we need to get.
    :param file_name:
    The name of the file to read from.
    :return:
    The next tweet from the file.
    """
	ln = filePointer.readline()
	if ln == '':
		filePointer.close()
		filePointer = open(file_name)
		ln = filePointer.readline()
	tm = "%f " % time.time()
	ln = "#btweetdmml " + tm + ln.strip()
	ln = ln[0:80]
	return ln


# some random tweets to post
tweet_file = 'some_tweets.txt'
fp = open(tweet_file)

# read in a set of user keys
accts = []
twy = []
for line in open("keys.csv"):
	a = line.strip().split(", ")
	accts.append(a)
	twy.append(Twython(a[0], a[1], a[2], a[3]))

# wait until this millisecond to begin the experiment.
target_start = 500

# remembers the delta of all of the last calls.
deltas = []

# post `no_spam` tweets and record their IDs
no_hits = 0
spam_id = 0
key_id = 0
while spam_id < no_spam:
	# queue up the next tweet
	msg = get_next_tweet(fp, tweet_file)

	# wait until the proper millisecond arrives.
	millis = -1
	while millis != target_start:
		t = time.time()
		millis = t - int(t)
		millis = int(millis * 1000)

	# post the tweet.
	try:
		key_id += 1
		tobj = twy[key_id % len(twy)].update_status(status=msg)
	except ValueError:
		continue
	except TwythonError:
		print("Dead Account:", twy[key_id % len(twy)])
		continue
	
	# print the relevant info.
	print("Tweeting: %s" % msg)
	print("%d,%f,%d,%s,%0.3f" % (spam_id, t * 1000, millis, tobj['id_str'], tweet_id_to_timestamp(tobj['id_str'])))
	m = int(tweet_id_to_timestamp(tobj['id_str']) % 1000)
	is_hit = 657 <= m <= 666
	no_hits += int(is_hit)
	print("Hit %d/%d = %0.3f" % (no_hits, spam_id + 1, no_hits/float(spam_id + 1)))

    # record the delta
	deltas.append((t * 1000, tweet_id_to_timestamp(tobj['id_str'])))

	# update the target to be a moving average 
	win = deltas[-window_size:]
	mu = mean([j - i for i, j in win])  # the average lag

	mu = int(mu % 1000)
	target_start = target_ms - mu
	target_start = 1000 + target_start if target_start < 0 else target_start
	print("The new target is %d, to hit our target of %d with a mean wait of %dms" % (target_start, target_ms, mu))

	# wait a bit and tweet again.
	time.sleep(5.0)
	spam_id += 1
