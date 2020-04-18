import logging
import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


"""
Same as my_first_test.py, but without the asserts.
"""

from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("https://xkcd.com/353/")
        self.click('a[rel="license"]')
        self.go_back()
        self.click("link=About")
        self.open("https://store.xkcd.com/collections/everything")
        self.update_text("input.search-input", "xkcd book\n")


    def test_gumtree(self):
        self.open("https://www.gumtree.com.au/")
        #Cars
        self.assert_element("#nav-my")
        self.click("#nav-my")
        self.assert_element("a[href='/cars']")
        self.assert_text("Cars & Vehicles", "a[href='/cars']")
        t1 = self.get_text("a[href='/cars']")
        logging.info(f"Text in link: {t1}")
        self.click("a[href='/cars']")
        self.click("a[href='/cars']")
        assert self.assert_text("Sell where the buyers are")
        assert self.assert_element(".header__home-hero-title__text")
        assert self.assert_element(".header__home-hero-subheader")


        self.go_back()

        self.assert_element("li[class*='primary-navigation']>a[href^='/s-home']")
        self.assert_element("li[class*='primary-navigation']>a[href^='/jobs']")
        self.assert_element("[class*='primary-navigation']>a[href^='/s-real']")

        self.assert_element("[class*='primary-navigation']>a[href^='/s-services']")

        t3 = self.get_attribute("#search-query", attribute="placeholder")
        logging.info(f"Text in search input: {t3}")
        self.assert_element("#search-query")
        self.click(".search-bar__category-name")
        self.click(".search-bar__category-name")
        self.assert_element(".search-bar__category-name")
        self.assert_element("[class*='new-listing-button']")

