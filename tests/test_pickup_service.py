"""
Test module for the Fedex Pickup Service WSDL.
"""

import unittest
import logging
import sys
import datetime

sys.path.insert(0, '..')
from fedex.services.pickup_service import FedexCreatePickupRequest

# Common global config object for testing.
from tests.common import get_fedex_config

CONFIG_OBJ = get_fedex_config()

logging.getLogger('suds').setLevel(logging.ERROR)
logging.getLogger('fedex').setLevel(logging.INFO)


@unittest.skipIf(not CONFIG_OBJ.account_number, "No credentials provided.")
class FedexCreatePickupRequestTests(unittest.TestCase):
    """
    These tests verify that the pikckup service WSDL is in good shape.
    """

    def setUp(self):
        self.config_obj = get_fedex_config()

    def tearDown(self):
        pass

    def test_pickup_request(self):
        pickup_service = FedexCreatePickupRequest(self.config_obj)

        pickup_service.OriginDetail.PickupLocation.Contact.PersonName = 'Sender Name'
        pickup_service.OriginDetail.PickupLocation.Contact.EMailAddress = 'test@user.com'
        pickup_service.OriginDetail.PickupLocation.Contact.CompanyName = 'Acme Inc.'
        pickup_service.OriginDetail.PickupLocation.Contact.PhoneNumber = '9012638716'
        pickup_service.OriginDetail.PickupLocation.Address.StateOrProvinceCode = 'SC'
        pickup_service.OriginDetail.PickupLocation.Address.PostalCode = '29631'
        pickup_service.OriginDetail.PickupLocation.Address.CountryCode = 'US'
        pickup_service.OriginDetail.PickupLocation.Address.StreetLines = ['155 Old Greenville Hwy', 'Suite 103']
        pickup_service.OriginDetail.PickupLocation.Address.City = 'Clemson'
        # pickup_service.OriginDetail.PickupLocation.Address.UrbanizationCode = ''  # For Puerto Rico only
        pickup_service.OriginDetail.PickupLocation.Address.Residential = False

        # FRONT, NONE, REAR, SIDE
        # pickup_service.OriginDetail.PackageLocation = 'NONE'

        # APARTMENT, BUILDING, DEPARTMENT, FLOOR, ROOM, SUITE
        # pickup_service.OriginDetail.BuildingPart = 'SUITE'

        # Identifies the date and time the package will be ready for pickup by FedEx.
        pickup_service.OriginDetail.ReadyTimestamp = datetime.datetime.now().replace(microsecond=0).isoformat()

        # Identifies the latest time at which the driver can gain access to pick up the package(s)
        pickup_service.OriginDetail.CompanyCloseTime = '23:00:00'

        pickup_service.CarrierCode = 'FDXE'

        pickup_service.TotalWeight.Units = 'LB'
        pickup_service.TotalWeight.Value = '1'
        pickup_service.PackageCount = '1'
        # pickup_service.OversizePackageCount = '1'

        # pickup_service.CommodityDescription = ''

        # DOMESTIC or INTERNATIONAL
        # pickup_service.CountryRelationship = 'DOMESTIC'

        # See PickupServiceCategoryType
        # pickup_service.PickupServiceCategory = 'FEDEX_DISTANCE_DEFERRED'

        pickup_service.send_request()

        assert pickup_service.response.HighestSeverity == 'SUCCESS', pickup_service.response.Notifications[0].Message


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()
