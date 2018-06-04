import sys
from util.copy_file import *

def main():

    credentials = get_credentials(sys.argv[1])
    sftp = connect_to_client(credentials)

    src = sys.argv[3]
    dest = sys.argv[4]

    if sys.argv[2] == 'put':
        copy_file_to_server(sftp,  src, dest)

    elif sys.argv[2] == 'get':
        get_file_from_server(sftp, src, dest)


if __name__ == '__main__':
    main()