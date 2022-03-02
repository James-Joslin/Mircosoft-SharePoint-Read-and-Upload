import os
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

sharepoint_base_url = 'https://company.sharepoint.com/teams/team_name/'
sharepoint_user = 'email'
sharepoint_password = 'password'
folder_in_sharepoint = '/teams/team_name/Shared%20Documents/dir/' # All that will change here is the "testing" part of the string, obviously change to required folder

#Constructing Details For Authenticating SharePoint

auth = AuthenticationContext(sharepoint_base_url)

auth.acquire_token_for_user(sharepoint_user, sharepoint_password)
ctx = ClientContext(sharepoint_base_url, auth)
web = ctx.web
ctx.load(web)
ctx.execute_query()
print('Connected to SharePoint: ',web.properties['Title'])

#Read filename - pptx file not included in push to git to save space, create new file if you want to test it out
fileName = '.\\Test_Powerpoints\\Upload_Test.pptx' # I guess you'd use glob to automate file searches, and loop over a lsit if multiple files

with open(fileName, 'rb') as content_file:
    file_content = content_file.read()
name = os.path.basename(fileName)

list_title = "Testing" # not sure why, but you need to add the name of the target directory, despite having it above
target_list = ctx.web.lists.get_by_title(list_title)
libraryRoot = ctx.web.get_folder_by_server_relative_url(folder_in_sharepoint)

target_file = libraryRoot.upload_file(name, file_content).execute_query()
print("File has been uploaded to url: {0}".format(target_file.serverRelativeUrl))