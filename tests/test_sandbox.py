from pathlib import Path

import pytest
import responses
from responses import matchers

from main import DCVotingInformationAPIClient

NO_RESULTS_POSTCODE = "AA11AA"
ONE_ELECTION_POSTCODE = "AA12AA"
ADDRESS_PICKER_POSTCODE = "AA13AA"


@pytest.fixture
def api_base_url():
    return "https://developers.democracyclub.org.uk/api/v1"


def load_from_sandbox(filename):
    path = Path() / "sandbox_responses" / f"{filename}.json"
    return path.open().read()


@responses.activate
def test_no_upcoming_elections(api_base_url):
    client = DCVotingInformationAPIClient("test")

    responses.get(
        url=f"{api_base_url}/postcode/{NO_RESULTS_POSTCODE}/",
        body=load_from_sandbox(NO_RESULTS_POSTCODE),
        match=[matchers.query_param_matcher(client.default_params)],
    )

    resp = client.get_postcode(NO_RESULTS_POSTCODE)
    assert resp["address_picker"] == False
    assert resp["dates"] == []
    assert resp["electoral_services"]["council_id"] == "E09000033"


@responses.activate
def test_one_upcoming_elections(api_base_url):
    client = DCVotingInformationAPIClient("test")

    responses.get(
        url=f"{api_base_url}/postcode/{ONE_ELECTION_POSTCODE}/",
        body=load_from_sandbox(ONE_ELECTION_POSTCODE),
        match=[matchers.query_param_matcher(client.default_params)],
    )

    resp = client.get_postcode(ONE_ELECTION_POSTCODE)
    assert resp["address_picker"] == False
    assert len(resp["dates"]) == 1
    date = resp["dates"][0]
    assert date["polling_station"]["polling_station_known"] == True
    assert date["advance_voting_station"]["name"] == "Exeter Guildhall"

    ballot = date["ballots"][0]
    assert ballot["candidates_verified"] == True
    assert len(ballot["candidates"]) == 4


@responses.activate
def test_address_picker(api_base_url):
    client = DCVotingInformationAPIClient("test")

    responses.get(
        url=f"{api_base_url}/postcode/{ADDRESS_PICKER_POSTCODE}/",
        body=load_from_sandbox(ADDRESS_PICKER_POSTCODE),
        match=[matchers.query_param_matcher(client.default_params)],
    )

    resp = client.get_postcode(ADDRESS_PICKER_POSTCODE)
    assert resp["address_picker"] == True
    assert len(resp["addresses"]) == 3
