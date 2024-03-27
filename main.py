from sys import argv
from functions import get_special, get_code_desc, send_special
from time import sleep

def main(*args):
    dev = False

    if (len(args[0]) > 1 and args[0][1] == "-d"):
        dev = True

    print("DEV: " + str(dev))

    n = 0

    while n < 3:
        try:
            text, image = get_special()

            code, desc = get_code_desc(text)

            send_special(code, desc, image, True)
        except:
            sleep(3)


if __name__ == "__main__":
    main(argv)
