import sys

tty = sys.stdout.isatty()


class TerminalColors:
    HEADER = '\033[95m' if tty else ''
    OKCYAN = '\033[96m' if tty else ''
    ERROR = '\033[31;1;4m' if tty else ''
    BOLD = '\033[1m' if tty else ''
    GREY = '\033[38;5;248m' if tty else ''
    ENDC = '\033[0m' if tty else ''
    PINK = '\033[38;5;206m' if tty else ''
    EXCYAN = ''
