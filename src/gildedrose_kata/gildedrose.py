from typing import List


class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return f"{self.name}, {self.sell_in}, {self.quality}"


class GildedRose:
    # SRP Violato: GildedRose deve sia categorizzare gli oggetti, sia
    # modificarne la qualità (il tipo di oggetto starebbe meglio negli Item)
    #
    def __init__(self, items: List[Item]):
        self.items = items

    def update_quality(self):
        for item in self.items:
            self._determine_quality_func(item)(item)  # noqa
            item.sell_in -= 1

    def _legendary(self, item: Item):
        pass

    def _aged_brie(self, item: Item):  # noqa
        item.quality = item.quality + 1 if item.quality <= 49 else 50

    def _conjured(self, item: Item):  # noqa
        quantity_drop = 2 if item.sell_in > 0 else 4
        item.quality = (
            item.quality - quantity_drop if item.quality >= quantity_drop else 0
        )

    def _backstage(self, item: Item):  # noqa
        if item.sell_in > 10:
            item.quality += 1
        elif 5 < item.sell_in <= 10:
            item.quality += 2
        elif 0 <= item.sell_in <= 5:
            item.quality += 3
        else:
            item.quality = 0

    def _normal(self, item: Item):  # noqa
        quantity_drop = 1 if item.sell_in > 0 else 2
        item.quality = (
            item.quality - quantity_drop if item.quality >= quantity_drop else 0
        )

    def _determine_quality_func(self, item: Item):
        special_item_funcs = {
            "Sulfuras": self._legendary,
            "Aged Brie": self._aged_brie,
            "Conjured": self._conjured,
            "Backstage": self._backstage,
        }
        for key in special_item_funcs.keys():
            if key in item.name:
                return special_item_funcs[key]
        return self._normal
