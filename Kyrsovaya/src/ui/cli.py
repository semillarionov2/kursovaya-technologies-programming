from __future__ import annotations

from data.catalog import get_catalog
from data.receipt_store import ReceiptStore
from domain.cart import Cart
from domain.customer import Customer
from domain.items import WeightedProduct
from services.checkout import CheckoutService, CheckoutError
from services.payment import CashOnlyPayment, BonusOnlyPayment, MixedPayment


class CLI:
    def __init__(self) -> None:
        self.catalog = get_catalog()
        self.cart = Cart()
        self.receipt_store = ReceiptStore("receipts.txt")

        self.customer = Customer(full_name="Покупатель", cash=50000.0, bonus_points=7000.0)
        self.checkout_service = CheckoutService()

    def run(self) -> None:
        while True:
            self._print_header()
            self._print_menu()
            choice = input("Выбери пункт: ").strip()

            try:
                if choice == "1":
                    self._show_catalog_menu()
                elif choice == "2":
                    self._add_to_cart()
                elif choice == "3":
                    self._show_cart()
                elif choice == "4":
                    self._weigh_item()
                elif choice == "5":
                    self._remove_from_cart()
                elif choice == "6":
                    self._pay()
                elif choice == "7":
                    self._show_purchases()
                elif choice == "0":
                    print("Выход.")
                    return
                else:
                    print("Неизвестная команда.")
            except Exception as e:
                print(f"Ошибка: {e}")

            input("\nНажми Enter, чтобы продолжить...")

    # ---------- UI ----------

    def _print_header(self) -> None:
        print("\n==============================")
        print("   ПРОДУКТОВЫЙ МАГАЗИН (консоль)")
        print("==============================")
        print(f"Покупатель: {self.customer.full_name}")
        print(f"Наличные: {self.customer.cash:.2f} ₽ | Бонусы: {self.customer.bonus_points:.2f}")
        print(f"Корзина: {len(self.cart.items)} поз. | Сумма: {self.cart.total():.2f} ₽")
        print("==============================\n")

    def _print_menu(self) -> None:
        print("1 — Каталог")
        print("2 — Добавить в корзину")
        print("3 — Показать корзину")
        print("4 — Взвесить товар в корзине")
        print("5 — Удалить из корзины")
        print("6 — Оплатить")
        print("7 — История покупок")
        print("0 — Выход")

    # ---------- Catalog ----------

    def _show_catalog_menu(self) -> None:
        print("\n--- Каталог ---")
        print("1 — Показать весь каталог")
        print("2 — Поиск по названию")
        choice = input("Выбери: ").strip()

        if choice == "1":
            self._show_catalog(self.catalog)
        elif choice == "2":
            q = input("Введите часть названия: ").strip().lower()
            filtered = [x for x in self.catalog if q in x.name.lower()]
            self._show_catalog(filtered)
        else:
            print("Неизвестный пункт.")

    def _show_catalog(self, items: list) -> None:
        if not items:
            print("Ничего не найдено.")
            return

        idx = 1
        for it in items:
            if isinstance(it, WeightedProduct):
                print(f"{idx}. {it.name} — {it.calc_cost(1):.2f} ₽/кг")
            else:
                print(f"{idx}. {it.name} — {it.calc_cost(1):.2f} ₽/шт")
            idx += 1

    # ---------- Cart actions ----------

    def _add_to_cart(self) -> None:
        print("\n--- Каталог ---")
        for i, item in enumerate(self.catalog, start=1):
            if isinstance(item, WeightedProduct):
                print(f"{i}. {item.name} — {item.calc_cost(1):.2f} ₽/кг")
            else:
                print(f"{i}. {item.name} — {item.calc_cost(1):.2f} ₽/шт")

        idx = int(input("Номер товара: ")) - 1
        if idx < 0 or idx >= len(self.catalog):
            print("Нет такого номера.")
            return

        item = self.catalog[idx]

        if isinstance(item, WeightedProduct):
            w = float(input("Введите вес (кг): "))
            self.cart.add(item, amount=w, is_weighed=True)
        else:
            amt = float(input("Введите количество: "))
            self.cart.add(item, amount=amt)

        print("Добавлено в корзину.")

    def _show_cart(self) -> None:
        print("\n--- Корзина ---")
        if not self.cart.items:
            print("Пусто.")
            return

        for i, ci in enumerate(self.cart.items, start=1):
            extra = ""
            if isinstance(ci.item, WeightedProduct) and not ci.is_weighed:
                extra = " [НЕ ВЗВЕШЕНО]"
            print(f"{i}. {ci.item.name} — {ci.amount} — {ci.cost():.2f} ₽{extra}")

        print(f"Итого: {self.cart.total():.2f} ₽")

    def _weigh_item(self) -> None:
        self._show_cart()
        idx = int(input("Номер позиции: ")) - 1
        w = float(input("Введите вес (кг): "))
        self.cart.weigh_item(idx, w)
        print("Товар взвешен.")

    def _remove_from_cart(self) -> None:
        self._show_cart()
        idx = int(input("Номер позиции: ")) - 1
        self.cart.remove(idx)
        print("Удалено.")

    # ---------- Payment ----------

    def _pay(self) -> None:
        self._show_cart()
        if not self.cart.items:
            return

        if self.cart.has_unweighed_items():
            print("Есть невзвешенные товары.")
            return

        print("\n--- Оплата ---")
        print("1 — Наличные")
        print("2 — Бонусы")
        print("3 — Смешанная")
        choice = input("Выбери: ").strip()

        if choice == "1":
            payment = CashOnlyPayment()
        elif choice == "2":
            payment = BonusOnlyPayment()
        elif choice == "3":
            b = float(input("Сколько бонусов списать? "))
            payment = MixedPayment(b)
        else:
            print("Неверный выбор.")
            return

        try:
            receipt = self.checkout_service.checkout(self.customer, self.cart, payment)
            print("\n" + receipt.text)
            self.receipt_store.save(receipt.text)
            self.cart = Cart()
        except CheckoutError as e:
            print(f"Ошибка оплаты: {e}")

    # ---------- Purchases ----------

    def _show_purchases(self) -> None:
        print("\n--- История покупок ---")
        if not self.customer.purchases:
            print("Пока нет покупок.")
            return

        for i, text in enumerate(self.customer.purchases, start=1):
            print(f"\nПокупка #{i}")
            print(text)
