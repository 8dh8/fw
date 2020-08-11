import sys
import yaml


LOCATIONS = []
DEFAULT_DATE_TIME_ORDER = ['year', 'month', 'day', 'hour', 'minute', 'second']
EVAL_INDICATOR = 'ev:'
CSV_SEP = ','
CASE_SENSITIVE = False
SETTING_PREFIX = '-'

_setting_types = {'LOCATIONS': list,
                 'DEFAULT_DATE_TIME_ORDER': list,
                 'EVAL_INDICATOR': str,
                 'CSV_SEP': str,
                 'CASE_SENSITIVE': bool,
                 'SETTING_PREFIX': str}


def _load_settings_from_yaml(file):
    config_dict = {}
    if file:
        with open(file, 'r') as stream:
            try:
                config_dict = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise AssertionError('The settings file could not be parsed correctly. '
                                     'The following errors occurred:\n{}'.format(exc))
    return config_dict


def _validate_settings(settings):
    yaml_settings = _load_settings_from_yaml(settings.get('config_file'))
    yaml_settings.update(settings)
    settings = {k: v for k, v in yaml_settings.items() if k.upper() == k}
    for key, typ in _setting_types.items():
        if key in settings.keys():
            assert isinstance(settings.get(key), typ), 'Parameter is not in correct type (should be {}, found was: {}' \
                                                       ')'.format(typ, settings.get(key).__class__)
    if 'LOCATIONS' in settings.keys():
        assert isinstance(settings.get('LOCATIONS'), list), 'Parameter LOCATIONS was not a valid parameter.'
    return settings


def update_settings(**settings):
    settings = _validate_settings(settings)
    thismodule = sys.modules[__name__]
    for setting, value in settings.items():
        setattr(thismodule, setting, value)
