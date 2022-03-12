""""Abstract classes for model of timetable and concrete classes for route and equipment"""
from abc import abstractmethod
from datetime import datetime
from typing import Optional


class Equipment:
    """"encapsulates equipment for routes (bus,tramway or trolleybus)"""

    def __init__(self, type_equipment: int):
        """"Constructor of equipment by int (0 - bus, 1 - tramway, 2 - trolleybus) """
        self.number = type_equipment

    def to_number(self) -> int:
        """Return number by type: 0 - bus, 1 - tramway, 2 - trolleybus"""
        return self.number

    @staticmethod
    def bus() -> 'Equipment':
        """"return Equipment object for bus"""
        return Equipment(0)

    @staticmethod
    def tramway() -> 'Equipment':
        """"return Equipment object for tramway"""
        return Equipment(1)

    @staticmethod
    def trolleybus() -> 'Equipment':
        """"return Equipment object for trolleybus"""
        return Equipment(2)

    def to_str(self) -> str:
        """"return english word for type of equipment"""
        if self.to_number() == 0:
            return "bus"
        if self.to_number() == 1:
            return "tramway"
        if self.to_number() == 2:
            return "trolleybus"

    @classmethod
    def by_number(cls, num: int) -> 'Equipment':
        """"Return Equipment object by int (0 - bus, 1 - tramway, 2 - trolleybus)
        """
        if num == 0:
            return cls.bus()
        if num == 1:
            return cls.tramway()
        if num == 2:
            return cls.trolleybus()

    def __eq__(self, other):
        """"Equipment is equal if it has same type (bus, tramway, trolleybus)"""
        return self.to_number() == (other.to_number())

    def __ne__(self, other):
        """"Equipment is not equal if it hasn't same type (bus, tramway, trolleybus)"""
        return not (self == other)

    def __hash__(self):
        """"Equipment hash is calculating by int for equipment (0 - bus, 1 - tramway, 2 - trolleybus)"""
        return hash(self.to_number())


class Route:
    """"encapsulates routes"""

    def __init__(self, id_mgt: str, equipment: Equipment, name: str):
        """"Construct Route object by
        :param id_mgt id route on t.mos.ru
        :param equipment type of route (Equipment.bus(), Equipment.tramway() or Equipment.trolleybus())
        :param name name of route
        """
        self.name = name
        self.equipment = equipment
        self.id_mgt = id_mgt

    def get_id_mgt(self) -> str:
        """"return id on t.mos.ru"""
        return self.id_mgt

    def get_equipment(self) -> Equipment:
        """"return type of Equipment"""
        return self.equipment

    def get_name(self) -> str:
        """"return name of route"""
        return self.name

    def __eq__(self, other):
        """"Routes is equal if they have same id, type of equipment and name"""
        return str(self.get_id_mgt()) == str(other.get_id_mgt()) and \
               self.get_equipment() == other.get_equipment() and \
               self.get_name() == other.get_name()
        # str() for old int type of field and changing format on t.mos.ru

    def __ne__(self, other):
        """"Routes is not equal if they haven't same id, type of equipment and name"""
        return not (self == other)

    def __hash__(self):
        """"Hash generated by id on t.mos.ru, type of equipment and name of route"""
        return hash((self.get_id_mgt(), self.get_equipment(), self.get_name()))

    def __str__(self):
        """"String representation"""
        return "{} ({}, id={})".format(self.get_name(), self.get_equipment().to_str(), self.get_id_mgt())

    def __repr__(self):
        """"String representation"""
        return str(self)


class Stop:
    """"Stop of transport (abstract)"""

    @abstractmethod
    def get_name(self) -> str:
        """"return name of stop"""
        pass

    @abstractmethod
    def get_coords(self) -> (float, float):
        """"return GPS coordinates of stop"""
        pass


class Stop_builder:
    """"Builder for stop"""

    @abstractmethod
    def set_name(self, name: str) -> 'Stop_builder':
        """Set name of stop
        :param name of stop
        """
        pass

    @abstractmethod
    def set_coords(self, coords: (float,float)) -> 'Stop_builder':
        """"Set GPS-coordinate of stop
        :param coords GPS-coordinate
        """
        pass

    @abstractmethod
    def build(self) -> Stop:
        """Build of Stop"""
        pass


class Timetable_stop:
    """"Timetable for stop for route"""

    def get_name(self) -> str:
        """"Return name of route """
        return self.get_stop().get_name()

    def get_coords(self) -> (float, float):
        """"Return coords of stop"""
        return self.get_stop().get_coords()

    @abstractmethod
    def get_times(self) -> iter:
        """"Return iterator for times of equipment being on stop"""
        pass

    @abstractmethod
    def get_stop(self) -> Stop:
        """"Return stop"""
        pass


class Timetable:
    """"Timetable of route"""

    @abstractmethod
    def __iter__(self):
        """Iterator for stops (with timetables on stop)"""
        pass

    @abstractmethod
    def get_direction(self) -> int:
        """"Return direction (0 - direct, 1 - opposite)"""
        pass

    @abstractmethod
    def get_id_route_t_mos_ru(self) -> str:
        """"Return id of route on t.mos.ru"""
        pass

    @abstractmethod
    def get_date(self) -> datetime.date:
        """"Return date of timetable"""
        pass

    @abstractmethod
    def get_stops(self) -> list[Timetable_stop]:
        """"Return timetables of stops"""
        pass


class Timetable_stop_time:
    """"Builder for timetable for stop on route"""
    @abstractmethod
    def get_time(self) -> datetime.time:
        """"Return time of arriving of equipment"""
        pass

    @abstractmethod
    def get_color_special_flight(self) -> Optional[str]:
        """"Return color of special race"""
        pass


class Timetable_stop_builder:
    """"Builder for timetable for stop"""

    @abstractmethod
    def add_item_timetable(self, time_flight: datetime.time,
                           special_flight: Optional[str] = None) -> 'Timetable_stop_builder':
        """"Adding time and color for special race
        :param time_flight time of arriving of equipment
        :param special_flight optional color of special races
        """
        pass

    @abstractmethod
    def build(self) -> Timetable_stop:
        """"Build of timetable for stop"""
        pass

    @abstractmethod
    def set_name(self, name: str) -> 'Timetable_stop_builder':
        """"Set name of stop
        :param name of stop
        """
        pass

    @abstractmethod
    def set_coords(self, coords: (float, float)) -> 'Timetable_stop_builder':
        """"Set GPS coordinates for stop"""
        pass


class Timetable_builder:
    """"Builder for timetable"""
    @abstractmethod
    def add_stop(self) -> Timetable_stop_builder:
        """"Add stop to timetable, return stop builder"""
        pass

    @abstractmethod
    def build(self) -> Timetable:
        """"Build timetable"""
        pass

    @abstractmethod
    def set_id_route_t_mos_ru(self, id_route_t_mos_ru: str) -> 'Timetable_builder':
        """"Set id from t.mos.ru for route
        :param id_route_t_mos_ru id from t.mos.ru
        """
        pass

    @abstractmethod
    def set_direction(self, direction: int) -> 'Timetable_builder':
        """"Set direction
        :param direction 0 - direct, 1 - opposite
        """
        pass

    @abstractmethod
    def set_date(self, date: datetime.date) -> 'Timetable_builder':
        """"Set date for timetable
        :param date for timetable
        """
        pass