COINS_VALUE = {"dollar": 1, "quarter": 0.25, "dime": 0.1, "nickel": 0.05, "penny": 0.01}

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.34,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.23,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 2.67,
    },
    "protein": {
        "ingredients": {
            "water": 10,
            "milk": 200,
            "coffee": 0,
        },
        "cost": 4.00,
    }
}


def print_report():
    """returns report with available amount of each resource"""
    return f"Water (ml): {resources['water']}\nMilk (ml): {resources['milk']}\n" \
           f"Coffee (g): {resources['coffee']}"


def enough_resources_for_choice():
    """returns True / False -> checks if it is possible to prepare drink with resources available"""
    can_make = True
    lack_of = ""
    for ingredient in choice_ing:
        if resources[ingredient] < choice_ing[ingredient]:
            can_make = False
            lack_of += ingredient
            lack_of += ", "
    if can_make is False:
        print(f"\nLack of {lack_of}please contact seller.")
    return can_make


def calculate_cad_value(coins_to_sum):
    """returns total sum for library of coins"""
    total = 0
    for i in coins_to_sum:
        total += COINS_VALUE[i] * coins_to_sum[i]
    return round(total, 2)


def coins_inserted_user():
    """returns library of coins inserted by user when total is enough to cover price,
    returns library with values of zero if user didn't have enough money"""
    total = 0
    coins_user_selected = {"dollar": 0, "quarter": 0, "dime": 0, "nickel": 0, "penny": 0}
    cont = True
    while total < choice_price and cont is True:
        coin = input("\nWhich coin is it? dollar / quarter / dime / nickel or penny? ").lower()
        coin_value = COINS_VALUE[coin]
        coins_user_selected[coin] += 1
        total += coin_value
        left = round(choice_price - total, 2)

        if left > 0:
            print(f"Current total is CAD {round(total,2)}. CAD {left} left.")
            cont_quest = input("Do you have more coins? y / n: ")
            if cont_quest == "n":
                cont = False
                print(f"Here is your money back - CAD {total}, please select other coffee.")
                coins_user_selected = {"dollar": 0, "quarter": 0, "dime": 0, "nickel": 0, "penny": 0}

        elif left == 0:
            print(f"Current total is CAD {round(total,2)}. It is exact amount needed!.")
        else:
            print(f"Current total is CAD {round(total,2)}. You put CAD {left * -1} more than needed.")

    return coins_user_selected


def coins_add(coins1, coins2):
    """adds value from two libraries, returns new library"""
    total_coins = {"dollar": 0, "quarter": 0, "dime": 0, "nickel": 0, "penny": 0}
    for i in total_coins:
        total_coins[i] = coins1[i] + coins2[i]
    return total_coins


def coins_minus(coins1, coins2):
    """find difference between values of first and second library and returns new library"""
    total_coins = coins1
    for i in total_coins:
        total_coins[i] -= coins2[i]
    return total_coins


def change_actual_coins():
    """returns coins used for change (maximal possible value based on coins available in machine)"""
    total_user = calculate_cad_value(coins_user)
    sum_left = total_user - choice_price
    total_coins = coins_add(coins_user, coins_machine)

    coins_used = {"dollar": 0, "quarter": 0, "dime": 0, "nickel": 0, "penny": 0}

    for i in coins_used:
        if total_coins[i] > 0 and COINS_VALUE[i] <= sum_left:
            amount = int(sum_left / COINS_VALUE[i])
            coins_used[i] = min(amount, total_coins[i])
            sum_left -= COINS_VALUE[i] * coins_used[i]
        else:
            coins_used[i] = 0

    return coins_used


def print_change_actual(change_coins):
    """prints text with description of coins used for change"""
    change_to_be_paid = calculate_cad_value(change_coins)

    text_change = ""
    for i in change_coins:
        if change_coins[i] > 0:
            text_change += str(change_coins[i])
            text_change += " "
            text_change += i
            text_change += "(s), "

    if change_to_be_paid > 0:
        print(f"Here is you change of CAD {round(change_to_be_paid,2)}: {text_change}please.")


def continue_if_change_not_paid(change_calculated, change_expected):
    """Asks if user want to continue if there is no some coins available and change is less than expected"""
    not_paid = change_calculated - change_expected
    quest = input(f"There is no coins for change of CAD {round(not_paid,2)}. Do you wanna proceed? y / n: ")
    if quest == "y":
        return True
    else:
        return False


