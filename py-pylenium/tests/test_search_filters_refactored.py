"""
Use of namedtuples and  passing functions @pytest.mark.parametrize make it possible to write concise test.
I also allows pass functions to
"""

import logging
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import pytest
from collections import namedtuple

search_category_locators = ['[id="label-mode.rooms"]', '[id="label-mode.people"]', '[id="label-mode.teamups"]']
search_queries = ['chippendale']
Rent = namedtuple('Rent', 'min max')
rents = [Rent(*r) for r in [(100, 600)]]

# TODO:  implement assertions for search results


# filter methods
def type_numbers(do_, values: Rent) -> None:
    do_.get('input[name="min_budget"]').should().be_visible().clear().type(str(values.min))
    do_.get('input[name="max_budget"]').should().be_visible().clear().type(str(values.max))


# package parameters for  @pytest.mark.parametrize()
filter_methods = [type_numbers]
Search_config = namedtuple('search_conf', 'category_locator query filter_method filter_value')
search_params = [
    Search_config(category_locator=category_item,
                  query=query_item,
                  filter_method=method_item,
                  filter_value=filter_item)
    for category_item in search_category_locators
    for query_item in search_queries
    for method_item in filter_methods
    for filter_item in rents]


def ids_(param):
    return repr(param)


# verify that search filters and categories work as expected: rooms, flatmates, teamups, rent, date, checkboxes, etc.
@pytest.mark.parametrize('search', search_params, ids=ids_)
def test_search_filters_param(do, search: Search_config):

    load_page(do)
    assert do.should().have_title('Share Accommodation | Flatmates.com.au')
    click_consent_button(do)
    do.click_with_retry(
        css='[class*="mainHeading"]', exp_condition=ec.invisibility_of_element_located(
            (By.CSS_SELECTOR, '[class*="mainHeading"]')))  # has retry cycle based on expected condition
    do.get('#choice-mode-rooms').should().be_clickable().click()
    do.get('.hiddenInput').should().be_clickable().type(search.query)
    do.get('.inputAutocomplete').children().first().click()
    assert do.get('.token').should().be_visible().should().contain_text(search.query.title())

    click_submit_button(do)
    assert do.get('.head > .logo').should().be_visible()  # logo.
    assert search.query.title() in do.get(
        '[class*="search"]  [class*="mainHeading"] ').should().be_visible().text()  # search bar

    click_filters_button(do)
    assert do.get('.token').should().be_visible().should().contain_text(search.query.title())

    do.get(search.category_locator).should().be_clickable().click()

    search.filter_method(do, search.filter_value)
    do.wait(use_py=True).sleep(2)


def click_submit_button(do) -> None:
    logo = do.get('.head > .logo')
    home_listings = do.get('[class*="home-listings"]')
    do.get('button[type="submit"]').click()
    logo.should().disappear()
    home_listings.should().disappear()


def click_consent_button(do) -> None:
    consent_button = do.get('button[class*="gdpr-consent"]')
    assert consent_button.should().be_visible().should().be_clickable()
    consent_button.click()


def load_page(do) -> None:
    do.visit('https://flatmates.com.au/')


def click_filters_button(do) -> None:
    filters_button = do.get('[class*="filters"]')
    filters_button.should().be_clickable().click()
    filters_button.should().disappear()

