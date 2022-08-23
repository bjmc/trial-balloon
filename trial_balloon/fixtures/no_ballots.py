from trial_balloon.data_template import DataTemplate, NamedFixture
from trial_balloon.models.postcode_search import (
    ElectoralServices,
    Point,
    PostcodeLocation,
    Registration,
    RootModel,
)

westminster_electoral_services = ElectoralServices(
    council_id='E09000033',
    name='City of Westminster',
    nation='England',
    address=(
        'Electoral Registration Officer\n'
        'Westminster City Council\n'
        '2nd Floor, City Hall\n'
        '5 Strand'
    ),
    postcode='WC2N 5HR',
    email='electoralservices@westminster.gov.uk',
    phone='020 7641 2730',
    website='http://www.westminster.gov.uk/',
)
westminister_registration = Registration(
    address=(
        'Electoral Registration Officer\n'
        'Westminster City Council\n'
        '2nd Floor, City Hall\n'
        '5 Strand'
    ),
    postcode='WC2N 5HR',
    email='electoralservices@westminster.gov.uk',
    phone='020 7641 2730',
    website='http://www.westminster.gov.uk/',
)
westminster_loc = PostcodeLocation(geometry=Point(coordinates=[-0.13447605, 51.489488200000004]))


cardiff_electoral_services = ElectoralServices(
    council_id='W06000015',
    name='Cardiff Council',
    nation='Wales',
    address=(
        'Electoral Registration Officer\n' 'City of Cardiff Council\n' 'County Hall Atlantic Wharf'
    ),
    postcode='CF10 4UW',
    email='electoralservices@cardiff.gov.uk',
    phone='029 2087 2034',
    website='http://www.cardiff.gov.uk/',
)
# Showing off here, but the point is these fixtures can be as repetitive as they need to be,
# or we can use all the features of Python & Pydantic to "DRY" up whatever we want:
cardiff_registration = Registration.parse_obj(cardiff_electoral_services.dict())
cardiff_loc = PostcodeLocation(geometry={'type': 'Point', 'coordinates': [-3.113797, 51.521175]})
cardiff = {
    'electoral_services': cardiff_electoral_services,
    'registration': cardiff_registration,
    'postcode_location': cardiff_loc,
}


no_ballot_template = DataTemplate(
    RootModel(
        address_picker=False,
        addresses=[],
        dates=[],
        electoral_services=westminster_electoral_services,
        registration=westminister_registration,
        postcode_location=westminster_loc,
    ),
)

FIXTURES = [
    NamedFixture('westminster', no_ballot_template.default),
    NamedFixture('cardiff', no_ballot_template.record(**cardiff)),
    NamedFixture(
        'mismatched_postcode_location', no_ballot_template.record(postcode_location=cardiff_loc)
    ),
    NamedFixture('address_picker_glitch', no_ballot_template.record(address_picker=True)),
]
