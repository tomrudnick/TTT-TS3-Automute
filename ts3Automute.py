#!/usr/bin/python3


import ts3
import time

PERM_TALKPOWER = "i_client_talk_power"
TTT_CHANNEL = "TTT"
UNMUTE_CHANNEL = "UNMUTE_CHANNEL"
DEAD_FILE = "dead.txt"
ALIVE_FILE = "alive.txt"

HOST = "127.0.0.1"
PORT = "10011"
USERNAME = "serveradmin"
PASSWORD = "your_password"

PERM_VALUE_MUTE = 40
PERM_VALUE_TALK = 55

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def same(first, second):
        second = set(second)
        return [item for item in first if item in second]

def readPlayerFiles(filename):
    try:
        data = []
        with open(filename, "r") as file:
            for player in file:
                playerString = player.rstrip("\n")
                data.append(playerString)
        return data
    except:
        print("File not found or couldn't be read")
        return []

def setClientChannelTalkPower(ts3conn, cid, nickname, pvalue):
    try:
        clid = ts3conn.clientfind(pattern=nickname).parsed[0]['clid']
        clientInfo = ts3conn.clientinfo(clid = clid).parsed[0]
        cldbid = clientInfo['client_database_id']
        playerCID = clientInfo['cid']

        if(cid == playerCID):
            ts3conn.channelclientaddperm(cid=cid, cldbid=cldbid, permsid=PERM_TALKPOWER, permvalue=pvalue)
    except:
        print("User not found or something else failed")


def automute(ts3conn, cid, unmute_cid):
    allreadyMuted = []
    connection_time = time.perf_counter()
    while True:
        deadPlayers = readPlayerFiles(DEAD_FILE)
        if len(deadPlayers) > 0:
            notMutedPlayers = diff(deadPlayers, allreadyMuted)
            for player in notMutedPlayers:
                allreadyMuted.append(player)
                print("Mute " + player)
                setClientChannelTalkPower(ts3conn, cid, player, PERM_VALUE_MUTE)
        else:
            if len(allreadyMuted) > 0:
                for player in allreadyMuted:
                    setClientChannelTalkPower(ts3conn, cid, player, PERM_VALUE_TALK)
            allreadyMuted.clear()
        
        aliveAgain = diff(allreadyMuted, deadPlayers)
        for player in aliveAgain:
            print("Someone is alive again")
            setClientChannelTalkPower(ts3conn, cid, player, PERM_VALUE_TALK)
            index = allreadyMuted.index(player)
            allreadyMuted.pop(index)
        
        #unmute everyone in the UNMUTE_CHANNEL
        clientlist = [client for client in ts3conn.clientlist() if client['cid'] == unmute_cid]
        for client in clientlist:
            ts3conn.channelclientaddperm(cid=cid, cldbid=client['client_database_id'], permsid=PERM_TALKPOWER, permvalue=PERM_VALUE_TALK)

        check_connection_time = time.perf_counter()
        differenceTime = check_connection_time - connection_time
        if differenceTime > 60:
            ts3conn.send_keepalive()
            connection_time = time.perf_counter()
            print("Send keep alive string")
        time.sleep(0.1)


        

if __name__ == "__main__":
    with ts3.query.TS3Connection(HOST, PORT) as ts3conn:
        try:
            ts3conn.login(client_login_name=USERNAME, client_login_password=PASSWORD)
            ts3conn.use(sid=1)
            cid = ts3conn.channelfind(pattern=TTT_CHANNEL)[0]['cid']
            unmute_cid = ts3conn.channelfind(pattern=UNMUTE_CHANNEL)[0]['cid']
            print(unmute_cid)
            print("connected")
        except ts3.query.TS3QueryError as err:
            print("Login Error: ", err.resp.error["msg"])
            exit(1)
        automute(ts3conn, cid, unmute_cid)  