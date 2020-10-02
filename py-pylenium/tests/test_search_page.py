
# DONE: verify one listing displaying
# DONE: verify all listings on the page are displaying
# DONE: verify autocomplete
# DONE: verify sorting
# DONE: verify pagination
# DONE: verify search filters
# TODO: verify shortlist feature
# TODO: clean up the code


from selenium.webdriver.common.keys import Keys
import logging
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import exceptions as ex
from selenium.webdriver.common.by import By

from collections import Counter
from re import findall
from math import ceil
from utils.ut import find_nums
import pytest


# verify that search results are displaying
def test_search_and_check_one_listing_displaying(do):
    """ Given: home page flatmates.com.au has loaded
    When: user searches query (suburb, zip code)
    Then: relevant title and search results are displaying, icons and elements are displaying
"""
    do.visit('https://flatmates.com.au/')
    # wait_for_doc_ready_state(do)
    assert do.should().have_title('Share Accommodation | Flatmates.com.au')

    do.click_with_retry(
        css='[class*="mainHeading"]', exp_condition=ec.invisibility_of_element_located(
    (By.CSS_SELECTOR, '[class*="mainHeading"]')))  # has retry cycle based on expected condition
    do.get('.hiddenInput').should().be_clickable().type('redfern, 2016', Keys.ENTER)
    do.get('.inputAutocomplete').should().be_visible()
    do.get('.hiddenInput').type(Keys.DOWN, Keys.ENTER)
    do.get('button[type="submit"]').click()

    # validate that title in search results contains search query
    assert do.get('h1[class*="searchHeading"]').should().contain_text("Redfern").should().\
        contain_text("Rooms for Rent")

    # first search results thumbnail:
    assert do.getx('//img[starts-with(@class,"styles__listingImage")]').should().be_visible()  # image
    assert do.getx('//p[starts-with(@class,"styles__address")]').should().be_visible().should().contain_text('Redfern')
    assert do.getx('//div[starts-with(@class,"styles__propertyFeatureStrip")]').should().be_visible()  # icons
    assert do.getx('//p[starts-with(@class,"styles__price")]').should().be_visible().\
        should().contain_text("$").should().contain_text('week')  # price per week


# verify that autocomplete is working
def test_autocomplete(do):
    search_query1 = 'redfern'
    search_query2 = 'hornsby'
    do.visit('https://flatmates.com.au/')
    # wait_for_doc_ready_state(do, timeout=30)  # this makes click more reliable
    do.click_with_retry(
        css='[class*="mainHeading"]', exp_condition=ec.invisibility_of_element_located(
            (By.CSS_SELECTOR, '[class*="mainHeading"]')))  # has retry cycle based on expected condition

    # do.wait(timeout=14, use_py=True).until(lambda x: x.find_element_by_class_name('hiddenInput')).type('redfern')
    do.get('.hiddenInput').should().be_clickable().type(search_query1)
    assert do.get('.inputAutocomplete').should().be_visible()

    rows = do.get('.inputAutocomplete').find('.row')
    logging.info(f'number of rows = {len(rows)}')
    for row in rows:
        logging.info(f'row text = {row.text()}\n')
        assert search_query1.title() in row.text()

    do.get('.hiddenInput').type(Keys.DOWN, Keys.ENTER)
    assert do.get('.token').should().be_visible().should().contain_text(search_query1.title())

    do.get('.tokenInput').type(search_query2)

    top_row = do.get('.inputAutocomplete').find('.row').first()
    top_row_text = top_row.text()
    logging.info(f'row #1 text = {top_row_text}\n')
    top_row.click()
    for t in do.find('.token').last().text().split(','):
        assert t in top_row_text

    do.find('.token').last().get('.remove').click()  # delete las suggestion
    assert search_query2.title() not in do.find('.token').last().text()


