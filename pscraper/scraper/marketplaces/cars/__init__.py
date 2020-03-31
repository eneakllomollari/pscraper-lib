from pscraper.utils.misc import measure_time
from .consts import ALLOWED_RD, CARS_COM_QUERY, PAGE, SEARCH, TOTAL_NUM_PAGES
from .helpers import get_cars_com_response, validate_params
from ..consts import LISTING_ID, PHONE_NUMBER, SELLER, STATE, VEHICLE, VIN
from ..helpers import update_vehicle


@measure_time
def scrape_cars(zip_code, search_radius, target_states, api):
    """ Scrape EV data from cars.com filtering with the specified parameters

    Args:
        zip_code (str): The zip code to perform the search in
        search_radius (int): The search radius for the specified zip code
        target_states (list): The states to search in (i.e. ```['CA', 'NV']```)
        api (pscraper.api.API): Pscraper API to communicate with the backend

    Returns:
        total (int): Total number of cars scraped
    """
    validate_params(search_radius, target_states)
    total = 0
    url = CARS_COM_QUERY.format('{}', search_radius, zip_code)
    num_pages = get_cars_com_response(url.format(1))[PAGE][SEARCH][TOTAL_NUM_PAGES]
    for i in range(num_pages):
        vehicles = get_cars_com_response(url.format(i))[PAGE][VEHICLE]
        for vehicle in vehicles:
            is_eligible_vehicle = all((vehicle[VIN], vehicle[LISTING_ID], vehicle[SELLER][PHONE_NUMBER]))
            is_target_state = vehicle[SELLER][STATE] in target_states or target_states == 'ALL'
            if is_eligible_vehicle and is_target_state:
                update_vehicle(vehicle, api)
                total += 1
    return total
