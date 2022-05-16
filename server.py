import sys, time

import escm_server as escm


def main():


        server = escm.ESCM_server()
        server.run()

if __name__ == '__main__':
    main()