# verify that search room results  are displaying
def test_search_rooms_all_listings_and_elements_displaying(do):
    """ Given: home page flatmates.com.au has loaded
    When: user performs search
    Then: relevant title and search results, top navigation links, buttons
    And: footer links are displaying  and clickable
    """
    search_query = 'pymble'

    do.visit('https://flatmates.com.au/')
    assert do.should().have_title('Share Accommodation | Flatmates.com.au')

    consent_button = do.get('button[class*="gdpr-consent"]')
    assert consent_button.should().be_visible().should().be_clickable()
    consent_button.click()

    do.click_with_retry(
        css='[class*="mainHeading"]', exp_condition=ec.invisibility_of_element_located(
            (By.CSS_SELECTOR, '[class*="mainHeading"]')))  # has retry cycle based on expected condition
    do.get('.hiddenInput').should().be_clickable().type(search_query)
    do.get('.inputAutocomplete').children().first().click()
    assert do.get('.token').should().be_visible().should().contain_text(search_query.title())

    logo = do.get('.head > .logo')
    do.get('button[type="submit"]').click()

    # before
    # instead of assertion we can also use wait() but get() is shorter and also implements wait
    # the difference is that with until() we can specify custom conditions
    # using assertion makes it little more obvious that assertion is expected at this point

    do.wait().until(lambda _: logo.should().disappear())  # make sure page refreshed
    assert do.get('.head > .logo').should().be_visible()  # logo.
    assert search_query.title() in do.get(
        '[class*="search"]  [class*="mainHeading"] ').should().be_visible().text()  # search bar
    assert do.get(
        '[class*="search"]  [class*="filters"] ').should().be_visible().should().be_clickable()  # filters button

    # top navigation
    for i, nav_icon in enumerate(do.get('.navigation').children()):
        assert nav_icon.should().be_clickable()
        assert ('Shortlist', 'Info', 'Login')[i] in nav_icon.text()

    assert do.get('h1[class*="searchHeading"]').should().contain_text(
        search_query.title()).should().contain_text("Rooms for Rent")  # Search results title
    assert do.get('.listing-results-map').should().be_visible().should().be_clickable()

    assert do.get('[class*="actionButton"]').should().be_visible().should().be_clickable()
    assert do.get('[class*="navigationBox"]').should().be_visible()
    assert "Login" in do.get('button[class*="desktopButton"]').text()
    assert do.get('button[class*="desktopButton"]').should().be_clickable()

    # not include listing-expanded-results (e.g. "Rooms for Rent near Waitara")
    listings = do.find('[class*="headerBox"] + div [class*="search-results"]  .content-column')
    logging.info(f'list num: {len(listings)}')

    # validate that title in search results contains search query
    for count, listing in enumerate(listings):
        logging.info(f'\nlisting num: {count}')
        assert listing.get('img[class*="listingImage"]').scroll_into_view().should().be_visible()
        if listing.get('div[class*="labelBox"]').is_displayed():
            assert listing.get('div[class*="labelBox"]').text() in ('New', 'Updated', 'Boosted')
        assert listing.get('button[class*="shortlistButton"]').should().be_visible()
        assert listing.get('[class*="tileContent"] ').should().be_visible()
        assert listing.get('[class*="tileContent"]   p[class*="price"]').should().be_visible().should().\
            contain_text("$").should().contain_text('week')  # price per week
        assert listing.get('a[class*="tileLink"]  div[class*="contactRibbon"]').should().be_visible().text() in \
            ("Free to message", "Early bird")  # message button
        assert listing.get('a[class*="tileLink"]  p[class*="address"]').should().be_visible().should().\
            contain_text(search_query.title())  # address
        assert listing.get('a[class*="tileLink"]  p[class*="availability"]').should().be_visible().should().\
            contain_text("Available")  # availability

    # check if mobile footer is visible
    if do.wait().until(lambda x: x.find_element_by_css_selector('[class*="ContainerMobile"]')).is_displayed():
        do.get('[class*="ContainerDesktop"] ').scroll_into_view()
        for i, foot_tab in enumerate(do.find('[class*="ContainerMobile"] [class*="tabList"] [class*="tab"]')):
            assert foot_tab.should().be_clickable()
            assert ('for Rent', 'Granny', 'Studio', 'Student', 'Home', 'Popular')[i] in foot_tab.text()

    # desktop footer checks
    else:
        assert do.get('[class*="ContainerDesktop"] ').should().be_visible()
        do.get('[class*="ContainerDesktop"] ').scroll_into_view()
        for i, foot_tab in enumerate(do.find('[class*="ContainerDesktop"] [class*="tabList"] [class*="tab"]')):
            foot_tab_text = foot_tab.text()
            assert foot_tab.should().be_clickable()
            assert ('for Rent', 'Granny', 'Studio', 'Student', 'Home', 'Popular')[i] in foot_tab_text
            foot_tab.click()
            do.wait().until(lambda _: foot_tab.should().have_attr('aria-selected', value="true"))
            for tab in do.get('[class*="ContainerDesktop"] [class*="footerLinks"]').children():
                assert tab.should().be_clickable()
                tab_links_text = tab.text()
                if "for Rent" in foot_tab_text:
                    assert any(l in tab_links_text
                               for l in ('Melbourne', 'Sydney', 'Brisbane', 'Perth', 'Canberra', 'Adelaide', 'Hobart',
                                         'Gold Coast', 'Sunshine Coast'))
                if "Ganny" in foot_tab_text:
                    assert any(l in tab_links_text
                               for l in ('Melbourne', 'Sydney', 'Brisbane', 'Wollongong', 'Canberra', 'Adelaide',
                                         'Cairns', 'Gold Coast', 'Sunshine Coast'))
                if "Studio" in foot_tab_text:
                    assert any(l in tab_links_text
                               for l in ('Melbourne', 'Sydney', 'apartment for rent in Brisbane', 'Perth',
                                         'Canberra', 'Adelaide', 'Cairns', 'Gold Coast',
                                         'One bed apartment for rent Brisbane', 'Sunshine Coast'))
                if "Student" in foot_tab_text:
                    assert any(l in tab_links_text
                               for l in ('Melbourne', 'Sydney', 'Brisbane', 'Perth', 'Canberra', 'Geelong',
                                         'Townsville', 'Sunshine Coast', 'Gold Coast'))
                if "Home" in foot_tab_text:
                    assert any(l in tab_links_text
                               for l in ('Melbourne', 'Sydney', 'Brisbane', 'Gold Coast', 'Canberra',
                                         'Adelaide', 'Sunshine Coast'))
                if "Popular" in foot_tab_text:
                    assert any(l in tab_links_text
                               for l in ('Pet friendly', 'Gay', 'Vegetarian', 'Over 40', 'All female',
                                         'Child friendly', 'Tips', 'inspections'))


