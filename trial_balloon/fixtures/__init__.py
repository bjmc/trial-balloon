from itertools import chain

from trial_balloon.fixtures import no_ballots

FIXTURES = chain(
    no_ballots.FIXTURES,
    # search_results.FIXTURES,
)

FIXTURES_BY_NAME = {f.name: f.fixture for f in FIXTURES}
