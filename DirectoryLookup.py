import ldap3
import json
from bcolors import bcolors
from ldap3 import Connection, Server, ANONYMOUS, SIMPLE, SYNC, ASYNC

def establish_session():
    server = Server('directory.utexas.edu')
    conn = Connection(server)
    conn.bind()
    return conn

def perform_search(search_string, identifier_string):
    conn = establish_session()
    conn.search('dc=directory,dc=utexas,dc=edu', search_string, attributes=['displayName','utexasEduPersonEid','mail', 'utexasEduPersonMajor', 'utexasEduPersonClassification','utexasEduPersonPubAffiliation','utexasEduPersonSchool'])
    if len(conn.entries) == 0:
        print(bcolors.WARNING+"No matching "+identifier_string+" found, skipping."+bcolors.ENDC)
        conn.unbind()
        return -1
    elif len(conn.entries) > 1:
        i = 0
        for entry in conn.entries:
            print("Entry Number "+str(i)+ ":  ")
            print(entry)
            i += 1
        entryNumber = int(input("Enter the number for the entry that matches the one you're looking for: "))
        entry = conn.entries[entryNumber]
        conn.unbind()
        return entry
    else:
        entry = conn.entries[0]
        conn.unbind()
        return entry

def searchByEID(userVal):
    eid = '(utexasEduPersonEid=' + userVal +')'
    return perform_search(eid,"EID")

def searchByFullName(userVal):
    name = '(cn=' + userVal +')'
    return perform_search(name,"name")

def process_list(input_file,output,searchMethod):
    searchID = input_file.readline().strip("\n")
    while searchID != "":
        entry = searchMethod(searchID)
        if entry != -1:
            output.write(searchID+","+str(entry.mail)+"\n")
        else:
            output.write(searchID+",NO_MATCH_IN_DB")
        searchID = input_file.readline().strip("\n")



def cli_options():
    choicePrompt = "UT Directory Services Data Lookup Tool\n\nOption 1: Search for student information by EID.\nOption 2: Search for student information by name.\nOption 3: Process file of names, return names and emails.\nOption 4: Process file of EIDs, return EIDs and emails\nOption 5: Exit Tool.\n\nSelect an option: "
    choiceSelection = input(choicePrompt)

    def command_line_list_processing(searchFunction):
        fileIn = input("Input file name (including extension): ")
        while fileIn == "":
            print(bcolors.FAIL+"Input file cannot be blank."+bcolors.ENDC)
            fileIn = input("Input file name (including extension): ")
        fileOut = input("Output file name (including extension, will be formatted as csv): ")
        if fileOut == "":
            print(bcolors.WARNING+"No output file provided, using output.csv"+bcolors.ENDC)
            fileOut = "output.csv"
        input_file = open(fileIn, "r")
        output = open(fileOut, "w")
        process_list(input_file, output, searchFunction)
        input_file.close()
        output.close()
        print(bcolors.OKGREEN+"File Processed. Output saved to "+fileOut+bcolors.ENDC)

    if (int(choiceSelection) == 1):
        eid = input("enter an EID to lookup: ")
        entry = searchByEID(eid)
        if entry != -1:
            print(entry.entry_to_json)

    elif (int(choiceSelection) == 2):
        name = input("enter a name to lookup: ")
        entry = searchByFullName(name)
        if entry != -1:
            print(entry.entry_to_json)

    elif (int(choiceSelection) == 3):
        command_line_list_processing(searchByFullName)

    elif (int(choiceSelection) == 4):
        command_line_list_processing(searchByEID)

    elif (int(choiceSelection) == 5):
        exit()

    else:
        print(bcolors.WARNING+"Selection not valid, please enter a valid selection.\n"+bcolors.ENDC)
        choiceSelection = input(choicePrompt)

    print("\n\n")
    cli_options()

if __name__ == "__main__":  # pragma: no cover
    cli_options()