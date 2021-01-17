# Python Ldap UTexasGetUser

A Python tool for getting emails and other student information from the UT Austin public directory. 

NOTE: As per a security change by the Unviersity of Texas at Austin Information Security Office, Access to the LDAP interface (and thus, this application which relies on it) is restricted to the university network as of December 2020. This interface is scheduled to be completely retired in July 2021. 
This application must now be run from within the UTexas network (via the UTexas VPN or on campus directly)

Requires ldap3 library:
pip install ldap3