def step_cash():
    """returns balance of coins in machine after operations done"""
    coins_total = calculate_cad_value(coins_user)

    if coins_total > 0:
        change_sum_expected = coins_total - choice_price
        coins_change_v = change_actual_coins()
        change_sum_actual = calculate_cad_value(coins_change_v)

        if change_sum_actual != change_sum_expected:
            wanna_proceed = continue_if_change_not_paid(change_sum_expected, change_sum_actual)

            if wanna_proceed:
                print_change_actual(coins_change_v)
                return coins_minus(coins_add(coins_user, coins_machine), coins_change_v)
            else:
                print(f"\nHere is your money back - CAD {coins_total}, please try to pay with credit card.")
                return coins_machine
        else:
            print_change_actual(coins_change_v)
            return coins_minus(coins_add(coins_user, coins_machine), coins_change_v)
    else:
        return coins_machine


def make_coffee():
    """decreases available resources according to recipe"""
    if enough_resources:
        resources_new = {"water": 0, "milk": 0, "coffee": 0}
        for ingredient in resources_new:
            if ingredient in choice_ing:
                resources_new[ingredient] = resources[ingredient] - choice_ing[ingredient]
            else:
                resources_new[ingredient] = resources[ingredient]
    else:
        resources_new = resources
    return resources_new


def reload():
    """allows to add resources, return new balance of resources"""
    for i in resources:
        resources[i] += int(input(f"How much {i} do you wanna add? "))
    return resources


# to set starting resources
resources = {"water": 100, "milk": 200, "coffee": 100}
coins_machine = {"dollar": 0, "quarter": 0, "dime": 0, "nickel": 0, "penny": 0}
account_machine = 0

# machine is turn on by default
machine_on = True

# if off bottom is not pressed
while machine_on:

    print("-------------------------------------------------------------------\nHi there!")

    # allows to check available resources if user wants
    if_report = input("Do you wanna know available resources? y / n: ").lower()
    if if_report == "y":
        print(f"\nHello, available resources are:\n{print_report()}")
        print(f"Available coins for change are: {coins_machine}.")

    # allows to add resources to machine if user wants
    if_reload = input("\nDo you wanna reload resources? y / n: ").lower()
    if if_reload == "y":
        resources = reload()

    # allows user to select coffee that he wants and finds needed ingredients and price
    choice = input("\nWhat would you like? (espresso/latte/cappuccino/protein): ")
    choice_lib = MENU[choice]
    choice_ing = choice_lib["ingredients"]
    choice_price = choice_lib["cost"]

    # checks if there are enough resources to prepare selected drink
    enough_resources = enough_resources_for_choice()

    if enough_resources:

        # checks if 10% discount should be provided
        reg_cust = input("\nDo you have a card of regular customer? y / n: ")
        if reg_cust == "y":
            choice_price = round(choice_lib["cost"] * (1 - 0.1), 2)

        # prints price and propose payment method selection
        print(f"\nThe price is CAD {choice_price}, please insert money.")
        payment_way = input("\nDo you wanna pay with bank (credit card) or cash? bank / cash: ").lower()

        # calculates coins before and after operation and identify if t was successful
        # if payment was successful, then coffee is made
        if payment_way == "cash":
            money_before = coins_machine
            coins_user = coins_inserted_user()
            coins_machine = step_cash()

            if money_before == coins_machine:
                should_make_coffee = False
            else:
                should_make_coffee = True

        else:
            # bank operation, adds money to account -> always successful
            print(f"\nCAD {choice_price} was paid from you card. Thank you for using credit card!")
            account_machine += choice_price
            should_make_coffee = True

        if should_make_coffee:
            # makes coffee, decreases resources
            resources = make_coffee()
            print_report()

            # final wording confirming successful operation
            print(f"\nHere is your {choice}. Enjoy!")
            print(f"\nTotal cash is {round(calculate_cad_value(coins_machine), 2)}.")
            print(f"\nTotal money on account is {round(account_machine,2)}.")

        # allows to stop or continue code
        on_off = input("\nDo you wanna turn off machine? y / n: ").lower()
        if on_off == "y":
            print("Turning off, goodbye!")
            machine_on = False
