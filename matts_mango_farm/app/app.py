from datetime import timedelta
from functools import reduce
from enum import Enum


class LETTER_GRADE(Enum):
    A = 1
    B = 2
    C = 3


LETTER_GRADES_SET = {LETTER_GRADE.A, LETTER_GRADE.B, LETTER_GRADE.C}


def map_letter_grade_to_number(letter):
    if letter not in LETTER_GRADES_SET:
        raise ValueError(f"letter grade must be in set: {LETTER_GRADES_SET}")

    if letter == LETTER_GRADE.A:
        return 95
    if letter == LETTER_GRADE.B:
        return 85
    if letter == LETTER_GRADE.C:
        return 75


def map_number_grade_to_letter(number):
    if number >= 90:
        return LETTER_GRADE.A
    if number >= 80 and number < 90:
        return LETTER_GRADE.B
    if number < 80:
        return LETTER_GRADE.C


def calculate_average_grade(items):
    number_grades = [map_letter_grade_to_number(item.grade) for item in items]
    return map_number_grade_to_letter(sum(number_grades) / len(items))


class Mango(object):
    LIFE_SPAN_DAYS = 11

    def calculate_life_span_at_time(self, to_day):
        expiration_date = self.date_picked + timedelta(days=self.LIFE_SPAN_DAYS)
        return (expiration_date - to_day).days

    def __init__(self, _id, weight_grams, date_picked, grade) -> None:
        self.id = _id
        self.weight_grams = weight_grams
        self.date_picked = date_picked
        self.grade = grade


class MangoCrate(object):
    CRATE_SIZE_SM_SQUARE_CM = 3000
    CRATE_SIZE_MD_SQUARE_CM = 5000
    CRATE_SIZE_LG_SQUARE_CM = 7000

    @classmethod
    def _map_size_name_to_cm(cls, size):
        if size == "small":
            return cls.CRATE_SIZE_SM_SQUARE_CM
        elif size == "medium":
            return cls.CRATE_SIZE_MD_SQUARE_CM
        else:
            return cls.CRATE_SIZE_LG_SQUARE_CM

    @classmethod
    def _calculate_grade(cls, mangos):
        return calculate_average_grade(mangos)

    @classmethod
    def _calculate_weight(cls, mangos):
        return (
            reduce(
                lambda current_sum, current_mango: current_sum
                + current_mango.weight_grams,
                mangos,
                0,
            )
            / 1000
        )

    def __init__(self, _id, size, date_packed, mangos) -> None:
        self.id = _id
        self.size_cm = self._map_size_name_to_cm(size)
        self.date_packed = date_packed
        self.mangos = mangos
        self.weight_kg = self._calculate_weight(mangos)
        self.grade = self._calculate_grade(mangos)


class Customer(object):
    def __init__(self, _id, name, address, email) -> None:
        self.id = _id
        self.name = name
        self.address = address
        self.email = email


class Order(object):
    def __init__(
        self, date_placed, date_fulfilled, unit_quantity, unit_price, customer_id
    ) -> None:
        self.date_placed = date_placed
        self.date_fulfilled = date_fulfilled
        self.unit_quantity = unit_quantity
        self.unit_price = unit_price
        self.customer_id = customer_id


class MangoCrateOrder(Order):
    @classmethod
    def _calculate_grade(cls, mango_crates):
        return calculate_average_grade(mango_crates)

    def __init__(
        self, _id, date_placed, date_fulfilled, crate_price, customer_id, mango_crates
    ) -> None:
        super().__init__(
            date_placed, date_fulfilled, len(mango_crates), crate_price, customer_id
        )
        self.id = _id
        self.mango_crates = mango_crates
        self.grade = self._calculate_grade(mango_crates)
