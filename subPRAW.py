#!/usr/bin/env python
"""
Queries r/todayiwatched and DMs a notification when it hits 1k subscribers.
"""
import praw
import configparser
import argparse

parser = argparse.ArgumentParser(description='Monitor a subreddit and DM the subscriber count if a goal was exceeded')
parser.add_argument('-f','--file', help='Specifiy a config (ini) file to use', default='config.ini', required=False)
parser.add_argument('-u','--user', help='Specifiy a user to message', required=False)
parser.add_argument('-s','--sub', help='Specifiy a subreddit to monitor', default='python', required=False)
parser.add_argument('-g','--goal', help='Specifiy a subscriber goal to use', default=1000, required=False)
args = vars(parser.parse_args())

config = configparser.ConfigParser()
config.read(args['file'])
botCfg = config['Bot']

reddit = praw.Reddit(
    client_id = botCfg['id'], 
    client_secret = botCfg['secret'], 
    username = botCfg['username'], 
    password = botCfg['password'], 
    user_agent = botCfg['agent']
)

def main():
    user = False
    if args['user'] != None:
        user = reddit.redditor(args['user'])
    subreddit = reddit.subreddit(args['sub'])
    name = subreddit.url
    subs = subreddit.subscribers
    goal = int(args['goal'])
    msg = (
    "The subreddit [r/{0}](https://www.reddit.com/r/{0}) has reached your set goal of {1:,} subscribers.\n\n"
    "*****\n"
    "I'm a ~~bot~~ *real human* ^^Beep ^^^Boop".format(subreddit, goal))

    print("{} has {:,} subscribers".format(name, subs))
    if subs > goal and user != False:
        print("More than sub goal, sending message")
        user.message("{:,} Subscriber Notification".format(goal), msg)
        print("Message sent")
    elif subs < goal:
        print("Less than sub goal, not sending message")
    else:
        print("More than sub goal, no user to send message to")

if __name__ == '__main__':
    main()
