import abc


class A(abc.ABC):
    """ An ABC and traditional Factory rolled into one """
    _registry = {}

    def __init_subclass__(cls, /, subclass_type: str, **kwargs):
        """
        identical to the registry part of traditional factory,
        EXCEPT it simplifies the process and auto-registers all subclasses, very much inline with DRY
        """
        super().__init_subclass__(**kwargs)
        cls._registry[subclass_type] = cls

    def __new__(cls, subclass_type: str, **kwargs):
        """ essentially a factory """
        return cls._factory(subclass_type=subclass_type)

    @classmethod
    def _factory(cls, subclass_type: str):
        subclass = cls._registry.get(subclass_type)
        obj = object.__new__(subclass)
        obj.subclass_type = subclass_type
        return obj

    @abc.abstractmethod
    def print(self):
        pass