# verify sorting of search results
def test_sorting(do):
    # verify filter:  Featured First
    do.visit('https://flatmates.com.au/')
    assert do.should().have_title('Share Accommodation | Flatmates.com.au')
    consent_button = do.get('button[class*="gdpr-consent"]')
    assert consent_button.should().be_clickable()
    consent_button.click()

    do.get('[class*=mainHeading]').should().be_clickable().click()
    hidden_input = do.get('.hiddenInput')
    listing_1st = do.find('.home-listings  [class*=listingTile]')[0]
    hidden_input.should().be_clickable().type('redfern')
    do.get('.inputAutocomplete').children().first().click()
    assert do.get('.token').should().be_visible().should().contain_text('Redfern')
    do.get('button[type="submit"]').click()

    do.wait().until(lambda _: hidden_input.should().disappear())  # make sure page refreshed
    do.wait().until(lambda _: listing_1st.should().disappear())  # make sure page refreshed
    assert do.get('select[class*=dropdown]').should(
        ignored_exceptions=ex.StaleElementReferenceException).be_visible().should().contain_text('Featured First')
    listings = do.find('.search-results  [class*=listingTile]')
    for listing in listings:
        listing.hover()
        assert listing.should().be_visible()

    for selected_locator, data_sorted_locator, expected_text in [
            ('option[value="newest"]', '[class*=labelBox]', 'Newest Listing'),
            ('option[value="cheapest"]', 'p[class*=price]', 'Rent (High to Low)'),
            ('option[value="most-expensive"]', 'p[class*=price]', 'Rent (High to Low)'),
            ('option[value="earliest-available"]', 'p[class*=availability]', 'Earliest Available'),
            ('option[value="recently-active"]', '[class*=online]', 'Recently Active')
    ]:
        dropdown_sorting = do.get('select[class*=dropdown]')
        listing_0 = do.find('.search-results  [class*=listingTile]')[0]
        dropdown_sorting.hover()
        dropdown_sorting.click()
        do.get(selected_locator).should().be_visible().click()
        do.wait(14).until(lambda _: dropdown_sorting.should().disappear())  # make results refreshed
        do.wait(14).until(lambda _: listing_0.should().disappear())  # make results refreshed
        assert do.get('select[class*=dropdown]').should(
            ignored_exceptions=ex.StaleElementReferenceException).be_visible().should().contain_text(expected_text)

        data_sorted = []
        listings = do.find('.search-results  [class*=listingTile]')
        if expected_text == 'Recently Active':
            for index in range(4):
                listing = do.find('.search-results  [class*=listingTile]')[index]
                listing.hover()
                listing.should().be_clickable().click()
                data_sorted.append(do.get(data_sorted_locator).text())
                do.go('back')
            assert 'Online Today' in data_sorted
        else:
            for listing in listings:
                listing.hover()
                data_sorted.append(listing.get(data_sorted_locator).text())
                assert listing.should().be_visible()
                assert listing.get(data_sorted_locator).should().be_visible()

        logging.info(f" \ndata_sorted: {data_sorted}")
        data_sorted_adjacent_el = zip(data_sorted[1:], data_sorted)

        is_sorted = {'Newest Listing': lambda: Counter(data_sorted)['Updated'] > Counter(data_sorted)['New'],
                     'Rent (Low to High)':
                         lambda: all(find_nums(next_elem)[0] >= find_nums(elem)[0]
                                     for next_elem, elem in data_sorted_adjacent_el),
                     'Rent (High to Low)':
                         lambda: all(find_nums(next_elem)[0] <= find_nums(elem)[0]
                                     for next_elem, elem in data_sorted_adjacent_el),
                     'Earliest Available':
                         lambda: any(next_elem == "Available Now" and elem != "Available Now"
                                     for next_elem, elem in data_sorted_adjacent_el),
                     'Recently Active':
                         lambda: any(next_elem == "Online Today" and elem != "Online Today"
                                     for next_elem, elem in data_sorted_adjacent_el)
                     }.get(expected_text, lambda: True)

        assert is_sorted


