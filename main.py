# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from multiprocessing import Pool, Manager
import webbrowser
from functools import partial

app = Flask(__name__)


def miner_checker(hostname):
    
    if hostname[:7] == "http://":
        hostname = hostname[7:]
    elif hostname[:8] == "https://":
        hostname = hostname[8:]

    response = requests.get("http://whoismining.com/?q=http://{}".format(hostname))
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find(id="text04")

    return {'host':hostname, 'result':result}

@app.route("/command", methods=['POST'])
def command(error=None):

    pool = Pool(processes=len(request.form['domainlist'].split(',')))

    try:
        commandResults = pool.map(miner_checker, request.form['domainlist'].split(','))
    except:
        error = "Fail to request"
        print error 

    pool.close()
    pool.join()

    return render_template('home.html',
                           commandResults=commandResults,
                           hosts=request.form['domainlist'],
                           error=error,)

@app.route("/")
def home():
    return render_template("home.html")


def Run():
    webbrowser.open('http://127.0.0.1:5000')


if __name__ == '__main__':
    #Run()
    app.run()
