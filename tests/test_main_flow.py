import allure


@allure.feature("Конструктор и Ингредиенты")
@allure.story("Проверка основной функциональности")
class TestMainFlow:
    @allure.title("Переход по клику на «Конструктор»")
    def test_navigate_to_constructor(self, main_page):
        main_page.go_to_feed()
        main_page.go_to_constructor()
        assert main_page.is_constructor_visible()

    @allure.title("При клике на ингредиент открывается окно с деталями")
    def test_ingredient_modal_opens(self, main_page, ingredient_modal):
        main_page.click_ingredient_card(index=0)
        assert ingredient_modal.is_modal_open()

    @allure.title("Окно ингредиента закрывается кликом по крестику")
    def test_modal_closes_on_click(self, main_page, ingredient_modal):
        main_page.click_ingredient_card(index=0)
        assert ingredient_modal.is_modal_open()
        ingredient_modal.close_modal()
        assert ingredient_modal.wait_for_modal_to_close()

    @allure.title("При добавлении ингредиента счётчик на карточке увеличивается")
    def test_ingredient_counter_increases(self, main_page):
        initial_count = main_page.get_ingredient_counter_value(index=0)
        main_page.add_ingredient_via_drag_and_drop(index=0)
        new_count = main_page.wait_for_ingredient_counter_increase(initial_count, index=0)
        assert new_count > initial_count
