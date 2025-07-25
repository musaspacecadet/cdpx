# # DO NOT EDIT THIS FILE!
# #
# # This file is generated from the CDP specification using AST. If you need to make
# # changes, edit the generator and regenerate all of the modules.

from __future__ import annotations
"""CDP domain: FedCm (experimental)

This domain allows interacting with the FedCM dialog."""
import typing
import enum
from dataclasses import dataclass
from .util import T_JSON_DICT, event_class
None


@dataclass
class Account:
    """Corresponds to IdentityRequestAccount"""
    account_id: str
    email: str
    name: str
    given_name: str
    picture_url: str
    idp_config_url: str
    idp_login_url: str
    login_state: LoginState
    terms_of_service_url: typing.Optional[str] = None
    privacy_policy_url: typing.Optional[str] = None

    def to_json(self) ->T_JSON_DICT:
        json_data: T_JSON_DICT = dict()
        json_data['accountId'] = self.account_id
        json_data['email'] = self.email
        json_data['name'] = self.name
        json_data['givenName'] = self.given_name
        json_data['pictureUrl'] = self.picture_url
        json_data['idpConfigUrl'] = self.idp_config_url
        json_data['idpLoginUrl'] = self.idp_login_url
        json_data['loginState'] = self.login_state.to_json()
        if self.terms_of_service_url is not None:
            json_data['termsOfServiceUrl'] = self.terms_of_service_url
        if self.privacy_policy_url is not None:
            json_data['privacyPolicyUrl'] = self.privacy_policy_url
        return json_data

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->Account:
        return cls(account_id=json_obj['accountId'], email=json_obj['email'
            ], name=json_obj['name'], given_name=json_obj['givenName'],
            picture_url=json_obj['pictureUrl'], idp_config_url=json_obj[
            'idpConfigUrl'], idp_login_url=json_obj['idpLoginUrl'],
            login_state=LoginState.from_json(json_obj['loginState']),
            terms_of_service_url=json_obj['termsOfServiceUrl'] if json_obj.
            get('termsOfServiceUrl') is not None else None,
            privacy_policy_url=json_obj['privacyPolicyUrl'] if json_obj.get
            ('privacyPolicyUrl') is not None else None)


class AccountUrlType(enum.Enum):
    """The URLs that each account has"""
    TERMS_OF_SERVICE = 'TermsOfService'
    PRIVACY_POLICY = 'PrivacyPolicy'

    @classmethod
    def from_json(cls, json: str) ->AccountUrlType:
        return cls(json)

    def to_json(self) ->str:
        return self.value

    def __repr__(self) ->str:
        return '<AccountUrlType.{}>'.format(self.value)


class DialogButton(enum.Enum):
    """The buttons on the FedCM dialog."""
    CONFIRM_IDP_LOGIN_CONTINUE = 'ConfirmIdpLoginContinue'
    ERROR_GOT_IT = 'ErrorGotIt'
    ERROR_MORE_DETAILS = 'ErrorMoreDetails'

    @classmethod
    def from_json(cls, json: str) ->DialogButton:
        return cls(json)

    def to_json(self) ->str:
        return self.value

    def __repr__(self) ->str:
        return '<DialogButton.{}>'.format(self.value)


class DialogType(enum.Enum):
    """The types of FedCM dialogs."""
    ACCOUNT_CHOOSER = 'AccountChooser'
    AUTO_REAUTHN = 'AutoReauthn'
    CONFIRM_IDP_LOGIN = 'ConfirmIdpLogin'
    ERROR = 'Error'

    @classmethod
    def from_json(cls, json: str) ->DialogType:
        return cls(json)

    def to_json(self) ->str:
        return self.value

    def __repr__(self) ->str:
        return '<DialogType.{}>'.format(self.value)


class LoginState(enum.Enum):
    """Whether this is a sign-up or sign-in action for this account, i.e.
whether this account has ever been used to sign in to this RP before."""
    SIGN_IN = 'SignIn'
    SIGN_UP = 'SignUp'

    @classmethod
    def from_json(cls, json: str) ->LoginState:
        return cls(json)

    def to_json(self) ->str:
        return self.value

    def __repr__(self) ->str:
        return '<LoginState.{}>'.format(self.value)


