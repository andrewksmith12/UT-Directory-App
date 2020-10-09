import ldap3

from ldap3 import Connection, Server, ANONYMOUS, SIMPLE, SYNC, ASYNC
server = Server('directory.utexas.edu')
conn = Connection(server)
conn.bind()
conn.search('dc=directory,dc=utexas,dc=edu', '(utexasEduPersonEid=aks3767)', attributes=['mail', 'utexasEduPersonMajor', 'utexasEduPersonClassification','utexasEduPersonPubAffiliation','utexasEduPersonSchool'])
entry = conn.entries[0]
print(entry.entry_to_json)