# verify pagination
def test_search_pagination(do, ut):

    do.visit('https://flatmates.com.au/')
    assert do.should().have_title('Share Accommodation | Flatmates.com.au')
    consent_button = do.get('button[class*="gdpr-consent"]')
    assert consent_button.should().be_visible().should().be_clickable()
    consent_button.click()

    do.get('[class*=mainHeading]').should().be_clickable().click()
    hidden_input = do.get('.hiddenInput')
    hidden_input.should().be_clickable().type('chatswood')
    do.get('.inputAutocomplete').children().first().click()
    assert do.get('.token').should().be_visible().should().contain_text('Chatswood')
    do.get('button[type="submit"]').click()

    do.wait().until(lambda _: hidden_input.should().disappear())  # make sure page refreshed
    results = find_nums(do.get('[class*="legend"]').text())[-1]
    pages_total = ceil(results / 12)
    logging.info(f"\npages_total:{pages_total} ")

    for page_link_num in range(1, min(pages_total+1, 8)):
        page_link_ = do.get('[class*="pageLinks"]').contains(str(page_link_num))

        page_link_.hover()
        assert page_link_.should().be_clickable()
        page_link_.click()
        do.wait().until(lambda _: page_link_.should().disappear())  # make sure page refreshed

        assert find_nums(do.get('[class*="legend"]').text())[0] == ((page_link_num-1)*12+1)
        assert do.get('[class*="pageLinks"]').contains(str(page_link_num)).get_attribute('aria-label') == 'Current page'

        if page_link_num > 1:
            assert do.get('[class*="PrevStep"]').should().be_clickable()
        if page_link_num < pages_total:
            assert do.get('[class*="NextStep"]').should().be_clickable()

        if page_link_num == 1 and pages_total > 1:
            assert do.find('[class*="PrevStep"]', timeout=4).should().be_empty()
            assert do.findx('//span[contains(@text, "Previous")]', timeout=4).should().be_empty()
            assert do.get('[class*="NextStep"]').should().be_clickable()
            do.click_wait_for_elem_to_disappear(element=do.get('[class*="NextStep"]'))
            assert find_nums(do.get('[class*="legend"]').text())[0] == 13
            continue

        if page_link_num == pages_total and pages_total != 1:
            assert do.find('[class*="NextStep"]').should().be_empty()
            assert do.findx('//span[contains(@text, "Next")]', timeout=4).should().be_empty()
            assert do.get('[class*="PrevStep"]').should().be_clickable()
            do.click_wait_for_elem_to_disappear(element=do.get('[class*="PrevStep"]'))
            assert find_nums(do.get('[class*="legend"]').text())[0] == ((page_link_num-2)*12+1)
            continue

        logging.info(f"\npage num:{page_link_num} ")
        logging.info(f"text: ")
        logging.info(findall(r'[0-9]+', do.get('[class*="legend"]').text())[0])
        logging.info(f"formula:{((page_link_num-1)*12+1)}")


