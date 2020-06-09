# Scheduler
A discord bot I wrote in python for scheduling friends availablity to go bouldering. Eventually going to port to Slack/Rocketchat

::Token::

Save bot token to a text file named token.txt

::Data structure::

Nested dict of days containing a dict of times containing a list of user ID numbers.

Stores to .json

::Commands::
- Ping - responds with pong
- Help - lists commands and descriptions
- Now - pings users who are scheduled in the next hour
- Schedule - Adds user to data structure at times specified by user (also appends the json)
- All - Shows Weeks schedule on the terminal

::Future Updates and Features::
- Implement faster fetching algorithms 
- Unschedule function
- read-in from json on launch
- Enable matrix bridged users to participate from a bot
- Put cap on max number of scheduled at a specific time, to prevent trolling friends from DOS'ing for the lols
- Fix Try block to be more specific
- Strip extra characters out of !now output
- User-flag for different gyms
- Port to slack/rocketchat
- Identify ideal climb times and ping a weekly climb schedule of ideal times
- Weight climbers based on past flakiness, to maximize schedule accuracy
