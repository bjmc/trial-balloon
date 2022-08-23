import pytest
import responses
from responses import matchers

from tests.client.main import DCVotingInformationAPIClient  # type: ignore
from trial_balloon.fixtures import FIXTURES_BY_NAME


@pytest.fixture
def api_base_url():
    return 'https://developers.democracyclub.org.uk/api/v1'


@responses.activate
def test_no_upcoming_elections(api_base_url):
    postcode = 'AA11AA'
    client = DCVotingInformationAPIClient('test')

    responses.get(
        url=f'{api_base_url}/postcode/{postcode}/',
        body=FIXTURES_BY_NAME['westminster'].json(),
        match=[matchers.query_param_matcher(client.default_params)],
    )

    resp = client.get_postcode(postcode)
    assert resp['address_picker'] is False
    assert resp['dates'] == []
    assert resp['electoral_services']['council_id'] == 'E09000033'
