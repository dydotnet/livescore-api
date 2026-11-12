import logging
from threading import Lock

from fastapi import APIRouter, HTTPException, Query

from app.services.models.country_schemas import CountryListResponse, LeagueListResponse
from app.services.scraper.country_scraper import CountryScraper


ROUTER_NAME = "countries"
country_scrape_lock = Lock()
router = APIRouter()


@router.get("/", response_model=CountryListResponse)
def get_countries(
    name: str | None = Query(None, description="The name of the country to search for"),
) -> CountryListResponse:
    try:
        with country_scrape_lock:
            country_scraper = CountryScraper()
            try:
                countries = country_scraper.scrape_countries(name)
            finally:
                country_scraper.driver.quit()

        return CountryListResponse(countries=countries)
    except Exception as e:
        logging.exception("Error occurred while scraping countries")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/{countryId}/leagues", response_model=LeagueListResponse)
def get_leagues_by_country(countryId: str) -> LeagueListResponse:
    try:
        with country_scrape_lock:
            country_scraper = CountryScraper()
            try:
                leagues = country_scraper.scrape_leagues_by_country(countryId)
            finally:
                country_scraper.driver.quit()

        return LeagueListResponse(leagues=leagues)
    except Exception as e:
        logging.exception("Error occurred while scraping leagues for %s", countryId)
        raise HTTPException(status_code=500, detail=str(e)) from e
