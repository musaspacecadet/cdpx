# # DO NOT EDIT THIS FILE!
# #
# # This file is generated from the CDP specification using AST. If you need to make
# # changes, edit the generator and regenerate all of the modules.

from __future__ import annotations
"""CDP domain: ServiceWorker (experimental)"""
import typing
import enum
from dataclasses import dataclass
from .util import T_JSON_DICT, event_class
from . import target
None


@dataclass
class ServiceWorkerErrorMessage:
    """ServiceWorker error message."""
    error_message: str
    registration_id: RegistrationID
    version_id: str
    source_url: str
    line_number: int
    column_number: int

    def to_json(self) ->T_JSON_DICT:
        json_data: T_JSON_DICT = dict()
        json_data['errorMessage'] = self.error_message
        json_data['registrationId'] = self.registration_id.to_json()
        json_data['versionId'] = self.version_id
        json_data['sourceURL'] = self.source_url
        json_data['lineNumber'] = self.line_number
        json_data['columnNumber'] = self.column_number
        return json_data

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->ServiceWorkerErrorMessage:
        return cls(error_message=json_obj['errorMessage'], registration_id=
            RegistrationID.from_json(json_obj['registrationId']),
            version_id=json_obj['versionId'], source_url=json_obj[
            'sourceURL'], line_number=json_obj['lineNumber'], column_number
            =json_obj['columnNumber'])


@dataclass
class ServiceWorkerRegistration:
    """ServiceWorker registration."""
    registration_id: RegistrationID
    scope_url: str
    is_deleted: bool

    def to_json(self) ->T_JSON_DICT:
        json_data: T_JSON_DICT = dict()
        json_data['registrationId'] = self.registration_id.to_json()
        json_data['scopeURL'] = self.scope_url
        json_data['isDeleted'] = self.is_deleted
        return json_data

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->ServiceWorkerRegistration:
        return cls(registration_id=RegistrationID.from_json(json_obj[
            'registrationId']), scope_url=json_obj['scopeURL'], is_deleted=
            json_obj['isDeleted'])


@dataclass
class ServiceWorkerVersion:
    """ServiceWorker version."""
    version_id: str
    registration_id: RegistrationID
    script_url: str
    running_status: ServiceWorkerVersionRunningStatus
    status: ServiceWorkerVersionStatus
    script_last_modified: typing.Optional[float] = None
    script_response_time: typing.Optional[float] = None
    controlled_clients: typing.Optional[typing.List[target.TargetID]] = None
    target_id: typing.Optional[target.TargetID] = None
    router_rules: typing.Optional[str] = None

    def to_json(self) ->T_JSON_DICT:
        json_data: T_JSON_DICT = dict()
        json_data['versionId'] = self.version_id
        json_data['registrationId'] = self.registration_id.to_json()
        json_data['scriptURL'] = self.script_url
        json_data['runningStatus'] = self.running_status.to_json()
        json_data['status'] = self.status.to_json()
        if self.script_last_modified is not None:
            json_data['scriptLastModified'] = self.script_last_modified
        if self.script_response_time is not None:
            json_data['scriptResponseTime'] = self.script_response_time
        if self.controlled_clients is not None:
            json_data['controlledClients'] = [i.to_json() for i in self.
                controlled_clients]
        if self.target_id is not None:
            json_data['targetId'] = self.target_id.to_json()
        if self.router_rules is not None:
            json_data['routerRules'] = self.router_rules
        return json_data

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->ServiceWorkerVersion:
        return cls(version_id=json_obj['versionId'], registration_id=
            RegistrationID.from_json(json_obj['registrationId']),
            script_url=json_obj['scriptURL'], running_status=
            ServiceWorkerVersionRunningStatus.from_json(json_obj[
            'runningStatus']), status=ServiceWorkerVersionStatus.from_json(
            json_obj['status']), script_last_modified=json_obj[
            'scriptLastModified'] if json_obj.get('scriptLastModified') is not
            None else None, script_response_time=json_obj[
            'scriptResponseTime'] if json_obj.get('scriptResponseTime') is not
            None else None, controlled_clients=[target.TargetID.from_json(i
            ) for i in json_obj['controlledClients']] if json_obj.get(
            'controlledClients') is not None else None, target_id=target.
            TargetID.from_json(json_obj['targetId']) if json_obj.get(
            'targetId') is not None else None, router_rules=json_obj[
            'routerRules'] if json_obj.get('routerRules') is not None else None
            )


class ServiceWorkerVersionRunningStatus(enum.Enum):
    STOPPED = 'stopped'
    STARTING = 'starting'
    RUNNING = 'running'
    STOPPING = 'stopping'

    @classmethod
    def from_json(cls, json: str) ->ServiceWorkerVersionRunningStatus:
        return cls(json)

    def to_json(self) ->str:
        return self.value

    def __repr__(self) ->str:
        return '<ServiceWorkerVersionRunningStatus.{}>'.format(self.value)


class ServiceWorkerVersionStatus(enum.Enum):
    NEW = 'new'
    INSTALLING = 'installing'
    INSTALLED = 'installed'
    ACTIVATING = 'activating'
    ACTIVATED = 'activated'
    REDUNDANT = 'redundant'

    @classmethod
    def from_json(cls, json: str) ->ServiceWorkerVersionStatus:
        return cls(json)

    def to_json(self) ->str:
        return self.value

    def __repr__(self) ->str:
        return '<ServiceWorkerVersionStatus.{}>'.format(self.value)