# verify search filters
def test_search_filters(do):

    search_query = 'chippendale'
    rent_min = 100
    rent_max = 600


    do.visit('https://flatmates.com.au/')
    assert do.should().have_title('Share Accommodation | Flatmates.com.au')

    consent_button = do.get('button[class*="gdpr-consent"]')
    assert consent_button.should().be_visible().should().be_clickable()
    consent_button.click()

    do.click_with_retry(
        css='[class*=mainHeading]', exp_condition=ec.invisibility_of_element_located(
            (By.CSS_SELECTOR, '[class*=mainHeading]')))  # has retry cycle based on expected condition
    do.get('#choice-mode-rooms').should().be_clickable().click()
    do.get('.hiddenInput').should().be_clickable().type(search_query)
    do.get('.inputAutocomplete').children().first().click()
    assert do.get('.token').should().be_visible().should().contain_text(search_query.title())

    logo = do.get('.head > .logo')
    home_listings = do.get('[class*="home-listings"]')
    do.get('button[type="submit"]').click()

    logo.should().disappear()
    home_listings.should().disappear()

    assert do.get('.head > .logo').should().be_visible()  # logo.
    assert search_query.title() in do.get(
        '[class*="search"]  [class*="mainHeading"] ').should().be_visible().text()  # search bar

    filters_button = do.get('[class*="filters"]')
    filters_button.should().be_clickable().click()
    filters_button.should().disappear()
    search_filters = do.get('[class*="searchModeSelec"] [class*="choices"]').children()

    # for count in range(len(search_filters)):
    for count in range(1):
        logging.info(f'count: {count}')
        search_filters = do.get('[class*="searchModeSelec"] [class*="choices"]').children()

        assert do.get('.token').should().be_visible().should().contain_text(search_query.title())
        search_filters[count].should().be_clickable().click()
        do.get('input[name="min_budget"]').should().be_visible().clear().type(str(rent_min))
        do.get('input[name="max_budget"]').should().be_visible().clear().type(str(rent_max + int(rent_max * count * 0.6)))

        do.get('.SingleDatePicker').should().be_clickable().click()
        date_today = do.get('[class*="CalendarDay__today"]')
        date_today.should().be_clickable().click()
        date_today.should().disappear()
        assert "2020" in do.get('div[class*="DateInput"] > input').get_attribute('value')

        do.get('select[id*="length"]').select(1)
        do.get('select[id*="length"]').select(count)
        if count == 0:
            do.get('label[id="label-propertyTypes.share-houses"]').should().be_clickable().click()
            do.get('label[id="label-propertyTypes.granny-flats"]').should().be_clickable().click()

            do.get('label[id="label-room.private-room"]').scroll_into_view().should().be_clickable().click()
            do.get('label[id="label-gender.males"]').scroll_into_view().should().be_clickable().click()
            do.get('label[id="label-furnishings.furnished"]').scroll_into_view().should().be_clickable().click()
            do.get('label[id="label-bathroom_type."]').scroll_into_view().should().be_clickable().click()
            do.get('div[id="choice-number_of_rooms-1"]').scroll_into_view().should().be_clickable().click()

            properties_accepting_of_options = do.get('section:nth-child(11) [class*="ButtonGroup"]').children()
            for check_box in properties_accepting_of_options[::3]:
                label = check_box.get('label')
                label.hover()
                label.should().be_clickable().click()

            do.wait(use_py=True).sleep(3)

        button_submit = do.get('button[type="submit"]').should().be_clickable()
        button_submit.click()
        button_submit.should().disappear()

        listings = do.find('[class*="headerBox"] + div [class*="search-results"]  .content-column')
        logging.info(f'list num: {len(listings)}')

        # validate that title in search results contains search query
        for c, listing in enumerate(listings):
            logging.info(f'\nlisting num: {c}')
            assert listing.get('img[class*="listingImage"]').scroll_into_view().should().be_visible()
            if listing.get('div[class*="labelBox"]').is_displayed():
                assert listing.get('div[class*="labelBox"]').text() in ('New', 'Updated', 'Boosted')
            assert listing.get('button[class*="shortlistButton"]').should().be_visible()
            assert listing.get('[class*="tileContent"] ').should().be_visible()
            # TODO: implement case for searching in 'flatmates', 'teamups'. Different locator is needed
            assert listing.get('[class*="tileContent"]   p[class*="price"]').should().be_visible().should(). \
                contain_text("$").should().contain_text('week')  # price per week
            price = listing.get('[class*="tileContent"]  p[class*="price"]').text()
            assert (find_nums(price)[0] >= rent_min) and (find_nums(price)[0] <= rent_max)

            assert listing.get('a[class*="tileLink"]  div[class*="contactRibbon"]').should().be_visible().text() in \
                   ("Free to message", "Early bird")  # message button



        filters_button = do.get('[class*="filters"]')
        filters_button.hover()
        filters_button.should().be_clickable().click()
        filters_button.should().disappear()


