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
import subprocess, random, string, sys

app = Flask(__name__)

authentication_token=''.join(random.choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for _ in range(32))

@app.route('/diagnostics', methods=['GET'])
def get_tasks():
    global authentication_token

    # To avoid malicious intent, check the token passed or else we return a default 404
    if authentication_token != request.args.get('token'):
        abort(404)

    # Call shell for diagnostic information available to bash
    proc = subprocess.Popen(['./diagnostics.sh'], stdout=subprocess.PIPE, shell=False)

    # get output
    (output,errors) = proc.communicate()

    if errors:
        print("Error:")
        print(errors)
        print("Default aborting.")
        abort(404)

    # Decode bytes and split by double newline for
    # individual sections based on bash script
    output=output.decode('utf-8')
    output=output.strip().split("\n\n")

    # Parse Memory information
    holder=output[0].strip().split('\n')

    final_output={}
    final_output[holder[0]]={}

    for j,y in enumerate(holder[1:]):
        hold2 = y.split(":")
        print(hold2)
        hold2[1] = hold2[1].split('|')

        tempDict={}

        for z in hold2[1]:
            z=z.split(",")
            tempDict[z[0]]=z[1]

        final_output[holder[0]][hold2[0]]=tempDict


    # Parse Filesystem information
    holder=output[1].strip().split('\n')

    final_output[holder[0]]=[]

    tmp = []

    for i,x in enumerate(holder[1:]):
        x=x.split("|")

        tempDict={}

        for z in x:
            z=z.split(",")

            tempDict[z[0]]=z[1]


        x=tempDict

        final_output[holder[0]].append(x)

    # Send
    return jsonify(final_output)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("{} <IP Address> <Port Number>".format(sys.argv[0]))
        sys.exit(0)

    print("Authentication Token: " + authentication_token)
    print("Use this parameter for calling diagnostics: ?token="+authentication_token)
    print("")

    app.run(host=sys.argv[1],port=int(sys.argv[2]))