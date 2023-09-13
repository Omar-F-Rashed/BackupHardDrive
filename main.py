import datetime
import os
import subprocess
import time

exclude_printers = ['OneNote for Windows 10', 'OneNote (Desktop)', 'Microsoft XPS Document Writer',
                    'Microsoft Print to PDF', 'Fax', 'Adobe PDF', 'Webex Document Loader', 'Send To OneNote 16']

def get_size(required_size, start_path = '.'):
    total_size = 0
    # print(required_size, start_path)
    enum = 0
    for dirpath, dirnames, filenames in os.walk(start_path):

        # print(dirpath, dirnames, filenames)
        if enum == 0:
            for i in dirnames:
                temp_dir = dirpath + '\\' + i
                j = temp_dir[temp_dir.rfind('\\') + 1:]
                fa = os.stat(temp_dir).st_file_attributes
                if fa == 17 and j != 'My Documents' and j != 'Start Menu' and j != 'Recent':
                    pass
                else:
                    dirnames.remove(j)



        j = dirpath[dirpath.rfind('\\')+1:]
        fa = os.stat(dirpath).st_file_attributes
        if (fa == 17 or fa == 16) and j != 'My Documents' and j != 'Start Menu' and j != 'Recent':
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
                    if total_size >= required_size*1000000:
                        break
        enum += 1
        if total_size >= required_size * 1000000:
            break
    print(total_size/1000000)
    if total_size/1000000 >= required_size:
        return True
    else:
        return False

exclude_list = ['All Users', 'Default User']
# Get the list of all files and directories
# user = 'DHMZITADMLP01'
user = 'GHMZITNOBANI'
path = f'\\\\{user}\\c$\\Users'
dir_list = os.listdir(path)
fa = os.stat(path).st_file_attributes
required_size = 20
print("Files and directories in '", path, "' :")
for i in dir_list:
    size = 0
    if i in exclude_list:
        continue
    size = get_size(required_size, path+'\\'+i)
    print(i, size)

    user_path = path+'\\'+i
    root_fa = os.stat(user_path).st_file_attributes
    if root_fa != 17 and root_fa != 16:
        continue
    user_dir_list = os.listdir(user_path)
    if size:
        print(f'{i} within size threshold. Backing up files')
        prev_time = time.time()
        for j in user_dir_list:

            source = user_path + r"\\" + j
            fa = os.stat(source).st_file_attributes
            target = f'\\\\aghfileserver\\PUBLIC\\newbackup\\{user}\\{i}\\{j}\\'
            # print(target, source)
            if (fa == 17 or fa == 16) and j != 'My Documents' and j != 'Start Menu' and j != 'Recent':
                os.system(f'robocopy "{source}\." "{target}\." /R:0 /j /mt:16 /njh')
        timedelta_obj = datetime.timedelta(seconds=time.time() - prev_time)
        print(f'Copying all {i} files took: {timedelta_obj}')

print(f'Done copying all users with data above: {required_size} MB')