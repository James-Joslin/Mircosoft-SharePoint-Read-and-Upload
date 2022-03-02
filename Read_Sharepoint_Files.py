from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

sharepoint_base_url = 'https://company.sharepoint.com/teams/team_name/'
sharepoint_user = 'email'
sharepoint_password = 'password'
folder_in_sharepoint = '/teams/team_name/Shared%20Documents/dir/' # All that will change here is the "dir" part of the string, obviously change to required folder

#Constructing Details For Authenticating SharePoint

auth = AuthenticationContext(sharepoint_base_url)

auth.acquire_token_for_user(sharepoint_user, sharepoint_password)
ctx = ClientContext(sharepoint_base_url, auth)
web = ctx.web
ctx.load(web)
ctx.execute_query()
print('Connected to SharePoint: ',web.properties['Title'])

#Constructing Function for getting file details in SharePoint Folder

def folder_details(connection_string, dir):
    folder = connection_string.web.get_folder_by_server_relative_url(dir)
    fold_names = []
    sub_folders = folder.files 
    connection_string.load(sub_folders)
    connection_string.execute_query()
    for s_folder in sub_folders:
        fold_names.append(s_folder.properties["Name"])
    return fold_names
file_list = folder_details(connection_string = ctx, dir = folder_in_sharepoint)

# #Reading File from SharePoint Folder - This loops over all files in directory, if you only want the latest file, it seems that the files are ordered in most recent date of modification
# As such, just select for the first file within file_list, instead of looping over whole list
for file in file_list:
    print(f"Opening: {file}")
    sharepoint_file = f"{folder_in_sharepoint}{file}"
    file_response = File.open_binary(ctx, sharepoint_file)
    #Saving file to local
    with open(file, 'wb') as output_file:  
        output_file.write(file_response.content)