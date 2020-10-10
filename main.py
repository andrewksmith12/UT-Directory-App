import ldap3
import json

from ldap3 import Connection, Server, ANONYMOUS, SIMPLE, SYNC, ASYNC


def searchByEID():
    eid = '(utexasEduPersonEid=' + input("enter an EID to lookup: ")+')'
    server = Server('directory.utexas.edu')
    conn = Connection(server)
    conn.bind()
    conn.search('dc=directory,dc=utexas,dc=edu', eid, attributes=['displayName','mail', 'utexasEduPersonMajor', 'utexasEduPersonClassification','utexasEduPersonPubAffiliation','utexasEduPersonSchool'])
    if len(conn.entries) > 0:
        entry = conn.entries[0]
        jsonEntry = entry.entry_to_json
        #print (entry.displayName)
        print(entry.entry_to_json)
    else:
        print("User not found")

def searchByFullName():
    name = '(cn=' + input("enter a full name to lookup: ")+')'
    server = Server('directory.utexas.edu')
    conn = Connection(server)
    conn.bind()
    conn.search('dc=directory,dc=utexas,dc=edu', name, attributes=['displayName','mail', 'utexasEduPersonMajor', 'utexasEduPersonClassification','utexasEduPersonPubAffiliation','utexasEduPersonSchool'])
    if len(conn.entries) > 0:
        entry = conn.entries[0]
        jsonEntry = entry.entry_to_json
        #print (entry.displayName)
        print(entry.entry_to_json)
    else:
        print("User not found")
    

def searchByLastName():
    name = '(sn=' + input("enter a last name to lookup: ")+')'
    server = Server('directory.utexas.edu')
    conn = Connection(server)
    conn.bind()
    conn.search('dc=directory,dc=utexas,dc=edu', name, attributes=['displayName','mail', 'utexasEduPersonMajor', 'utexasEduPersonClassification','utexasEduPersonPubAffiliation','utexasEduPersonSchool'])
    if len(conn.entries) > 0:
        entry = conn.entries[0]
        jsonEntry = entry.entry_to_json
        #print (entry.displayName)
        print(entry.entry_to_json)
    else:
        print("User not found")

def main():
    choicePrompt = "Type 1 to search by EID.\nType 2 to search by full name.\nType 3 to search by last name.\nType 4 to exit.\n  "
    choiceSelection = input(choicePrompt)
    validChoices = ["1", "2", "3"]
    while choiceSelection not in validChoices:
        choiceSelection = input("\n" + choicePrompt)
    if (int(choiceSelection) == 1):
        searchByEID()
    elif (int(choiceSelection) == 2):
        searchByFullName()
    elif (int(choiceSelection) == 3):
        searchByLastName()
    elif (int(choiceSelection) == 4):
        exit()

main()
