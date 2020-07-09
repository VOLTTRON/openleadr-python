from pyopenadr.utils import create_message, generate_id
from pyopenadr import enums
from lxml import etree
import os
from datetime import datetime, timedelta, timezone
from termcolor import colored
import jinja2

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
SCHEMA_LOCATION = os.path.join('schema', 'oadr_20b.xsd')

schema_root = etree.parse(SCHEMA_LOCATION)
schema = etree.XMLSchema(schema_root)
parser = etree.XMLParser(schema=schema)

def create_dummy_event(ven_id):
    """
    Creates a dummy event
    """
    now = datetime.now(timezone.utc)
    event_id = generate_id()
    active_period = {"dtstart": now + timedelta(minutes=1),
                     "duration": timedelta(minutes=10)}

    event_descriptor = {"event_id": event_id,
                        "modification_number": 1,
                        "modification_date_time": now,
                        "priority": 1,
                        "market_context": "http://MarketContext1",
                        "created_date_time": now,
                        "event_status": "near",
                        "test_event": "false",
                        "vtn_comment": "This is an event"}

    event_signals = [{"intervals": [{"duration": timedelta(minutes=1), "uid": 1, "signal_payload": 8},
                                    {"duration": timedelta(minutes=1), "uid": 2, "signal_payload": 10},
                                    {"duration": timedelta(minutes=1), "uid": 3, "signal_payload": 12},
                                    {"duration": timedelta(minutes=1), "uid": 4, "signal_payload": 14},
                                    {"duration": timedelta(minutes=1), "uid": 5, "signal_payload": 16},
                                    {"duration": timedelta(minutes=1), "uid": 6, "signal_payload": 18},
                                    {"duration": timedelta(minutes=1), "uid": 7, "signal_payload": 20},
                                    {"duration": timedelta(minutes=1), "uid": 8, "signal_payload": 10},
                                    {"duration": timedelta(minutes=1), "uid": 9, "signal_payload": 20}],
                    "signal_name": "LOAD_CONTROL",
                    #"signal_name": "simple",
                    #"signal_type": "level",
                    "signal_type": "x-loadControlCapacity",
                    "signal_id": generate_id(),
                    "current_value": 9.99}]

    event_targets = [{"ven_id": 'VEN001'}, {"ven_id": 'VEN002'}]
    event = {'active_period': active_period,
             'event_descriptor': event_descriptor,
             'event_signals': event_signals,
             'targets': event_targets,
             'response_required': 'always'}
    return event

# Test oadrPoll
def test_message(type, **payload):
    try:
        message = create_message(type, **payload)
        etree.fromstring(message.encode('utf-8'), parser)
        print(colored(f"pass: {type} OK", "green"))
    except etree.XMLSyntaxError as err:
        print(colored(f"fail: {type} failed validation: {err}", "red"))
        print(message)
    except jinja2.exceptions.UndefinedError as err:
        print(colored(f"fail: {type} failed message construction: {err}", "yellow"))


test_message('oadrCanceledOpt', response={'response_code': 200, 'response_description': 'OK', 'request_id': generate_id()}, opt_id=generate_id())
test_message('oadrCanceledPartyRegistration', response={'response_code': 200, 'response_description': 'OK', 'request_id': generate_id()}, registration_id=generate_id(), ven_id='123ABC')
test_message('oadrCanceledReport', response={'response_code': 200, 'response_description': 'OK', 'request_id': generate_id()}, pending_reports=[{'request_id': generate_id()}, {'request_id': generate_id()}])
test_message('oadrCanceledReport', response={'response_code': 200, 'response_description': 'OK', 'request_id': generate_id()}, pending_reports=[{'request_id': generate_id()}, {'request_id': generate_id()}], ven_id='123ABC')
test_message('oadrCancelOpt', request_id=generate_id(), ven_id='123ABC', opt_id=generate_id())
test_message('oadrCancelPartyRegistration', request_id=generate_id(), ven_id='123ABC', registration_id=generate_id())
test_message('oadrCancelReport', request_id=generate_id(), ven_id='123ABC', report_request_id=generate_id(), report_to_follow=True)
test_message('oadrCreatedEvent', response={'response_code': 200, 'response_description': 'OK', 'request_id': generate_id()},
                                 event_responses=[{'response_code': 200, 'response_description': 'OK', 'request_id': generate_id(), 'event_id': generate_id(), 'modification_number': 1, 'opt_type': 'optIn'},
                                                  {'response_code': 200, 'response_description': 'OK', 'request_id': generate_id(), 'event_id': generate_id(), 'modification_number': 1, 'opt_type': 'optIn'},
                                                  {'response_code': 200, 'response_description': 'OK', 'request_id': generate_id(), 'event_id': generate_id(), 'modification_number': 1, 'opt_type': 'optIn'}],
                                 ven_id='123ABC')
