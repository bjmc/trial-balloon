from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from geojson_pydantic import Feature, Point
from pydantic import BaseModel, EmailStr, Extra, Field, HttpUrl


class Address(BaseModel):
    address: str
    postcode: str
    slug: str
    url: str = Field(..., description='Call this URL to get data for this registered address')


class StationProperties(BaseModel):
    postcode: str = Field(..., description='Postcode for this polling station')
    address: str = Field(..., description='Address for this polling station')


class Station(Feature):
    id: str
    geometry: Optional[Point] = Field(
        None,
        description=(
            'A GeoJSON [Point'
            ' object](https://tools.ietf.org/html/rfc7946#section-3.1.2) object'
            ' describing the location of this polling station. Optionally null if we'
            " know the address only but can't geocode a location."
        ),
    )
    properties: StationProperties


class PollingStation(BaseModel):
    polling_station_known: bool = Field(..., description='Do we know where this user should vote?')
    custom_finder: Optional[str] = Field(
        ...,
        description=(
            "If we don't know a user's polling station, sometimes we can provide the"
            ' URL of another polling station finder. This will always be populated for'
            ' users in Northern Ireland where Electoral Office for Northern Ireland run'
            ' their own service.'
        ),
    )
    report_problem_url: Optional[str] = Field(
        ...,
        description=(
            'If we provide a polling station result, this URL may be used to provide a'
            ' user with a back-channel to report inaccurate data.'
        ),
    )
    station: Optional[Station] = Field(
        None,
        description=(
            'A [GeoJSON Feature](https://tools.ietf.org/html/rfc7946#section-3.2)'
            " describing the user's polling station (if known)"
        ),
    )


