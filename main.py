from sys import argv
from functions import get_special, get_code_desc, send_special

def main(*args):
    dev = False

    if (len(args[0]) > 1 and args[0][1] == "-d"):
        dev = True

    print(str(dev))


    text, image = get_special()

    code, desc = get_code_desc(text)

    send_special(code, desc, image, True)

if __name__ == "__main__":
    main(argv)
