from relocation_helper import nlu


def test_simple_text():
    assert nlu.preprocess_text(
        "попроси переезд создать коробку из холодильника") == "попросить переезд создавать коробка холодильник"


def test_simple_list():
    assert nlu.preprocess_list("попроси переезд создать коробку из холодильника") == \
           ["попросить", "переезд", "создавать", "коробка", "холодильник"]


def test_simple_set():
    assert len(nlu.preprocess_set("попроси переезд создать коробку из холодильника") & \
               set(["попросить", "переезд", "создавать", "коробка", "холодильник"])) == 5


def test_lexems_transformation():
    print(nlu.preprocess_text("создай новую коробку вещи"))
    print(nlu.preprocess_text("создай коробку посудочка посуда посуды"))
