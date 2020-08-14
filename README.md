# Trouble-in-Terrorist-Town-Teamspeak-Automute
These two scripts automatically mute and unmute players on a Teamspeak server
when they are dead or alive in the game: Trouble in Terrorist Town.

## How it works

The Lua script writes the alive and dead players in two files.
The Python Scripts reads both files and checks for differences.
The new dead or alive players will get muted or unmuted.
It communicates with the Teamspeak Server
by the ts3 library. The player mute process is controlled by
the i_client_talk_power permission.

## How to use

- Put the Lua Script in the autorun folder of your server (/garrysmod/lua/autorun/)
- create the following directory (/garrysmod/data/**automute**)
- Put the Python Script in the created directory
- modify the Python Script variables according to your TS3-Server Query Credentials     (USERNAME, PASSWORD, possibly HOST or PORT)
- The Lua Script will write the dead.txt and alive.txt files in this folder as well.
- Create a "TTT" Channel with the Talk Power of 50
- Start the Python Script in a different screen e.g. screen -S ts3

## Optional
When a player leave the Teamspeak Server and is still muted he can't be unmuted and
therefore is muted the next time he joins the channel. Solution:
- Create an UNMUTE_CHANNEL Channel (default name)
- Every player who joins this channel gets automatically unmuted

## Dependecies

- \>= python 3.7
- = ts3 1.0.11