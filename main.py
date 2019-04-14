import restaurant.cafe_magdalen


if __name__ == "__main__":

    food_for_the_week = restaurant.cafe_magdalen.food()

    for num, lst in food_for_the_week.items():
        print(lst)

