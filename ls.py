import os
from colorama import Fore, Style
from sys import argv
import argparse

class DD:
    def __init__(self, args):
        self.source = args.source
        self.show_hidden = args.show_hidden
        self.sort_by_name = args.sort_by_name
        self.detailed_listing = args.detailed_listing

        self.FOLDER_COLOR = Fore.BLUE
        self.EXE_COLOR = Fore.GREEN
        self.NEUTRAL_COLOR = Fore.WHITE

        if args.help:
            self.display_help()
        else:
            self.display_dir()
        print(Style.RESET_ALL)

    def display_dir(self) -> int:
        dirList = [item for item in os.listdir(self.source) if self.show_hidden or not item.startswith(".")]

        if self.sort_by_name:
            dirList.sort()

        for item in dirList:
            item_path = os.path.join(self.source, item)
            item_type = "d" if os.path.isdir(item_path) else "f"
            item_color = (
                self.FOLDER_COLOR if item_type == "d"
                else self.EXE_COLOR if os.access(item_path, os.X_OK)
                else self.NEUTRAL_COLOR
            )

            if self.detailed_listing:
                item_stats = os.stat(item_path)
                size = item_stats.st_size
                modified_time = item_stats.st_mtime
                formatted_time = self.format_time(modified_time)
                print(f"{Style.BRIGHT}{item_color}{item} {Fore.RESET}Size: {size} bytes, Modified: {formatted_time}")
            else:
                print(f"{Style.BRIGHT}{item_color}{item}", end=f"{Style.RESET_ALL}  ")

        return 0

    def display_help(self):
        print(f"Usage: python {argv[0]} [OPTIONS] [SOURCE]")
        print("List files and directories in the specified directory.")
        print("\nOptions:")
        print("  -a      Show hidden files and directories")
        print("  -S      Sort entries by name")
        print("  -l      Long format (detailed) listing")
        print("  -h      Display this help message and exit")
        print("\nIf SOURCE is not specified, the current directory is used.")

    @staticmethod
    def format_time(timestamp):
        import datetime
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("source", nargs="?", default=".")
    parser.add_argument("-a", "--show-hidden", action="store_true", help="Show hidden files and directories")
    parser.add_argument("-S", "--sort-by-name", action="store_true", help="Sort entries by name")
    parser.add_argument("-l", "--detailed-listing", action="store_true", help="Long format (detailed) listing")
    parser.add_argument("-h", "--help", action="store_true", help="Display this help message")

    args = parser.parse_args()
    DD(args)
