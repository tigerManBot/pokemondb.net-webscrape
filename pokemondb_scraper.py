from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from time import sleep
import re


def exit_privacy_control_popup(browser):
    """
    On chrome there is a popup from the site about privacy and control.
    This function closes the popup (if it actually pops up).
    Arguments:
        browser: WebDriver, for finding a web element on the page.
    """
    try:
        popup = browser.find_element(By.XPATH, './/a[@class = "text-small gdpr-decline"]')
        popup.click()
        return
    except NoSuchElementException:
        return


def display_pokedex_lst(native_pokedex_lst):
    """
    prints out the pokedex list the user chooses from.
    Arguments:
        native_pokedex_lst: a list of WebElements, each containing a link to a pokedex on the page.
    """
    for i, pokedex in enumerate(native_pokedex_lst):
        print(f"[{i}]: {pokedex.text}")
    print()


def get_pokedex(native_pokedex_lst):
    """
    Prompts the user to Enter the number that corresponds to the pokedex
    they wish to explore.
    Arguments:
        native_pokedex_lst: a list of WebElements, each containing a link to a pokedex on the page.
    Returns:
         a WebElement link that will later be clicked on.
    """
    while True:
        user_input = input("Enter a number corresponding to the pokedex you wish to explore [0-16]: ")
        try:
            index = int(user_input)
            if index in range(0, 17):
                return native_pokedex_lst[index]
            else:
                print(f"Error, {index} is outside of the expected range [0-16]. Please try again.")
        except ValueError:
            print(f"Error, {user_input} is not a number. Please try again.")


def reformat_pokedex(pokedex):
    """
    Removes the portion of the pokedex string starting with the parenthesis.
    For example, FireRed & LeafGreen (Kanto) turns into FireRed & LeafGreen
    The reason for this is that the link to the pokedex does not contain this text in the parenthesis.
    Without reformatting, the link can not be clicked on.
    Arguments:
        pokedex: A WebElement link. Its text will be worked on in this function.
    Returns:
        The pokedex's text reformatted (removed everything starting on the left parenthesis onwards)
    """
    reformatted_pokedex = pokedex.text
    portion_to_remove_regex = re.compile(r"(\(.+)\)$")
    # regex: Left parenthesis + any combination of characters(except new line) after the left parenthesis
    # and must end with right parenthesis

    match_obj = portion_to_remove_regex.search(pokedex.text)
    if match_obj:
        reformatted_pokedex = reformatted_pokedex.replace(match_obj.group(), '')
        reformatted_pokedex = reformatted_pokedex.rstrip()
    else:
        # this should never be reached as every pokedex WebElement should have a match
        print(f"Error in reformat_pokdex, invalid link. Ending program.\n")
        exit()
    return reformatted_pokedex


def get_national_number(browser):
    """" Grabs the national number for the current pokemeon.
    The current national number is an int needed to get the current pokemon's table data.
    Note, this number is different from the normal pokedex id.
    Arguments:
        browser: WebDriver, for finding a web element on the page.
    Returns:
       the national number of the current pokemon as an int.
    """
    next_national_number_link = browser.find_element(By.CLASS_NAME, "entity-nav-next")

    # The next national number will be used to calculate the current one
    # there is always a next national number so no need to worry about out of bounds index errors
    next_national_number = next_national_number_link.text.split()
    next_national_number = next_national_number[0].replace('#', '')     # necessary for converting to int
    return int(next_national_number) - 1


def sort_pokedex(pokemon_links, browser, pokedex_name):
    """
    Sorts the pokedex by type, into a dictionary (Key: pokemon type, Value: List of WebElements that link to pokemon of
    that type.)
    For example, all grass pokemon will be stored as a list for the key "GRASS".
    Any pokemon that has two types will be stored into each key.
    For example, Torterra is a Grass-Ground type and is stored in both GRASS and GROUND keys.
    The list is a list of WebElemenents (the link to that specific pokemon). Later on the user will select a type
    they wish to explore. So if they choose "Fire" as the type, then all the links in the FIRE key will be openend.
    Arguments:
        pokemon_links: list of WebElements: each element is a link to a pokemon in the pokedex
        browser: WebDriver, for finding a web element on the page.
        pokedex_name: str, the name of the pokedex that will be explored.
    Returns:
        A dictionary containing all the pokemon sorted by type.
        The dictionary is of the form:
            Key: pokemon type (For example, "FIRE", "GRASS", etc.
            Value: List of WebElements that link to pokemon of that type.
                Later on the user will select a type they wish to explore. So if they choose "Fire" as the type, then
                all the links in the FIRE key will be openend.
    """
    pokedex_by_type = {}  # Key: pokemon type, Value: list of WebElements (that link to pokemon of that type)
    print(f"\nGathering data from the entire {pokedex_name} pokedex! This will take a few minutes.")
    for pokemon in pokemon_links:
        pokemon.send_keys(Keys.CONTROL, Keys.ENTER)  # open the link in new tab
        browser.switch_to.window(browser.window_handles[1])  # switch view to next tab
        sleep(1)
        # get the type data of the current pokemon
        pokemon_types = get_current_types(browser)
        # loop through the current pokemon's types, to add the pokemon to pokedex_by_type
        for pokemon_type in pokemon_types:
            if pokemon_type not in pokedex_by_type:
                # this avoids a KeyError and initalizes the list for this type of pokemon
                pokedex_by_type[pokemon_type] = []
            pokedex_by_type[pokemon_type].append(pokemon)
        # switch back to main tab
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

    return pokedex_by_type