class RegistrationID(str):
    """Represents the CDP type 'ServiceWorker.RegistrationID'."""

    def to_json(self) ->str:
        return self

    @classmethod
    def from_json(cls, json: str) ->RegistrationID:
        return cls(json)

    def __repr__(self) ->str:
        return 'RegistrationID({})'.format(super().__repr__())


def deliver_push_message(origin: str, registration_id: RegistrationID, data:
    str) ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """:param ...:

:param origin:

:param registration_id:

:param data:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['origin'] = origin
    params_dict['registrationId'] = registration_id.to_json()
    params_dict['data'] = data
    cmd_dict = {'method': 'ServiceWorker.deliverPushMessage', 'params':
        params_dict}
    json_result = yield cmd_dict
    return None


def disable() ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    cmd_dict = {'method': 'ServiceWorker.disable'}
    json_result = yield cmd_dict
    return None


def dispatch_periodic_sync_event(origin: str, registration_id:
    RegistrationID, tag: str) ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None
    ]:
    """:param ...:

:param origin:

:param registration_id:

:param tag:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['origin'] = origin
    params_dict['registrationId'] = registration_id.to_json()
    params_dict['tag'] = tag
    cmd_dict = {'method': 'ServiceWorker.dispatchPeriodicSyncEvent',
        'params': params_dict}
    json_result = yield cmd_dict
    return None


def dispatch_sync_event(origin: str, registration_id: RegistrationID, tag:
    str, last_chance: bool) ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """:param ...:

:param origin:

:param registration_id:

:param tag:

:param last_chance:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['origin'] = origin
    params_dict['registrationId'] = registration_id.to_json()
    params_dict['tag'] = tag
    params_dict['lastChance'] = last_chance
    cmd_dict = {'method': 'ServiceWorker.dispatchSyncEvent', 'params':
        params_dict}
    json_result = yield cmd_dict
    return None


def enable() ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    cmd_dict = {'method': 'ServiceWorker.enable'}
    json_result = yield cmd_dict
    return None


def inspect_worker(version_id: str) ->typing.Generator[T_JSON_DICT,
    T_JSON_DICT, None]:
    """:param ...:

:param version_id:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['versionId'] = version_id
    cmd_dict = {'method': 'ServiceWorker.inspectWorker', 'params': params_dict}
    json_result = yield cmd_dict
    return None


def set_force_update_on_page_load(force_update_on_page_load: bool
    ) ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """:param ...:

:param force_update_on_page_load:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['forceUpdateOnPageLoad'] = force_update_on_page_load
    cmd_dict = {'method': 'ServiceWorker.setForceUpdateOnPageLoad',
        'params': params_dict}
    json_result = yield cmd_dict
    return None


def skip_waiting(scope_url: str) ->typing.Generator[T_JSON_DICT,
    T_JSON_DICT, None]:
    """:param ...:

:param scope_url:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['scopeURL'] = scope_url
    cmd_dict = {'method': 'ServiceWorker.skipWaiting', 'params': params_dict}
    json_result = yield cmd_dict
    return None


def start_worker(scope_url: str) ->typing.Generator[T_JSON_DICT,
    T_JSON_DICT, None]:
    """:param ...:

:param scope_url:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['scopeURL'] = scope_url
    cmd_dict = {'method': 'ServiceWorker.startWorker', 'params': params_dict}
    json_result = yield cmd_dict
    return None


def stop_all_workers() ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    cmd_dict = {'method': 'ServiceWorker.stopAllWorkers'}
    json_result = yield cmd_dict
    return None


def stop_worker(version_id: str) ->typing.Generator[T_JSON_DICT,
    T_JSON_DICT, None]:
    """:param ...:

:param version_id:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['versionId'] = version_id
    cmd_dict = {'method': 'ServiceWorker.stopWorker', 'params': params_dict}
    json_result = yield cmd_dict
    return None


def unregister(scope_url: str) ->typing.Generator[T_JSON_DICT, T_JSON_DICT,
    None]:
    """:param ...:

:param scope_url:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['scopeURL'] = scope_url
    cmd_dict = {'method': 'ServiceWorker.unregister', 'params': params_dict}
    json_result = yield cmd_dict
    return None


def update_registration(scope_url: str) ->typing.Generator[T_JSON_DICT,
    T_JSON_DICT, None]:
    """:param ...:

:param scope_url:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['scopeURL'] = scope_url
    cmd_dict = {'method': 'ServiceWorker.updateRegistration', 'params':
        params_dict}
    json_result = yield cmd_dict
    return None


@event_class('ServiceWorker.workerErrorReported')
@dataclass
class WorkerErrorReported:
    error_message: ServiceWorkerErrorMessage

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->WorkerErrorReported:
        return cls(error_message=ServiceWorkerErrorMessage.from_json(
            json_obj['errorMessage']))


@event_class('ServiceWorker.workerRegistrationUpdated')
@dataclass
class WorkerRegistrationUpdated:
    registrations: typing.List[ServiceWorkerRegistration]

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->WorkerRegistrationUpdated:
        return cls(registrations=[ServiceWorkerRegistration.from_json(i) for
            i in json_obj['registrations']])


@event_class('ServiceWorker.workerVersionUpdated')
@dataclass
class WorkerVersionUpdated:
    versions: typing.List[ServiceWorkerVersion]

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->WorkerVersionUpdated:
        return cls(versions=[ServiceWorkerVersion.from_json(i) for i in
            json_obj['versions']])
