class BaseModel:
    def get_fields(self):
        fields = dict()
        field_names = [name for name in self.__dict__.keys()
                       if not name.startswith('_') or
                          not name.startswith('__')]
        for name in field_names:
            value = getattr(self, name)
            fields[name] = value
        return fields

    def set_fields(self, **kwargs):
        for name, value in kwargs.items():
            if name in self.__dict__.keys():
                setattr(self, name, value)
            else:
                raise AttributeError