def get_current_types(browser):
    """
    Gets the current pokemon's type(s) and returns it as a list.
    A pokemon can have at most two types.
    Arguments:
        browser: WebDriver, for finding a web element on the page.
    Returns:
        a list of the pokemon types. Each element is a string and there can be at most two strings
    """
    national_number = get_national_number(browser)  # needed in order to get the table data as the xpath for each table
    # for each pokemon changes based on the national number.
    table_data = browser.find_elements(By.XPATH, f'//*[@id="tab-basic-{national_number}"]/div[1]/div[2]/table')
    table_data = table_data[0].text.split('\n')
    formatted_types = table_data[1].replace("Type", '')
    # For example, "Type GRASS GROUND" -> ["GRASS", "GROUND"]
    return formatted_types.split()


def explore_by_type(sorted_pokedex, browser):
    """
    The user enters a pokemon type they wish to explore.
    This function then opens all the links for pokemon who matche the entered type.
    The user can continue with another type or exit the program from here.
    Arguments:
        sorted_pokedex: a dictionary of pokemon sorted by their type.
        browser: WebDriver, for finding a web element on the page.
    """
    user_reply = 'y'
    while user_reply == 'y':
        type_to_explore = input("\nEnter a pokemon type to explore: ")
        reformatted_type = type_to_explore.upper()
        if reformatted_type not in sorted_pokedex:
            print(f"Error, {type_to_explore} is not a valid pokemon type in the selected pokedex.\nPlease try again.")
            return explore_by_type(sorted_pokedex, browser)
        else:
            print(f"\nOpenining the links for all {type_to_explore} pokemon.")
            for pokemon in sorted_pokedex[reformatted_type]:
                pokemon.send_keys(Keys.CONTROL, Keys.ENTER)     # open in next tab
                sleep(1)

        close_tabs(browser)
        user_reply = input("Would you like to explore another type? Quiting will end the program.\n"
                           "Enter Y/y or N/n: ").lower()


def close_tabs(browser):
    """
    When the user is ready, this will close all of the opened tabs.
    Arguments:
        browser: WebDriver, for finding a web element on the page.
    """
    user_input = input("When you're ready, press enter to close the opened tabs: ")
    for opened_tab in browser.window_handles[1:]:
        browser.switch_to.window(opened_tab)
        browser.close()

    browser.switch_to.window(browser.window_handles[0])


def main():
    print()

    # open up the pokedex page on pokemondb.net
    browser = webdriver.Firefox()
    browser.get("https://pokemondb.net/pokedex")

    exit_privacy_control_popup(browser)     # get rid of the privacy popup (if it pops up)

    # this page has a list of pokedexes to choose from
    native_pokedex_lst = browser.find_elements(By.TAG_NAME, "li")[69:86]
    # it excludes the national pokedex (this includes all the pokedex in all games, which would take too long)

    # have the user select a pokedex, then click on the link corresponding to their selection
    display_pokedex_lst(native_pokedex_lst)
    pokedex = get_pokedex(native_pokedex_lst)   # a WebElement, a link
    reformatted_pokedex = reformat_pokedex(pokedex)  # as a string now
    browser.find_element(By.LINK_TEXT, reformatted_pokedex).click()

    # grab the links for every pokemon in the pokedex
    pokemon_links = browser.find_elements(By.XPATH, './/a[@class= "ent-name"]')

    sorted_pokedex = sort_pokedex(pokemon_links, browser, reformatted_pokedex)

    explore_by_type(sorted_pokedex, browser)

    sleep(1)
    browser.quit()


if __name__ == "__main__":
    main()

    print()
