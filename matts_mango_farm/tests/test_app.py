from datetime import datetime, timedelta
import pytest

from matts_mango_farm.app.app import (
    LETTER_GRADE,
    Customer,
    Mango,
    MangoCrate,
    MangoCrateOrder,
)


def test_mango_gets_created():
    now = datetime.now()
    mango = Mango(_id="abc", weight_grams=300, date_picked=now, grade=LETTER_GRADE.A)
    assert mango.id == "abc"
    assert mango.weight_grams == 300
    assert isinstance(mango.date_picked, datetime)
    assert mango.grade == LETTER_GRADE.A


def test_mango_life_span_calculation():
    now = datetime.now()
    d = now - timedelta(days=3)
    mango = Mango(_id="abc", weight_grams=300, date_picked=d, grade=LETTER_GRADE.A)
    assert mango.calculate_life_span_at_time(to_day=now) == 8


def test_mango_crate_gets_created():
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    mangos = [
        Mango(_id="abc", weight_grams=325, date_picked=yesterday, grade=LETTER_GRADE.A),
        Mango(_id="def", weight_grams=350, date_picked=yesterday, grade=LETTER_GRADE.B),
        Mango(_id="ghi", weight_grams=325, date_picked=yesterday, grade=LETTER_GRADE.C),
    ]
    mango_crate = MangoCrate(_id="-a12", size="small", date_packed=now, mangos=mangos)
    assert mango_crate.id == "-a12"
    assert mango_crate.size_cm == mango_crate.CRATE_SIZE_SM_SQUARE_CM
    assert mango_crate.weight_kg == 1
    assert mango_crate.grade == LETTER_GRADE.B


# This test should NOT exist in its current form please fix
# You should be prevented at mango __init__ from creating a mango with an invalid grade
def test_mango_crate_creation_throws_exception_if_not_given_real_grade():
    with pytest.raises(ValueError):
        MangoCrate(
            _id="-a12",
            size="small",
            date_packed=datetime.now(),
            mangos=[
                Mango(
                    _id="abc", weight_grams=300, date_picked=datetime.now(), grade="D"
                )
            ],
        )

def test_mango_crate_order_gets_created():
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    last_week = now - timedelta(weeks=1)

    customer = Customer(
        _id=":123",
        name="William Grocery Inc.",
        address="555 Friendly Grocer Rd, Austin, TX, 78758",
        email="mickey@willgrocer.com",
    )

    mangos_a = [
        Mango(_id="abc", weight_grams=325, date_picked=yesterday, grade=LETTER_GRADE.A),
        Mango(_id="def", weight_grams=390, date_picked=yesterday, grade=LETTER_GRADE.B),
        Mango(_id="ghi", weight_grams=320, date_picked=yesterday, grade=LETTER_GRADE.A),
    ]
    mangos_b = [
        Mango(_id="jkl", weight_grams=420, date_picked=yesterday, grade=LETTER_GRADE.B),
        Mango(_id="mno", weight_grams=355, date_picked=yesterday, grade=LETTER_GRADE.C),
        Mango(_id="pqr", weight_grams=320, date_picked=yesterday, grade=LETTER_GRADE.C),
        Mango(_id="apq", weight_grams=320, date_picked=yesterday, grade=LETTER_GRADE.C),
    ]
    mangos_c = [
        Mango(_id="stu", weight_grams=425, date_picked=yesterday, grade=LETTER_GRADE.A),
        Mango(_id="vwx", weight_grams=450, date_picked=yesterday, grade=LETTER_GRADE.B),
        Mango(_id="yzz", weight_grams=325, date_picked=yesterday, grade=LETTER_GRADE.C),
        Mango(_id="zab", weight_grams=450, date_picked=yesterday, grade=LETTER_GRADE.B),
        Mango(_id="zcd", weight_grams=400, date_picked=yesterday, grade=LETTER_GRADE.C),
        Mango(_id="zef", weight_grams=410, date_picked=yesterday, grade=LETTER_GRADE.A),
    ]
    mango_crate_a = MangoCrate(
        _id="-a12", size="small", date_packed=now, mangos=mangos_a
    )
    mango_crate_b = MangoCrate(
        _id="-a12", size="medium", date_packed=now, mangos=mangos_b
    )
    mango_crate_c = MangoCrate(
        _id="-a12", size="large", date_packed=now, mangos=mangos_c
    )

    mango_crates = [mango_crate_a, mango_crate_b, mango_crate_c]

    mango_crate_order = MangoCrateOrder(
        _id="_ABC",
        date_placed=last_week,
        date_fulfilled=now,
        crate_price=10,
        customer_id=customer.id,
        mango_crates=mango_crates,
    )

    assert mango_crate_order.id == "_ABC"