def click_dialog_button(dialog_id: str, dialog_button: DialogButton
    ) ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """:param ...:

:param dialog_id:

:param dialog_button:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['dialogId'] = dialog_id
    params_dict['dialogButton'] = dialog_button.to_json()
    cmd_dict = {'method': 'FedCm.clickDialogButton', 'params': params_dict}
    json_result = yield cmd_dict
    return None


def disable() ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    cmd_dict = {'method': 'FedCm.disable'}
    json_result = yield cmd_dict
    return None


def dismiss_dialog(dialog_id: str, trigger_cooldown: typing.Optional[bool]=None
    ) ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """:param ...:

:param dialog_id:

:param trigger_cooldown: *(Optional)*"""
    params_dict: T_JSON_DICT = dict()
    params_dict['dialogId'] = dialog_id
    if trigger_cooldown is not None:
        params_dict['triggerCooldown'] = trigger_cooldown
    cmd_dict = {'method': 'FedCm.dismissDialog', 'params': params_dict}
    json_result = yield cmd_dict
    return None


def enable(disable_rejection_delay: typing.Optional[bool]=None
    ) ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """:param ...:

:param disable_rejection_delay: *(Optional)* Allows callers to disable the promise rejection delay that would normally happen, if this is unimportant to what's being tested. (step 4 of https://fedidcg.github.io/FedCM/#browser-api-rp-sign-in)"""
    params_dict: T_JSON_DICT = dict()
    if disable_rejection_delay is not None:
        params_dict['disableRejectionDelay'] = disable_rejection_delay
    cmd_dict = {'method': 'FedCm.enable', 'params': params_dict}
    json_result = yield cmd_dict
    return None


def open_url(dialog_id: str, account_index: int, account_url_type:
    AccountUrlType) ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """:param ...:

:param dialog_id:

:param account_index:

:param account_url_type:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['dialogId'] = dialog_id
    params_dict['accountIndex'] = account_index
    params_dict['accountUrlType'] = account_url_type.to_json()
    cmd_dict = {'method': 'FedCm.openUrl', 'params': params_dict}
    json_result = yield cmd_dict
    return None


def reset_cooldown() ->typing.Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """Resets the cooldown time, if any, to allow the next FedCM call to show
a dialog even if one was recently dismissed by the user."""
    cmd_dict = {'method': 'FedCm.resetCooldown'}
    json_result = yield cmd_dict
    return None


def select_account(dialog_id: str, account_index: int) ->typing.Generator[
    T_JSON_DICT, T_JSON_DICT, None]:
    """:param ...:

:param dialog_id:

:param account_index:"""
    params_dict: T_JSON_DICT = dict()
    params_dict['dialogId'] = dialog_id
    params_dict['accountIndex'] = account_index
    cmd_dict = {'method': 'FedCm.selectAccount', 'params': params_dict}
    json_result = yield cmd_dict
    return None


@event_class('FedCm.dialogClosed')
@dataclass
class DialogClosed:
    """Triggered when a dialog is closed, either by user action, JS abort,
or a command below."""
    dialog_id: str

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->DialogClosed:
        return cls(dialog_id=json_obj['dialogId'])


@event_class('FedCm.dialogShown')
@dataclass
class DialogShown:
    dialog_id: str
    dialog_type: DialogType
    accounts: typing.List[Account]
    title: str
    subtitle: typing.Optional[str] = None

    @classmethod
    def from_json(cls, json_obj: T_JSON_DICT) ->DialogShown:
        return cls(dialog_id=json_obj['dialogId'], dialog_type=DialogType.
            from_json(json_obj['dialogType']), accounts=[Account.from_json(
            i) for i in json_obj['accounts']], title=json_obj['title'],
            subtitle=json_obj['subtitle'] if json_obj.get('subtitle') is not
            None else None)