test_message('oadrCreatedReport', response={'response_code': 200, 'response_description': 'OK', 'request_id': generate_id()}, pending_reports=[{'request_id': generate_id()}, {'request_id': generate_id()}], ven_id='123ABC')
test_message('oadrCreatedEvent', response={'response_code': 200, 'response_description': 'OK', 'request_id': generate_id()},
                                 event_responses=[{'response_code': 200, 'response_description': 'OK', 'request_id': generate_id(),
                                                    'event_id': generate_id(),
                                                    'modification_number': 1,
                                                    'opt_type': 'optIn'},
                                                    {'response_code': 200, 'response_description': 'OK', 'request_id': generate_id(),
                                                    'event_id': generate_id(),
                                                    'modification_number': 1,
                                                    'opt_type': 'optOut'}],
                                 ven_id='123ABC')
test_message('oadrCreatedPartyRegistration', response={'response_code': 200, 'response_description': 'OK', 'request_id': generate_id()},
                                             registration_id=generate_id(),
                                             ven_id='123ABC',
                                             profiles=[{'profile_name': '2.0b',
                                                        'transports': [{'transport_name': 'simpleHttp'}]}],
                                             vtn_id='VTN123')
test_message('oadrCreatedReport', response={'response_code': 200, 'response_description': 'OK', 'request_id': generate_id()}, pending_reports=[{'request_id': generate_id()}, {'request_id': generate_id()}])
test_message('oadrCreateOpt', opt_id=generate_id(),
                              opt_type='optIn',
                              opt_reason='participating',
                              created_date_time=datetime.now(timezone.utc),
                              request_id=generate_id(),
                              event_id=generate_id(),
                              modification_number=1,
                              targets=[{'ven_id': '123ABC'}],
                              ven_id='VEN123')
test_message('oadrCreatePartyRegistration', request_id=generate_id(), ven_id='123ABC', profile_name='2.0b', transport_name='simpleHttp', transport_address='http://localhost', report_only=False, xml_signature=False, ven_name='test', http_pull_model=True)
test_message('oadrCreateReport', request_id=generate_id(),
                                 ven_id='123ABC',
                                 report_requests=[{'report_request_id': 'd2b7bade5f',
                                                  'report_specifier': {'granularity': timedelta(seconds=900),
                                                                       'report_back_duration': timedelta(seconds=900),
                                                                       'report_interval': {'dtstart': datetime(2019, 11, 19, 11, 0, 18, 672768, tzinfo=timezone.utc),
                                                                                           'duration': timedelta(seconds=7200),
                                                                                           'tolerance': {'tolerate': {'startafter': timedelta(seconds=300)}}},
                                                                       'report_specifier_id': '9c8bdc00e7',
                                                                       'specifier_payload': {'r_id': 'd6e2e07485',
                                                                                             'reading_type': 'Direct Read'}}}])
