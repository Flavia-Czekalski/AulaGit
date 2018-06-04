import sys
from util.connect_to_server import *


def main():
    credentials = get_credentials(sys.argv[1])

    command = str(sys.argv[2])

    client = connect_to_client(credentials)

    run_command(client, command)



if __name__ == '__main__':
    main()