import ldap3
import json
from bcolors import bcolors
from ldap3 import Connection, Server, ANONYMOUS, SIMPLE, SYNC, ASYNC

def searchByEID(eid):
    server = Server('directory.utexas.edu')
    conn = Connection(server)
    conn.bind()
    conn.search('dc=directory,dc=utexas,dc=edu', eid, attributes=['displayName','mail', 'utexasEduPersonMajor', 'utexasEduPersonClassification','utexasEduPersonPubAffiliation','utexasEduPersonSchool'])
    if len(conn.entries) == 0:
        print(bcolors.WARNING+"No matching EID found, skipping."+bcolors.ENDC)
        return -1
    elif len(conn.entries) > 1:
        i = 0
        for entry in conn.entries:
            print("Entry Number "+str(i)+ ":  ")
            print(entry)
            i += 1
        entryNumber = int(input("Enter the number for the entry that matches the one you're looking for: "))
        entry = conn.entries[entryNumber]
        return entry
    else:
        entry = conn.entries[0]
        return entry

def searchByFullName(name):
    server = Server('directory.utexas.edu')
    conn = Connection(server)
    conn.bind()
    conn.search('dc=directory,dc=utexas,dc=edu', name, attributes=['displayName','utexasEduPersonEid','mail', 'utexasEduPersonMajor', 'utexasEduPersonClassification','utexasEduPersonPubAffiliation','utexasEduPersonSchool'])
    if len(conn.entries) == 0:
        print(bcolors.WARNING+"No matching name found, skipping."+bcolors.ENDC)
        return -1
    elif len(conn.entries) > 1:
        i = 0
        for entry in conn.entries:
            print("Entry Number "+str(i)+":  ")
            print(entry)
            i += 1
        entryNumber = int(input("Enter the number for the entry that matches the one you're looking for: "))
        entry = conn.entries[entryNumber]
        return entry
    else:
        entry = conn.entries[0]
        return entry

def process_list(input_file, output_file,searchMethod,searchKey):
    input_file = open(input_file, "r")
    output = open(output_file, "w")
    searchID = input_file.readline().strip("\n")
    #print(searchID)
    while searchID != "":
        entry = searchMethod(searchKey+ searchID+')')
        if entry != -1:
            output.write(searchID+","+str(entry.mail)+"\n")
        else:
            output.write(searchID+",NO_MATCH_IN_DB")
        searchID = input_file.readline().strip("\n")



def main():
    choicePrompt = "UT Directory Services Data Lookup Tool\n\nOption 1: Search for student information by EID.\nOption 2: Search for student information by name.\nOption 3: Process file of names, return names and emails.\nOption 4: Process file of EIDs, return EIDs and emails\nOption 5: Exit Tool.\n\nSelect an option: "
    choiceSelection = input(choicePrompt)

    if (int(choiceSelection) == 1):
        eid = '(utexasEduPersonEid=' + input("enter an EID to lookup: ")+')'
        entry = searchByEID(eid)
        if entry != -1:
            print(entry.entry_to_json)

    elif (int(choiceSelection) == 2):
        name = '(cn=' + input("enter a full name to lookup: ")+')'
        entry = searchByFullName(name)
        if entry != -1:
            print(entry.entry_to_json)

    elif (int(choiceSelection) == 3):
        fileIn = input("Input file name (including extension): ")
        while fileIn == "":
            print(bcolors.FAIL+"Input file cannot be blank."+bcolors.ENDC)
            fileIn = input("Input file name (including extension): ")
        fileOut = input("Output file name (including extension, will be formatted as csv): ")
        if fileOut == "":
            print(bcolors.WARNING+"No output file provided, using output.csv"+bcolors.ENDC)
            fileOut = "output.csv"
        #outputField = "mail"
        process_list(fileIn, fileOut, searchByFullName,'(cn=')
        print(bcolors.OKGREEN+"File Processed. Output saved to "+fileOut+bcolors.ENDC)

    elif (int(choiceSelection) == 4):
        fileIn = input("Input file name (including extension): ")
        while fileIn == "":
            print(bcolors.FAIL+"Input file cannot be blank."+bcolors.ENDC)
            fileIn = input("Input file name (including extension): ")
        fileOut = input("Output file name (including extension, will be formatted as csv): ")
        if fileOut == "":
            print(bcolors.WARNING+"No output file provided, using output.csv"+bcolors.ENDC)
            fileOut = "output.csv"
        #outputField = "mail"
        process_list(fileIn, fileOut, searchByEID,'(utexasEduPersonEid=')
        print(bcolors.OKGREEN+"File Processed. Output saved to "+fileOut+bcolors.ENDC)

    elif (int(choiceSelection) == 5):
        exit()

    else:
        print(bcolors.WARNING+"Selection not valid, please enter a valid selection.\n"+bcolors.ENDC)
        choiceSelection = input(choicePrompt)

    print("\n\n")
    main()


main()