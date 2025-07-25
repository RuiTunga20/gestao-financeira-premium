import flet as ft
import json
from datetime import datetime
import math
from collections import Counter


class FinancialApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.dialog_open = False  # Controle manual de diálogo
        self.current_view_index = 0  # Para controlar a view atual
        self.setup_page()
        self.load_data()
        self.check_new_month()
        self.create_components()
        self.setup_layout()

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

    def categorize_transactions(self):
        """Categoriza transações por tipo"""
        regular_expenses = []
        goal_payments = []
        debt_payments = []
        extra_income = []

        for expense in self.expenses:
            if expense['amount'] < 0:  # Renda extra
                extra_income.append(expense)
            elif expense['description'].startswith("💰 Meta:"):
                goal_payments.append(expense)
            elif expense['description'].startswith("💳 Dívida:"):
                debt_payments.append(expense)
            else:
                regular_expenses.append(expense)

        return regular_expenses, goal_payments, debt_payments, extra_income

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

    def create_fixed_header(self):
        """Cria cabeçalho fixo"""
        headers = [
            "💳 Controle Financeiro",
            "🎯 Metas & Objetivos",
            "💰 Extras & Dívidas",
            "📊 Dashboard"
        ]

        return ft.Container(
            content=ft.Row([
                ft.Text(
                    headers[self.current_view_index],
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#1F2937"
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor="#FFFFFF",
            padding=ft.padding.symmetric(vertical=16, horizontal=20),
            border=ft.border.only(bottom=ft.BorderSide(1, "#E5E7EB")),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

    def close_dialog(self):
        """Fecha diálogo/bottom sheet de forma limpa"""
        try:
            print("Fechando diálogo...")

            # Fecha bottom sheet
            if hasattr(self.page, 'bottom_sheet') and self.page.bottom_sheet:
                self.page.bottom_sheet.open = False
                self.page.bottom_sheet = None

            # Fecha diálogo regular (fallback)
            if hasattr(self.page, 'dialog') and self.page.dialog:
                self.page.dialog.open = False
                self.page.dialog = None

            # Reset do controle manual
            self.dialog_open = False

            # Atualização única
            self.page.update()

            print("Diálogo fechado com sucesso!")

        except Exception as e:
            print(f"Erro ao fechar diálogo: {e}")
            self.dialog_open = False

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
        self.create_extras_view()
        self.create_summary_view()

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

        # Análise de gastos
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
            self.salary_field,
            self.create_mobile_button("💾 Salvar Salário", self.save_salary, ft.Icons.SAVE, "#2563EB"),

            self.summary_card,
            spending_analysis,

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
        """Cria a vista de resumo otimizada para mobile com categorias"""
        total_spent, current_balance = self.calculate_totals()
        regular_expenses, goal_payments, debt_payments, extra_income = self.categorize_transactions()

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

        # Função para criar lista de transações
        def create_transaction_list(transactions, title, icon, color, max_items=3):
            if not transactions:
                return ft.Container()

            sorted_transactions = sorted(transactions, key=lambda x: x['amount'], reverse=True)[:max_items]

            return self.create_mobile_card(
                ft.Column([
                    ft.Text(f"{icon} {title}", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    ft.Container(height=8),
                    ft.Column([
                        ft.Row([
                            ft.Text(f"{i + 1}.", size=12, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Column([
                                ft.Text(transaction['description'][:25] + "..." if len(transaction['description']) > 25
                                        else transaction['description'], size=13, weight=ft.FontWeight.BOLD),
                                ft.Text(transaction['date'], size=11, color="#6B7280")
                            ], expand=True, spacing=2),
                            ft.Text(f"{abs(transaction['amount']):,.0f} Kz", size=13, weight=ft.FontWeight.BOLD,
                                    color=color)
                        ]) for i, transaction in enumerate(sorted_transactions)
                    ], spacing=8),
                    ft.Container(height=8),
                    ft.Text(
                        f"Total: {sum(abs(t['amount']) for t in transactions):,.0f} Kz • {len(transactions)} transações",
                        size=11, color="#6B7280", weight=ft.FontWeight.BOLD)
                ])
            )

        # Cards de transações categorizadas
        transaction_cards = []

        # Despesas regulares
        if regular_expenses:
            transaction_cards.append(
                create_transaction_list(regular_expenses, "Despesas Regulares", "🛒", "#EC4899")
            )

        # Pagamentos de metas
        if goal_payments:
            transaction_cards.append(
                create_transaction_list(goal_payments, "Investimentos em Metas", "🎯", "#059669")
            )

        # Pagamentos de dívidas
        if debt_payments:
            transaction_cards.append(
                create_transaction_list(debt_payments, "Pagamentos de Dívidas", "💳", "#DC2626")
            )

        # Renda extra
        if extra_income:
            transaction_cards.append(
                create_transaction_list(extra_income, "Renda Extra", "💰", "#059669")
            )

        self.summary_view = ft.Column([
            stats_cards,
            ft.Container(height=16),
            *transaction_cards

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

    def setup_layout(self):
        """Configura o layout com header fixo, conteúdo scrollable e navegação fixa"""
        # Header fixo
        self.header = self.create_fixed_header()

        # Container do conteúdo scrollable
        self.content_container = ft.Container(
            content=self.finances_view,
            expand=True,
            padding=ft.padding.only(left=12, right=12, top=12, bottom=20)  # Padding extra no fundo
        )

        # Navegação fixa
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
            bgcolor="transparent",  # Transparente para mostrar o container por trás
            indicator_color="#EFF6FF",
            selected_index=0,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            height=64,  # Altura ligeiramente maior
            surface_tint_color="#FFFFFF"
        )

        # Layout principal com header fixo, conteúdo e navegação fixa
        self.page.add(
            ft.Column([
                self.header,  # Header fixo no topo
                self.content_container,  # Conteúdo scrollable no meio
                ft.Container(
                    content=self.navigation_bar,
                    margin=ft.margin.only(bottom=8),  # Espaço acima da navegação
                    bgcolor="#FFFFFF",
                    border_radius=ft.border_radius.only(top_left=16, top_right=16),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color="#1F293720",
                        offset=ft.Offset(0, -2)
                    )
                )  # Navegação fixa no fundo com espaçamento
            ], expand=True, spacing=0)
        )

    def show_add_payment_dialog(self, goal_index):
        """BottomSheet para adicionar pagamento à meta - SE ADAPTA AO TECLADO"""
        print(f"Abrindo bottom sheet para meta {goal_index}")

        # Evita múltiplas chamadas
        if self.dialog_open:
            print("Diálogo já está aberto")
            return

        self.dialog_open = True
        _, current_balance = self.calculate_totals()

        # Verifica se a meta existe
        if goal_index >= len(self.goals):
            print(f"Erro: Meta {goal_index} não existe")
            self.dialog_open = False
            return

        payment_field = ft.TextField(
            label="Valor do Pagamento (Kz)",
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor="#FFFFFF",
            border_color="#E5E7EB",
            focused_border_color="#059669",
            border_radius=12,
            content_padding=ft.padding.all(16),
            text_size=14,
            autofocus=True
        )

        error_text = ft.Text("", size=12, color="#DC2626")

        def add_payment_action(e):
            print(f"Processando pagamento para meta {goal_index}")
            try:
                if not payment_field.value or payment_field.value.strip() == "":
                    error_text.value = "❌ Digite um valor!"
                    self.page.update()
                    return

                amount = float(payment_field.value.strip())
                if amount <= 0:
                    error_text.value = "❌ Valor deve ser maior que zero!"
                    self.page.update()
                    return

                if amount > current_balance:
                    error_text.value = f"❌ Saldo insuficiente! Disponível: {current_balance:,.0f} Kz"
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

                # Fecha bottom sheet
                self.close_dialog()

                # Atualiza views
                self.update_all_views()

                # Mostra sucesso
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("💰 Investimento realizado com sucesso!"),
                    bgcolor="#059669"
                )
                self.page.snack_bar.open = True
                self.page.update()

                print(f"Pagamento de {amount} realizado com sucesso para meta {goal_index}")

            except ValueError:
                error_text.value = "❌ Valor inválido! Use apenas números."
                self.page.update()
            except Exception as ex:
                print(f"Erro ao processar pagamento: {ex}")
                error_text.value = f"❌ Erro: {str(ex)}"
                self.page.update()

        def close_sheet_action(e):
            print("Fechando bottom sheet")
            self.close_dialog()

        # Cria BottomSheet que se adapta ao teclado
        bottom_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column([
                    # Header com linha de arraste
                    ft.Container(
                        content=ft.Container(
                            bgcolor="#E5E7EB",
                            border_radius=3,
                            height=4,
                            width=40
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=12, bottom=8)
                    ),

                    # Título e botão fechar
                    ft.Row([
                        ft.Text("💰 Investir na Meta", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=close_sheet_action,
                            icon_color="#6B7280",
                            icon_size=20
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    ft.Container(height=12),

                    # Card com informações da meta
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.SAVINGS, color="#059669", size=20),
                                ft.Text(f"{self.goals[goal_index]['name']}", size=16, weight=ft.FontWeight.BOLD,
                                        color="#1F2937", expand=True)
                            ], spacing=8),
                            ft.Container(height=8),
                            ft.Row([
                                ft.Column([
                                    ft.Text("Custo Total", size=11, color="#6B7280"),
                                    ft.Text(f"{self.goals[goal_index]['total_cost']:,.0f} Kz", size=13,
                                            weight=ft.FontWeight.BOLD, color="#1F2937")
                                ], spacing=2),
                                ft.Column([
                                    ft.Text("Já Investido", size=11, color="#6B7280"),
                                    ft.Text(f"{self.goals[goal_index].get('saved_amount', 0):,.0f} Kz", size=13,
                                            weight=ft.FontWeight.BOLD, color="#059669")
                                ], spacing=2),
                                ft.Column([
                                    ft.Text("Saldo Disponível", size=11, color="#6B7280"),
                                    ft.Text(f"{current_balance:,.0f} Kz", size=13, weight=ft.FontWeight.BOLD,
                                            color="#2563EB")
                                ], spacing=2),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ], spacing=0),
                        bgcolor="#F8FAFC",
                        border_radius=12,
                        padding=ft.padding.all(16),
                        border=ft.border.all(1, "#E2E8F0")
                    ),

                    ft.Container(height=20),

                    # Campo de valor
                    payment_field,

                    ft.Container(height=8),

                    # Texto de erro
                    error_text,

                    ft.Container(height=20),

                    # Botões
                    ft.Row([
                        ft.ElevatedButton(
                            "Cancelar",
                            on_click=close_sheet_action,
                            bgcolor="#F3F4F6",
                            color="#374151",
                            expand=1,
                            height=48
                        ),
                        ft.Container(width=12),
                        ft.ElevatedButton(
                            "💰 Investir",
                            on_click=add_payment_action,
                            bgcolor="#059669",
                            color="#FFFFFF",
                            expand=2,
                            height=48
                        )
                    ]),

                    # Espaço extra para o teclado
                    ft.Container(height=32)

                ], spacing=0, scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.symmetric(horizontal=20, vertical=0),
                bgcolor="#FFFFFF",
                border_radius=ft.border_radius.only(top_left=20, top_right=20)
            ),
            open=True,
            maintain_bottom_view_insets_padding=True,  # Mantém padding quando teclado aparece
            is_scroll_controlled=True,  # Permite scroll quando teclado aparece
            use_safe_area=True  # Usa área segura do dispositivo
        )

        # Abre BottomSheet
        self.page.bottom_sheet = bottom_sheet
        self.page.update()
        print(f"Bottom sheet aberto para meta {goal_index}")

    def show_pay_debt_dialog(self, debt_index):
        """BottomSheet para pagar dívida - SE ADAPTA AO TECLADO"""
        print(f"Abrindo bottom sheet para dívida {debt_index}")

        # Evita múltiplas chamadas
        if self.dialog_open:
            print("Diálogo já está aberto")
            return

        self.dialog_open = True
        _, current_balance = self.calculate_totals()

        # Verifica se a dívida existe
        if debt_index >= len(self.debts):
            print(f"Erro: Dívida {debt_index} não existe")
            self.dialog_open = False
            return

        payment_field = ft.TextField(
            label="Valor do Pagamento (Kz)",
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor="#FFFFFF",
            border_color="#E5E7EB",
            focused_border_color="#DC2626",
            border_radius=12,
            content_padding=ft.padding.all(16),
            text_size=14,
            autofocus=True
        )

        error_text = ft.Text("", size=12, color="#DC2626")

        def pay_debt_action(e):
            print(f"Processando pagamento para dívida {debt_index}")
            try:
                if not payment_field.value or payment_field.value.strip() == "":
                    error_text.value = "❌ Digite um valor!"
                    self.page.update()
                    return

                amount = float(payment_field.value.strip())
                if amount <= 0:
                    error_text.value = "❌ Valor deve ser maior que zero!"
                    self.page.update()
                    return

                if amount > current_balance:
                    error_text.value = f"❌ Saldo insuficiente! Disponível: {current_balance:,.0f} Kz"
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

                # Fecha bottom sheet
                self.close_dialog()

                # Atualiza views
                self.update_all_views()

                # Mostra sucesso
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("💳 Pagamento realizado com sucesso!"),
                    bgcolor="#DC2626"
                )
                self.page.snack_bar.open = True
                self.page.update()

                print(f"Pagamento de {amount} realizado com sucesso para dívida {debt_index}")

            except ValueError:
                error_text.value = "❌ Valor inválido! Use apenas números."
                self.page.update()
            except Exception as ex:
                print(f"Erro ao processar pagamento: {ex}")
                error_text.value = f"❌ Erro: {str(ex)}"
                self.page.update()

        def close_sheet_action(e):
            print("Fechando bottom sheet de dívida")
            self.close_dialog()

        # Cria BottomSheet que se adapta ao teclado
        bottom_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column([
                    # Header com linha de arraste
                    ft.Container(
                        content=ft.Container(
                            bgcolor="#E5E7EB",
                            border_radius=3,
                            height=4,
                            width=40
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=12, bottom=8)
                    ),

                    # Título e botão fechar
                    ft.Row([
                        ft.Text("💳 Pagar Dívida", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=close_sheet_action,
                            icon_color="#6B7280",
                            icon_size=20
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    ft.Container(height=12),

                    # Card com informações da dívida
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.PAYMENT, color="#DC2626", size=20),
                                ft.Text(f"{self.debts[debt_index]['name']}", size=16, weight=ft.FontWeight.BOLD,
                                        color="#1F2937", expand=True)
                            ], spacing=8),
                            ft.Container(height=8),
                            ft.Row([
                                ft.Column([
                                    ft.Text("Total", size=11, color="#6B7280"),
                                    ft.Text(f"{self.debts[debt_index]['total_amount']:,.0f} Kz", size=13,
                                            weight=ft.FontWeight.BOLD, color="#1F2937")
                                ], spacing=2),
                                ft.Column([
                                    ft.Text("Já Pago", size=11, color="#6B7280"),
                                    ft.Text(f"{self.debts[debt_index].get('paid_amount', 0):,.0f} Kz", size=13,
                                            weight=ft.FontWeight.BOLD, color="#DC2626")
                                ], spacing=2),
                                ft.Column([
                                    ft.Text("Saldo Disponível", size=11, color="#6B7280"),
                                    ft.Text(f"{current_balance:,.0f} Kz", size=13, weight=ft.FontWeight.BOLD,
                                            color="#2563EB")
                                ], spacing=2),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ], spacing=0),
                        bgcolor="#FEF2F2",
                        border_radius=12,
                        padding=ft.padding.all(16),
                        border=ft.border.all(1, "#FECACA")
                    ),

                    ft.Container(height=20),

                    # Campo de valor
                    payment_field,

                    ft.Container(height=8),

                    # Texto de erro
                    error_text,

                    ft.Container(height=20),

                    # Botões
                    ft.Row([
                        ft.ElevatedButton(
                            "Cancelar",
                            on_click=close_sheet_action,
                            bgcolor="#F3F4F6",
                            color="#374151",
                            expand=1,
                            height=48
                        ),
                        ft.Container(width=12),
                        ft.ElevatedButton(
                            "💳 Pagar",
                            on_click=pay_debt_action,
                            bgcolor="#DC2626",
                            color="#FFFFFF",
                            expand=2,
                            height=48
                        )
                    ]),

                    # Espaço extra para o teclado
                    ft.Container(height=32)

                ], spacing=0, scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.symmetric(horizontal=20, vertical=0),
                bgcolor="#FFFFFF",
                border_radius=ft.border_radius.only(top_left=20, top_right=20)
            ),
            open=True,
            maintain_bottom_view_insets_padding=True,  # Mantém padding quando teclado aparece
            is_scroll_controlled=True,  # Permite scroll quando teclado aparece
            use_safe_area=True  # Usa área segura do dispositivo
        )

        # Abre BottomSheet
        self.page.bottom_sheet = bottom_sheet
        self.page.update()
        print(f"Bottom sheet aberto para dívida {debt_index}")

    def navigation_changed(self, e):
        """Gerencia navegação e atualiza header"""
        selected_index = e.control.selected_index
        self.current_view_index = selected_index

        # Atualiza header
        self.header.content = ft.Row([
            ft.Text(
                ["💳 Controle Financeiro", "🎯 Metas & Objetivos", "💰 Extras & Dívidas", "📊 Dashboard"][selected_index],
                size=20,
                weight=ft.FontWeight.BOLD,
                color="#1F2937"
            )
        ], alignment=ft.MainAxisAlignment.CENTER)

        if selected_index == 0:
            self.content_container.content = self.finances_view
            self.update_finances_view()
        elif selected_index == 1:
            self.content_container.content = self.goals_view
            self.update_goals_view()
        elif selected_index == 2:
            self.content_container.content = self.extras_view
            self.update_extras_view()
        elif selected_index == 3:
            self.content_container.content = self.summary_view
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
            try:
                if index < len(self.expenses):
                    self.expenses.pop(index)
                    self.save_data()
                    self.update_all_views()

                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text("🗑️ Transação removida!"),
                        bgcolor="#DC2626"
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
            except Exception as ex:
                print(f"Erro ao remover despesa: {ex}")

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
        """Atualiza lista de metas"""
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

            # Função para criar handler de clique seguro
            def create_invest_click_handler(goal_index):
                def handle_invest_click(e):
                    print(f"Clique no botão investir para meta {goal_index}")
                    self.show_add_payment_dialog(goal_index)

                return handle_invest_click

            # Função para criar handler de remoção seguro
            def create_remove_click_handler(goal_index):
                def handle_remove_click(e):
                    try:
                        if goal_index < len(self.goals):
                            self.goals.pop(goal_index)
                            self.save_data()
                            self.update_all_views()

                            self.page.snack_bar = ft.SnackBar(
                                content=ft.Text("🗑️ Meta removida!"),
                                bgcolor="#DC2626"
                            )
                            self.page.snack_bar.open = True
                            self.page.update()
                    except Exception as ex:
                        print(f"Erro ao remover meta: {ex}")

                return handle_remove_click

            # Botão de investir
            if can_invest:
                invest_button = ft.ElevatedButton(
                    text="💰 Investir",
                    on_click=create_invest_click_handler(i),
                    bgcolor="#059669",
                    color="#FFFFFF",
                    height=32
                )
            else:
                invest_button = ft.Container(
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
                            on_click=create_remove_click_handler(i),
                            tooltip="Remover meta"
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
        """Atualiza lista de dívidas"""
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

            # Função para criar handler de clique seguro
            def create_pay_click_handler(debt_index):
                def handle_pay_click(e):
                    print(f"Clique no botão pagar para dívida {debt_index}")
                    self.show_pay_debt_dialog(debt_index)

                return handle_pay_click

            # Função para criar handler de remoção seguro
            def create_remove_click_handler(debt_index):
                def handle_remove_click(e):
                    try:
                        if debt_index < len(self.debts):
                            self.debts.pop(debt_index)
                            self.save_data()
                            self.update_all_views()

                            self.page.snack_bar = ft.SnackBar(
                                content=ft.Text("🗑️ Dívida removida!"),
                                bgcolor="#DC2626"
                            )
                            self.page.snack_bar.open = True
                            self.page.update()
                    except Exception as ex:
                        print(f"Erro ao remover dívida: {ex}")

                return handle_remove_click

            # Botão de pagamento
            if can_pay:
                pay_button = ft.ElevatedButton(
                    text="💳 Pagar",
                    on_click=create_pay_click_handler(i),
                    bgcolor="#DC2626",
                    color="#FFFFFF",
                    height=32
                )
            else:
                pay_button = ft.Container(
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
                            on_click=create_remove_click_handler(i),
                            tooltip="Remover dívida"
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
        if hasattr(self, 'content_container') and hasattr(self, 'finances_view'):
            if self.current_view_index == 0:
                self.content_container.content = self.finances_view

    def update_goals_view(self):
        """Atualiza vista de metas"""
        self.create_goals_view()
        if hasattr(self, 'content_container') and hasattr(self, 'goals_view'):
            if self.current_view_index == 1:
                self.content_container.content = self.goals_view

    def update_extras_view(self):
        """Atualiza vista de extras"""
        self.create_extras_view()
        if hasattr(self, 'content_container') and hasattr(self, 'extras_view'):
            if self.current_view_index == 2:
                self.content_container.content = self.extras_view

    def update_summary_view(self):
        """Atualiza vista de resumo"""
        self.create_summary_view()
        if hasattr(self, 'content_container') and hasattr(self, 'summary_view'):
            if self.current_view_index == 3:
                self.content_container.content = self.summary_view

    def update_all_views(self):
        """Atualiza todas as vistas"""
        if self.current_view_index == 0:
            self.update_finances_view()
        elif self.current_view_index == 1:
            self.update_goals_view()
        elif self.current_view_index == 2:
            self.update_extras_view()
        elif self.current_view_index == 3:
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