"""
This script scrapes the Sundhed.dk website to find dentists in a specific municipality.
"""

import json
import requests


def get_srvname_cookie(session, municipality_id, category):
    """
    Sends an initial request to the Sundhed.dk website to obtain the necessary cookies.

    Args:
        session (requests.Session): The session object to handle cookies.
        municipality_id (str): The ID of the municipality.
        category (str): The category of information to search for.

    Returns:
        str: The referer URL for subsequent requests.
    """
    html_url = 'https://www.sundhed.dk/borger/guides/find-behandler/'
    html_params = {
        'MunicipalityId': municipality_id,
        'Informationskategori': category
    }
    resp = session.get(html_url, params=html_params, timeout=10)
    resp.raise_for_status()

    return resp.url


def fetch_additional_search_data(session, referer):
    """
    Calls the JSON searchadditionalfilters endpoint to retrieve any additional headers, tokens,
    or metadata required for subsequent API calls. This function ensures that the necessary
    context or authentication details are in place before performing the main search.

    Args:
        session (requests.Session): The session object to handle cookies.
        referer (str): The referer URL from the initial request.

    Returns:
        None
    """
    filters_url = 'https://www.sundhed.dk/api/search/searchadditionalfilters'
    resp = session.get(
        filters_url,
        headers={
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': referer,
            'Origin': 'https://www.sundhed.dk'
        },
        timeout=10
    )
    resp.raise_for_status()


def search_dentists(session, municipality_id, category):
    """
    Queries the search endpoint with specific parameters to fetch dentist data.

    Args:
        session (requests.Session): The session object to handle cookies.
        municipality_id (str): The ID of the municipality.
        category (str): The category of information to search for.

    Returns:
        dict: A dictionary containing the JSON response from the search endpoint.
    """
    search_url = 'https://www.sundhed.dk/app/findbehandlerv2/api/v1/findbehandlerv2/search'
    search_params = {
        'Page':                    '1',
        'Pagesize':                '100',
        'RegionId':                '0',
        'MunicipalityId':          municipality_id,
        'Sex':                     '0',
        'AgeGroup':                '0',
        'Informationskategori':    category,
        'InformationsUnderkategori':'',
        'DisabilityFriendlyAccess':'false',
        'GodAdgang':               'false',
        'EMailConsultation':       'false',
        'EMailAppointmentReservation':'false',
        'EMailPrescriptionRenewal':'false',
        'TakesNewPatients':        'false',
        'TreatmentAtHome':         'false',
        'WaitTime':                'false',
        'Name':                    '',
        'Latitude':                'null',
        'Longitude':               'null',
        'Address':                 'null'
    }
    resp = session.get(
        search_url,
        params=search_params,
        headers={
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest'
        },
        timeout=10
    )
    resp.raise_for_status()
    return resp.json()


def get_dentists(municipality_id: str, category: str) -> dict:
    """
    Scrapes the Sundhed.dk website to retrieve a list of dentists in a specific municipality.

    Args:
        municipality_id (str): The ID of the municipality to search for dentists.
        category (str): The category of healthcare providers to search for (e.g., 'Tandlæge').

    Returns:
        dict: A dictionary containing the JSON response from the search endpoint.
    """
    session = requests.Session()

    referer = get_srvname_cookie(session, municipality_id, category)
    fetch_additional_search_data(session, referer)
    data = search_dentists(session, municipality_id, category)
    return data


if __name__ == '__main__':
    result = get_dentists(
        municipality_id='751',
        category='Tandlæge'
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
