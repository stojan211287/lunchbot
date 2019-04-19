import restaurant.cafe_magdalen

from collections import defaultdict

from argparse import ArgumentParser


if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("--day", default="monday", dest="day")
    args = parser.parse_args()

    menu = restaurant.cafe_magdalen.menu()
    
    try:
        print(menu[args.day.lower()])
    except KeyError:
        raise Exception(f"Day {args.day} does not seem to be present in the menu.")