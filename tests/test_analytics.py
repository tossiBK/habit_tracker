# # for unit tests to be available in a subfolder, to avoid package and module errors we must do add the absolute path
# # to our root folder, where the files to import are located
# import sys
# import os
 
# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)

# from analytics import Analytics
# # import analytics

# import datetime

# def test_get_habit():
#     analytics = Analytics()
#     assert Analytics.__compareDates(datetime, datetime, 'd') == False