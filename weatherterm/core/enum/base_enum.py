from enum import Enum

class BaseEnum(Enum):
    def _generate_next_value_(self, start, count, last_value):
        # Overriden so that enums derived from BaseEnum with auto()
        # properties will get same value as property name
        return self