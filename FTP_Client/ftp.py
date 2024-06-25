from ftplib import FTP

host = ""
user = ""
password = ""

with FTP(host) as ftp:

    ftp.login(user=user, passwd=password)
    print(ftp.getwelcome())

    # To download files from the server:

    with open('local_name_for_the_file', 'wb') as f:
        # wb: it means write in binary mode.
        ftp.retrbinary("RETR " + "filename_to_be_downloaded_from_server", f.write, 1024)

    # To upload files to the server:
    with open('filename_to_be_uploaded', 'rb') as f:
        # rb: it means read in binary mode.
        ftp.storbinary('STOR ' + 'server_filename_for_uploaded_file', f)

    # To download files from the directory:

    ftp.cwd("directory_name_in_server_from_where_file_will_be_downloaded")

    with open('local_filename_for_the_downloaded_file', 'wb') as f:
        ftp.retrbinary('STOR ' + 'file_to_download.txt', f.write, 1024)

    ftp.quit()