class AdvanceVotingStation(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str = Field(..., description='The name of the Advance Voting Station')
    address: str = Field(..., description='The address of the Advance Voting Station')
    postcode: str = Field(..., description='The postcode of the Advance Voting Station')
    location: Point = Field(
        ...,
        description=(
            'A GeoJSON [Point'
            ' object](https://tools.ietf.org/html/rfc7946#section-3.1.2) object'
            ' describing the location of this Advance Voting Station.'
        ),
    )
    opening_times: List[List]


class Type(Enum):
    cancelled_election = 'cancelled_election'
    voter_id = 'voter_id'


class Notification(BaseModel):
    title: str
    type: Type = Field(..., description='Type of notification')
    detail: str
    url: str


class VotingSystem(BaseModel):
    slug: str = Field(..., description='One of `AMS`, `FPTP`, `PR-CL`, `sv`, `STV`')
    name: str = Field(
        ..., description='The name of this voting system (e.g: "First-past-the-post")'
    )
    uses_party_lists: bool = Field(
        False, description='True if this voting system uses party lists'
    )


class Husting(BaseModel):
    title: str = Field(..., description='Title of the event')
    location: str = Field(..., description='Address of the event')
    url: Optional[str] = Field(None, description='URL to the event or event sign up page')
    starts: Optional[datetime] = Field(None, description='Start datetime')
    ends: Optional[datetime] = Field(None, description='End datetime')
    postevent_url: str = Field(
        None, description='Any post-event URL, e.g a YouTube recording of the event'
    )


class Party(BaseModel):
    party_id: str
    party_name: str


class PreviousPartyAffiliation(BaseModel):
    party_id: str
    party_name: str


class Leaflet(BaseModel):
    leaflet_id: float = Field(..., description='The electionleaflets.org ID for this leaflet')
    thumb_url: str = Field(..., description='URL to the thumbnail image of this leaflet')
    leaflet_url: str = Field(..., description='URL to the leaflet page on electionleaflets.org')


class Person(BaseModel):
    ynr_id: float
    name: str
    absolute_url: str = Field(
        None,
        description='Link for more (human-readable) information about this candidate',
    )
    email: Optional[str] = Field(
        None, description='Email address for this candidate, if we hold it'
    )
    photo_url: Optional[str] = Field(
        None, description='URL for a photo of this candidate, if we hold one'
    )
    leaflets: List[Leaflet] = Field(
        [],
        description=('Leaflets uploaded to electionleaflets.org and tagged with this person'),
    )


class Candidate(BaseModel):
    list_position: Optional[int] = Field(
        None,
        description=(
            'Numeric position in party list. This value is only relevant to elections'
            ' using party lists. It will always be null in First-Past-The-post'
            ' elections.'
        ),
    )
    party: Party
    previous_party_affiliations: List[PreviousPartyAffiliation]
    person: Person


class Ballot(BaseModel):
    ballot_paper_id: str = Field(..., description='Identifier for this ballot')
    ballot_title: Optional[str] = Field(None, description='Friendly name for this ballot')
    ballot_url: str = Field(
        ...,
        description=(
            'API link for more detailed info about this ballot from the /elections' ' endpoint'
        ),
    )
    poll_open_date: date = Field(None, description='Polling day for this ballot  (ISO 8601)')
    elected_role: str = Field(
        ..., description='Name of the role the winner(s) of this election will assume'
    )
    metadata: Dict[str, Any] = Field(
        {},
        description=(
            'Object containing information about special conditions for the user to be'
            ' aware about (e.g: cancelled elections, voter id pilot). (details TBC)'
        ),
    )
    cancelled: bool = Field(None, description='True if this ballot has been cancelled')
    replaced_by: Optional[str] = Field(
        None,
        description=(
            'If a ballot has been cancelled (cancelled = true) and rescheduled for a'
            ' later date, this key will hold the ballot_paper_id of the ballot that'
            ' replaces it.'
        ),
    )
    replaces: Optional[str] = Field(
        None,
        description=(
            'If this ballot replaces another cancelled ballot, this key will hold the'
            ' ballot_paper_id of the ballot that it replaces.'
        ),
    )
    election_id: str = Field(..., description="Identifier for this ballot's parent election group")
    election_name: str = Field(
        None, description="Friendly name for this ballot's parent election group"
    )
    post_name: str = Field(
        None,
        description=('Name of the division or post the winner(s) of this election will represent'),
    )
    candidates_verified: bool = Field(
        None,
        description=(
            'True if the list of candidates for this election has been confirmed'
            ' against the nomination papers for this ballot. If this property is False,'
            ' the candidate list is provisional or unconfirmed.'
        ),
    )
    voting_system: VotingSystem = Field(
        None, description='The voting system used in this election'
    )
    hustings: List[Husting] = Field(None, description='Hustings related to this election')
    seats_contested: float
    candidates: List[Candidate] = Field(
        None,
        description=(
            'Array of candidate objects describing candidates that will appear on this'
            ' ballot paper. In an election which uses party lists, the `candidates`'
            ' array is sorted by party and `list_position` within parties. For other'
            ' election types it is sorted alphabetically by candidate name.'
        ),
    )
    wcivf_url: str = Field(
        None, description='Link for more (human-readable) information about this ballot'
    )


class Date(BaseModel):
    date: str = Field(None, description='Polling day on which an election will occur')
    polling_station: PollingStation = Field(None, description='Results for polling station search')
    advance_voting_station: AdvanceVotingStation = Field(
        None, description='Advance Voting Stations'
    )
    notifications: List[Notification] = Field(
        None,
        description=(
            'Array of notifications to be shown to the user about special conditions to'
            ' be aware of on this date.'
        ),
    )
    ballots: List[Ballot] = Field(
        None,
        description=(
            'List of ballots happening on this date. It is possible for more than one'
            ' ballot to occur on the same date. For example, a user may vote in a local'
            ' council election and mayoral election on the same day.'
        ),
    )


class ElectoralServices(BaseModel):
    council_id: str = Field(..., description='GSS code for this council')
    name: str = Field(..., description='Name of this council')
    nation: str = Field(..., description='Name of nation')
    address: str = Field(..., description='Contact address for this council')
    postcode: str = Field(
        ..., description='Postcode component of contact address for this council'
    )
    email: EmailStr = Field(
        ...,
        description="Contact email address for this council's Electoral Services team",
    )
    phone: str = Field(
        ..., description="Telephone number for this council's Electoral Services team"
    )
    website: HttpUrl = Field(..., description="URL for this council's website")


class Registration(BaseModel):
    address: str = Field(..., description='Contact address for this council')
    postcode: str = Field(
        ..., description='Postcode component of contact address for this council'
    )
    email: EmailStr = Field(
        ...,
        description="Contact email address for this council's Electoral Services team",
    )
    phone: str = Field(
        ..., description="Telephone number for this council's Electoral Services team"
    )
    website: HttpUrl = Field(..., description="URL for this council's website")


PostcodeLocation = Feature[Point, Dict]


class RootModel(BaseModel):
    address_picker: bool = Field(
        False, description='True if we need to show this user an address picker'
    )
    addresses: List[Address] = Field(
        ...,
        description=(
            'An array of address objects containing the addresses applicable to this'
            ' request (if necessary)'
        ),
    )
    dates: List[Date] = Field(
        [],
        description=(
            'An array of date objects (each describing a date on which an election or'
            ' poll will take place) containing details of relevant ballots, candidates'
            ' and polling station information'
        ),
    )
    electoral_services: Optional[ElectoralServices] = Field(
        None,
        description=(
            "Contact details for the user's local Electoral Services team. If we do not"
            " know the user's polling station, this can be used to provide contact info"
            ' for their local council. This may be `null` if we are not able to'
            " determine the user's council."
        ),
    )
    registration: Optional[Registration] = Field(
        None,
        description=(
            'Sometimes the contact information for registration and proxy voting is'
            ' different to the electoral services contact details. Use these if they'
            ' exist and your users might have questions about voter registration. If'
            ' this key is null, assume the electoral services contact details can be'
            ' used for electoral registration related enquiries.'
        ),
    )
    postcode_location: Optional[PostcodeLocation] = Field(
        None,
        description=(
            'A [GeoJSON Feature](https://tools.ietf.org/html/rfc7946#section-3.2)'
            ' containing a [Point'
            ' object](https://tools.ietf.org/html/rfc7946#section-3.1.2) describing the'
            ' centroid of the input postcode. If providing a map or directions for a'
            ' polling station journey, use this as the start point. This may be `null`'
            ' if we are not able to accurately geocode.'
        ),
    )
