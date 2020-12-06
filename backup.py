# import flask dependencies
from flask import Flask, request, make_response, jsonify
from ldap3 import Connection, Server, ANONYMOUS, SIMPLE, SYNC, ASYNC

# initialize the flask app
app = Flask(__name__)



def establish_session():
    server = Server('directory.utexas.edu')
    conn = Connection(server)
    conn.bind()
    return conn

def perform_search(search_string, identifier_string):
    response = ""
    conn = establish_session()
    conn.search('dc=directory,dc=utexas,dc=edu', search_string, attributes=['displayName','utexasEduPersonEid','mail', 'utexasEduPersonMajor', 'utexasEduPersonClassification','utexasEduPersonPubAffiliation','utexasEduPersonSchool'])
    if len(conn.entries) == 0:
        response += str("No matching "+identifier_string+" found, skipping.")
        conn.unbind()
        return response
    elif len(conn.entries) > 1:
        response += "I found multiple matches. \n"
        i = 0
        for entry in conn.entries:
            response+=str(entry.displayName)+" is a "+str(entry.utexasEduPersonMajor)+" major in the "+str(entry.utexasEduPersonSchool)+". Their email is "+str(entry.mail)+ ". \n"
        return response
    else:
        entry = conn.entries[0]
        response+=str(entry.displayName)+" is a "+str(entry.utexasEduPersonMajor)+" major in the "+str(entry.utexasEduPersonSchool)+". Their email is "+str(entry.mail)+". "
        return response

def searchByEID(userVal):
    eid = '(utexasEduPersonEid=' + userVal +')'
    return perform_search(eid,"EID")

def searchByFullName(userVal):
    name = '(cn=' + userVal +')'
    return perform_search(name,"name")

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    #action = req.get('queryResult').get('action')
    result = req['queryResult']['parameters']
    search_type = result['search_type']
    print("request_recieved.")
    if search_type == 'EID':
        eid = result['eid']
        output = searchByEID(eid)
        print(output)
        return {'fulfillmentText': output}
    elif search_type == 'full_name':
        full_name = result['full_name']
        output = searchByFullName(full_name)
        return {'fulfillmentText': output}
    else:
        return {'fulfillmentText': 'Invalid Request to Server.'}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()
