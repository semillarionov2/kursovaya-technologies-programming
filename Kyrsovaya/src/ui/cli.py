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

        # Деньги/бонусы можешь менять под задачу
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
        print("   МАГАЗИН ТЕХНИКИ (консоль)")
        print("==============================")
        print(f"Покупатель: {self.customer.full_name}")
        print(f"Наличные: {self.customer.cash:.2f} ₽ | Бонусы: {self.customer.bonus_points:.2f}")
        print(f"Корзина: {len(self.cart.items)} поз. | Сумма: {self.cart.total():.2f} ₽")
        print("==============================\n")

    def _print_menu(self) -> None:
        print("1 — Каталог (просмотр/поиск)")
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
            q = input("Введите часть названия (например 'ноут'): ").strip().lower()
            filtered = [x for x in self.catalog if q in x.name.lower()]
            self._show_catalog(filtered)
        else:
            print("Неизвестный пункт.")

    def _category_of(self, name: str) -> str:
        n = name.lower()
        if "ноут" in n:
            return "Ноутбуки"
        if "смартф" in n or "телефон" in n:
            return "Смартфоны"
        if "монитор" in n:
            return "Мониторы"
        if "мыш" in n or "клав" in n:
            return "Периферия"
        if "науш" in n:
            return "Аудио"
        if "достав" in n or "настрой" in n or "гарант" in n:
            return "Услуги"
        if "кабель" in n or "термопаст" in n:
            return "Расходники"
        return "Другое"

    def _show_catalog(self, items: list) -> None:
        if not items:
            print("Ничего не найдено.")
            return

        # группировка по категориям
        groups: dict[str, list] = {}
        for it in items:
            cat = self._category_of(it.name)
            groups.setdefault(cat, []).append(it)

        idx = 1
        for cat in sorted(groups.keys()):
            print(f"\n[{cat}]")
            for it in groups[cat]:
                if isinstance(it, WeightedProduct):
                    print(f"{idx}. {it.name} — {it.price_per_kg:.2f} ₽/кг")
                else:
                    print(f"{idx}. {it.name} — {it.calc_cost(1):.2f} ₽/ед.")
                idx += 1

        print("\n(Нумерация соответствует общему каталогу в пункте 'Добавить в корзину')")

    # ---------- Cart actions ----------

    def _add_to_cart(self) -> None:
        # показываем общий каталог с номерами
        print("\n--- Общий каталог ---")
        for i, item in enumerate(self.catalog, start=1):
            if isinstance(item, WeightedProduct):
                print(f"{i}. {item.name} — {item.price_per_kg:.2f} ₽/кг")
            else:
                print(f"{i}. {item.name} — {item.calc_cost(1):.2f} ₽/ед.")
        print("---------------------")

        idx = int(input("Номер товара/услуги: ")) - 1
        if idx < 0 or idx >= len(self.catalog):
            print("Нет такого номера.")
            return

        item = self.catalog[idx]

        if isinstance(item, WeightedProduct):
            print("Это взвешиваемый товар.")
            choice = input("Добавить сразу с весом? (y/n): ").strip().lower()
            if choice == "y":
                w = float(input("Вес (кг): "))
                self.cart.add(item, amount=w, is_weighed=True)
            else:
                # добавляем как НЕ ВЗВЕШЕНО, вес заглушка
                self.cart.add(item, amount=0.1, is_weighed=False)
        else:
            amt = float(input("Количество (например 1): "))
            self.cart.add(item, amount=amt)

        print("Добавлено в корзину.")

    def _show_cart(self) -> None:
        print("\n--- Корзина ---")
        if len(self.cart.items) == 0:
            print("Пусто.")
            return

        for i, ci in enumerate(self.cart.items, start=1):
            extra = ""
            if isinstance(ci.item, WeightedProduct) and not ci.is_weighed:
                extra = " [НЕ ВЗВЕШЕНО]"
            print(f"{i}. {ci.item.name} — amount={ci.amount} — {ci.cost():.2f} ₽{extra}")

        print(f"Итого: {self.cart.total():.2f} ₽")
        print("--------------")

    def _weigh_item(self) -> None:
        self._show_cart()
        if len(self.cart.items) == 0:
            return

        idx = int(input("Номер позиции для взвешивания: ")) - 1
        w = float(input("Введите вес (кг): "))
        self.cart.weigh_item(idx, w)
        print("Товар взвешен.")

    def _remove_from_cart(self) -> None:
        self._show_cart()
        if len(self.cart.items) == 0:
            return
        idx = int(input("Номер позиции для удаления: ")) - 1
        self.cart.remove(idx)
        print("Удалено.")

    # ---------- Payment (with required scenario) ----------

    def _pay(self) -> None:
        self._show_cart()
        if len(self.cart.items) == 0:
            return

        # 1) Если есть НЕ ВЗВЕШЕНО — предложим взвесить сразу
        if self.cart.has_unweighed_items():
            print("\nЕсть товары, которые НЕ ВЗВЕШЕНЫ. Нужно взвесить перед оплатой.")
            while self.cart.has_unweighed_items():
                self._show_cart()
                idx = int(input("Номер позиции, которую взвесить (0 — отмена оплаты): ")) - 1
                if idx == -1:
                    return
                w = float(input("Введите вес (кг): "))
                try:
                    self.cart.weigh_item(idx, w)
                except Exception as e:
                    print(f"Ошибка: {e}")

        # выбор способа оплаты
        print("\n--- Оплата ---")
        print("1 — Только наличными")
        print("2 — Только бонусами")
        print("3 — Смешанная (бонусы + наличные)")
        choice = input("Выбери: ").strip()

        if choice == "1":
            payment = CashOnlyPayment()
        elif choice == "2":
            payment = BonusOnlyPayment()
        elif choice == "3":
            b = float(input("Сколько бонусов списать? "))
            payment = MixedPayment(bonus_to_use=b)
        else:
            print("Неизвестный вариант оплаты.")
            return

        # 2) Сценарий "не хватает денег" -> удаляй из корзины пока не хватит
        while True:
            try:
                receipt = self.checkout_service.checkout(self.customer, self.cart, payment)
                print("\n" + receipt.text)

                # 3) Сохраняем чек в файл
                self.receipt_store.save(receipt.text)
                print("\nЧек сохранён в файл: receipts.txt")

                # очищаем корзину
                self.cart = Cart()
                return

            except CheckoutError as e:
                msg = str(e)
                print(f"\nОплата не прошла: {msg}")

                if "Недостаточно" in msg:
                    print("\nНе хватает средств. Удаляйте товары из корзины, пока сумма не станет меньше.")
                    self._show_cart()
                    idx = int(input("Номер позиции для удаления (0 — отмена оплаты): ")) - 1
                    if idx == -1:
                        return
                    try:
                        self.cart.remove(idx)
                    except Exception as ex:
                        print(f"Ошибка удаления: {ex}")
                else:
                    # другие ошибки (например, пустая корзина)
                    return

    # ---------- Purchases ----------

    def _show_purchases(self) -> None:
        print("\n--- История покупок (в памяти) ---")
        if not self.customer.purchases:
            print("Пока нет покупок.")
            return

        for i, text in enumerate(self.customer.purchases, start=1):
            print(f"\nПокупка #{i}")
            print(text)
