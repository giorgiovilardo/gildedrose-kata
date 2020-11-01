from gildedrose_kata.gildedrose import Item, GildedRose


def instance_gilded_rose(item_list, days_to_pass=1):
    gilded_rose = GildedRose(item_list)
    for i in range(days_to_pass):
        gilded_rose.update_quality()
    return gilded_rose


def test_quality_dont_go_under_zero():
    gr = instance_gilded_rose(
        [Item("foo", 0, 0), Item(name="Conjured Mana Cake", sell_in=3, quality=2)], 2
    )
    assert gr.items[0].quality == 0
    assert gr.items[1].quality == 0


def test_brie_increasing():
    gr = instance_gilded_rose([Item("Aged Brie", 0, 3)], 2)
    assert gr.items[0].quality == 5


def test_quality_dont_go_over_50():
    gr = instance_gilded_rose([Item("Aged Brie", 10, 50)])
    assert gr.items[0].quality == 50


def test_legendary_items_stays_the_same():
    gr = instance_gilded_rose(
        [Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80)], 2
    )
    assert gr.items[0].quality == 80
    assert gr.items[0].sell_in == -3


def test_conjured_items_degrade_at_double_rate():
    gr = instance_gilded_rose([Item(name="Conjured Mana Cake", sell_in=3, quality=6)])
    assert gr.items[0].quality == 4
    assert gr.items[0].sell_in == 2


def test_conjured_late_items_degrade_at_double_double_rate():
    gr = instance_gilded_rose([Item(name="Conjured Mana Cake", sell_in=-1, quality=6)])
    assert gr.items[0].quality == 2
    assert gr.items[0].sell_in == -2


def test_backstage_pass_increase_by_one_before_10_days():
    gr = instance_gilded_rose([Item(name="Backstage passes", sell_in=40, quality=6)])
    assert gr.items[0].quality == 7
    assert gr.items[0].sell_in == 39


def test_backstage_pass_increase_by_two_between_10_and_5_days():
    gr = instance_gilded_rose([Item(name="Backstage passes", sell_in=9, quality=6)])
    assert gr.items[0].quality == 8
    assert gr.items[0].sell_in == 8


def test_backstage_pass_increase_by_three_between_5_and_0_days():
    gr = instance_gilded_rose([Item(name="Backstage passes", sell_in=2, quality=6)])
    assert gr.items[0].quality == 9
    assert gr.items[0].sell_in == 1


def test_backstage_pass_is_0_after_concert():
    gr = instance_gilded_rose([Item(name="Backstage passes", sell_in=-1, quality=6)])
    assert gr.items[0].quality == 0
    assert gr.items[0].sell_in == -2


def test_normal_items_degrades_normally():
    gr = instance_gilded_rose([Item(name="Foo", sell_in=23, quality=4)])
    assert gr.items[0].quality == 3
    assert gr.items[0].sell_in == 22


def test_normal_items_out_of_time_degrades_doubly():
    gr = instance_gilded_rose([Item(name="Foo", sell_in=-23, quality=4)])
    assert gr.items[0].quality == 2
    assert gr.items[0].sell_in == -24


def test_normal_items_out_of_time_degrades_doubly_error_case():
    gr = instance_gilded_rose([Item(name="Foo", sell_in=-23, quality=1)])
    assert gr.items[0].quality == 0
    assert gr.items[0].sell_in == -24
