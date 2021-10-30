from factory_separate import factory_separate_a


class B(factory_separate_a.A, subclass_type='b'):
    def print(self):
        print(self.subclass_type)