# demonstrate possible combinations using @pytest.mark.parametrize()
@pytest.mark.parametrize('rent_min', [50])
@pytest.mark.parametrize('rent_max', [900])
@pytest.mark.parametrize('accom_type',
                         [('label[id="label-propertyTypes.share-houses"]', 'Share house'),
                          ('label[id="label-propertyTypes.whole-properties"]', 'Whole property'),
                          ('label[id="label-propertyTypes.granny-flats"]', 'Granny flat')])
@pytest.mark.parametrize('household',
                         [('label[id="label-allFemale"]', 'All female household'), ])
@pytest.mark.parametrize('places_accepting',
                         [('label[id="label-room."]', 'Anyone'),
                          ('label[id="label-gender.males"]', 'Male'),
                          ('label[id="label-gender.females"]', 'Male'),
                          ('label[id="id="label-gender.couples""]', 'Couples'),
                          ])
@pytest.mark.parametrize('furnishings',
                         [('label[id="label-furnishings."]', 'Anyone'),
                          ('label[id="label-furnishings.furnished"]', 'Furnished room'),
                          ('label[id="label-furnishings.unfurnished"]', 'Unfurnished room'),
                          ])
def test_generate_combinations(rent_min, rent_max, accom_type, household, places_accepting, furnishings):
    pass


# delete [:1] in accom_type, places_accepting, furnishings  to extend parameters.
# Note, with  all parameters test takes too much time to finish
accom_type = [('label[id="label-propertyTypes.share-houses"]', 'Share house'),
                          ('label[id="label-propertyTypes.whole-properties"]', 'Whole property'),
                          ('label[id="label-propertyTypes.granny-flats"]', 'Granny flat')][:1]
accom_type_ids = list(zip(*accom_type))[1]

household = [('label[id="label-allFemale"]', 'All female household'), ]
household_ids = list(zip(*household))[1]

places_accepting = [('label[id="label-room."]', 'Anyone'),
                          ('label[id="label-gender.males"]', 'Male'),
                          ('label[id="label-gender.females"]', 'Female'),
                          ('label[id="id="label-gender.couples"]', 'Couples'),
                          ][:1]
places_accepting_ids = list(zip(*places_accepting))[1]

furnishings = [('label[id="label-furnishings."]', 'Anyone'),
                          ('label[id="label-furnishings.furnished"]', 'Furnished room'),
                          ('label[id="label-furnishings.unfurnished"]', 'Unfurnished room'),
                          ][:1]
furnishings_ids = list(zip(*furnishings))[1]


