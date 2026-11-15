from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

Window.clearcolor = (0.09, 0.11, 0.15, 1)


class TradeProApp(App):

    def build(self):
        self.total_profit = 0.0
        self.goal = 1000.0
        self.last_profit = 0.0

        main_layout = BoxLayout(orientation='vertical', padding=30, spacing=18)

        title = Label(
            text='[b]TRADE PRO[/b]',
            markup=True,
            font_size='28sp',
            size_hint=(1, 0.12),
            color=(1, 0.78, 0.15, 1),
        )
        main_layout.add_widget(title)

        self.goal_label = Label(
            text=f'Копилка: 0.00 G  |  Цель: {self.goal:.0f} G',
            font_size='16sp',
            size_hint=(1, 0.08),
            color=(0.65, 0.85, 1, 1),
        )
        main_layout.add_widget(self.goal_label)

        self.buy_input = TextInput(
            hint_text='Цена покупки за 1 шт (G)',
            multiline=False,
            input_filter='float',
            font_size='18sp',
            size_hint=(1, 0.11),
            background_color=(0.16, 0.19, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.55, 0.58, 0.65, 1),
        )
        main_layout.add_widget(self.buy_input)

        self.sell_input = TextInput(
            hint_text='Цена продажи / Рыночная цена (G)',
            multiline=False,
            input_filter='float',
            font_size='18sp',
            size_hint=(1, 0.11),
            background_color=(0.16, 0.19, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.55, 0.58, 0.65, 1),
        )
        main_layout.add_widget(self.sell_input)

        self.qty_input = TextInput(
            text='1',
            hint_text='Количество штук',
            multiline=False,
            input_filter='int',
            font_size='18sp',
            size_hint=(1, 0.11),
            background_color=(0.16, 0.19, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
        )
        main_layout.add_widget(self.qty_input)

        btn_calc = Button(
            text='ПОСЧИТАТЬ ПРОФИТ (-20%)',
            font_size='16sp',
            bold=True,
            size_hint=(1, 0.12),
            background_color=(0.14, 0.65, 0.35, 1),
            background_normal='',
        )
        btn_calc.bind(on_press=self.calculate_trade)
        main_layout.add_widget(btn_calc)

        btn_order = Button(
            text='КАКОЙ ЗАПРОС ПОСТАВИТЬ? (+15%)',
            font_size='15sp',
            bold=True,
            size_hint=(1, 0.12),
            background_color=(0.2, 0.45, 0.85, 1),
            background_normal='',
        )
        btn_order.bind(on_press=self.calculate_order)
        main_layout.add_widget(btn_order)

        self.result_label = Label(
            text='Введи цены и нажми кнопку расчета',
            font_size='17sp',
            halign='center',
            size_hint=(1, 0.22),
            color=(0.9, 0.92, 0.95, 1),
        )
        main_layout.add_widget(self.result_label)

        bottom_box = BoxLayout(
            orientation='horizontal', spacing=12, size_hint=(1, 0.11)
        )

        btn_save = Button(
            text='+ В КОПИЛКУ',
            bold=True,
            background_color=(0.88, 0.55, 0.1, 1),
            background_normal='',
        )
        btn_save.bind(on_press=self.add_to_goal)

        btn_clear = Button(
            text='ОЧИСТИТЬ',
            bold=True,
            background_color=(0.75, 0.25, 0.25, 1),
            background_normal='',
        )
        btn_clear.bind(on_press=self.clear_fields)

        bottom_box.add_widget(btn_save)
        bottom_box.add_widget(btn_clear)
        main_layout.add_widget(bottom_box)

        return main_layout

    def calculate_trade(self, instance):
        try:
            buy = float(self.buy_input.text)
            qty = int(self.qty_input.text) if self.qty_input.text else 1
            min_sell = buy / 0.8

            if not self.sell_input.text:
                self.result_label.text = (
                    f'Выход в ноль от: {min_sell:.2f} G (за 1 шт)'
                )
                self.result_label.color = (1, 0.85, 0.3, 1)
                self.last_profit = 0.0
                return

            sell = float(self.sell_input.text)
            profit_one = (sell * 0.8) - buy
            total = profit_one * qty
            self.last_profit = total

            if total > 0:
                self.result_label.text = (
                    f'ЧИСТЫЙ ПЛЮС: +{total:.2f} G\n'
                    f'({profit_one:.2f} G за шт | Ноль от {min_sell:.2f} G)'
                )
                self.result_label.color = (0.3, 1, 0.45, 1)
            elif total < 0:
                self.result_label.text = (
                    f'МИНУС: {total:.2f} G\n'
                    f'Чтобы выйти в ноль, ставь {min_sell:.2f} G'
                )
                self.result_label.color = (1, 0.35, 0.35, 1)
            else:
                self.result_label.text = 'РОВНО В НОЛЬ (0.00 G)'
                self.result_label.color = (1, 1, 1, 1)
        except ValueError:
            self.result_label.text = 'Введи цену покупки в первое поле!'
            self.result_label.color = (1, 0.4, 0.4, 1)

    def calculate_order(self, instance):
        try:
            market_price = float(self.sell_input.text)
            net_after_fee = market_price * 0.8
            recommended_order = net_after_fee / 1.15
            self.result_label.text = (
                f'Ставь запрос: {recommended_order:.2f} G\n'
                f'(Чистый плюс будет ~15%)\n'
                f'Макс. запрос в ноль: {net_after_fee:.2f} G'
            )
            self.result_label.color = (0.4, 0.8, 1, 1)
        except ValueError:
            self.result_label.text = 'Введи рыночную цену во второе поле!'
            self.result_label.color = (1, 0.4, 0.4, 1)

    def add_to_goal(self, instance):
        if self.last_profit > 0:
            self.total_profit += self.last_profit
            self.goal_label.text = (
                f'Копилка: {self.total_profit:.2f} G  |  Цель: {self.goal:.0f} G'
            )
            self.last_profit = 0.0
            self.result_label.text = 'Прибыль добавлена в копилку!'

    def clear_fields(self, instance):
        self.buy_input.text = ''
        self.sell_input.text = ''
        self.qty_input.text = '1'
        self.result_label.text = 'Поля очищены'
        self.result_label.color = (0.9, 0.92, 0.95, 1)


if __name__ == '__main__':
    TradeProApp().run()
