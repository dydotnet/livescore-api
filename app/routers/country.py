import logging
from threading import Lock
from fastapi import APIRouter, HTTPException, Query
from app.services.models.country_schemas import CountryListResponse, Country, LeagueListResponse
from app.services.scraper.country_scraper import CountryScraper

ROUTER_NAME = 'countries'
country_scrape_lock = Lock()
router = APIRouter()

@router.get("/", response_model=CountryListResponse)
def get_countries(name: str = Query(None, description="The name of the country to search for")) -> CountryListResponse:
    """
    Retrieves a list of available countries.

    Args:
        name (str, optional): The name of the country to search for. Defaults to None.

    Returns:
        CountryListResponse: A list of countries matching the search criteria.
    """
    try:
        logging.info(f"GET /{ROUTER_NAME} - Starting country scraping process.")
        country_scraper
        logging.info(f"GET /{ROUTER_NAME} call successful - Scraped {len(countries)} countries.")
        return CountryListResponse(countries=countries)
    except Exception as e:
        logging.error(f"Error occurred while scraping countries: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{countryId}/leagues", response_model=LeagueListResponse)
def get_leagues_by_country(countryId: str) -> LeagueListResponse:
    """
    Retrieves all leagues for a specific country.

    Args:
        countryId (str): The unique identifier of the country to scrape leagues from.

    Returns:
        LeagueListResponse: A list of leagues for the specified country.
    """
    try:
        logging.info(f"GET /{ROUTER_NAME}/{countryId}/leagues - Starting country's leagues scraping process.")
              with country_scrape_lock:
            country_scraper = CountryScraper()
            try:
                leagues = country_scraper.scrape_leagues_by_country(countryId)
            finally:
                country_scraper.driver.quit()
        logging.info(f"GET /{ROUTER_NAME}/{countryId}/leagues call successful - Scraped {len(leagues)} leagues for country {countryId}.")
        return LeagueListResponse(leagues=leagues)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
