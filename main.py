import flet as ft
import json
from datetime import datetime
import math
from collections import Counter


class FinancialApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.load_data()
        self.check_new_month()
        self.create_components()
        self.setup_navigation()

    def setup_page(self):
        """Configuração inicial da página com design premium e mobile-first"""
        self.page.title = "✨ Gestão Financeira"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = "#FAFBFF"
        self.page.padding = 0
        # Configuração mobile-first
        self.page.window.width = 400
        self.page.window.height = 800
        self.page.window.resizable = True
        self.page.scroll = ft.ScrollMode.AUTO

    def load_data(self):
        """Carrega dados do client_storage"""
        try:
            salary_data = self.page.client_storage.get("salary")
            self.base_salary = float(salary_data) if salary_data else 0.0

            accumulated_data = self.page.client_storage.get("accumulated_balance")
            self.accumulated_balance = float(accumulated_data) if accumulated_data else 0.0

            self.salary = self.base_salary + self.accumulated_balance

            expenses_data = self.page.client_storage.get("expenses")
            self.expenses = json.loads(expenses_data) if expenses_data else []

            goals_data = self.page.client_storage.get("goals")
            self.goals = json.loads(goals_data) if goals_data else []

            # Nova funcionalidade: Dívidas
            debts_data = self.page.client_storage.get("debts")
            self.debts = json.loads(debts_data) if debts_data else []

            current_month_data = self.page.client_storage.get("current_month")
            self.current_month = current_month_data if current_month_data else datetime.now().strftime("%m/%Y")

        except:
            self.base_salary = 0.0
            self.accumulated_balance = 0.0
            self.salary = 0.0
            self.expenses = []
            self.goals = []
            self.debts = []
            self.current_month = datetime.now().strftime("%m/%Y")

    def save_data(self):
        """Salva dados no client_storage"""
        self.page.client_storage.set("salary", str(self.base_salary))
        self.page.client_storage.set("accumulated_balance", str(self.accumulated_balance))
        self.page.client_storage.set("expenses", json.dumps(self.expenses))
        self.page.client_storage.set("goals", json.dumps(self.goals))
        self.page.client_storage.set("debts", json.dumps(self.debts))
        self.page.client_storage.set("current_month", self.current_month)

    def check_new_month(self):
        """Verifica se é um novo mês e faz a transição automática"""
        new_month = datetime.now().strftime("%m/%Y")

        if new_month != self.current_month and self.current_month != "":
            total_spent, current_balance = self.calculate_totals()

            if current_balance > 0:
                self.accumulated_balance += current_balance

            self.expenses = []
            self.current_month = new_month
            self.salary = self.base_salary + self.accumulated_balance
            self.save_data()

    def calculate_totals(self):
        """Calcula totais financeiros"""
        total_spent = sum(expense['amount'] for expense in self.expenses if expense['amount'] > 0)
        current_balance = self.salary - total_spent
        return total_spent, current_balance

    def analyze_spending_patterns(self):
        """Analisa padrões de gastos"""
        if not self.expenses:
            return [], 0, "", []

        descriptions = [expense['description'].lower().strip() for expense in self.expenses]
        description_counter = Counter(descriptions)
        most_common = description_counter.most_common(5)

        expense_by_desc = {}
        for expense in self.expenses:
            desc = expense['description'].lower().strip()
            if desc in expense_by_desc:
                expense_by_desc[desc] += expense['amount']
            else:
                expense_by_desc[desc] = expense['amount']

        highest_spending = max(expense_by_desc.items(), key=lambda x: x[1]) if expense_by_desc else ("", 0)
        top_expenses = sorted(self.expenses, key=lambda x: x['amount'], reverse=True)[:3]

        return most_common, highest_spending[1], highest_spending[0], top_expenses

    def create_mobile_card(self, content, color="#FFFFFF"):
        """Cria card otimizado para mobile"""
        return ft.Container(
            content=content,
            bgcolor=color,
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=16,
            padding=ft.padding.all(16),
            margin=ft.margin.only(bottom=16),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

    def create_mobile_button(self, text, on_click, icon=None, color="#2563EB"):
        """Cria botão otimizado para mobile"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color="#FFFFFF", size=20) if icon else ft.Container(),
                ft.Text(text, color="#FFFFFF", size=14, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            bgcolor=color,
            border_radius=12,
            padding=ft.padding.symmetric(vertical=14, horizontal=20),
            on_click=on_click,
            margin=ft.margin.only(bottom=12),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=f"{color}40",
                offset=ft.Offset(0, 2)
            )
        )

    def save_salary(self, e):
        """Salva o salário base digitado"""
        try:
            salary_value = self.salary_field.content.value
            if salary_value:
                self.base_salary = float(salary_value)
                self.salary = self.base_salary + self.accumulated_balance
                self.save_data()
                self.update_all_views()

                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("💰 Salário salvo!"),
                    bgcolor="#059669"
                )
                self.page.snack_bar.open = True
                self.page.update()
        except ValueError:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ Valor inválido!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()

    def create_components(self):
        """Cria todos os componentes da interface"""
        self.create_finances_view()
        self.create_goals_view()
        self.create_extras_view()  # Nova aba combinada
        self.create_summary_view()

        self.main_container = ft.Container(
            content=self.finances_view,
            expand=True,
            padding=ft.padding.all(12)
        )

    def create_finances_view(self):
        """Cria a vista de finanças otimizada para mobile"""
        # Campo salário
        self.salary_field = ft.Container(
            content=ft.TextField(
                label="💰 Salário Mensal (Kz)",
                value=str(self.base_salary) if self.base_salary > 0 else "",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#2563EB",
                border_radius=12,
                content_padding=ft.padding.all(16),
                text_size=14
            ),
            margin=ft.margin.only(bottom=12)
        )

        # Card resumo financeiro mobile
        total_spent, current_balance = self.calculate_totals()

        self.summary_card = self.create_mobile_card(
            ft.Column([
                ft.Text("💎 Resumo Financeiro", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Text(f"Mês: {self.current_month}", size=12, color="#6B7280"),
                ft.Container(height=12),

                # Grid responsivo para mobile
                ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Total", size=10, color="#6B7280"),
                                ft.Text(f"{self.salary:,.0f}", size=14, weight=ft.FontWeight.BOLD, color="#2563EB"),
                                ft.Text("Kz", size=9, color="#9CA3AF")
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                            bgcolor="#EFF6FF",
                            border_radius=12,
                            padding=ft.padding.all(12),
                            expand=True
                        ),
                        ft.Container(width=8),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Gasto", size=10, color="#6B7280"),
                                ft.Text(f"{total_spent:,.0f}", size=14, weight=ft.FontWeight.BOLD, color="#EC4899"),
                                ft.Text("Kz", size=9, color="#9CA3AF")
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                            bgcolor="#FDF2F8",
                            border_radius=12,
                            padding=ft.padding.all(12),
                            expand=True
                        )
                    ]),
                    ft.Container(height=8),
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Saldo", size=10, color="#6B7280"),
                                ft.Text(f"{current_balance:,.0f}", size=14, weight=ft.FontWeight.BOLD,
                                        color="#059669" if current_balance >= 0 else "#DC2626"),
                                ft.Text("Kz", size=9, color="#9CA3AF")
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                            bgcolor="#ECFDF5" if current_balance >= 0 else "#FEF2F2",
                            border_radius=12,
                            padding=ft.padding.all(12),
                            expand=True
                        ),
                        ft.Container(width=8),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Uso", size=10, color="#6B7280"),
                                ft.Text(f"{(total_spent / self.salary * 100):,.0f}%" if self.salary > 0 else "0%",
                                        size=14, weight=ft.FontWeight.BOLD, color="#D97706"),
                                ft.Text("%", size=9, color="#9CA3AF")
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                            bgcolor="#FFFBEB",
                            border_radius=12,
                            padding=ft.padding.all(12),
                            expand=True
                        )
                    ])
                ])
            ])
        )

        # Análise de gastos - ADICIONADO DE VOLTA
        most_common, highest_amount, highest_desc, top_expenses = self.analyze_spending_patterns()

        spending_analysis = self.create_mobile_card(
            ft.Column([
                ft.Text("📊 Análise de Gastos", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(height=12),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Text("🔥", size=20),
                                bgcolor="#FEF2F2",
                                border_radius=25,
                                padding=ft.padding.all(8)
                            ),
                            ft.Text("Maior Gasto", size=11, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{highest_amount:,.0f} Kz", size=14, weight=ft.FontWeight.BOLD, color="#DC2626"),
                            ft.Text(highest_desc.title()[:15] + "..." if len(
                                highest_desc) > 15 else highest_desc.title() if highest_desc else "N/A",
                                    size=9, color="#9CA3AF")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                        bgcolor="#FAFAFA",
                        border_radius=12,
                        padding=ft.padding.all(12),
                        expand=True
                    ),
                    ft.Container(width=12),
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Text("🎯", size=20),
                                bgcolor="#FFFBEB",
                                border_radius=25,
                                padding=ft.padding.all(8)
                            ),
                            ft.Text("Mais Frequente", size=11, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{most_common[0][1]}x" if most_common else "0x", size=14,
                                    weight=ft.FontWeight.BOLD, color="#D97706"),
                            ft.Text(
                                most_common[0][0].title()[:15] + "..." if most_common and len(most_common[0][0]) > 15
                                else most_common[0][0].title() if most_common else "N/A",
                                size=9, color="#9CA3AF")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                        bgcolor="#FAFAFA",
                        border_radius=12,
                        padding=ft.padding.all(12),
                        expand=True
                    )
                ])
            ])
        ) if self.expenses else ft.Container()

        # Campos despesa
        self.expense_description = ft.Container(
            content=ft.TextField(
                label="📝 Descrição da Despesa",
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#EC4899",
                border_radius=12,
                content_padding=ft.padding.all(16),
                text_size=14
            ),
            margin=ft.margin.only(bottom=12)
        )

        self.expense_amount = ft.Container(
            content=ft.TextField(
                label="💵 Valor da Despesa (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#EC4899",
                border_radius=12,
                content_padding=ft.padding.all(16),
                text_size=14
            ),
            margin=ft.margin.only(bottom=12)
        )

        # Lista despesas mobile
        self.expenses_list = ft.ListView(
            spacing=8,
            height=200,
            padding=ft.padding.all(0)
        )
        self.update_expenses_list()

        # Layout mobile
        self.finances_view = ft.Column([
            ft.Text("💳 Controle Financeiro", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),

            self.salary_field,
            self.create_mobile_button("💾 Salvar Salário", self.save_salary, ft.Icons.SAVE, "#2563EB"),

            self.summary_card,

            spending_analysis,  # ADICIONADO DE VOLTA

            ft.Text("💸 Nova Despesa", size=18, weight=ft.FontWeight.BOLD, color="#EC4899"),
            self.expense_description,
            self.expense_amount,
            self.create_mobile_button("Adicionar Despesa", self.add_expense, ft.Icons.ADD_CIRCLE, "#EC4899"),

            ft.Text("📋 Últimas Transações", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
            self.create_mobile_card(self.expenses_list)

        ], scroll=ft.ScrollMode.AUTO, spacing=0)

    def create_goals_view(self):
        """Cria a vista de metas otimizada para mobile"""
        _, current_balance = self.calculate_totals()

        # Campos meta
        self.goal_name = ft.Container(
            content=ft.TextField(
                label="🎯 Nome da Meta",
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                border_radius=12,
                content_padding=ft.padding.all(16),
                text_size=14
            ),
            margin=ft.margin.only(bottom=12)
        )

        self.goal_total_cost = ft.Container(
            content=ft.TextField(
                label="💎 Custo Total (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                border_radius=12,
                content_padding=ft.padding.all(16),
                text_size=14
            ),
            margin=ft.margin.only(bottom=12)
        )

        self.goal_monthly_saving = ft.Container(
            content=ft.TextField(
                label="📅 Guardar por Mês (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                border_radius=12,
                content_padding=ft.padding.all(16),
                text_size=14,
                on_change=self.calculate_goal_time
            ),
            margin=ft.margin.only(bottom=12)
        )

        self.goal_time_estimate = ft.Container(
            content=ft.Text("⏱️ Tempo: -- meses", size=14, color="#D97706", weight=ft.FontWeight.BOLD),
            bgcolor="#FFFBEB",
            border_radius=8,
            padding=ft.padding.all(12),
            margin=ft.margin.only(bottom=12)
        )

        # Lista metas
        self.goals_list = ft.ListView(
            spacing=8,
            height=300,
            padding=ft.padding.all(0)
        )
        self.update_goals_list()

        self.goals_view = ft.Column([
            ft.Text("🎯 Metas & Objetivos", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),

            self.create_mobile_card(
                ft.Column([
                    ft.Text("💰 Saldo Disponível", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    ft.Text(f"{current_balance:,.0f} Kz", size=20, weight=ft.FontWeight.BOLD,
                            color="#059669" if current_balance >= 0 else "#DC2626"),
                    ft.Text("Para investir em suas metas", size=12, color="#6B7280")
                ])
            ),

            ft.Text("✨ Nova Meta", size=18, weight=ft.FontWeight.BOLD, color="#059669"),
            self.goal_name,
            self.goal_total_cost,
            self.goal_monthly_saving,
            self.goal_time_estimate,
            self.create_mobile_button("Criar Meta", self.add_goal, ft.Icons.ROCKET_LAUNCH, "#059669"),

            ft.Text("🏆 Minhas Metas", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
            self.create_mobile_card(self.goals_list)

        ], scroll=ft.ScrollMode.AUTO, spacing=0)

    def create_extras_view(self):
        """Cria a vista de extras (renda extra + dívidas) otimizada para mobile"""
        # Campos renda extra
        self.extra_income_description = ft.Container(
            content=ft.TextField(
                label="💸 Descrição da Renda Extra",
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                border_radius=12,
                content_padding=ft.padding.all(16),
                text_size=14
            ),
            margin=ft.margin.only(bottom=12)
        )

        self.extra_income_amount = ft.Container(
            content=ft.TextField(
                label="💰 Valor da Renda (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                border_radius=12,
                content_padding=ft.padding.all(16),
                text_size=14
            ),
            margin=ft.margin.only(bottom=12)
        )

        # Campos dívida
        self.debt_name = ft.Container(
            content=ft.TextField(
                label="💳 Nome da Dívida",
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#DC2626",
                border_radius=12,
                content_padding=ft.padding.all(16),
                text_size=14
            ),
            margin=ft.margin.only(bottom=12)
        )

        self.debt_total_amount = ft.Container(
            content=ft.TextField(
                label="💰 Valor Total (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#DC2626",
                border_radius=12,
                content_padding=ft.padding.all(16),
                text_size=14
            ),
            margin=ft.margin.only(bottom=12)
        )

        self.debt_monthly_payment = ft.Container(
            content=ft.TextField(
                label="📅 Pagamento Mensal (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#DC2626",
                border_radius=12,
                content_padding=ft.padding.all(16),
                text_size=14
            ),
            margin=ft.margin.only(bottom=12)
        )

        # Lista dívidas
        self.debts_list = ft.ListView(
            spacing=8,
            height=250,
            padding=ft.padding.all(0)
        )
        self.update_debts_list()

        self.extras_view = ft.Column([
            ft.Text("💰 Extras & Dívidas", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),

            # SEÇÃO RENDA EXTRA
            ft.Text("💰 Renda Extra", size=18, weight=ft.FontWeight.BOLD, color="#059669"),
            ft.Text("Freelances, vendas, bonificações, etc.", size=12, color="#6B7280"),
            self.extra_income_description,
            self.extra_income_amount,
            self.create_mobile_button("Adicionar Renda", self.add_extra_income, ft.Icons.ADD_CIRCLE, "#059669"),

            ft.Container(height=24),

            # SEÇÃO DÍVIDAS
            ft.Text("💳 Dívidas", size=18, weight=ft.FontWeight.BOLD, color="#DC2626"),
            ft.Text("Cartões, empréstimos, financiamentos", size=12, color="#6B7280"),
            self.debt_name,
            self.debt_total_amount,
            self.debt_monthly_payment,
            self.create_mobile_button("Adicionar Dívida", self.add_debt, ft.Icons.ADD_CIRCLE, "#DC2626"),

            ft.Text("📋 Minhas Dívidas", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
            self.create_mobile_card(self.debts_list)

        ], scroll=ft.ScrollMode.AUTO, spacing=0)

    def create_summary_view(self):
        """Cria a vista de resumo otimizada para mobile"""
        total_spent, current_balance = self.calculate_totals()
        most_common, highest_amount, highest_desc, top_expenses = self.analyze_spending_patterns()

        # Cards estatísticas mobile
        stats_cards = ft.Column([
            ft.Row([
                self.create_stat_card_mobile("💰", "Salário", f"{self.salary:,.0f}", "Kz", "#2563EB"),
                ft.Container(width=8),
                self.create_stat_card_mobile("💸", "Gastos", f"{total_spent:,.0f}", "Kz", "#EC4899")
            ]),
            ft.Container(height=8),
            ft.Row([
                self.create_stat_card_mobile("💎", "Saldo", f"{current_balance:,.0f}", "Kz",
                                             "#059669" if current_balance >= 0 else "#DC2626"),
                ft.Container(width=8),
                self.create_stat_card_mobile("🎯", "Metas", str(len(self.goals)), "", "#8B5CF6")
            ])
        ])

        # Top gastos mobile
        top_expenses_card = self.create_mobile_card(
            ft.Column([
                ft.Text("🔥 Maiores Gastos", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(height=8),
                ft.Column([
                    ft.Row([
                        ft.Text(f"{i + 1}.", size=12, color="#6B7280", weight=ft.FontWeight.BOLD),
                        ft.Column([
                            ft.Text(expense['description'][:25] + "..." if len(expense['description']) > 25
                                    else expense['description'], size=13, weight=ft.FontWeight.BOLD),
                            ft.Text(expense['date'], size=11, color="#6B7280")
                        ], expand=True, spacing=2),
                        ft.Text(f"{expense['amount']:,.0f} Kz", size=13, weight=ft.FontWeight.BOLD, color="#DC2626")
                    ]) for i, expense in enumerate(top_expenses[:3])
                ], spacing=8) if top_expenses else [ft.Text("Nenhuma despesa", size=12, color="#6B7280")]
            ])
        ) if self.expenses else ft.Container()

        self.summary_view = ft.Column([
            ft.Text("📊 Dashboard", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),

            stats_cards,
            ft.Container(height=16),
            top_expenses_card

        ], scroll=ft.ScrollMode.AUTO, spacing=0)

    def create_stat_card_mobile(self, icon, title, value, unit, color):
        """Cria card de estatística otimizado para mobile"""
        return ft.Container(
            content=ft.Column([
                ft.Text(icon, size=20),
                ft.Text(title, size=10, color="#6B7280", weight=ft.FontWeight.BOLD),
                ft.Text(value, size=14, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(unit, size=9, color="#9CA3AF") if unit else ft.Container(height=8)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=12,
            padding=ft.padding.all(12),
            expand=True,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

    def setup_navigation(self):
        """Configura a navegação mobile"""
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.CREDIT_CARD_OUTLINED, label="Finanças",
                                            selected_icon=ft.Icons.CREDIT_CARD),
                ft.NavigationBarDestination(icon=ft.Icons.SAVINGS_OUTLINED, label="Metas",
                                            selected_icon=ft.Icons.SAVINGS),
                ft.NavigationBarDestination(icon=ft.Icons.PAYMENT_OUTLINED, label="Extras",
                                            selected_icon=ft.Icons.PAYMENT),
                ft.NavigationBarDestination(icon=ft.Icons.ANALYTICS_OUTLINED, label="Dashboard",
                                            selected_icon=ft.Icons.ANALYTICS)
            ],
            on_change=self.navigation_changed,
            bgcolor="#FFFFFF",
            indicator_color="#EFF6FF",
            selected_index=0,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            height=60
        )

        self.page.add(
            ft.Column([
                self.main_container,
                self.navigation_bar
            ], expand=True, spacing=0)
        )

    def show_add_payment_dialog(self, goal_index):
        """Diálogo para adicionar pagamento à meta - CORRIGIDO"""
        print(f"Abrindo diálogo para meta {goal_index}")  # Debug
        _, current_balance = self.calculate_totals()

        payment_field = ft.TextField(
            label="Valor do Pagamento (Kz)",
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor="#FFFFFF",
            border_color="#E5E7EB",
            focused_border_color="#059669",
            border_radius=12,
            content_padding=ft.padding.all(16),
            text_size=14
        )

        error_text = ft.Text("", size=12)

        def add_payment_action(e):
            print(f"Tentando adicionar pagamento à meta {goal_index}")  # Debug
            try:
                if not payment_field.value:
                    error_text.value = "❌ Digite um valor!"
                    error_text.color = "#DC2626"
                    self.page.update()
                    return

                amount = float(payment_field.value)
                if amount <= 0:
                    error_text.value = "❌ Valor deve ser maior que zero!"
                    error_text.color = "#DC2626"
                    self.page.update()
                    return

                if amount > current_balance:
                    error_text.value = f"❌ Saldo insuficiente! Disponível: {current_balance:,.0f} Kz"
                    error_text.color = "#DC2626"
                    self.page.update()
                    return

                # Adiciona pagamento à meta
                if 'saved_amount' not in self.goals[goal_index]:
                    self.goals[goal_index]['saved_amount'] = 0
                self.goals[goal_index]['saved_amount'] += amount

                # Adiciona como despesa
                payment_expense = {
                    'description': f"💰 Meta: {self.goals[goal_index]['name']}",
                    'amount': amount,
                    'date': datetime.now().strftime("%d/%m/%Y")
                }
                self.expenses.append(payment_expense)

                self.save_data()
                self.update_all_views()

                # Fecha diálogo
                self.page.dialog.open = False
                self.page.update()

                # Mostra sucesso
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("💰 Pagamento realizado!"),
                    bgcolor="#059669"
                )
                self.page.snack_bar.open = True
                self.page.update()

            except ValueError:
                error_text.value = "❌ Valor inválido!"
                error_text.color = "#DC2626"
                self.page.update()
            except Exception as ex:
                print(f"Erro ao processar pagamento: {ex}")
                error_text.value = f"❌ Erro: {str(ex)}"
                error_text.color = "#DC2626"
                self.page.update()

        def close_dialog_action(e):
            self.page.dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("💰 Investir na Meta", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text(f"Meta: {self.goals[goal_index]['name']}", size=14, weight=ft.FontWeight.BOLD),
                ft.Text(f"Custo: {self.goals[goal_index]['total_cost']:,.0f} Kz", size=12, color="#6B7280"),
                ft.Text(f"Já pago: {self.goals[goal_index].get('saved_amount', 0):,.0f} Kz", size=12, color="#059669"),
                ft.Text(f"Disponível: {current_balance:,.0f} Kz", size=12, color="#2563EB"),
                ft.Container(height=12),
                payment_field,
                error_text
            ], tight=True, spacing=8),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog_action),
                ft.ElevatedButton("Investir", on_click=add_payment_action, bgcolor="#059669", color="#FFFFFF")
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_pay_debt_dialog(self, debt_index):
        """Diálogo para pagar dívida - CORRIGIDO"""
        print(f"Abrindo diálogo para dívida {debt_index}")  # Debug
        _, current_balance = self.calculate_totals()

        payment_field = ft.TextField(
            label="Valor do Pagamento (Kz)",
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor="#FFFFFF",
            border_color="#E5E7EB",
            focused_border_color="#DC2626",
            border_radius=12,
            content_padding=ft.padding.all(16),
            text_size=14
        )

        error_text = ft.Text("", size=12)

        def pay_debt_action(e):
            print(f"Tentando pagar dívida {debt_index}")  # Debug
            try:
                if not payment_field.value:
                    error_text.value = "❌ Digite um valor!"
                    error_text.color = "#DC2626"
                    self.page.update()
                    return

                amount = float(payment_field.value)
                if amount <= 0:
                    error_text.value = "❌ Valor deve ser maior que zero!"
                    error_text.color = "#DC2626"
                    self.page.update()
                    return

                if amount > current_balance:
                    error_text.value = f"❌ Saldo insuficiente! Disponível: {current_balance:,.0f} Kz"
                    error_text.color = "#DC2626"
                    self.page.update()
                    return

                # Adiciona pagamento à dívida
                if 'paid_amount' not in self.debts[debt_index]:
                    self.debts[debt_index]['paid_amount'] = 0
                self.debts[debt_index]['paid_amount'] += amount

                # Adiciona como despesa
                debt_expense = {
                    'description': f"💳 Dívida: {self.debts[debt_index]['name']}",
                    'amount': amount,
                    'date': datetime.now().strftime("%d/%m/%Y")
                }
                self.expenses.append(debt_expense)

                self.save_data()
                self.update_all_views()

                # Fecha diálogo
                self.page.dialog.open = False
                self.page.update()

                # Mostra sucesso
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("💳 Pagamento realizado!"),
                    bgcolor="#DC2626"
                )
                self.page.snack_bar.open = True
                self.page.update()

            except ValueError:
                error_text.value = "❌ Valor inválido!"
                error_text.color = "#DC2626"
                self.page.update()
            except Exception as ex:
                print(f"Erro ao processar pagamento: {ex}")
                error_text.value = f"❌ Erro: {str(ex)}"
                error_text.color = "#DC2626"
                self.page.update()

        def close_dialog_action(e):
            self.page.dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("💳 Pagar Dívida", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text(f"Dívida: {self.debts[debt_index]['name']}", size=14, weight=ft.FontWeight.BOLD),
                ft.Text(f"Total: {self.debts[debt_index]['total_amount']:,.0f} Kz", size=12, color="#6B7280"),
                ft.Text(f"Já pago: {self.debts[debt_index].get('paid_amount', 0):,.0f} Kz", size=12, color="#DC2626"),
                ft.Text(f"Disponível: {current_balance:,.0f} Kz", size=12, color="#2563EB"),
                ft.Container(height=12),
                payment_field,
                error_text
            ], tight=True, spacing=8),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog_action),
                ft.ElevatedButton("Pagar", on_click=pay_debt_action, bgcolor="#DC2626", color="#FFFFFF")
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def navigation_changed(self, e):
        """Gerencia navegação"""
        selected_index = e.control.selected_index

        if selected_index == 0:
            self.main_container.content = self.finances_view
            self.update_finances_view()
        elif selected_index == 1:
            self.main_container.content = self.goals_view
            self.update_goals_view()
        elif selected_index == 2:
            self.main_container.content = self.extras_view
            self.update_extras_view()
        elif selected_index == 3:
            self.main_container.content = self.summary_view
            self.update_summary_view()

        self.page.update()

    def add_extra_income(self, e):
        """Adiciona renda extra"""
        description_field = self.extra_income_description.content
        amount_field = self.extra_income_amount.content

        if not description_field.value or not amount_field.value:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ Preencha todos os campos!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        try:
            amount = float(amount_field.value)

            self.accumulated_balance += amount
            self.salary = self.base_salary + self.accumulated_balance

            income_entry = {
                'description': f"💰 {description_field.value}",
                'amount': -amount,  # Negativo para mostrar como entrada
                'date': datetime.now().strftime("%d/%m/%Y")
            }

            self.expenses.append(income_entry)
            self.save_data()

            description_field.value = ""
            amount_field.value = ""

            self.update_all_views()

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("💰 Renda adicionada!"),
                bgcolor="#059669"
            )
            self.page.snack_bar.open = True
            self.page.update()
        except ValueError:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ Valor inválido!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()

    def add_expense(self, e):
        """Adiciona despesa"""
        description_field = self.expense_description.content
        amount_field = self.expense_amount.content

        if not description_field.value or not amount_field.value:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ Preencha todos os campos!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        try:
            amount = float(amount_field.value)
            expense = {
                'description': description_field.value,
                'amount': amount,
                'date': datetime.now().strftime("%d/%m/%Y")
            }

            self.expenses.append(expense)
            self.save_data()

            description_field.value = ""
            amount_field.value = ""

            self.update_all_views()

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("💸 Despesa adicionada!"),
                bgcolor="#EC4899"
            )
            self.page.snack_bar.open = True
            self.page.update()
        except ValueError:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ Valor inválido!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()

    def add_goal(self, e):
        """Adiciona meta"""
        name_field = self.goal_name.content
        total_cost_field = self.goal_total_cost.content
        monthly_saving_field = self.goal_monthly_saving.content

        if not all([name_field.value, total_cost_field.value, monthly_saving_field.value]):
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ Preencha todos os campos!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        try:
            goal = {
                'name': name_field.value,
                'total_cost': float(total_cost_field.value),
                'monthly_saving': float(monthly_saving_field.value),
                'saved_amount': 0,
                'created_date': datetime.now().strftime("%d/%m/%Y")
            }

            self.goals.append(goal)
            self.save_data()

            name_field.value = ""
            total_cost_field.value = ""
            monthly_saving_field.value = ""
            self.goal_time_estimate.content.value = "⏱️ Tempo: -- meses"

            self.update_all_views()

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("🎯 Meta criada!"),
                bgcolor="#059669"
            )
            self.page.snack_bar.open = True
            self.page.update()
        except ValueError:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ Valores inválidos!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()

    def add_debt(self, e):
        """Adiciona dívida"""
        name_field = self.debt_name.content
        total_field = self.debt_total_amount.content
        monthly_field = self.debt_monthly_payment.content

        if not all([name_field.value, total_field.value, monthly_field.value]):
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ Preencha todos os campos!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        try:
            debt = {
                'name': name_field.value,
                'total_amount': float(total_field.value),
                'monthly_payment': float(monthly_field.value),
                'paid_amount': 0,
                'created_date': datetime.now().strftime("%d/%m/%Y")
            }

            self.debts.append(debt)
            self.save_data()

            name_field.value = ""
            total_field.value = ""
            monthly_field.value = ""

            self.update_all_views()

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("💳 Dívida adicionada!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()
        except ValueError:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ Valores inválidos!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()

    def calculate_goal_time(self, e):
        """Calcula tempo da meta"""
        total_cost_field = self.goal_total_cost.content
        monthly_saving_field = self.goal_monthly_saving.content

        try:
            if total_cost_field.value and monthly_saving_field.value:
                total_cost = float(total_cost_field.value)
                monthly_saving = float(monthly_saving_field.value)

                if monthly_saving > 0:
                    months = math.ceil(total_cost / monthly_saving)
                    self.goal_time_estimate.content.value = f"⏱️ Tempo: {months} meses"
                else:
                    self.goal_time_estimate.content.value = "⏱️ Tempo: -- meses"

                self.page.update()
        except ValueError:
            self.goal_time_estimate.content.value = "⏱️ Tempo: -- meses"
            self.page.update()

    def remove_expense(self, index):
        """Remove despesa"""

        def remove(e):
            self.expenses.pop(index)
            self.save_data()
            self.update_all_views()

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("🗑️ Removido!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()

        return remove

    def remove_goal(self, index):
        """Remove meta"""

        def remove(e):
            self.goals.pop(index)
            self.save_data()
            self.update_all_views()

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("🗑️ Meta removida!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()

        return remove

    def remove_debt(self, index):
        """Remove dívida"""

        def remove(e):
            self.debts.pop(index)
            self.save_data()
            self.update_all_views()

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("🗑️ Dívida removida!"),
                bgcolor="#DC2626"
            )
            self.page.snack_bar.open = True
            self.page.update()

        return remove

    def update_expenses_list(self):
        """Atualiza lista de despesas"""
        self.expenses_list.controls.clear()

        for i, expense in enumerate(reversed(self.expenses[-10:])):  # Últimas 10
            is_income = expense['amount'] < 0
            is_goal_payment = expense['description'].startswith("💰 Meta:")
            is_debt_payment = expense['description'].startswith("💳 Dívida:")

            # Escolhe ícone e cor
            if is_income:
                icon = ft.Icons.ARROW_UPWARD
                color = "#059669"
                bg_color = "#ECFDF5"
            elif is_goal_payment:
                icon = ft.Icons.SAVINGS
                color = "#059669"
                bg_color = "#ECFDF5"
            elif is_debt_payment:
                icon = ft.Icons.PAYMENT
                color = "#DC2626"
                bg_color = "#FEF2F2"
            else:
                icon = ft.Icons.ARROW_DOWNWARD
                color = "#EC4899"
                bg_color = "#FDF2F8"

            expense_item = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, color=color, size=16),
                        bgcolor=bg_color,
                        border_radius=20,
                        padding=ft.padding.all(8)
                    ),
                    ft.Column([
                        ft.Text(expense['description'][:30] + "..." if len(expense['description']) > 30
                                else expense['description'],
                                size=12, weight=ft.FontWeight.NORMAL, color="#1F2937"),
                        ft.Text(expense['date'], size=10, color="#6B7280")
                    ], expand=True, spacing=2),
                    ft.Column([
                        ft.Text(f"{abs(expense['amount']):,.0f} Kz", size=12, weight=ft.FontWeight.BOLD, color=color),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color="#DC2626",
                            icon_size=14,
                            on_click=self.remove_expense(len(self.expenses) - 1 - i),
                            tooltip="Remover"
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=0)
                ]),
                bgcolor="#FFFFFF",
                border=ft.border.all(1, "#F3F4F6"),
                border_radius=8,
                padding=ft.padding.all(8),
                margin=ft.margin.only(bottom=4)
            )
            self.expenses_list.controls.append(expense_item)

    def update_goals_list(self):
        """Atualiza lista de metas - CORRIGIDO"""
        self.goals_list.controls.clear()

        for i, goal in enumerate(self.goals):
            saved_amount = goal.get('saved_amount', 0)
            progress = saved_amount / goal['total_cost'] if goal['total_cost'] > 0 else 0
            remaining = goal['total_cost'] - saved_amount

            # Status da meta
            if progress >= 1.0:
                status_text = "✅ Concluída!"
                status_color = "#059669"
                can_invest = False
            elif progress >= 0.75:
                status_text = f"🔥 Quase lá!"
                status_color = "#D97706"
                can_invest = True
            else:
                status_text = f"💰 Faltam {remaining:,.0f} Kz"
                status_color = "#6B7280"
                can_invest = True

            # CORRIGIDO: Usar closure para capturar o índice correto
            invest_button = ft.Container(
                content=ft.Text("💰 Investir", size=12, weight=ft.FontWeight.BOLD, color="#059669"),
                bgcolor="#ECFDF5" if can_invest else "#F3F4F6",
                border_radius=6,
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                on_click=lambda e, idx=i: self.show_add_payment_dialog(idx) if can_invest else None
            ) if can_invest else ft.Container(
                content=ft.Text("✅ Completa", size=12, weight=ft.FontWeight.BOLD, color="#059669"),
                bgcolor="#ECFDF5",
                border_radius=6,
                padding=ft.padding.symmetric(horizontal=12, vertical=6)
            )

            goal_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(goal['name'], size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
                            ft.Text(status_text, size=11, color=status_color)
                        ], expand=True, spacing=2),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color="#DC2626",
                            icon_size=16,
                            on_click=self.remove_goal(i),
                            tooltip="Remover"
                        )
                    ]),
                    ft.Container(height=8),
                    ft.ProgressBar(
                        value=min(progress, 1.0),
                        bgcolor="#E5E7EB",
                        color="#059669" if progress >= 1.0 else "#2563EB",
                        height=6
                    ),
                    ft.Container(height=8),
                    ft.Row([
                        ft.Text(f"{saved_amount:,.0f} / {goal['total_cost']:,.0f} Kz", size=11, color="#6B7280"),
                        ft.Text(f"{progress * 100:.0f}%", size=11, weight=ft.FontWeight.BOLD, color="#2563EB")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=8),
                    invest_button
                ]),
                bgcolor="#FFFFFF",
                border=ft.border.all(1, "#E5E7EB"),
                border_radius=12,
                padding=ft.padding.all(12),
                margin=ft.margin.only(bottom=8)
            )
            self.goals_list.controls.append(goal_card)

    def update_debts_list(self):
        """Atualiza lista de dívidas - CORRIGIDO"""
        self.debts_list.controls.clear()

        for i, debt in enumerate(self.debts):
            paid_amount = debt.get('paid_amount', 0)
            progress = paid_amount / debt['total_amount'] if debt['total_amount'] > 0 else 0
            remaining = debt['total_amount'] - paid_amount

            # Status da dívida
            if progress >= 1.0:
                status_text = "✅ Quitada!"
                status_color = "#059669"
                can_pay = False
            else:
                status_text = f"💳 Devendo {remaining:,.0f} Kz"
                status_color = "#DC2626"
                can_pay = True

            # CORRIGIDO: Usar closure para capturar o índice correto
            pay_button = ft.Container(
                content=ft.Text("💳 Pagar", size=12, weight=ft.FontWeight.BOLD, color="#DC2626"),
                bgcolor="#FEF2F2" if can_pay else "#F3F4F6",
                border_radius=6,
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                on_click=lambda e, idx=i: self.show_pay_debt_dialog(idx) if can_pay else None
            ) if can_pay else ft.Container(
                content=ft.Text("✅ Quitada", size=12, weight=ft.FontWeight.BOLD, color="#059669"),
                bgcolor="#ECFDF5",
                border_radius=6,
                padding=ft.padding.symmetric(horizontal=12, vertical=6)
            )

            debt_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(debt['name'], size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
                            ft.Text(status_text, size=11, color=status_color)
                        ], expand=True, spacing=2),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color="#DC2626",
                            icon_size=16,
                            on_click=self.remove_debt(i),
                            tooltip="Remover"
                        )
                    ]),
                    ft.Container(height=8),
                    ft.ProgressBar(
                        value=min(progress, 1.0),
                        bgcolor="#E5E7EB",
                        color="#059669" if progress >= 1.0 else "#DC2626",
                        height=6
                    ),
                    ft.Container(height=8),
                    ft.Row([
                        ft.Text(f"{paid_amount:,.0f} / {debt['total_amount']:,.0f} Kz", size=11, color="#6B7280"),
                        ft.Text(f"{progress * 100:.0f}%", size=11, weight=ft.FontWeight.BOLD, color="#DC2626")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=8),
                    pay_button
                ]),
                bgcolor="#FFFFFF",
                border=ft.border.all(1, "#E5E7EB"),
                border_radius=12,
                padding=ft.padding.all(12),
                margin=ft.margin.only(bottom=8)
            )
            self.debts_list.controls.append(debt_card)

    def update_finances_view(self):
        """Atualiza vista de finanças"""
        self.create_finances_view()
        if hasattr(self, 'main_container') and hasattr(self, 'finances_view'):
            if self.navigation_bar.selected_index == 0:
                self.main_container.content = self.finances_view

    def update_goals_view(self):
        """Atualiza vista de metas"""
        self.create_goals_view()
        if hasattr(self, 'main_container') and hasattr(self, 'goals_view'):
            if self.navigation_bar.selected_index == 1:
                self.main_container.content = self.goals_view

    def update_extras_view(self):
        """Atualiza vista de extras"""
        self.create_extras_view()
        if hasattr(self, 'main_container') and hasattr(self, 'extras_view'):
            if self.navigation_bar.selected_index == 2:
                self.main_container.content = self.extras_view

    def update_summary_view(self):
        """Atualiza vista de resumo"""
        self.create_summary_view()
        if hasattr(self, 'main_container') and hasattr(self, 'summary_view'):
            if self.navigation_bar.selected_index == 3:
                self.main_container.content = self.summary_view

    def update_all_views(self):
        """Atualiza todas as vistas"""
        current_index = getattr(self.navigation_bar, 'selected_index', 0)

        if current_index == 0:
            self.update_finances_view()
        elif current_index == 1:
            self.update_goals_view()
        elif current_index == 2:
            self.update_extras_view()
        elif current_index == 3:
            self.update_summary_view()

        self.page.update()


def main(page: ft.Page):
    """Função principal otimizada para mobile"""
    try:
        loading = ft.Container(
            content=ft.Column([
                ft.ProgressRing(width=40, height=40, stroke_width=3, color="#2563EB"),
                ft.Container(height=16),
                ft.Text("💰 Carregando...", size=16, weight=ft.FontWeight.BOLD, color="#2563EB")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#FAFBFF",
            expand=True,
            alignment=ft.alignment.center
        )

        page.add(loading)
        page.update()

        page.controls.clear()
        app = FinancialApp(page)

    except Exception as e:
        page.controls.clear()
        error_container = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ERROR, size=50, color="#DC2626"),
                ft.Container(height=16),
                ft.Text("❌ Erro ao carregar", size=18, weight=ft.FontWeight.BOLD, color="#DC2626"),
                ft.Text(f"{str(e)}", size=12, color="#6B7280"),
                ft.Container(height=16),
                ft.ElevatedButton("🔄 Tentar Novamente",
                                  on_click=lambda _: main(page),
                                  bgcolor="#2563EB",
                                  color="#FFFFFF")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#FAFBFF",
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.all(20)
        )
        page.add(error_container)
        page.update()


if __name__ == "__main__":
    ft.app(target=main)