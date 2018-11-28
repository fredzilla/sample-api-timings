# Run Sample API Timing Experiment.
Code to run Sample API calibration experiment as described in [1]. This will post to Twitter in an attempt to get as many tweets into the Sample API as possible.

## How to run
1. First, you must generate a key, or keys with write permissions to Twitter's API. This is done at http://developer.twitter.com/.
2. Add these keys to keys.csv in the format specified in the template file.
3. For best performance, synchronize your system's clock.
4. run `calibrate_and_spam_ma.py`.


## References
[1] Morstatter, Fred, et al. "Can one tamper with the sample api?: Toward neutralizing bias from spam and bot content." Proceedings of the 25th International Conference Companion on World Wide Web. International World Wide Web Conferences Steering Committee, 2016.
