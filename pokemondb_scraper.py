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
        browser: selenium webdriver, for finding a web element on the page.
    """
    try:
        popup = browser.find_element(By.XPATH, './/a[@class = "text-small gdpr-decline"]')
        popup.click()
        sleep(1)
    except NoSuchElementException:
        sleep(1)
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
    Prompts the user to select the number that corresponds to the pokedex
    they wish to explore.
    Arguments:
        native_pokedex_lst: a list of WebElements, each containing a link to a pokedex on the page.
    Returns:
         a WebElement link that will later be clicked on.
    """
    user_input = input("Select a number corresponding to the pokedex you wish to explore (0-17): ")
    try:
        index = int(user_input)
        if index in range(0, 18):
            return native_pokedex_lst[index]
        else:
            print(f"Error, {index} is outside of the expected range [0-17]. Please try again.")
            return get_pokedex(native_pokedex_lst)
    except ValueError:
        print(f"Error, {user_input} is not a number. Please try again.")
        return get_pokedex(native_pokedex_lst)


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
    # + must end with right parenthesis

    match_obj = portion_to_remove_regex.search(pokedex.text)
    if match_obj:
        reformatted_pokedex = reformatted_pokedex.replace(match_obj.group(), '')
        reformatted_pokedex = reformatted_pokedex.rstrip()
    else:
        # this should never be reached as every pokedex WebElement should have a match
        print(f"Error in reformat_pokdex, invalid link. Ending program.\n")
        exit()
    return reformatted_pokedex


def main():
    print()

    # open up the pokedex page on pokemondb.net
    browser = webdriver.Chrome()
    browser.get("https://pokemondb.net/pokedex")
    sleep(1)

    exit_privacy_control_popup(browser)     # get rid of the privacy popup (if it pops up)

    # this page has a list of pokedexes to choose from
    native_pokedex_lst = browser.find_elements(By.TAG_NAME, "li")[68:86]
    # 68-86 is the section of the list that contain the pokedex links
    sleep(1)

    # have the user select a pokedex, then click on the link corresponding to their selection
    display_pokedex_lst(native_pokedex_lst)
    pokedex = get_pokedex(native_pokedex_lst)   # a web element
    reformatted_pokedex = reformat_pokedex(pokedex)  # as a string now
    browser.find_element(By.LINK_TEXT, reformatted_pokedex).click()

    # For tommorow
    # open the pokemeon links, a class="ent-name" in a new tab
    # possibly switch views to the new tab if necessary
    # gather the specific data

    # data to gather:
    #

    # loop through their type list (could just be one type)
    # in loop: add the pokemon to a dictionary: Key: type, Value: List of pokemon with this type
    # note, that the list of pokemon is a list of Pokemon (custom type) containing all relevant data

    # this way th

    # close this new tab, possibly switch views to main window
    # begin on the next pokemon and so on
    # test it in increments, (ie, test 3 pokemon, then test 5, then test 10, then test all)

    sleep(5)
    browser.quit()


if __name__ == "__main__":
    main()

    print()
