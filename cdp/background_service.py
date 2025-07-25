# # DO NOT EDIT THIS FILE!
# #
# # This file is generated from the CDP specification using AST. If you need to make
# # changes, edit the generator and regenerate all of the modules.

from __future__ import annotations
"""CDP domain: BackgroundService (experimental)

Defines events for background web platform features."""
import typing
import enum
from dataclasses import dataclass
from .util import T_JSON_DICT, event_class
from . import network
from . import service_worker
None


@dataclass
class BackgroundServiceEvent:
    timestamp: network.TimeSinceEpoch
    origin: str
    service_worker_registration_id: service_worker.RegistrationID
    service: ServiceName
    event_name: str
    instance_id: str
    event_metadata: typing.List[EventMetadata]
    storage_key: str

    def to_json(self) ->T_JSON_DICT:
        json_data: T_JSON_DICT = dict()
        json_data['timestamp'] = self.timestamp.to_json()
        json_data['origin'] = self.origin
        json_data['serviceWorkerRegistrationId'
            ] = self.service_worker_registration_id.to_json()
        json_data['service'] = self.service.to_json()
        json_data['eventName'] = self.event_name
        json_data['instanceId'] = self.instance_id
        json_data['eventMetadata'] = [i.to_json() for i in self.event_metadata]
        json_data['storageKey'] = self.storage_key
        return json_data

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->BackgroundServiceEvent:
        return cls(timestamp=network.TimeSinceEpoch.from_json(json_obj[
            'timestamp']), origin=json_obj['origin'],
            service_worker_registration_id=service_worker.RegistrationID.
            from_json(json_obj['serviceWorkerRegistrationId']), service=
            ServiceName.from_json(json_obj['service']), event_name=json_obj
            ['eventName'], instance_id=json_obj['instanceId'],
            event_metadata=[EventMetadata.from_json(i) for i in json_obj[
            'eventMetadata']], storage_key=json_obj['storageKey'])


@dataclass
class EventMetadata:
    """A key-value pair for additional event information to pass along."""
    key: str
    value: str

    def to_json(self) ->T_JSON_DICT:
        json_data: T_JSON_DICT = dict()
        json_data['key'] = self.key
        json_data['value'] = self.value
        return json_data

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->EventMetadata:
        return cls(key=json_obj['key'], value=json_obj['value'])


class ServiceName(enum.Enum):
    """The Background Service that will be associated with the commands/events.
Every Background Service operates independently, but they share the same
API."""
    BACKGROUND_FETCH = 'backgroundFetch'
    BACKGROUND_SYNC = 'backgroundSync'
    PUSH_MESSAGING = 'pushMessaging'
    NOTIFICATIONS = 'notifications'
    PAYMENT_HANDLER = 'paymentHandler'
    PERIODIC_BACKGROUND_SYNC = 'periodicBackgroundSync'

    @classmethod
    def from_json(cls, json: str) ->ServiceName:
        return cls(json)

    def to_json(self) ->str:
        return self.value

    def __repr__(self) ->str:
        return '<ServiceName.{}>'.format(self.value)


def clear_events(service: ServiceName) ->typing.Generator[T_JSON_DICT,
    T_JSON_DICT, None]:
    """Clears all stored data for the service.

:param ...:

:param service:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['service'] = service.to_json()
    cmd_dict = {'method': 'BackgroundService.clearEvents', 'params':
        params_dict}
    json_result = yield cmd_dict
    return None


def set_recording(should_record: bool, service: ServiceName
    ) ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """Set the recording state for the service.

:param ...:

:param should_record:

:param service:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['shouldRecord'] = should_record
    params_dict['service'] = service.to_json()
    cmd_dict = {'method': 'BackgroundService.setRecording', 'params':
        params_dict}
    json_result = yield cmd_dict
    return None


def start_observing(service: ServiceName) ->typing.Generator[T_JSON_DICT,
    T_JSON_DICT, None]:
    """Enables event updates for the service.

:param ...:

:param service:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['service'] = service.to_json()
    cmd_dict = {'method': 'BackgroundService.startObserving', 'params':
        params_dict}
    json_result = yield cmd_dict
    return None


def stop_observing(service: ServiceName) ->typing.Generator[T_JSON_DICT,
    T_JSON_DICT, None]:
    """Disables event updates for the service.

:param ...:

:param service:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['service'] = service.to_json()
    cmd_dict = {'method': 'BackgroundService.stopObserving', 'params':
        params_dict}
    json_result = yield cmd_dict
    return None


@event_class('BackgroundService.backgroundServiceEventReceived')
@dataclass
class BackgroundServiceEventReceived:
    """Called with all existing backgroundServiceEvents when enabled, and all new
events afterwards if enabled and recording."""
    background_service_event: BackgroundServiceEvent

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->BackgroundServiceEventReceived:
        return cls(background_service_event=BackgroundServiceEvent.
            from_json(json_obj['backgroundServiceEvent']))


@event_class('BackgroundService.recordingStateChanged')
@dataclass
class RecordingStateChanged:
    """Called when the recording state for the service has been updated."""
    is_recording: bool
    service: ServiceName

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->RecordingStateChanged:
        return cls(is_recording=json_obj['isRecording'], service=
            ServiceName.from_json(json_obj['service']))