test_message('oadrDistributeEvent', request_id=generate_id(), response={'request_id': 123, 'response_code': 200, 'response_description': 'OK'}, events=[create_dummy_event(ven_id='123ABC')], vtn_id='VTN123')
test_message('oadrPoll', ven_id='123ABC')
test_message('oadrQueryRegistration', request_id=generate_id())
test_message('oadrRegisteredReport', ven_id='VEN123', response={'response_code': 200, 'response_description': 'OK', 'request_id': generate_id()},
                                     report_requests=[{'report_request_id': generate_id(),
                                                       'report_specifier': {'report_specifier_id': generate_id(),
                                                                            'granularity': timedelta(minutes=15),
                                                                            'report_back_duration': timedelta(minutes=15),
                                                                            'report_interval': {'dtstart': datetime.now(timezone.utc),
                                                                                                'duration': timedelta(hours=2),
                                                                                                'tolerance': {'tolerate': {'startafter': timedelta(minutes=5)}},
                                                                                                'notification': timedelta(minutes=30),
                                                                                                'ramp_up': timedelta(minutes=15),
                                                                                                'recovery': timedelta(minutes=5)},
                                                                            'specifier_payload': {'r_id': generate_id(),
                                                                                                  'reading_type': 'Direct Read'}}},
                                                      {'report_request_id': generate_id(),
                                                       'report_specifier': {'report_specifier_id': generate_id(),
                                                                            'granularity': timedelta(minutes=15),
                                                                            'report_back_duration': timedelta(minutes=15),
                                                                            'report_interval': {'dtstart': datetime.now(timezone.utc),
                                                                                                'duration': timedelta(hours=2),
                                                                                                'tolerance': {'tolerate': {'startafter': timedelta(minutes=5)}},
                                                                                                'notification': timedelta(minutes=30),
                                                                                                'ramp_up': timedelta(minutes=15),
                                                                                                'recovery': timedelta(minutes=5)},
                                                                            'specifier_payload': {'r_id': generate_id(),
                                                                                                  'reading_type': 'Direct Read'}}}])
test_message('oadrRequestEvent', request_id=generate_id(), ven_id='123ABC')
test_message('oadrRequestReregistration', ven_id='123ABC')
test_message('oadrRegisterReport', request_id=generate_id(), reports=[{'report_id': generate_id(),
                                                                       'report_descriptions': [{
                                                                            'r_id': generate_id(),
                                                                            'report_subjects': {'ven_id': '123ABC'},
                                                                            'report_data_sources': {'ven_id': '123ABC'},
                                                                            'report_type': 'reading',
                                                                            'reading_type': 'Direct Read',
                                                                            'market_context': 'http://localhost',
                                                                            'sampling_rate': {'min_period': timedelta(minutes=1), 'max_period': timedelta(minutes=1), 'on_change': True}}],
                                                                       'report_request_id': generate_id(),
                                                                       'report_specifier_id': generate_id(),
                                                                       'report_name': 'HISTORY_USAGE',
                                                                       'created_date_time': datetime.now(timezone.utc)}],
                                                        ven_id='123ABC',
                                                        report_request_id=generate_id())
