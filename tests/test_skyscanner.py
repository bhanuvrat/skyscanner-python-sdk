#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_skyscanner
----------------------------------

Tests for `skyscanner` module.
"""

import unittest
from datetime import datetime, timedelta

from skyscanner.skyscanner import Flights, Transport, FlightsCache, CarHire, Hotels


class SkyScannerTestCase(unittest.TestCase):
    """Generic TestCase class to support default failure messages."""

    def setUp(self):
        self.result = None

    def tearDown(self):
        self.result = None

    def assertTrue(self, expr, msg=None):
        default_message = ('API Response: %s' % self.result) if self.result else None
        super(SkyScannerTestCase, self).assertTrue(expr, msg=msg or default_message)


class TestCarHire(SkyScannerTestCase):

    def setUp(self):
        # API Key that's meant for testing only
        # Taken from: http://business.skyscanner.net/portal/en-GB/Documentation/FlightsLivePricingQuickStart
        super(TestCarHire, self).setUp()
        self.api_key = 'prtl6749387986743898559646983194'
        datetime_format = '%Y-%m-%dT%H:%S'
        pickup_datetime = datetime.now()
        dropoff_datetime = pickup_datetime + timedelta(days=3)
        self.pickup = pickup_datetime.strftime(datetime_format)
        self.dropoff = dropoff_datetime.strftime(datetime_format)

    def test_location_autosuggest(self):
        carhire_service = CarHire(self.api_key)

        self.result = carhire_service.location_autosuggest(
            market='UK',
            currency='GBP',
            locale='en-GB',
            query='Kuala')

        self.assertTrue('results' in self.result)
        self.assertTrue(len(self.result['results']) > 0)

    def test_get_result(self):
        """
        http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip}
        YYYY-MM-DDThh:mm
        """
        carhire_service = CarHire(self.api_key)

        self.result = carhire_service.get_result(
            market='UK',
            currency='GBP',
            locale='en-GB',
            pickupplace='LHR-sky',
            dropoffplace='LHR-sky',
            pickupdatetime=self.pickup,
            dropoffdatetime=self.dropoff,
            driverage='30',
            userip='175.156.244.174')

        self.assertTrue('cars' in self.result)
        self.assertTrue('websites' in self.result)

    def test_create_session(self):
        """
        http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip}
        YYYY-MM-DDThh:mm
        """
        carhire_service = CarHire(self.api_key)

        poll_url = carhire_service.create_session(
            market='UK',
            currency='GBP',
            locale='en-GB',
            pickupplace='LHR-sky',
            dropoffplace='LHR-sky',
            pickupdatetime=self.pickup,
            dropoffdatetime=self.dropoff,
            driverage='30',
            userip='175.156.244.174')

        self.assertTrue(poll_url)


class TestHotels(SkyScannerTestCase):

    def setUp(self):
        # API Key that's meant for testing only
        # Taken from: http://business.skyscanner.net/portal/en-GB/Documentation/FlightsLivePricingQuickStart
        super(TestHotels, self).setUp()
        self.api_key = 'prtl6749387986743898559646983194'
        datetime_format = '%Y-%m-%d'
        checkin_datetime = datetime.now()
        checkout_datetime = checkin_datetime + timedelta(days=4)
        self.checkin = checkin_datetime.strftime(datetime_format)
        self.checkout = checkout_datetime.strftime(datetime_format)

    def test_location_autosuggest(self):
        hotels_service = Hotels(self.api_key)

        self.result = hotels_service.location_autosuggest(
            market='UK',
            currency='GBP',
            locale='en-GB',
            query='Kuala')

        self.assertTrue('results' in self.result)
        self.assertTrue(len(self.result['results']) > 0)

    def test_get_result(self):
        """
        http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip}
        YYYY-MM-DDThh:mm
        """

        hotels_service = Hotels(self.api_key)
        self.result = hotels_service.get_result(
            market='UK',
            currency='GBP',
            locale='en-GB',
            entityid=27543923,
            checkindate=self.checkin,
            checkoutdate=self.checkout,
            guests=1,
            rooms=1)

        self.assertTrue('hotels' in self.result)
        self.assertTrue(len(self.result['hotels']) > 0)

    def test_create_session(self):
        """
        http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip}
        YYYY-MM-DDThh:mm
        """
        hotels_service = Hotels(self.api_key)

        poll_url = hotels_service.create_session(
            market='UK',
            currency='GBP',
            locale='en-GB',
            entityid=27543923,
            checkindate=self.checkin,
            checkoutdate=self.checkout,
            guests=1,
            rooms=1)

        self.assertTrue(poll_url)


class TestFlights(SkyScannerTestCase):

    def setUp(self):
        # API Key that's meant for testing only
        # Taken from: http://business.skyscanner.net/portal/en-GB/Documentation/FlightsLivePricingQuickStart
        super(TestFlights, self).setUp()
        self.api_key = 'prtl6749387986743898559646983194'
        datetime_format = '%Y-%m'
        outbound_datetime = datetime.now()
        inbound_datetime = outbound_datetime + timedelta(days=31)
        self.outbound = outbound_datetime.strftime(datetime_format)
        self.inbound = inbound_datetime.strftime(datetime_format)

        datetime_format = '%Y-%m-%d'
        inbound_datetime = outbound_datetime + timedelta(days=3)
        self.outbound_days = outbound_datetime.strftime(datetime_format)
        self.inbound_days = inbound_datetime.strftime(datetime_format)

    def test_get_cheapest_quotes(self):
        flights_cache_service = FlightsCache(self.api_key)
        self.result = flights_cache_service.get_cheapest_quotes(
            country='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            outbounddate=self.outbound,
            inbounddate=self.inbound)

        self.assertTrue('Quotes' in self.result)
        self.assertTrue(len(self.result['Quotes']) > 0)

    # I'm getting the following result:
    # {u'ValidationErrors': [{u'Message': u'For this query please use the following service [BrowseDates]'}]}
    def test_get_cheapest_price_by_route(self):
        flights_cache_service = FlightsCache(self.api_key)
        self.result = flights_cache_service.get_cheapest_price_by_route(
            country='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            outbounddate=self.outbound,
            inbounddate=self.inbound)

        print("result: %s" % self.result)

    def test_get_cheapest_price_by_date(self):
        flights_cache_service = FlightsCache(self.api_key)
        self.result = flights_cache_service.get_cheapest_price_by_date(
            country='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            outbounddate=self.outbound,
            inbounddate=self.inbound)

        self.assertTrue('Quotes' in self.result)
        self.assertTrue(len(self.result['Quotes']) > 0)

    def test_get_grid_prices_by_date(self):
        flights_cache_service = FlightsCache(self.api_key)
        self.result = flights_cache_service.get_grid_prices_by_date(
            country='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            outbounddate=self.outbound,
            inbounddate=self.inbound)

        self.assertTrue('Dates' in self.result)
        self.assertTrue(len(self.result['Dates']) > 0)

    def test_create_session(self):
        flights_service = Flights(self.api_key)
        poll_url = flights_service.create_session(
            country='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            outbounddate=self.outbound_days,
            inbounddate=self.inbound_days,
            adults=1)

        self.assertTrue(poll_url)

    def test_get_markets(self):
        transport = Transport(self.api_key)
        self.result = transport.get_markets('en-GB')

        self.assertTrue('Countries' in self.result)
        self.assertTrue(len(self.result['Countries']) > 0)

    def test_location_autosuggest(self):
        transport = Transport(self.api_key)
        self.result = transport.location_autosuggest('KUL', 'UK', 'GBP', 'en-GB')

        self.assertTrue('Places' in self.result)
        self.assertTrue(len(self.result['Places']) > 0)

    # def test_poll_session(self):
    #     flights_service = Flights(self.api_key)

    #     poll_url = flights_service.create_session(
    #         country='UK',
    #         currency='GBP',
    #         locale='en-GB',
    #         originplace='SIN-sky',
    #         destinationplace='KUL-sky',
    #         outbounddate='2015-05-28',
    #         inbounddate='2015-05-31',
    #         adults=1)

    #     result = flights_service.poll_session(poll_url, sorttype='carrier')

    #     self.assertTrue(len(result['Itineraries']) > 0)

    #     pass

    # def test_request_booking_details(self):
    #     flights_service = Flights(self.api_key)

    #     poll_url = flights_service.create_session(
    #         country='UK',
    #         currency='GBP',
    #         locale='en-GB',
    #         originplace='SIN-sky',
    #         destinationplace='KUL-sky',
    #         outbounddate='2015-05-28',
    #         inbounddate='2015-05-31',
    #         adults=1)

    #     flights_results = flights_service.poll_session(poll_url, sorttype='carrier')

    #     print(flights_results)

    #     itinerary = flights_results['Itineraries'][0]

    #     result = flights_service.request_booking_details(poll_url, outboundlegid=itinerary['OutboundLegId'],
    #                                                      inboundlegid=itinerary['InboundLegId'])

    #     print(result)

    #     pass

    def test_get_result(self):
        flights_service = Flights(self.api_key)
        self.result = flights_service.get_result(
            country='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            outbounddate=self.outbound_days,
            inbounddate=self.inbound_days,
            adults=1)

        # print(result)
        print("status: %s" % self.result['Status'])
        # self.assertTrue(len(result['Flights']['Itineraries']) > 0)


if __name__ == '__main__':
    unittest.main()
