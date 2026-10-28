from urllib.parse import urlparse
import allure

@allure.step("Оформление заказа и получение его номера")
def create_order(page, modal):
    page.go_to_constructor()
    initial_count = page.get_ingredient_counter_value(index=0)
    page.add_ingredient_via_drag_and_drop(index=0)
    page.wait_for_ingredient_counter_increase(initial_count, index=0)
    page.click_order_button()
    number = modal.get_order_number()
    modal.close_modal()
    modal.wait_for_modal_to_close()
    return number


@allure.feature("Лента заказов и глобальные счетчики")
@allure.story("Проверка заказов")
class TestOrderFeed:
    @allure.title("Переход в раздел «Лента заказов»")
    def test_navigate_to_feed(self, main_page):
        main_page.go_to_feed()
        assert urlparse(main_page.get_current_url()).path == "/feed"

    @allure.title("Счётчик «Выполнено за всё время» увеличивается при оформлении заказа")
    def test_counter_all_time_increases(self, logged_in_main_page, ingredient_modal):
        page = logged_in_main_page
        page.go_to_feed()
        initial_all, _ = page.get_counters()
        create_order(page, ingredient_modal)
        page.go_to_feed()
        new_all = page.wait_for_all_time_counter_increase(initial_all)
        assert new_all > initial_all

    @allure.title("Счётчик «Выполнено за сегодня» увеличивается при оформлении заказа")
    def test_counter_today_increases(self, logged_in_main_page, ingredient_modal):
        page = logged_in_main_page
        page.go_to_feed()
        _, initial_today = page.get_counters()
        initial_today = int(initial_today)
        create_order(page, ingredient_modal)
        page.go_to_feed()
        new_today = page.wait_for_today_counter_increase(initial_today)
        assert new_today > initial_today

    @allure.title("Номер созданного заказа появляется в разделе «В работе»")
    def test_order_appears_in_work_section(
        self, logged_in_main_page, order_feed_page, ingredient_modal
    ):
        number = create_order(logged_in_main_page, ingredient_modal)
        logged_in_main_page.go_to_feed()
        assert order_feed_page.check_order_exists_in_feed(number), (
            f"Заказ {number} не найден в разделе «В работе»"
        )
