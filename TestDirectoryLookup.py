from io import StringIO
from unittest import main, TestCase
from DirectoryLookup import searchByEID, searchByFullName, process_list

class TestDirectoryLookup(TestCase):
    def test_eid_lookup(self):
        entry = searchByEID("aks3767")
        email = entry.mail
        self.assertEqual(email, "college@andrewksmith.net")

    def test_eid_lookup_2(self):
        entry = searchByEID("ZZZZZZZ")
        self.assertEqual(entry, -1) #Entry should not exist, return error code -1
    
    def test_name_lookup(self):
        entry = searchByFullName("Jonathan Cope")
        email = entry.mail
        self.assertEqual(email,"jonathan.cope@utexas.edu")

    def test_name_lookup_2(self):                   # This unit test requires clarification input from user. I'm not sure how to fully automate this test in the current program state.
        entry = searchByFullName("Andrew Smith")
        email = entry.mail
        self.assertEqual(email,"college@andrewksmith.net")

    def test_name_lookup_3(self):                   # This unit test requires clarification input from user. I'm not sure how to fully automate this test in the current program state.
        entry = searchByFullName("Katrina Fisher")
        self.assertEqual(entry,-1)
    
    def test_process_list_Names(self):
        fileIn = StringIO("Jonathan Cope\nAndrew Smith\nAlexander Canright\nKatrina Fisher\n")
        fileOut = StringIO()
        process_list(fileIn,fileOut,searchByFullName)
        self.assertEqual(fileOut.getvalue(),"Jonathan Cope,jonathan.cope@utexas.edu\nAndrew Smith,college@andrewksmith.net\nAlexander Canright,alexandercanright@austin.utexas.edu\nKatrina Fisher,NO_MATCH_IN_DB")
    def test_process_list_EIDs(self):
        fileIn = StringIO("jec4777\naks3767\nagc2632\nkaf0000")
        fileOut = StringIO()
        process_list(fileIn,fileOut,searchByEID)
        self.assertEqual(fileOut.getvalue(),"jec4777,jonathan.cope@utexas.edu\naks3767,college@andrewksmith.net\nagc2632,alexandercanright@austin.utexas.edu\nkaf0000,NO_MATCH_IN_DB")



if __name__ == "__main__":  # pragma: no cover
    main()