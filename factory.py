import json
from abc import ABC, abstractmethod
from typing import Union


class Feature(ABC):
    """ An ABC and traditional Factory rolled into one """
    _registry = {}

    def __init_subclass__(cls, feature_type: str, **kwargs):
        """
        identical to the registry part of traditional factory,
        EXCEPT it simplifies the process and auto-registers all subclasses, very much in line with DRY
        """
        super().__init_subclass__(**kwargs)
        cls._registry[feature_type] = cls

    def __new__(cls, config: Union[str, dict] = None, **kwargs):
        """ essentially a factory """
        # processing config, either path to json file, or dict, or in kwargs
        if config and isinstance(config, str):
            with open(config, 'r') as f:
                config = json.load(f)
        config = config or kwargs

        # get feature_type and select subclass
        feature_type = config.get('feature_type')
        subclass = cls._registry.get(feature_type)
        if not subclass:
            raise NotImplementedError(f'subclass of {feature_type=} is not implemented')

        # create subclass obj
        obj = object.__new__(subclass)

        # modify subclass obj
        # the following could be moved to __init__
        # however, since config is already processed here, DRY is violated if the processing is repeated in __init__
        # note: if __init__ is defined, the same arguments will be passed into __init__ after __new__ is called
        obj.config = config
        return obj

    @abstractmethod
    def print(self):
        pass


class FeatureA(Feature, feature_type='A'):
    def print(self):
        print('A')
        print(self.config)


class FeatureB(Feature, feature_type='B'):
    def print(self):
        print('B')
        print(self.config)


if __name__ == '__main__':
    Feature(feature_type='A', some_other_config='hello world A').print()
    Feature(feature_type='B', some_other_config='hello world B').print()
