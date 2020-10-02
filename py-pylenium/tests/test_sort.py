
import pytest
import logging
from collections import Counter
import re
from math import ceil

# parametrize test using dict and lambda
@pytest.mark.parametrize('sorting', ['newest', 'low_hi', 'hi_low', 'earliest available'])
def test_sorting(sorting):
    if sorting in ('low_hi', 'hi_low'):
        lst = [1, 2, 3, 4]
    elif sorting == 'newest':
        lst = [1, 1, 3, 4]
    elif sorting == 'earliest available':
        lst = [1, 1, 2, 4]
    is_sorted = {'newest': lambda: all(k in ('Boosted', 'Updated', 'New') for k in lst),
                 'low_hi': lambda: all(k >= m for k, m in zip(lst[1:], lst)),
                 'hi_low': lambda: all(k <= m for k, m in zip(lst[1:], lst)),
                 'earliest_available': lambda: any(k == "Available Now" and m != "Available Now"
                                                   for k, m in zip(lst[1:], lst))
                 }[sorting]()
    logging.info(f" arg: {sorting},  result: {is_sorted}")


# test sorting
@pytest.mark.parametrize('key', [lambda x, y: x >= y,
                                 lambda x, y: x <= y],
                         ids=['low_hi', 'hi_low'])
def test_sorting(key):
    lst = [1, 2, 3, 4]
    out = all(key(k, m) for k, m in zip(lst[1:], lst))
    logging.info(f"\n  result: {out}")


def test_counter():
    c = ['New', 'Updated', 'Updated', 'New', 'Updated', 'Updated', 'Boosted', 'Updated', 'Updated', 'Updated', 'Updated', 'New']

    logging.info(f" counter: {Counter(c)}")
    logging.info(f" c['Updated'] > c['New']: {Counter(c)['Updated'] > Counter(c)['New']}")


# regex extract number from string
def test_function():
    t1 = '$115-215 / week'
    t2 = '$115 / week'
    t3 = 'Viewing 37-48 of 78 results'
    logging.info(f" t1: {t1.split()[0].split('-')[0][1:]}")
    logging.info(f" t2: {t2.split()[0].split('-')[0][1:]}")
    logging.info(re.findall(r'[0-9]+', t1)[0])
    logging.info(re.findall(r'[0-9]+', t3)[-1])
    results = int(re.findall(r'[0-9]+', t3)[-1])
    logging.info(f" ceil: {ceil(results / 12)}")
    pass


# summary comment
def test_function_1():
    for page_link_num in range(1, min(7, 8)):
        logging.info(f" some text: {page_link_num}")
    pass


def find_all_nums(_str: str, _int=True):
    value = re.findall(r'[0-9]+', _str)
    if value and _int is True:
        value = [int(e) for e in value]
    return value


accom_type = [('label[id="label-propertyTypes.share-houses"]', 'Share house'),
                          ('label[id="label-propertyTypes.whole-properties"]', 'Whole property'),
                          ('label[id="label-propertyTypes.granny-flats"]', 'Granny flat')]
accom_type_ids = list(zip(*accom_type))[1]

places_accepting = [('label[id="label-room."]', 'Anyone'),
                          ('label[id="label-gender.males"]', 'Male'),
                          ('label[id="label-gender.females"]', 'Female'),
                          ('label[id="id="label-gender.couples""]', 'Couples'),
                          ]
places_accepting_ids = list(zip(*places_accepting))[1]

furnishings = [('label[id="label-furnishings."]', 'Anyone'),
                          ('label[id="label-furnishings.furnished"]', 'Furnished room'),
                          ('label[id="label-furnishings.unfurnished"]', 'Unfurnished room'),
                          ]
furnishings_ids = list(zip(*furnishings))[1]

@pytest.mark.parametrize('rent_min', [50])
@pytest.mark.parametrize('rent_max', [900])
@pytest.mark.parametrize('accom_type', accom_type, ids=accom_type_ids)
@pytest.mark.parametrize('household',
                         [('label[id="label-allFemale"]', 'All female household'), ], ids=['All female household'])
@pytest.mark.parametrize('places_accepting', places_accepting, ids=places_accepting_ids)
@pytest.mark.parametrize('furnishings', furnishings, ids=furnishings_ids)
def test_search_filters_param(rent_min, rent_max, accom_type, household, places_accepting, furnishings):
    pass


def a(data_):
    print(f'\naction: a, data: {data_}')


def b(data_):
    print(f'\naction: b, data: {data_}')


def c(data_):
    print(f'\naction: c, data: {data_}')


@pytest.mark.parametrize('action, data_', [
    (a, 1),
    (b, 2),
    (c, 3),
])
def test_param_with_functions(action, data_):
    action(data_)