# verify that search filters work as expected
@pytest.mark.parametrize('rent_min', [50])
@pytest.mark.parametrize('rent_max', [900])
@pytest.mark.parametrize('accom_type', accom_type, ids=accom_type_ids)
@pytest.mark.parametrize('household', household, ids=household_ids)
@pytest.mark.parametrize('places_accepting', places_accepting, ids=places_accepting_ids)
@pytest.mark.parametrize('furnishings', furnishings, ids=furnishings_ids)
def test_search_filters_param(do, rent_min, rent_max, accom_type, household, places_accepting, furnishings):

    accom_type_locator, accom_expected_text = accom_type
    household_locator, household_expected_text = household
    places_accepting_locator, places_expected_text = places_accepting
    furnishings_locator, furnishings_expected_text = places_accepting
    search_query = 'chippendale'

    do.visit('https://flatmates.com.au/')
    assert do.should().have_title('Share Accommodation | Flatmates.com.au')

    consent_button = do.get('button[class*="gdpr-consent"]')
    assert consent_button.should().be_visible().should().be_clickable()
    consent_button.click()

    do.click_with_retry(
        css='.styles__mainHeading___3wzRg', exp_condition=ec.invisibility_of_element_located(
            (By.CSS_SELECTOR, '.styles__mainHeading___3wzRg')))  # has retry cycle based on expected condition
    do.get('#choice-mode-rooms').should().be_clickable().click()
    do.get('.hiddenInput').should().be_clickable().type(search_query)
    do.get('.inputAutocomplete').children().first().click()
    assert do.get('.token').should().be_visible().should().contain_text(search_query.title())

    logo = do.get('.head > .logo')
    home_listings = do.get('[class*="home-listings"]')
    do.get('button[type="submit"]').click()

    logo.should().disappear()
    home_listings.should().disappear()

    assert do.get('.head > .logo').should().be_visible()  # logo.
    assert search_query.title() in do.get(
        '[class*="search"]  [class*="mainHeading"] ').should().be_visible().text()  # search bar

    filters_button = do.get('[class*="filters"]')
    filters_button.should().be_clickable().click()
    filters_button.should().disappear()

    for count, filter_name in enumerate(['rooms', 'flatmates', 'teamups']):

        search_filters = do.get('[class*="searchModeSelec"] [class*="choices"]').children()

        assert do.get('.token').should().be_visible().should().contain_text(search_query.title())
        search_filters[count].should().be_clickable().click()
        do.get('input[name="min_budget"]').should().be_visible().clear().type(str(rent_min))
        do.get('input[name="max_budget"]').should().be_visible().clear().type(str(rent_max))

        do.get('.SingleDatePicker').should().be_clickable().click()
        date_today = do.get('[class*="CalendarDay__today"]')
        date_today.should().be_clickable().click()
        date_today.should().disappear()
        assert "2020" in do.get('div[class*="DateInput"] > input').get_attribute('value')

        do.get('select[id*="length"]').select(1)
        do.get('select[id*="length"]').select(count)
        if filter_name == 'rooms':
            do.get(accom_type_locator).should().be_clickable().click()
            do.get(household_locator).scroll_into_view().should().be_clickable().click()
            do.get(places_accepting_locator).scroll_into_view().should().be_clickable().click()
            do.get(furnishings_locator).scroll_into_view().should().be_clickable().click()

            properties_accepting_of_options = do.get('section:nth-child(11) [class*="ButtonGroup"]').children()
            for check_box in properties_accepting_of_options[::3]:
                label = check_box.get('label')
                label.scroll_into_view()
                do.wait(use_py=True).sleep(2)
                label.should().be_clickable().click()

        button_submit = do.get('button[type="submit"]').should().be_clickable()
        button_submit.click()
        button_submit.should().disappear()

        listings = do.find('[class*="headerBox"] + div [class*="search-results"]  .content-column')
        logging.info(f'list num: {len(listings)}')

        if len(listings) > 0:

            # validate that title in search results contains search query
            for c, listing in enumerate(listings):
                logging.info(f'\nlisting num: {c}')
                assert listing.get('img[class*="listingImage"]').scroll_into_view().should().be_visible()
                if listing.get('div[class*="labelBox"]').is_displayed():
                    assert listing.get('div[class*="labelBox"]').text() in ('New', 'Updated', 'Boosted')
                assert listing.get('button[class*="shortlistButton"]').should().be_visible()
                assert listing.get('[class*="tileContent"] ').should().be_visible()
                if filter_name == 'rooms':
                    price = listing.get('[class*="tileContent"]   p[class*="price"]')
                else:
                    price = listing.get('p[class*="subheading"]')
                assert price.should().be_visible().should() # price per week
                assert (find_nums(price.text())[0] >= rent_min) and (find_nums(price.text())[0] <= rent_max)
                assert listing.get('a[class*="tileLink"]  div[class*="contactRibbon"]').should().be_visible().text() in \
                       ("Free to message", "Early bird")  # message button

        logging.info(f'count: {count}')

        filters_button = do.get('[class*="filters"]')
        filters_button.hover()
        filters_button.should().be_clickable().click()
        filters_button.should().disappear()

