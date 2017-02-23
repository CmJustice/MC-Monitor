#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Cem'

from flask import *
import mcstatus, yaml
from mcstatus import MinecraftServer
import os, datetime, threading, logging
app = Flask(__name__)
app.secret_key = os.urandom(24)

serverlist = []
#Loads the servers from config
with open("config.yml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as e:
        print(e)
for server in config['Servers']:
    s = {}
    s['name'] = server
    s['ip'] = config['Servers'][server]
    serverlist.append(s)




#Server querier
def genJson():
    allstats = []
    for server in serverlist:
        ip = server['ip']
        name = server['name']
        mcserver = MinecraftServer.lookup(str(ip))
        stats = {}
        try:
            status = mcserver.status()
        except Exception as e:
            stats['durum'] = "Offline"
            pass
        else:
            stats['durum'] = "Online"
        if stats['durum'] == "Online":
            players = status.players.online
            maxplayers = status.players.max
            motd = status.description
            stats['players'] = players
            stats['maxplayers'] = maxplayers
            stats['motd'] = motd
        stats['ip'] = ip
        stats['name'] = name
        allstats.append(stats)
    return allstats

#Making it async and run in background
def schedule_json():
    threading.Timer(5, schedule_json).start()
    global stats
    stats = genJson()



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getStatus")
def status():
    return jsonify(data=stats)





schedule_json()


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)