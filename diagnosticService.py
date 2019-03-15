#!flask/bin/python

# Simple Web API that prints diagnostics information
# By: Luke (luke.a.programmer@gmail.com)
# Last Updated: 3/2/2019
# 
# Requirements: Flask, python 3.4.9 or better.
# Download flask using pip: sudo pip install flask
# 
# Authentication token is provided to ensure that malicious intent doesn't occur.
# Currently the program provides information on memory use and disk use from commands 'free -m' and 'df -h'
# which can be seen in the diagnostics.sh bash script (which is required in the same directory as this program to work)
#
# Recommend using python's virtualenv to run an instance of the service independently from your CLI
# 

from flask import Flask, jsonify, request, abort
import subprocess, random, string, sys, os, psutil

from flaskdiagnostic import callers
import click


@click.command()
@click.option('--port', default="9999", help="Port to listen on")
@click.option('--ip',default="localhost", help="IP Address to listen on")
def main(ip, port):
    # Generate 32 string length random token
    authentication_token=''.join(random.choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for _ in range(32))

    print("Authentication Token: "+authentication_token)
    print("Add this to the end of the URL when calling diagnostics: ?token="+authentication_token)
    print("")

    app = Flask(__name__)
    app.config.update(
        AUTH_TOKEN=authentication_token
    )

    app.register_blueprint(callers)

    app.run(ip, port)

    return


if __name__ == '__main__':
    main()