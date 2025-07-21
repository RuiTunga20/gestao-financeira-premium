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
        """Configuração inicial da página com design premium e leve"""
        self.page.title = "✨ Gestão Financeira Premium"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        # Fundo gradiente suave e claro
        self.page.bgcolor = "#FAFBFF"  # Branco levemente azulado
        self.page.padding = 0
        self.page.window.width = 420
        self.page.window.height = 750

    def load_data(self):
        """Carrega dados do client_storage"""
        try:
            salary_data = self.page.client_storage.get("salary")
            self.base_salary = float(salary_data) if salary_data else 0.0

            # Carrega saldo acumulado de meses anteriores
            accumulated_data = self.page.client_storage.get("accumulated_balance")
            self.accumulated_balance = float(accumulated_data) if accumulated_data else 0.0

            # Salário efetivo = salário base + saldo acumulado
            self.salary = self.base_salary + self.accumulated_balance

            expenses_data = self.page.client_storage.get("expenses")
            self.expenses = json.loads(expenses_data) if expenses_data else []

            goals_data = self.page.client_storage.get("goals")
            self.goals = json.loads(goals_data) if goals_data else []

            # Carrega o mês atual salvo
            current_month_data = self.page.client_storage.get("current_month")
            self.current_month = current_month_data if current_month_data else datetime.now().strftime("%m/%Y")

        except:
            self.base_salary = 0.0
            self.accumulated_balance = 0.0
            self.salary = 0.0
            self.expenses = []
            self.goals = []
            self.current_month = datetime.now().strftime("%m/%Y")

    def save_data(self):
        """Salva dados no client_storage"""
        self.page.client_storage.set("salary", str(self.base_salary))
        self.page.client_storage.set("accumulated_balance", str(self.accumulated_balance))
        self.page.client_storage.set("expenses", json.dumps(self.expenses))
        self.page.client_storage.set("goals", json.dumps(self.goals))
        self.page.client_storage.set("current_month", self.current_month)

    def check_new_month(self):
        """Verifica se é um novo mês e faz a transição automática"""
        new_month = datetime.now().strftime("%m/%Y")

        if new_month != self.current_month and self.current_month != "":
            # Novo mês detectado!
            total_spent, current_balance = self.calculate_totals()

            # Se há saldo positivo, adiciona ao acumulado
            if current_balance > 0:
                self.accumulated_balance += current_balance

            # Limpa as despesas do mês anterior
            self.expenses = []

            # Atualiza o mês atual
            self.current_month = new_month

            # Recalcula o salário efetivo
            self.salary = self.base_salary + self.accumulated_balance

            self.save_data()

    def calculate_totals(self):
        """Calcula totais financeiros"""
        total_spent = sum(expense['amount'] for expense in self.expenses)
        current_balance = self.salary - total_spent
        return total_spent, current_balance

    def analyze_spending_patterns(self):
        """Analisa padrões de gastos"""
        if not self.expenses:
            return [], 0, "", []

        # Análise por descrição (categorias mais comuns)
        descriptions = [expense['description'].lower().strip() for expense in self.expenses]
        description_counter = Counter(descriptions)
        most_common = description_counter.most_common(5)

        # Categoria com maior valor gasto
        expense_by_desc = {}
        for expense in self.expenses:
            desc = expense['description'].lower().strip()
            if desc in expense_by_desc:
                expense_by_desc[desc] += expense['amount']
            else:
                expense_by_desc[desc] = expense['amount']

        highest_spending = max(expense_by_desc.items(), key=lambda x: x[1]) if expense_by_desc else ("", 0)

        # Top 3 gastos mais caros individuais
        top_expenses = sorted(self.expenses, key=lambda x: x['amount'], reverse=True)[:3]

        return most_common, highest_spending[1], highest_spending[0], top_expenses

    def create_elegant_card(self, content, accent_color="#2563EB"):
        """Cria card elegante com glassmorphism claro"""
        return ft.Container(
            content=content,
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=24,
            padding=ft.padding.all(28),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=25,
                color="#1F293740",
                offset=ft.Offset(0, 8)
            )
        )

    def create_premium_button(self, text, on_click, icon=None, color="#2563EB"):
        """Cria botão premium com gradiente elegante"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color="#FFFFFF", size=22) if icon else ft.Container(),
                ft.Text(text, color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            bgcolor=color,
            border_radius=16,
            padding=ft.padding.symmetric(vertical=18, horizontal=28),
            on_click=on_click,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=f"{color}50",
                offset=ft.Offset(0, 6)
            )
        )

    def create_components(self):
        """Cria todos os componentes da interface"""
        self.create_expenses_view()
        self.create_goals_view()
        self.create_summary_view()

        # Container principal com gradiente elegante e claro
        self.main_container = ft.Container(
            content=self.expenses_view,
            expand=True,
            padding=ft.padding.all(24),
            # Gradiente suave e luminoso
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#FAFBFF", "#F1F5F9", "#E2E8F0"]
            )
        )

    def create_expenses_view(self):
        """Cria a vista de despesas com design elegante e leve"""
        # Campo de salário elegante
        self.salary_field = ft.Container(
            content=ft.TextField(
                label="💰 Salário Base Mensal (Kz)",
                value=str(self.base_salary) if self.base_salary > 0 else "",
                keyboard_type=ft.KeyboardType.NUMBER,
                on_change=self.update_salary,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#2563EB",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=16,
                content_padding=ft.padding.all(20),
                text_size=16
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color="#2563EB20",
                offset=ft.Offset(0, 4)
            )
        )

        # Card de resumo financeiro premium
        total_spent, current_balance = self.calculate_totals()

        self.quick_summary_card = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("💎", size=32),
                    ft.Column([
                        ft.Text("Resumo Financeiro", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text(f"Mês: {self.current_month}", size=14, color="#6B7280")
                    ], expand=True, spacing=4)
                ], spacing=16),
                ft.Container(height=16),
                # Mostra breakdown do salário se há acumulado
                ft.Column([
                    ft.Row([
                        ft.Text("Salário Base:", size=13, color="#6B7280"),
                        ft.Text(f"{self.base_salary:,.0f} Kz", size=13, weight=ft.FontWeight.BOLD, color="#2563EB")
                    ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN) if self.accumulated_balance > 0 else ft.Container(),
                    ft.Row([
                        ft.Text("Saldo Anterior:", size=13, color="#6B7280"),
                        ft.Text(f"+{self.accumulated_balance:,.0f} Kz", size=13, weight=ft.FontWeight.BOLD,
                                color="#059669")
                    ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN) if self.accumulated_balance > 0 else ft.Container(),
                    ft.Container(height=8) if self.accumulated_balance > 0 else ft.Container(),
                ]) if self.accumulated_balance > 0 else ft.Container(),
                # Stats em grid elegante
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Total Disponível", size=13, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{self.salary:,.0f}", size=20, weight=ft.FontWeight.BOLD, color="#2563EB"),
                            ft.Text("Kz", size=12, color="#9CA3AF")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                        bgcolor="#EFF6FF",
                        border_radius=16,
                        padding=ft.padding.all(16),
                        expand=True
                    ),
                    ft.Container(width=12),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Gasto", size=13, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{total_spent:,.0f}", size=20, weight=ft.FontWeight.BOLD, color="#EC4899"),
                            ft.Text("Kz", size=12, color="#9CA3AF")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                        bgcolor="#FDF2F8",
                        border_radius=16,
                        padding=ft.padding.all(16),
                        expand=True
                    ),
                    ft.Container(width=12),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Saldo", size=13, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{current_balance:,.0f}", size=20, weight=ft.FontWeight.BOLD,
                                    color="#059669" if current_balance >= 0 else "#DC2626"),
                            ft.Text("Kz", size=12, color="#9CA3AF")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                        bgcolor="#ECFDF5" if current_balance >= 0 else "#FEF2F2",
                        border_radius=16,
                        padding=ft.padding.all(16),
                        expand=True
                    )
                ]),
                ft.Container(height=20),
                # Barra de progresso elegante
                ft.Column([
                    ft.Row([
                        ft.Text("Orçamento Utilizado", size=14, color="#4B5563", weight=ft.FontWeight.BOLD),
                        ft.Text(f"{(total_spent / self.salary * 100):,.1f}%" if self.salary > 0 else "0%",
                                size=14, color="#2563EB", weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=8),
                    ft.ProgressBar(
                        value=min(total_spent / self.salary, 1.0) if self.salary > 0 else 0,
                        bgcolor="#E5E7EB",
                        color="#EC4899" if total_spent > self.salary * 0.8 else "#059669",
                        height=10
                    )
                ])
            ])
        )

        # Campos para adicionar despesa elegantes
        self.expense_description = ft.Container(
            content=ft.TextField(
                label="📝 Descrição da Despesa",
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#2563EB",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=16,
                content_padding=ft.padding.all(20)
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

        self.expense_amount = ft.Container(
            content=ft.TextField(
                label="💵 Valor (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#2563EB",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=16,
                content_padding=ft.padding.all(20)
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

        # Análise de gastos elegante
        most_common, highest_amount, highest_desc, top_expenses = self.analyze_spending_patterns()

        spending_analysis = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("📊", size=28),
                    ft.Column([
                        ft.Text("Insights de Gastos", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Análise dos seus padrões", size=14, color="#6B7280")
                    ], expand=True, spacing=4)
                ], spacing=16),
                ft.Container(height=20),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Text("🔥", size=24),
                                bgcolor="#FEF2F2",
                                border_radius=50,
                                padding=ft.padding.all(12)
                            ),
                            ft.Text("Maior Gasto", size=13, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{highest_amount:,.0f} Kz", size=18, weight=ft.FontWeight.BOLD, color="#DC2626"),
                            ft.Text(highest_desc.title() if highest_desc else "N/A", size=11, color="#9CA3AF")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                        bgcolor="#FAFAFA",
                        border_radius=18,
                        padding=ft.padding.all(20),
                        expand=True
                    ),
                    ft.Container(width=16),
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Text("🎯", size=24),
                                bgcolor="#FFFBEB",
                                border_radius=50,
                                padding=ft.padding.all(12)
                            ),
                            ft.Text("Mais Frequente", size=13, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{most_common[0][1]}x" if most_common else "0x", size=18,
                                    weight=ft.FontWeight.BOLD, color="#D97706"),
                            ft.Text(most_common[0][0].title() if most_common else "N/A", size=11, color="#9CA3AF")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                        bgcolor="#FAFAFA",
                        border_radius=18,
                        padding=ft.padding.all(20),
                        expand=True
                    )
                ])
            ])
        ) if self.expenses else ft.Container()

        # Lista de despesas elegante
        self.expenses_list = ft.ListView(
            spacing=12,
            padding=ft.padding.all(0),
            height=280
        )
        self.update_expenses_list()

        # Container da vista de despesas
        self.expenses_view = ft.Column([
            ft.Text("💳 Controle de Despesas", size=32, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text("Gerencie suas finanças com elegância", size=16, color="#6B7280"),
            ft.Container(height=28),
            self.salary_field,
            ft.Container(height=24),
            self.quick_summary_card,
            ft.Container(height=24),
            spending_analysis,
            ft.Container(height=32),
            ft.Text("➕ Nova Despesa", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),
            self.expense_description,
            ft.Container(height=16),
            self.expense_amount,
            ft.Container(height=24),
            self.create_premium_button("Adicionar Despesa", self.add_expense, ft.icons.ADD_CIRCLE, "#2563EB"),
            ft.Container(height=32),
            ft.Text("📋 Histórico de Despesas", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),
            self.create_elegant_card(self.expenses_list)
        ], scroll=ft.ScrollMode.AUTO)

    def create_goals_view(self):
        """Cria a vista de metas com design premium"""
        _, current_balance = self.calculate_totals()

        # Card de potencial de poupança elegante
        self.savings_potential_card = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("💰", size=32),
                    ft.Column([
                        ft.Text("Potencial de Poupança", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Seu poder de investimento mensal", size=14, color="#6B7280")
                    ], expand=True, spacing=4)
                ], spacing=16),
                ft.Container(height=28),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Disponível para poupar", size=14, color="#6B7280"),
                        ft.Text(f"{current_balance:,.0f} Kz", size=36, weight=ft.FontWeight.BOLD,
                                color="#059669" if current_balance >= 0 else "#DC2626"),
                        ft.Container(height=12),
                        ft.Container(
                            content=ft.Text(
                                "🎯 Pronto para seus objetivos!" if current_balance > 0 else "📈 Ajuste seus gastos",
                                size=14, color="#059669" if current_balance > 0 else "#DC2626",
                                weight=ft.FontWeight.BOLD),
                            bgcolor="#ECFDF5" if current_balance > 0 else "#FEF2F2",
                            border_radius=25,
                            padding=ft.padding.symmetric(horizontal=20, vertical=10)
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor="#F8FAFC",
                    border_radius=20,
                    padding=ft.padding.all(24)
                )
            ])
        )

        # Campos para adicionar meta elegantes
        self.goal_name = ft.Container(
            content=ft.TextField(
                label="🎯 Nome do Artigo",
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=16,
                content_padding=ft.padding.all(20)
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

        self.goal_total_cost = ft.Container(
            content=ft.TextField(
                label="💎 Custo Total (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=16,
                content_padding=ft.padding.all(20)
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

        self.goal_monthly_saving = ft.Container(
            content=ft.TextField(
                label="📅 Valor a Poupar por Mês (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=16,
                content_padding=ft.padding.all(20),
                on_change=self.calculate_goal_time
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

        self.goal_time_estimate = ft.Container(
            content=ft.Text("⏱️ Tempo estimado: -- meses", size=16, color="#D97706", weight=ft.FontWeight.BOLD),
            bgcolor="#FFFBEB",
            border_radius=25,
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        )

        # Lista de metas
        self.goals_list = ft.ListView(
            spacing=16,
            padding=ft.padding.all(0),
            height=350
        )
        self.update_goals_list()

        # Container da vista de metas
        self.goals_view = ft.Column([
            ft.Text("🎯 Metas de Poupança", size=32, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text("Transforme sonhos em objetivos alcançáveis", size=16, color="#6B7280"),
            ft.Container(height=28),
            self.savings_potential_card,
            ft.Container(height=32),
            ft.Text("✨ Nova Meta", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),
            self.goal_name,
            ft.Container(height=16),
            self.goal_total_cost,
            ft.Container(height=16),
            self.goal_monthly_saving,
            ft.Container(height=16),
            self.goal_time_estimate,
            ft.Container(height=24),
            self.create_premium_button("Criar Meta", self.add_goal, ft.icons.ROCKET_LAUNCH, "#059669"),
            ft.Container(height=32),
            ft.Text("🏆 Minhas Metas", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),
            self.create_elegant_card(self.goals_list)
        ], scroll=ft.ScrollMode.AUTO)

    def create_summary_view(self):
        """Cria a vista de resumo premium com análises detalhadas"""
        total_spent, current_balance = self.calculate_totals()
        most_common, highest_amount, highest_desc, top_expenses = self.analyze_spending_patterns()

        # Stats cards elegantes
        stats_row = ft.Row([
            self.create_stats_card("💰", "Salário Total", f"{self.salary:,.0f}", "Kz", "#2563EB", "#EFF6FF"),
            self.create_stats_card("💸", "Gastos", f"{total_spent:,.0f}", "Kz", "#EC4899", "#FDF2F8"),
            self.create_stats_card("💎", "Saldo", f"{current_balance:,.0f}", "Kz",
                                   "#059669" if current_balance >= 0 else "#DC2626",
                                   "#ECFDF5" if current_balance >= 0 else "#FEF2F2")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Card dos Top 3 gastos mais avultados
        top_expenses_card = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("💎", size=32),
                    ft.Column([
                        ft.Text("Gastos Mais Avultados", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Suas maiores despesas individuais", size=14, color="#6B7280")
                    ], expand=True, spacing=4)
                ], spacing=16),
                ft.Container(height=20),
                ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Text("🥇", size=20),
                                bgcolor="#FEF2F2",
                                border_radius=25,
                                padding=ft.padding.all(8)
                            ),
                            ft.Column([
                                ft.Text(expense['description'], size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
                                ft.Text(expense['date'], size=12, color="#6B7280")
                            ], expand=True, spacing=2),
                            ft.Text(f"{expense['amount']:,.0f} Kz", size=16, weight=ft.FontWeight.BOLD, color="#DC2626")
                        ]),
                        bgcolor="#FAFAFA",
                        border_radius=12,
                        padding=ft.padding.all(12)
                    ) for i, expense in enumerate(top_expenses[:3])
                ], spacing=8) if top_expenses else [ft.Text("Nenhuma despesa registrada", size=14, color="#6B7280")]
            ])
        ) if self.expenses else ft.Container()

        # Análise avançada de gastos por categoria
        spending_insights = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("📊", size=32),
                    ft.Column([
                        ft.Text("Análise por Categoria", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Padrões de gastos mais recorrentes", size=14, color="#6B7280")
                    ], expand=True, spacing=4)
                ], spacing=16),
                ft.Container(height=20),
                ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Text(f"#{i + 1}", size=16, color="#FFFFFF", weight=ft.FontWeight.BOLD),
                                bgcolor="#059669" if i == 0 else "#D97706" if i == 1 else "#EC4899",
                                border_radius=20,
                                padding=ft.padding.all(8),
                                width=40,
                                height=40
                            ),
                            ft.Column([
                                ft.Text(category[0].title(), size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
                                ft.Text(f"Repetida {category[1]} vezes", size=12, color="#6B7280")
                            ], expand=True, spacing=2),
                            ft.Text(f"{category[1]}x", size=16, weight=ft.FontWeight.BOLD,
                                    color="#059669" if i == 0 else "#D97706" if i == 1 else "#EC4899")
                        ]),
                        bgcolor="#FAFAFA",
                        border_radius=12,
                        padding=ft.padding.all(12)
                    ) for i, category in enumerate(most_common[:3])
                ], spacing=8) if most_common else [
                    ft.Text("Ainda não há padrões para analisar", size=14, color="#6B7280")]
            ])
        ) if self.expenses else ft.Container()

        # Análise de metas
        active_goals = len(self.goals)
        total_goal_value = sum(goal['total_cost'] for goal in self.goals)
        total_saved_for_goals = sum(goal.get('saved_amount', 0) for goal in self.goals)

        goals_analysis = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("🎯", size=32),
                    ft.Column([
                        ft.Text("Status das Metas", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Progresso dos seus objetivos", size=14, color="#6B7280")
                    ], expand=True, spacing=4)
                ], spacing=16),
                ft.Container(height=24),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Metas Ativas", size=14, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(str(active_goals), size=28, weight=ft.FontWeight.BOLD, color="#059669")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#ECFDF5",
                        border_radius=18,
                        padding=ft.padding.all(20),
                        expand=True
                    ),
                    ft.Container(width=12),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Total das Metas", size=14, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{total_goal_value:,.0f}", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),
                            ft.Text("Kz", size=12, color="#9CA3AF")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#F8FAFC",
                        border_radius=18,
                        padding=ft.padding.all(20),
                        expand=True
                    ),
                    ft.Container(width=12),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Já Investido", size=14, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{total_saved_for_goals:,.0f}", size=20, weight=ft.FontWeight.BOLD,
                                    color="#059669"),
                            ft.Text("Kz", size=12, color="#9CA3AF")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#ECFDF5",
                        border_radius=18,
                        padding=ft.padding.all(20),
                        expand=True
                    )
                ])
            ])
        )

        # Lista de despesas recentes elegante
        recent_expenses = self.expenses[-8:] if len(self.expenses) > 8 else self.expenses
        recent_expenses_list = ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.TRENDING_DOWN, color="#EC4899", size=18),
                        bgcolor="#FDF2F8",
                        border_radius=25,
                        padding=ft.padding.all(10)
                    ),
                    ft.Column([
                        ft.Text(expense['description'], size=15, weight=ft.FontWeight.NORMAL, color="#1F2937"),
                        ft.Text(expense['date'], size=12, color="#6B7280")
                    ], expand=True, spacing=4),
                    ft.Text(f"{expense['amount']:,.0f} Kz", size=15, weight=ft.FontWeight.BOLD, color="#EC4899")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor="#FFFFFF",
                border=ft.border.all(1, "#F3F4F6"),
                border_radius=16,
                padding=ft.padding.all(16)
            ) for expense in reversed(recent_expenses)
        ], spacing=10)

        # Container da vista de resumo
        self.summary_view = ft.Column([
            ft.Text("📈 Dashboard Financeiro", size=32, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text(f"Visão completa do mês {self.current_month}", size=16, color="#6B7280"),
            ft.Container(height=28),
            stats_row,
            ft.Container(height=24),
            top_expenses_card,
            ft.Container(height=24),
            spending_insights,
            ft.Container(height=24),
            goals_analysis,
            ft.Container(height=32),
            ft.Text("🕒 Transações Recentes", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),
            self.create_elegant_card(
                recent_expenses_list if recent_expenses else ft.Text("Nenhuma transação registrada ainda",
                                                                     size=14, color="#6B7280")
            )
        ], scroll=ft.ScrollMode.AUTO)

    def create_stats_card(self, icon, title, value, unit, color, bg_color):
        """Cria um card de estatística elegante"""
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(icon, size=28),
                    bgcolor=bg_color,
                    border_radius=50,
                    padding=ft.padding.all(12)
                ),
                ft.Text(title, size=12, color="#6B7280", weight=ft.FontWeight.BOLD),
                ft.Text(value, size=18, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(unit, size=10, color="#9CA3AF")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=20,
            padding=ft.padding.all(20),
            width=115,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color="#1F293720",
                offset=ft.Offset(0, 4)
            )
        )

    def setup_navigation(self):
        """Configura a navegação elegante"""
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon=ft.icons.CREDIT_CARD_OUTLINED, label="Despesas",
                                         selected_icon=ft.icons.CREDIT_CARD),
                ft.NavigationDestination(icon=ft.icons.SAVINGS_OUTLINED, label="Metas", selected_icon=ft.icons.SAVINGS),
                ft.NavigationDestination(icon=ft.icons.ANALYTICS_OUTLINED, label="Dashboard",
                                         selected_icon=ft.icons.ANALYTICS)
            ],
            on_change=self.navigation_changed,
            bgcolor="#FFFFFF",
            indicator_color="#EFF6FF",
            selected_index=0,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW
        )

        # Adiciona os componentes à página
        self.page.add(
            ft.Column([
                self.main_container,
                self.navigation_bar
            ], expand=True, spacing=0)
        )

    def show_add_payment_dialog(self, goal_index):
        """Mostra diálogo elegante para adicionar pagamento à meta"""
        _, current_balance = self.calculate_totals()

        payment_field = ft.TextField(
            label="Valor do Pagamento (Kz)",
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor="#FFFFFF",
            border_color="#E5E7EB",
            focused_border_color="#059669",
            border_radius=12,
            content_padding=ft.padding.all(16)
        )

        def add_payment(e):
            try:
                amount = float(payment_field.value)
                if amount > 0:
                    # Verifica se há saldo suficiente
                    if amount <= current_balance:
                        # Adiciona o pagamento à meta
                        self.goals[goal_index]['saved_amount'] = self.goals[goal_index].get('saved_amount', 0) + amount

                        # Deduz o valor como uma despesa automática
                        payment_expense = {
                            'description': f"Pagamento: {self.goals[goal_index]['name']}",
                            'amount': amount,
                            'date': datetime.now().strftime("%d/%m/%Y")
                        }
                        self.expenses.append(payment_expense)

                        self.save_data()
                        self.update_all_views()
                        dialog.open = False
                        self.page.update()
                    else:
                        # Mostra erro de saldo insuficiente
                        error_text.value = f"Saldo insuficiente! Disponível: {current_balance:,.0f} Kz"
                        error_text.color = "#DC2626"
                        self.page.update()
            except ValueError:
                pass

        error_text = ft.Text("", size=12)

        dialog = ft.AlertDialog(
            title=ft.Text(f"💰 Adicionar Pagamento", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),
            content=ft.Column([
                ft.Text(f"Meta: {self.goals[goal_index]['name']}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"Custo Total: {self.goals[goal_index]['total_cost']:,.0f} Kz", size=14, color="#6B7280"),
                ft.Text(f"Já investido: {self.goals[goal_index].get('saved_amount', 0):,.0f} Kz", size=14,
                        color="#059669"),
                ft.Text(f"Saldo disponível: {current_balance:,.0f} Kz", size=14, color="#2563EB"),
                ft.Container(height=16),
                payment_field,
                error_text
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False) or self.page.update(),
                              style=ft.ButtonStyle(color="#6B7280")),
                ft.ElevatedButton("Investir", on_click=add_payment, bgcolor="#059669", color="#FFFFFF",
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)))
            ],
            shape=ft.RoundedRectangleBorder(radius=20)
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def navigation_changed(self, e):
        """Gerencia mudanças na navegação"""
        selected_index = e.control.selected_index

        if selected_index == 0:
            self.main_container.content = self.expenses_view
            self.update_expenses_view()
        elif selected_index == 1:
            self.main_container.content = self.goals_view
            self.update_goals_view()
        elif selected_index == 2:
            self.main_container.content = self.summary_view
            self.update_summary_view()

        self.page.update()

    def update_salary(self, e):
        """Atualiza o salário base"""
        try:
            self.base_salary = float(e.control.value) if e.control.value else 0.0
            self.salary = self.base_salary + self.accumulated_balance
            self.save_data()
            self.update_all_views()
        except ValueError:
            pass

    def add_expense(self, e):
        """Adiciona uma nova despesa"""
        description_field = self.expense_description.content
        amount_field = self.expense_amount.content

        if not description_field.value or not amount_field.value:
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

            # Limpa os campos
            description_field.value = ""
            amount_field.value = ""

            self.update_all_views()
        except ValueError:
            pass

    def remove_expense(self, index):
        """Remove uma despesa"""

        def remove(e):
            self.expenses.pop(index)
            self.save_data()
            self.update_all_views()

        return remove

    def calculate_goal_time(self, e):
        """Calcula o tempo estimado para atingir a meta"""
        total_cost_field = self.goal_total_cost.content
        monthly_saving_field = self.goal_monthly_saving.content

        try:
            if total_cost_field.value and monthly_saving_field.value:
                total_cost = float(total_cost_field.value)
                monthly_saving = float(monthly_saving_field.value)

                if monthly_saving > 0:
                    months = math.ceil(total_cost / monthly_saving)
                    self.goal_time_estimate.content.value = f"⏱️ Tempo estimado: {months} meses"
                else:
                    self.goal_time_estimate.content.value = "⏱️ Tempo estimado: -- meses"

                self.page.update()
        except ValueError:
            self.goal_time_estimate.content.value = "⏱️ Tempo estimado: -- meses"
            self.page.update()

    def add_goal(self, e):
        """Adiciona uma nova meta"""
        name_field = self.goal_name.content
        total_cost_field = self.goal_total_cost.content
        monthly_saving_field = self.goal_monthly_saving.content

        if not all([name_field.value, total_cost_field.value, monthly_saving_field.value]):
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

            # Limpa os campos
            name_field.value = ""
            total_cost_field.value = ""
            monthly_saving_field.value = ""
            self.goal_time_estimate.content.value = "⏱️ Tempo estimado: -- meses"

            self.update_all_views()
        except ValueError:
            pass

    def remove_goal(self, index):
        """Remove uma meta"""

        def remove(e):
            self.goals.pop(index)
            self.save_data()
            self.update_all_views()

        return remove

    def update_expenses_list(self):
        """Atualiza a lista de despesas"""
        self.expenses_list.controls.clear()

        for i, expense in enumerate(reversed(self.expenses)):
            # Destaca pagamentos para metas
            is_goal_payment = expense['description'].startswith("Pagamento:")

            expense_item = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(
                            ft.icons.SAVINGS if is_goal_payment else ft.icons.TRENDING_DOWN,
                            color="#059669" if is_goal_payment else "#EC4899",
                            size=20
                        ),
                        bgcolor="#ECFDF5" if is_goal_payment else "#FDF2F8",
                        border_radius=30,
                        padding=ft.padding.all(12)
                    ),
                    ft.Column([
                        ft.Text(expense['description'], size=15, weight=ft.FontWeight.NORMAL,
                                color="#059669" if is_goal_payment else "#1F2937"),
                        ft.Text(expense['date'], size=12, color="#6B7280")
                    ], expand=True, spacing=4),
                    ft.Column([
                        ft.Text(f"{expense['amount']:,.0f} Kz", size=15, weight=ft.FontWeight.BOLD,
                                color="#059669" if is_goal_payment else "#EC4899"),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color="#DC2626",
                            icon_size=18,
                            on_click=self.remove_expense(len(self.expenses) - 1 - i),
                            tooltip="Remover despesa"
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=0)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor="#FFFFFF",
                border=ft.border.all(1, "#A7F3D0" if is_goal_payment else "#F3F4F6"),
                border_radius=16,
                padding=ft.padding.all(16),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color="#1F293715",
                    offset=ft.Offset(0, 2)
                )
            )
            self.expenses_list.controls.append(expense_item)

    def update_goals_list(self):
        """Atualiza a lista de metas"""
        self.goals_list.controls.clear()

        for i, goal in enumerate(self.goals):
            saved_amount = goal.get('saved_amount', 0)
            progress = saved_amount / goal['total_cost'] if goal['total_cost'] > 0 else 0
            remaining_cost = goal['total_cost'] - saved_amount
            remaining_months = math.ceil(remaining_cost / goal['monthly_saving']) if goal[
                                                                                         'monthly_saving'] > 0 and remaining_cost > 0 else 0

            # Ícone e status baseado no progresso
            if progress >= 1.0:
                icon = ft.icons.CHECK_CIRCLE
                icon_color = "#059669"
                bg_color = "#ECFDF5"
                status_text = "🎉 Meta Concluída!"
                status_color = "#059669"
            elif progress >= 0.75:
                icon = ft.icons.ROCKET_LAUNCH
                icon_color = "#D97706"
                bg_color = "#FFFBEB"
                status_text = f"🔥 Quase lá! {remaining_months} meses"
                status_color = "#D97706"
            else:
                icon = ft.icons.SAVINGS
                icon_color = "#2563EB"
                bg_color = "#EFF6FF"
                status_text = f"⏱️ {remaining_months} meses restantes"
                status_color = "#6B7280"

            goal_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(icon, color=icon_color, size=26),
                            bgcolor=bg_color,
                            border_radius=30,
                            padding=ft.padding.all(14)
                        ),
                        ft.Column([
                            ft.Text(goal['name'], size=17, weight=ft.FontWeight.BOLD, color="#1F2937"),
                            ft.Text(status_text, size=13, color=status_color, weight=ft.FontWeight.NORMAL)
                        ], expand=True, spacing=4),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color="#DC2626",
                            icon_size=20,
                            on_click=self.remove_goal(i),
                            tooltip="Remover meta"
                        )
                    ]),
                    ft.Container(height=20),
                    # Barra de progresso elegante
                    ft.Column([
                        ft.ProgressBar(
                            value=min(progress, 1.0),
                            bgcolor="#E5E7EB",
                            color="#059669" if progress >= 1.0 else "#2563EB",
                            height=10
                        ),
                        ft.Container(height=12),
                        ft.Row([
                            ft.Text(f"{saved_amount:,.0f} / {goal['total_cost']:,.0f} Kz",
                                    size=14, color="#6B7280"),
                            ft.Text(f"{progress * 100:.1f}%", size=14, weight=ft.FontWeight.BOLD,
                                    color="#059669" if progress >= 1.0 else "#2563EB")
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    ft.Container(height=20),
                    # Botão para adicionar pagamento elegante
                    ft.Container(
                        content=ft.Text("💰 Investir na Meta", size=14, weight=ft.FontWeight.BOLD, color="#059669"),
                        bgcolor="#ECFDF5",
                        border=ft.border.all(1, "#A7F3D0"),
                        border_radius=25,
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        on_click=lambda e, idx=i: self.show_add_payment_dialog(idx)
                    ) if progress < 1.0 else ft.Container(
                        content=ft.Text("✅ Objetivo Alcançado!", size=14, weight=ft.FontWeight.BOLD, color="#059669"),
                        bgcolor="#ECFDF5",
                        border=ft.border.all(1, "#A7F3D0"),
                        border_radius=25,
                        padding=ft.padding.symmetric(horizontal=20, vertical=12)
                    )
                ]),
                bgcolor="#FFFFFF",
                border=ft.border.all(1, "#E5E7EB"),
                border_radius=24,
                padding=ft.padding.all(24),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=15,
                    color="#1F293720",
                    offset=ft.Offset(0, 4)
                )
            )
            self.goals_list.controls.append(goal_card)

    def update_expenses_view(self):
        """Atualiza a vista de despesas"""
        self.create_expenses_view()
        if hasattr(self, 'main_container') and hasattr(self, 'expenses_view'):
            current_view = self.main_container.content
            if current_view == self.expenses_view or self.navigation_bar.selected_index == 0:
                self.main_container.content = self.expenses_view

    def update_goals_view(self):
        """Atualiza a vista de metas"""
        self.create_goals_view()
        if hasattr(self, 'main_container') and hasattr(self, 'goals_view'):
            current_view = self.main_container.content
            if current_view == self.goals_view or self.navigation_bar.selected_index == 1:
                self.main_container.content = self.goals_view

    def update_summary_view(self):
        """Atualiza a vista de resumo"""
        self.create_summary_view()
        if hasattr(self, 'main_container') and hasattr(self, 'summary_view'):
            current_view = self.main_container.content
            if current_view == self.summary_view or self.navigation_bar.selected_index == 2:
                self.main_container.content = self.summary_view

    def update_all_views(self):
        """Atualiza todas as vistas"""
        current_index = getattr(self.navigation_bar, 'selected_index', 0)

        if current_index == 0:
            self.update_expenses_view()
        elif current_index == 1:
            self.update_goals_view()
        elif current_index == 2:
            self.update_summary_view()

        self.page.update()


def main(page: ft.Page):
    """Função principal da aplicação"""
    app = FinancialApp(page)


if __name__ == "__main__":
    ft.app(target=main)