test_message('oadrRegisterReport', **{'request_id': '8a4f859883', 'reports': [{'duration': timedelta(seconds=7200), 'report_descriptions': [{'r_id': 'resource1_status', 'report_data_sources': [{'resource_id': 'resource1'}], 'report_type': 'x-resourceStatus', 'reading_type': 'x-notApplicable', 'market_context': 'http://MarketContext1', 'sampling_rate': {'min_period': timedelta(seconds=60), 'max_period': timedelta(seconds=60), 'on_change': False}}], 'report_request_id': '0', 'report_specifier_id': '789ed6cd4e_telemetry_status', 'report_name': 'METADATA_TELEMETRY_STATUS', 'created_date_time': datetime(2019, 11, 20, 15, 4, 52, 638621, tzinfo=timezone.utc)}, {'duration': timedelta(seconds=7200), 'report_descriptions': [{'r_id': 'resource1_energy', 'report_data_sources': [{'resource_id': 'resource1'}], 'report_type': 'usage', 'energy_real': {'item_description': 'RealEnergy', 'item_units': 'Wh', 'si_scale_code': 'n'}, 'reading_type': 'Direct Read', 'market_context': 'http://MarketContext1', 'sampling_rate': {'min_period': timedelta(seconds=60), 'max_period': timedelta(seconds=60), 'on_change': False}}, {'r_id': 'resource1_power', 'report_data_sources': [{'resource_id': 'resource1'}], 'report_type': 'usage', 'power_real': {'item_description': 'RealPower', 'item_units': 'W', 'si_scale_code': 'n', 'power_attributes': {'hertz': 60, 'voltage': 110, 'ac': False}}, 'reading_type': 'Direct Read', 'market_context': 'http://MarketContext1', 'sampling_rate': {'min_period': timedelta(seconds=60), 'max_period': timedelta(seconds=60), 'on_change': False}}], 'report_request_id': '0', 'report_specifier_id': '789ed6cd4e_telemetry_usage', 'report_name': 'METADATA_TELEMETRY_USAGE', 'created_date_time': datetime(2019, 11, 20, 15, 4, 52, 638621, tzinfo=timezone.utc)}, {'duration': timedelta(seconds=7200), 'report_descriptions': [{'r_id': 'resource1_energy', 'report_data_sources': [{'resource_id': 'resource1'}], 'report_type': 'usage', 'energy_real': {'item_description': 'RealEnergy', 'item_units': 'Wh', 'si_scale_code': 'n'}, 'reading_type': 'Direct Read', 'market_context': 'http://MarketContext1', 'sampling_rate': {'min_period': timedelta(seconds=60), 'max_period': timedelta(seconds=60), 'on_change': False}}, {'r_id': 'resource1_power', 'report_data_sources': [{'resource_id': 'resource1'}], 'report_type': 'usage', 'power_real': {'item_description': 'RealPower', 'item_units': 'W', 'si_scale_code': 'n', 'power_attributes': {'hertz': 60, 'voltage': 110, 'ac': False}}, 'reading_type': 'Direct Read', 'market_context': 'http://MarketContext1', 'sampling_rate': {'min_period': timedelta(seconds=60), 'max_period': timedelta(seconds=60), 'on_change': False}}], 'report_request_id': '0', 'report_specifier_id': '789ed6cd4e_history_usage', 'report_name': 'METADATA_HISTORY_USAGE', 'created_date_time': datetime(2019, 11, 20, 15, 4, 52, 638621, tzinfo=timezone.utc)}], 'ven_id': 's3cc244ee6'})
test_message('oadrResponse', response={'response_code': 200, 'response_description': 'OK', 'request_id': generate_id()}, ven_id='123ABC')
test_message('oadrResponse', response={'response_code': 200, 'response_description': 'OK', 'request_id': None}, ven_id='123ABC')
test_message('oadrUpdatedReport', response={'response_code': 200, 'response_description': 'OK', 'request_id': generate_id()}, ven_id='123ABC', cancel_report={'request_id': generate_id(), 'report_request_id': [generate_id(), generate_id(), generate_id()], 'report_to_follow': False, 'ven_id': '123ABC'})
test_message('oadrUpdateReport', request_id=generate_id(), reports=[{'report_id': generate_id(),
                                                                                  'report_name': enums.REPORT_NAME.values[0],
                                                                                  'created_date_time': datetime.now(timezone.utc),
                                                                                  'report_request_id': generate_id(),
                                                                                  'report_specifier_id': generate_id(),
                                                                                 'report_descriptions': [{'r_id': generate_id(),
                                                                                                          'report_subjects': [{'ven_id': '123ABC'}, {'ven_id': 'DEF456'}],
                                                                                                          'report_data_sources': [{'ven_id': '123ABC'}],
                                                                                                          'report_type': enums.REPORT_TYPE.values[0],
                                                                                                          'reading_type': enums.READING_TYPE.values[0],
                                                                                                          'market_context': 'http://localhost',
                                                                                                          'sampling_rate': {'min_period': timedelta(minutes=1),
                                                                                                                            'max_period': timedelta(minutes=2),
                                                                                                                            'on_change': False}}]}], ven_id='123ABC')

# for report_name in enums.REPORT_NAME.values:
#     for reading_type in enums.READING_TYPE.values:
#         for report_type in enums.REPORT_TYPE.values:
#             test_message('oadrUpdateReport', request_id=generate_id(), reports=[{'report_id': generate_id(),
#                                                                                   'report_name': report_name,
#                                                                                   'created_date_time': datetime.now(timezone.utc),
#                                                                                   'report_request_id': generate_id(),
#                                                                                   'report_specifier_id': generate_id(),
#                                                                                  'report_descriptions': [{'r_id': generate_id(),
#                                                                                                           'report_subjects': [{'ven_id': '123ABC'}, {'ven_id': 'DEF456'}],
#                                                                                                           'report_data_sources': [{'ven_id': '123ABC'}],
#                                                                                                           'report_type': report_type,
#                                                                                                           'reading_type': reading_type,
#                                                                                                           'market_context': 'http://localhost',
#                                                                                                           'sampling_rate': {'min_period': timedelta(minutes=1),
#                                                                                                                             'max_period': timedelta(minutes=2),
#                                                                                                                             'on_change': False}}]}], ven_id='123ABC')
