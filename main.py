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
        self.page.title = "Gestão Financeira Premium"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        # Fundo gradiente suave e claro
        self.page.bgcolor = "#FAFBFF"  # Branco levemente azulado
        self.page.padding = 0

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
            
            # Carrega dívidas
            debts_data = self.page.client_storage.get("debts")
            self.debts = json.loads(debts_data) if debts_data else []

            # Carrega o mês atual salvo
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
        # Separa despesas reais (valores positivos) de rendas extras (valores negativos)
        total_spent = sum(expense['amount'] for expense in self.expenses if expense['amount'] > 0)
        current_balance = self.salary - total_spent
        return total_spent, current_balance

    def analyze_spending_patterns(self):
        """Analisa padrões de gastos"""
        # Filtra apenas despesas reais (valores positivos, exclui rendas extras)
        real_expenses = [expense for expense in self.expenses if expense['amount'] > 0]
        
        if not real_expenses:
            return [], 0, "", []

        # Análise por descrição (categorias mais comuns) - apenas despesas reais
        descriptions = [expense['description'].lower().strip() for expense in real_expenses]
        description_counter = Counter(descriptions)
        most_common = description_counter.most_common(5)

        # Categoria com maior valor gasto - apenas despesas reais
        expense_by_desc = {}
        for expense in real_expenses:
            desc = expense['description'].lower().strip()
            if desc in expense_by_desc:
                expense_by_desc[desc] += expense['amount']
            else:
                expense_by_desc[desc] = expense['amount']

        highest_spending = max(expense_by_desc.items(), key=lambda x: x[1]) if expense_by_desc else ("", 0)

        # Top 3 gastos mais caros individuais - apenas despesas reais
        top_expenses = sorted(real_expenses, key=lambda x: x['amount'], reverse=True)[:3]

        return most_common, highest_spending[1], highest_spending[0], top_expenses

    def create_elegant_card(self, content, accent_color="#2563EB"):
        """Cria card elegante com glassmorphism claro e compacto"""
        return ft.Container(
            content=content,
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=16,  # Reduzido de 20 para 16
            padding=ft.padding.all(16),  # Reduzido de 20 para 16
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,  # Reduzido de 20 para 15
                color="#1F293740",
                offset=ft.Offset(0, 4)  # Reduzido de 6 para 4
            )
        )

    def create_premium_button(self, text, on_click, icon=None, color="#2563EB"):
        """Cria botão premium com gradiente elegante"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color="#FFFFFF", size=20) if icon else ft.Container(),  # Reduzido de 22 para 20
                ft.Text(text, color="#FFFFFF", size=15, weight=ft.FontWeight.BOLD)  # Reduzido de 16 para 15
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            bgcolor=color,
            border_radius=14,  # Reduzido de 16 para 14
            padding=ft.padding.symmetric(vertical=16, horizontal=24),  # Reduzido padding
            on_click=on_click,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,  # Reduzido de 15 para 12
                color=f"{color}50",
                offset=ft.Offset(0, 4)  # Reduzido de 6 para 4
            )
        )

    def create_components(self):
        """Cria todos os componentes da interface"""
        self.create_expenses_view()
        self.create_goals_view()
        self.create_finance_view()  # Nova view unificada
        self.create_summary_view()

        # Container principal com gradiente elegante e claro
        self.main_container = ft.Container(
            content=self.expenses_view,
            expand=True,
            padding=ft.padding.all(12),  # Reduzido de 16 para 12
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
                label="Salário Base Mensal (Kz)",
                value=str(self.base_salary) if self.base_salary > 0 else "",
                keyboard_type=ft.KeyboardType.NUMBER,
                on_change=self.update_salary,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#2563EB",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=14,  # Reduzido de 16 para 14
                content_padding=ft.padding.all(16),  # Reduzido de 20 para 16
                text_size=15  # Reduzido de 16 para 15
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,  # Reduzido de 10 para 8
                color="#2563EB20",
                offset=ft.Offset(0, 3)  # Reduzido de 4 para 3
            )
        )

        # Card de resumo financeiro premium
        total_spent, current_balance = self.calculate_totals()

        self.quick_summary_card = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("💎", size=28),  # Reduzido de 32 para 28
                    ft.Column([
                        ft.Text("Resumo Financeiro", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 24
                        ft.Text(f"Mês: {self.current_month}", size=13, color="#6B7280")  # Reduzido de 14
                    ], expand=True, spacing=3)  # Reduzido de 4 para 3
                ], spacing=12),  # Reduzido de 16 para 12
                ft.Container(height=12),  # Reduzido de 16 para 12
                # Mostra breakdown do salário se há acumulado
                ft.Column([
                    ft.Row([
                        ft.Text("Salário Base:", size=12, color="#6B7280"),  # Reduzido de 13
                        ft.Text(f"{self.base_salary} Kz", size=12, weight=ft.FontWeight.BOLD, color="#2563EB")
                    ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN) if self.accumulated_balance > 0 else ft.Container(),
                    ft.Row([
                        ft.Text("Saldo Anterior:", size=12, color="#6B7280"),
                        ft.Text(f"+{self.accumulated_balance:,.0f} Kz", size=12, weight=ft.FontWeight.BOLD,
                                color="#059669")
                    ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN) if self.accumulated_balance > 0 else ft.Container(),
                    ft.Container(height=6) if self.accumulated_balance > 0 else ft.Container(),  # Reduzido de 8
                ]) if self.accumulated_balance > 0 else ft.Container(),
                # Mostra rendas extras se houver
                ft.Column([
                    ft.Row([
                        ft.Text("Rendas Extras:", size=10, color="#6B7280"),  # Reduzido de 11
                        ft.Text(f"+{sum(abs(expense['amount']) for expense in self.expenses if expense['amount'] < 0):,.0f} Kz", 
                               size=10, weight=ft.FontWeight.BOLD, color="#059669")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=5)  # Reduzido de 6
                ]) if any(expense['amount'] < 0 for expense in self.expenses) else ft.Container(),
                # Stats row simples e elegante
                ft.Row([
                    self.create_stats_card("💰", "Salário Total", f"{self.salary:,.0f}", "Kz", "#2563EB", "#EFF6FF"),
                    self.create_stats_card("💸", "Gastos", f"{total_spent:,.0f}", "Kz", "#EC4899", "#FDF2F8"),
                    self.create_stats_card("💎", "Saldo", f"{current_balance:,.0f}", "Kz",
                                           "#059669" if current_balance >= 0 else "#DC2626",
                                           "#ECFDF5" if current_balance >= 0 else "#FEF2F2")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=12),  # Reduzido de 15
                # Barra de progresso compacta
                ft.Column([
                    ft.Row([
                        ft.Text("Orçamento Utilizado", size=11, color="#4B5563", weight=ft.FontWeight.BOLD),  # Reduzido de 12
                        ft.Text(f"{(total_spent / self.salary * 100):,.1f}%" if self.salary > 0 else "0%",
                                size=11, color="#2563EB", weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=5),  # Reduzido de 6
                    ft.ProgressBar(
                        value=min(total_spent / self.salary, 1.0) if self.salary > 0 else 0,
                        bgcolor="#E5E7EB",
                        color="#EC4899" if total_spent > self.salary * 0.8 else "#059669",
                        height=7  # Reduzido de 8
                    )
                ])
            ])
        )

        # Campos para adicionar despesa elegantes
        self.expense_description = ft.Container(
            content=ft.TextField(
                label="Descrição da Despesa",
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#2563EB",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=14,  # Reduzido de 16
                content_padding=ft.padding.all(16)  # Reduzido de 20
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,  # Reduzido de 8
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

        self.expense_amount = ft.Container(
            content=ft.TextField(
                label="Valor (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#2563EB",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=14,
                content_padding=ft.padding.all(16)
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

        # Análise de gastos elegante
        most_common, highest_amount, highest_desc, top_expenses = self.analyze_spending_patterns()

        spending_analysis = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("📊", size=24),  # Reduzido de 28
                    ft.Column([
                        ft.Text("Insights de Gastos", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 20
                        ft.Text("Análise dos seus padrões", size=13, color="#6B7280")  # Reduzido de 14
                    ], expand=True, spacing=3)
                ], spacing=12),  # Reduzido de 16
                ft.Container(height=16),  # Reduzido de 20
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Text("🔥", size=20),  # Reduzido de 24
                                bgcolor="#FEF2F2",
                                border_radius=50,
                                padding=ft.padding.all(10)  # Reduzido de 12
                            ),
                            ft.Text("Maior Gasto", size=12, color="#6B7280", weight=ft.FontWeight.BOLD),  # Reduzido de 13
                            ft.Text(f"{highest_amount:,.0f} Kz", size=16, weight=ft.FontWeight.BOLD, color="#DC2626"),  # Reduzido de 18
                            ft.Text(highest_desc.title() if highest_desc else "N/A", size=10, color="#9CA3AF")  # Reduzido de 11
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),  # Reduzido de 8
                        bgcolor="#FAFAFA",
                        border_radius=16,  # Reduzido de 18
                        padding=ft.padding.all(16),  # Reduzido de 20
                        expand=True
                    ),
                    ft.Container(width=12),  # Reduzido de 16
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Text("🎯", size=20),
                                bgcolor="#FFFBEB",
                                border_radius=50,
                                padding=ft.padding.all(10)
                            ),
                            ft.Text("Mais Frequente", size=12, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{most_common[0][1]}x" if most_common else "0x", size=16,
                                    weight=ft.FontWeight.BOLD, color="#D97706"),
                            ft.Text(most_common[0][0].title() if most_common else "N/A", size=10, color="#9CA3AF")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
                        bgcolor="#FAFAFA",
                        border_radius=16,
                        padding=ft.padding.all(16),
                        expand=True
                    )
                ])
            ])
        ) if self.expenses else ft.Container()

        # Lista de despesas elegante
        self.expenses_list = ft.ListView(
            spacing=10,  # Reduzido de 12
            padding=ft.padding.all(0),
            height=240  # Reduzido de 280
        )
        self.update_expenses_list()

        # Container da vista de despesas
        self.expenses_view = ft.Column([
            ft.Text("Controle de Despesas", size=28, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 32
            ft.Text("Gerencie suas finanças com elegância", size=15, color="#6B7280"),  # Reduzido de 16
            ft.Container(height=20),  # Reduzido de 28
            self.salary_field,
            ft.Container(height=18),  # Reduzido de 24
            self.quick_summary_card,
            ft.Container(height=18),  # Reduzido de 24
            spending_analysis,
            ft.Container(height=24),  # Reduzido de 32
            ft.Text("Nova Despesa", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 22
            ft.Container(height=12),  # Reduzido de 16
            self.expense_description,
            ft.Container(height=12),  # Reduzido de 16
            self.expense_amount,
            ft.Container(height=18),  # Reduzido de 24
            self.create_premium_button("Adicionar Despesa", self.add_expense, ft.icons.ADD_CIRCLE, "#2563EB"),
            ft.Container(height=24),  # Reduzido de 32
            ft.Text("Histórico de Despesas", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 22
            ft.Container(height=12),  # Reduzido de 16
            self.create_elegant_card(self.expenses_list)
        ], scroll=ft.ScrollMode.AUTO)

    def create_goals_view(self):
        """Cria a vista de metas com design premium"""
        _, current_balance = self.calculate_totals()

        # Card de potencial de poupança elegante
        self.savings_potential_card = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("💰", size=28),  # Reduzido de 32
                    ft.Column([
                        ft.Text("Potencial de Poupança", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 24
                        ft.Text("Seu poder de investimento mensal", size=13, color="#6B7280")  # Reduzido de 14
                    ], expand=True, spacing=3)
                ], spacing=12),  # Reduzido de 16
                ft.Container(height=20),  # Reduzido de 28
                ft.Container(
                    content=ft.Column([
                        ft.Text("Disponível para poupar", size=13, color="#6B7280"),  # Reduzido de 14
                        ft.Text(f"{current_balance:,.0f} Kz", size=32, weight=ft.FontWeight.BOLD,  # Reduzido de 36
                                color="#059669" if current_balance >= 0 else "#DC2626"),
                        ft.Container(height=10),  # Reduzido de 12
                        ft.Container(
                            content=ft.Text(
                                "Pronto para seus objetivos!" if current_balance > 0 else "Ajuste seus gastos",
                                size=13, color="#059669" if current_balance > 0 else "#DC2626",  # Reduzido de 14
                                weight=ft.FontWeight.BOLD),
                            bgcolor="#ECFDF5" if current_balance > 0 else "#FEF2F2",
                            border_radius=20,  # Reduzido de 25
                            padding=ft.padding.symmetric(horizontal=16, vertical=8)  # Reduzido padding
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor="#F8FAFC",
                    border_radius=16,  # Reduzido de 20
                    padding=ft.padding.all(20)  # Reduzido de 24
                )
            ])
        )

        # Campos para adicionar meta elegantes
        self.goal_name = ft.Container(
            content=ft.TextField(
                label="Nome do Artigo",
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=14,  # Reduzido de 16
                content_padding=ft.padding.all(16)  # Reduzido de 20
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,  # Reduzido de 8
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

        self.goal_total_cost = ft.Container(
            content=ft.TextField(
                label="Custo Total (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=14,
                content_padding=ft.padding.all(16)
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

        self.goal_monthly_saving = ft.Container(
            content=ft.TextField(
                label="Valor a Poupar por Mês (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=14,
                content_padding=ft.padding.all(16),
                on_change=self.calculate_goal_time
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

        self.goal_time_estimate = ft.Container(
            content=ft.Text("Tempo estimado: -- meses", size=15, color="#D97706", weight=ft.FontWeight.BOLD),  # Reduzido de 16
            bgcolor="#FFFBEB",
            border_radius=20,  # Reduzido de 25
            padding=ft.padding.symmetric(horizontal=16, vertical=10)  # Reduzido padding
        )

        # Lista de metas
        self.goals_list = ft.ListView(
            spacing=12,  # Reduzido de 16
            padding=ft.padding.all(0),
            height=300  # Reduzido de 350
        )
        self.update_goals_list()

        # Container da vista de metas
        self.goals_view = ft.Column([
            ft.Text("Metas de Poupança", size=28, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 32
            ft.Text("Transforme sonhos em objetivos alcançáveis", size=15, color="#6B7280"),  # Reduzido de 16
            ft.Container(height=20),  # Reduzido de 28
            self.savings_potential_card,
            ft.Container(height=24),  # Reduzido de 32
            ft.Text("Nova Meta", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 22
            ft.Container(height=12),  # Reduzido de 16
            self.goal_name,
            ft.Container(height=12),  # Reduzido de 16
            self.goal_total_cost,
            ft.Container(height=12),  # Reduzido de 16
            self.goal_monthly_saving,
            ft.Container(height=12),  # Reduzido de 16
            self.goal_time_estimate,
            ft.Container(height=18),  # Reduzido de 24
            self.create_premium_button("Criar Meta", self.add_goal, ft.icons.ROCKET_LAUNCH, "#059669"),
            ft.Container(height=24),  # Reduzido de 32
            ft.Text("Minhas Metas", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 22
            ft.Container(height=12),  # Reduzido de 16
            self.create_elegant_card(self.goals_list)
        ], scroll=ft.ScrollMode.AUTO)
    
    def create_finance_view(self):
        """Cria a vista unificada de Renda Extra e Dívidas"""
        _, current_balance = self.calculate_totals()
        total_debts = sum(debt.get('total_amount', 0) - debt.get('paid_amount', 0) for debt in self.debts)
        total_extra_income = sum(abs(expense['amount']) for expense in self.expenses if expense['amount'] < 0)
        debt_ratio = (total_debts / self.salary * 100) if self.salary > 0 else 0
        
        # Card de resumo financeiro extra
        self.finance_summary_card = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("💰", size=28),  # Reduzido de 32
                    ft.Column([
                        ft.Text("Panorama Financeiro", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 24
                        ft.Text("Rendas extras e controle de dívidas", size=13, color="#6B7280")  # Reduzido de 14
                    ], expand=True, spacing=3)
                ], spacing=12),  # Reduzido de 16
                ft.Container(height=16),  # Reduzido de 20
                # Stats em row como as metas
                ft.Row([
                    self.create_stats_card("💸", "Renda Extra", f"{total_extra_income:,.0f}", "Kz", "#059669", "#ECFDF5"),
                    self.create_stats_card("💳", "Em Dívidas", f"{total_debts:,.0f}", "Kz", "#DC2626", "#FEF2F2"),
                    self.create_stats_card("📊", "% Comprometido", f"{debt_ratio:.1f}%", "", 
                                         "#DC2626" if debt_ratio > 30 else "#F59E0B" if debt_ratio > 20 else "#059669",
                                         "#FEF2F2" if debt_ratio > 30 else "#FFFBEB" if debt_ratio > 20 else "#ECFDF5")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=12),  # Reduzido de 16
                # Alerta de endividamento
                ft.Container(
                    content=ft.Text(
                        "ALERTA! Endividamento Alto! Evite novas dívidas!" if debt_ratio > 30
                        else "CUIDADO! Mantenha abaixo de 30%!" if debt_ratio > 20
                        else "Endividamento Controlado!" if debt_ratio > 0
                        else "Sem Dívidas Ativas!",
                        size=13, weight=ft.FontWeight.BOLD,  # Reduzido de 14
                        color="#DC2626" if debt_ratio > 30 else "#F59E0B" if debt_ratio > 20 else "#059669"
                    ),
                    bgcolor="#FEF2F2" if debt_ratio > 30 else "#FFFBEB" if debt_ratio > 20 else "#ECFDF5",
                    border_radius=20,  # Reduzido de 25
                    padding=ft.padding.symmetric(horizontal=14, vertical=8)  # Reduzido padding
                )
            ])
        )
        
        # Seção de Renda Extra
        self.extra_income_description = ft.Container(
            content=ft.TextField(
                label="Descrição da Renda Extra",
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=14,  # Reduzido de 16
                content_padding=ft.padding.all(16)  # Reduzido de 20
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,  # Reduzido de 8
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )

        self.extra_income_amount = ft.Container(
            content=ft.TextField(
                label="Valor (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#059669",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=14,
                content_padding=ft.padding.all(16)
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )
        
        # Seção de Dívidas (como as metas)
        self.debt_description = ft.Container(
            content=ft.TextField(
                label="Descrição da Dívida",
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#DC2626",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=14,
                content_padding=ft.padding.all(16)
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )
        
        self.debt_total_amount = ft.Container(
            content=ft.TextField(
                label="Valor Total (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#DC2626",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=14,
                content_padding=ft.padding.all(16),
                on_change=self.calculate_debt_impact
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )
        
        self.debt_due_date = ft.Container(
            content=ft.TextField(
                label="Vencimento (DD/MM/AAAA)",
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#DC2626",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=14,
                content_padding=ft.padding.all(16)
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color="#1F293720",
                offset=ft.Offset(0, 2)
            )
        )
        
        self.debt_impact_estimate = ft.Container(
            content=ft.Text("Impacto no endividamento: -- %", size=15, color="#6B7280", weight=ft.FontWeight.BOLD),  # Reduzido de 16
            bgcolor="#F8FAFC",
            border_radius=20,  # Reduzido de 25
            padding=ft.padding.symmetric(horizontal=16, vertical=10)  # Reduzido padding
        )
        
        # Lista de dívidas (como metas)
        self.debts_list = ft.ListView(
            spacing=12,  # Reduzido de 16
            padding=ft.padding.all(0),
            height=260  # Reduzido de 300
        )
        self.update_debts_list()
        
        # Container da nova vista
        self.finance_view = ft.Column([
            ft.Text("Renda & Dívidas", size=28, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 32
            ft.Text("Gerencie rendas extras e controle dívidas", size=15, color="#6B7280"),  # Reduzido de 16
            ft.Container(height=20),  # Reduzido de 28
            self.finance_summary_card,
            ft.Container(height=24),  # Reduzido de 32
            ft.Text("Adicionar Renda Extra", size=20, weight=ft.FontWeight.BOLD, color="#059669"),  # Reduzido de 22
            ft.Text("Freelances, vendas, bonificações, etc.", size=13, color="#6B7280"),  # Reduzido de 14
            ft.Container(height=12),  # Reduzido de 16
            self.extra_income_description,
            ft.Container(height=12),  # Reduzido de 16
            self.extra_income_amount,
            ft.Container(height=16),  # Reduzido de 20
            self.create_premium_button("Adicionar Renda", self.add_extra_income, ft.icons.ADD_CIRCLE, "#059669"),
            ft.Container(height=24),  # Reduzido de 32
            ft.Text("Adicionar Dívida", size=20, weight=ft.FontWeight.BOLD, color="#DC2626"),  # Reduzido de 22
            ft.Text("Pense bem antes de se endividar!", size=13, color="#DC2626"),  # Reduzido de 14
            ft.Container(height=12),  # Reduzido de 16
            self.debt_description,
            ft.Container(height=12),  # Reduzido de 16
            self.debt_total_amount,
            ft.Container(height=12),  # Reduzido de 16
            self.debt_due_date,
            ft.Container(height=12),  # Reduzido de 16
            self.debt_impact_estimate,
            ft.Container(height=16),  # Reduzido de 20
            self.create_premium_button("Adicionar Dívida", self.add_debt, ft.icons.WARNING, "#DC2626"),
            ft.Container(height=24),  # Reduzido de 32
            ft.Text("Minhas Dívidas", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 22
            ft.Container(height=12),  # Reduzido de 16
            self.create_elegant_card(self.debts_list)
        ], scroll=ft.ScrollMode.AUTO)

    def create_summary_view(self):
        """Cria a vista de resumo premium com análises detalhadas"""
        total_spent, current_balance = self.calculate_totals()
        most_common, highest_amount, highest_desc, top_expenses = self.analyze_spending_patterns()

        # Stats row simples e elegante
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
                    ft.Text("💎", size=28),  # Reduzido de 32
                    ft.Column([
                        ft.Text("Gastos Mais Avultados", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 22
                        ft.Text("Suas maiores despesas individuais", size=13, color="#6B7280")  # Reduzido de 14
                    ], expand=True, spacing=3)
                ], spacing=12),  # Reduzido de 16
                ft.Container(height=16),  # Reduzido de 20
                ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Text(f"#{i+1}", size=16, color="#FFFFFF", weight=ft.FontWeight.BOLD),  # Reduzido de 18
                                bgcolor="#DC2626" if i == 0 else "#F59E0B" if i == 1 else "#6B7280",
                                border_radius=20,  # Reduzido de 25
                                padding=ft.padding.all(6),  # Reduzido de 8
                                width=30,  # Reduzido de 35
                                height=30  # Reduzido de 35
                            ),
                            ft.Column([
                                ft.Text(expense['description'], size=13, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 14
                                ft.Text(expense['date'], size=11, color="#6B7280")  # Reduzido de 12
                            ], expand=True, spacing=1),  # Reduzido de 2
                            ft.Text(f"{expense['amount']:,.0f} Kz", size=15, weight=ft.FontWeight.BOLD, color="#DC2626")  # Reduzido de 16
                        ]),
                        bgcolor="#FAFAFA",
                        border_radius=10,  # Reduzido de 12
                        padding=ft.padding.all(10)  # Reduzido de 12
                    ) for i, expense in enumerate(top_expenses[:3])
                ], spacing=6) if top_expenses else [ft.Text("Nenhuma despesa registrada", size=13, color="#6B7280")]  # Reduzido de 14
            ])
        ) if self.expenses else ft.Container()

        # Análise avançada de gastos por categoria
        spending_insights = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("📊", size=28),  # Reduzido de 32
                    ft.Column([
                        ft.Text("Análise por Categoria", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 22
                        ft.Text("Padrões de gastos mais recorrentes", size=13, color="#6B7280")  # Reduzido de 14
                    ], expand=True, spacing=3)
                ], spacing=12),  # Reduzido de 16
                ft.Container(height=16),  # Reduzido de 20
                ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Text(f"#{i + 1}", size=14, color="#FFFFFF", weight=ft.FontWeight.BOLD),  # Reduzido de 16
                                bgcolor="#059669" if i == 0 else "#D97706" if i == 1 else "#EC4899",
                                border_radius=16,  # Reduzido de 20
                                padding=ft.padding.all(6),  # Reduzido de 8
                                width=32,  # Reduzido de 40
                                height=32  # Reduzido de 40
                            ),
                            ft.Column([
                                ft.Text(category[0].title(), size=13, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 14
                                ft.Text(f"Repetida {category[1]} vezes", size=11, color="#6B7280")  # Reduzido de 12
                            ], expand=True, spacing=1),  # Reduzido de 2
                            ft.Text(f"{category[1]}x", size=15, weight=ft.FontWeight.BOLD,  # Reduzido de 16
                                    color="#059669" if i == 0 else "#D97706" if i == 1 else "#EC4899")
                        ]),
                        bgcolor="#FAFAFA",
                        border_radius=10,  # Reduzido de 12
                        padding=ft.padding.all(10)  # Reduzido de 12
                    ) for i, category in enumerate(most_common[:3])
                ], spacing=6) if most_common else [  # Reduzido de 8
                    ft.Text("Ainda não há padrões para analisar", size=13, color="#6B7280")]  # Reduzido de 14
            ])
        ) if self.expenses else ft.Container()

        # Análise de metas
        active_goals = len(self.goals)
        total_goal_value = sum(goal['total_cost'] for goal in self.goals)
        total_saved_for_goals = sum(goal.get('saved_amount', 0) for goal in self.goals)

        # Análise de dívidas
        active_debts = len([debt for debt in self.debts if debt.get('total_amount', 0) - debt.get('paid_amount', 0) > 0])
        total_debts = sum(debt.get('total_amount', 0) - debt.get('paid_amount', 0) for debt in self.debts)
        total_paid_debts = sum(debt.get('paid_amount', 0) for debt in self.debts)

        goals_analysis = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("🎯", size=28),  # Reduzido de 32
                    ft.Column([
                        ft.Text("Status das Metas", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 22
                        ft.Text("Progresso dos seus objetivos", size=13, color="#6B7280")  # Reduzido de 14
                    ], expand=True, spacing=3)
                ], spacing=12),  # Reduzido de 16
                ft.Container(height=18),  # Reduzido de 24
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Metas", size=9, color="#6B7280", weight=ft.FontWeight.BOLD),  # Reduzido de 10
                            ft.Text(str(active_goals), size=18, weight=ft.FontWeight.BOLD, color="#059669")  # Reduzido de 20
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#ECFDF5",
                        border_radius=16,  # Reduzido de 18
                        padding=ft.padding.all(16),  # Reduzido de 20
                        expand=True
                    ),
                    ft.Container(),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Total", size=9, color="#6B7280", weight=ft.FontWeight.BOLD),  # Reduzido de 10
                            ft.Text(f"{total_goal_value:,.0f}", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 20
                            ft.Text("Kz", size=11, color="#9CA3AF")  # Reduzido de 12
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#F8FAFC",
                        border_radius=16,  # Reduzido de 18
                        padding=ft.padding.all(16),  # Reduzido de 20
                        expand=True
                    ),
                    ft.Container(),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Pago", size=9, color="#6B7280", weight=ft.FontWeight.BOLD),  # Reduzido de 10
                            ft.Text(f"{total_saved_for_goals:,.0f}", size=18, weight=ft.FontWeight.BOLD,  # Reduzido de 20
                                    color="#059669"),
                            ft.Text("Kz", size=11, color="#9CA3AF")  # Reduzido de 12
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#ECFDF5",
                        border_radius=16,  # Reduzido de 18
                        padding=ft.padding.all(16),  # Reduzido de 20
                        expand=True
                    )
                ])
            ])
        )

        debts_analysis = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("💳", size=28),  # Reduzido de 32
                    ft.Column([
                        ft.Text("Status das Dívidas", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 22
                        ft.Text("Controle do seu endividamento", size=13, color="#6B7280")  # Reduzido de 14
                    ], expand=True, spacing=3)
                ], spacing=12),  # Reduzido de 16
                ft.Container(height=18),  # Reduzido de 24
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Dívidas", size=9, color="#6B7280", weight=ft.FontWeight.BOLD),  # Reduzido de 10
                            ft.Text(str(active_debts), size=18, weight=ft.FontWeight.BOLD,  # Reduzido de 20
                                   color="#DC2626" if active_debts > 0 else "#059669")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#FEF2F2" if active_debts > 0 else "#ECFDF5",
                        border_radius=16,  # Reduzido de 18
                        padding=ft.padding.all(16),  # Reduzido de 20
                        expand=True
                    ),
                    ft.Container(),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Devendo", size=9, color="#6B7280", weight=ft.FontWeight.BOLD),  # Reduzido de 10
                            ft.Text(f"{total_debts:,.0f}", size=18, weight=ft.FontWeight.BOLD,  # Reduzido de 20
                                   color="#DC2626" if total_debts > 0 else "#059669"),
                            ft.Text("Kz", size=11, color="#9CA3AF")  # Reduzido de 12
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#FEF2F2" if total_debts > 0 else "#ECFDF5",
                        border_radius=16,  # Reduzido de 18
                        padding=ft.padding.all(16),  # Reduzido de 20
                        expand=True
                    ),
                    ft.Container(),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Já Pago", size=9, color="#6B7280", weight=ft.FontWeight.BOLD),  # Reduzido de 10
                            ft.Text(f"{total_paid_debts:,.0f}", size=18, weight=ft.FontWeight.BOLD, color="#059669"),  # Reduzido de 20
                            ft.Text("Kz", size=11, color="#9CA3AF")  # Reduzido de 12
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#ECFDF5",
                        border_radius=16,  # Reduzido de 18
                        padding=ft.padding.all(16),  # Reduzido de 20
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
                        content=ft.Icon(ft.icons.TRENDING_DOWN, color="#EC4899", size=16),  # Reduzido de 18
                        bgcolor="#FDF2F8",
                        border_radius=20,  # Reduzido de 25
                        padding=ft.padding.all(8)  # Reduzido de 10
                    ),
                    ft.Column([
                        ft.Text(expense['description'], size=14, weight=ft.FontWeight.NORMAL, color="#1F2937"),  # Reduzido de 15
                        ft.Text(expense['date'], size=11, color="#6B7280")  # Reduzido de 12
                    ], expand=True, spacing=3),  # Reduzido de 4
                    ft.Text(f"{expense['amount']:,.0f} Kz", size=14, weight=ft.FontWeight.BOLD, color="#EC4899")  # Reduzido de 15
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor="#FFFFFF",
                border=ft.border.all(1, "#F3F4F6"),
                border_radius=14,  # Reduzido de 16
                padding=ft.padding.all(12)  # Reduzido de 16
            ) for expense in reversed(recent_expenses)
        ], spacing=8)  # Reduzido de 10

        # Container da vista de resumo com scroll otimizado
        self.summary_view = ft.Column([
            ft.Text("Dashboard Financeiro", size=26, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 28
            ft.Text(f"Visão completa do mês {self.current_month}", size=13, color="#6B7280"),  # Reduzido de 14
            ft.Container(height=16),  # Reduzido de 20
            stats_row,
            ft.Container(height=16),  # Reduzido de 20
            top_expenses_card,
            ft.Container(height=16),  # Reduzido de 20
            spending_insights,
            ft.Container(height=16),  # Reduzido de 20
            goals_analysis,
            ft.Container(height=16),  # Reduzido de 20
            debts_analysis,
            ft.Container(height=20),  # Reduzido de 25
            ft.Text("Transações Recentes", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 20
            ft.Container(height=10),  # Reduzido de 12
            self.create_elegant_card(
                recent_expenses_list if recent_expenses else ft.Text("Nenhuma transação registrada ainda",
                                                                     size=13, color="#6B7280")  # Reduzido de 14
            )
        ], scroll=ft.ScrollMode.AUTO)

    def create_stats_card(self, icon, title, value, unit, color, bg_color):
        """Cria um card de estatística simples e elegante"""
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(icon, size=24),  # Reduzido de 28
                    bgcolor=bg_color,
                    border_radius=50,
                    padding=ft.padding.all(10)  # Reduzido de 12
                ),
                ft.Text(title, size=11, color="#6B7280", weight=ft.FontWeight.BOLD),  # Reduzido de 12
                ft.Text(value, size=16, weight=ft.FontWeight.BOLD, color=color),  # Reduzido de 18
                ft.Text(unit, size=9, color="#9CA3AF") if unit else ft.Container(height=10)  # Reduzido de 10 para 9, altura 12 para 10
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),  # Reduzido de 8
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=16,  # Reduzido de 20
            padding=ft.padding.all(16),  # Reduzido de 20
            width=115,  # Reduzido de 125
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,  # Reduzido de 15
                color="#1F293720",
                offset=ft.Offset(0, 3)  # Reduzido de 4
            )
        )

    def setup_navigation(self):
        """Configura a navegação elegante"""
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.CREDIT_CARD_OUTLINED, label="Despesas",
                                         selected_icon=ft.icons.CREDIT_CARD),
                ft.NavigationBarDestination(icon=ft.icons.SAVINGS_OUTLINED, label="Metas", selected_icon=ft.icons.SAVINGS),
                ft.NavigationBarDestination(icon=ft.icons.ACCOUNT_BALANCE_OUTLINED, label="Renda & Dívidas", 
                                       selected_icon=ft.icons.ACCOUNT_BALANCE),
                ft.NavigationBarDestination(icon=ft.icons.ANALYTICS_OUTLINED, label="Dashboard",
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
            title=ft.Text(f"Adicionar Pagamento", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),
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

    def show_debt_payment_dialog(self, debt_index):
        """Mostra diálogo para pagar dívida"""
        debt = self.debts[debt_index]
        remaining_debt = debt['total_amount'] - debt.get('paid_amount', 0)
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
                    if amount <= current_balance:
                        if amount <= remaining_debt:
                            # Adiciona o pagamento à dívida
                            self.debts[debt_index]['paid_amount'] = self.debts[debt_index].get('paid_amount', 0) + amount
                            
                            # Adiciona como despesa
                            payment_expense = {
                                'description': f"Pagamento Dívida: {debt['description']}",
                                'amount': amount,
                                'date': datetime.now().strftime("%d/%m/%Y")
                            }
                            self.expenses.append(payment_expense)
                            
                            self.save_data()
                            self.update_all_views()
                            dialog.open = False
                            self.page.update()
                        else:
                            error_text.value = f"Valor maior que a dívida restante: {remaining_debt:,.0f} Kz"
                            error_text.color = "#DC2626"
                            self.page.update()
                    else:
                        error_text.value = f"Saldo insuficiente! Disponível: {current_balance:,.0f} Kz"
                        error_text.color = "#DC2626"
                        self.page.update()
            except ValueError:
                pass
        
        error_text = ft.Text("", size=12)
        
        dialog = ft.AlertDialog(
            title=ft.Text(f"Pagar Dívida", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),
            content=ft.Column([
                ft.Text(f"Dívida: {debt['description']}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"Total: {debt['total_amount']:,.0f} Kz", size=14, color="#6B7280"),
                ft.Text(f"Já pago: {debt.get('paid_amount', 0):,.0f} Kz", size=14, color="#059669"),
                ft.Text(f"Restante: {remaining_debt:,.0f} Kz", size=14, color="#DC2626"),
                ft.Text(f"Saldo disponível: {current_balance:,.0f} Kz", size=14, color="#2563EB"),
                ft.Container(height=16),
                payment_field,
                error_text
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False) or self.page.update(),
                             style=ft.ButtonStyle(color="#6B7280")),
                ft.ElevatedButton("Pagar", on_click=add_payment, bgcolor="#059669", color="#FFFFFF",
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
            self.main_container.content = self.finance_view
            self.update_finance_view()
        elif selected_index == 3:
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

    def add_extra_income(self, e):
        """Adiciona renda extra ao saldo"""
        description_field = self.extra_income_description.content
        amount_field = self.extra_income_amount.content

        if not description_field.value or not amount_field.value:
            return

        try:
            amount = float(amount_field.value)
            
            # Adiciona ao saldo acumulado
            self.accumulated_balance += amount
            self.salary = self.base_salary + self.accumulated_balance
            
            # Cria entrada no histórico como "renda extra"
            income_entry = {
                'description': f"Renda Extra: {description_field.value}",
                'amount': -amount,  # Valor negativo para mostrar como entrada
                'date': datetime.now().strftime("%d/%m/%Y")
            }
            
            self.expenses.append(income_entry)
            self.save_data()

            # Limpa os campos
            description_field.value = ""
            amount_field.value = ""

            self.update_all_views()
        except ValueError:
            pass

    def calculate_debt_impact(self, e):
        """Calcula o impacto da nova dívida no endividamento"""
        amount_field = self.debt_total_amount.content
        
        try:
            if amount_field.value:
                new_debt = float(amount_field.value)
                current_debts = sum(debt.get('total_amount', 0) - debt.get('paid_amount', 0) for debt in self.debts)
                new_debt_ratio = ((current_debts + new_debt) / self.salary * 100) if self.salary > 0 else 0
                
                if new_debt_ratio > 50:
                    self.debt_impact_estimate.content.value = f"PERIGO! Endividamento: {new_debt_ratio:.1f}%"
                    self.debt_impact_estimate.bgcolor = "#FEF2F2"
                    self.debt_impact_estimate.content.color = "#DC2626"
                elif new_debt_ratio > 30:
                    self.debt_impact_estimate.content.value = f"ALTO RISCO! Endividamento: {new_debt_ratio:.1f}%"
                    self.debt_impact_estimate.bgcolor = "#FFFBEB"
                    self.debt_impact_estimate.content.color = "#F59E0B"
                else:
                    self.debt_impact_estimate.content.value = f"Endividamento: {new_debt_ratio:.1f}%"
                    self.debt_impact_estimate.bgcolor = "#ECFDF5"
                    self.debt_impact_estimate.content.color = "#059669"
                
                self.page.update()
        except ValueError:
            self.debt_impact_estimate.content.value = "Impacto no endividamento: -- %"
            self.debt_impact_estimate.bgcolor = "#F8FAFC"
            self.debt_impact_estimate.content.color = "#6B7280"
            self.page.update()

    def add_debt(self, e):
        """Adiciona uma nova dívida com verificação de endividamento"""
        description_field = self.debt_description.content
        amount_field = self.debt_total_amount.content
        due_date_field = self.debt_due_date.content

        if not description_field.value or not amount_field.value:
            return

        try:
            amount = float(amount_field.value)
            
            # Calcula novo percentual de endividamento
            current_debts = sum(debt.get('total_amount', 0) - debt.get('paid_amount', 0) for debt in self.debts)
            new_debt_ratio = ((current_debts + amount) / self.salary * 100) if self.salary > 0 else 0
            
            # Mostra diálogo de confirmação se endividamento alto
            if new_debt_ratio > 30:
                self.show_debt_confirmation_dialog(amount, new_debt_ratio)
                return
            
            # Adiciona a dívida diretamente se endividamento OK
            self.create_debt(amount, description_field, amount_field, due_date_field)
            
        except ValueError:
            pass

    def show_debt_confirmation_dialog(self, amount, debt_ratio):
        """Mostra diálogo de confirmação para dívidas com alto endividamento"""
        title = "PERIGO EXTREMO!" if debt_ratio > 50 else "CUIDADO!"
        message = (f"Esta dívida levará seu endividamento para {debt_ratio:.1f}% da renda!\n\n" +
                  ("ISTO É MUITO PERIGOSO! Você pode entrar em uma espiral de dívidas." if debt_ratio > 50
                   else "Mais de 30% é considerado alto risco.") +
                  "\n\nTem certeza que deseja continuar?")
        color = "#DC2626" if debt_ratio > 50 else "#F59E0B"
        
        dialog = ft.AlertDialog(
            title=ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=color),
            content=ft.Text(message, size=14, color="#1F2937"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False) or self.page.update(),
                             style=ft.ButtonStyle(color="#059669")),
                ft.ElevatedButton("Continuar Mesmo Assim", 
                                on_click=lambda e: self.confirm_add_debt(dialog, amount), 
                                bgcolor=color, color="#FFFFFF",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)))
            ],
            shape=ft.RoundedRectangleBorder(radius=20)
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def confirm_add_debt(self, dialog, amount):
        """Confirma e adiciona a dívida após aviso"""
        description_field = self.debt_description.content
        amount_field = self.debt_total_amount.content
        due_date_field = self.debt_due_date.content
        
        self.create_debt(amount, description_field, amount_field, due_date_field)
        dialog.open = False
        self.page.update()

    def create_debt(self, amount, description_field, amount_field, due_date_field):
        """Cria a dívida e limpa os campos"""
        debt = {
            'description': description_field.value,
            'total_amount': amount,
            'paid_amount': 0,
            'due_date': due_date_field.value if due_date_field.value else "Sem prazo",
            'created_date': datetime.now().strftime("%d/%m/%Y")
        }
        
        self.debts.append(debt)
        self.save_data()
        
        # Limpa os campos
        description_field.value = ""
        amount_field.value = ""
        due_date_field.value = ""
        self.debt_impact_estimate.content.value = "Impacto no endividamento: -- %"
        self.debt_impact_estimate.bgcolor = "#F8FAFC"
        
        self.update_all_views()

    def remove_debt(self, index):
        """Remove uma dívida"""
        def remove(e):
            self.debts.pop(index)
            self.save_data()
            self.update_all_views()
        return remove

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
                    self.goal_time_estimate.content.value = f"Tempo estimado: {months} meses"
                else:
                    self.goal_time_estimate.content.value = "Tempo estimado: -- meses"

                self.page.update()
        except ValueError:
            self.goal_time_estimate.content.value = "Tempo estimado: -- meses"
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
            self.goal_time_estimate.content.value = "Tempo estimado: -- meses"

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
            # Destaca pagamentos para metas e rendas extras
            is_goal_payment = expense['description'].startswith("Pagamento:")
            is_extra_income = expense['description'].startswith("Renda Extra:")
            
            # Define cores e ícones baseado no tipo
            if is_extra_income:
                icon = ft.icons.TRENDING_UP
                icon_color = "#059669"
                bg_color = "#ECFDF5"
                border_color = "#A7F3D0"
                text_color = "#059669"
                amount_color = "#059669"
            elif is_goal_payment:
                icon = ft.icons.SAVINGS
                icon_color = "#059669"
                bg_color = "#ECFDF5"
                border_color = "#A7F3D0"
                text_color = "#059669"
                amount_color = "#059669"
            else:
                icon = ft.icons.TRENDING_DOWN
                icon_color = "#EC4899"
                bg_color = "#FDF2F8"
                border_color = "#F3F4F6"
                text_color = "#1F2937"
                amount_color = "#EC4899"

            expense_item = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, color=icon_color, size=18),  # Reduzido de 20
                        bgcolor=bg_color,
                        border_radius=25,  # Reduzido de 30
                        padding=ft.padding.all(10)  # Reduzido de 12
                    ),
                    ft.Column([
                        ft.Text(expense['description'], size=14, weight=ft.FontWeight.NORMAL, color=text_color),  # Reduzido de 15
                        ft.Text(expense['date'], size=11, color="#6B7280")  # Reduzido de 12
                    ], expand=True, spacing=3),  # Reduzido de 4
                    ft.Column([
                        ft.Text(
                            f"+{abs(expense['amount']):,.0f} Kz" if is_extra_income 
                            else f"{expense['amount']:,.0f} Kz", 
                            size=14, weight=ft.FontWeight.BOLD, color=amount_color  # Reduzido de 15
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color="#DC2626",
                            icon_size=16,  # Reduzido de 18
                            on_click=self.remove_expense(len(self.expenses) - 1 - i),
                            tooltip="Remover entrada"
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=0)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor="#FFFFFF",
                border=ft.border.all(1, border_color),
                border_radius=14,  # Reduzido de 16
                padding=ft.padding.all(12),  # Reduzido de 16
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=6,  # Reduzido de 8
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
                status_text = "Meta Concluída!"
                status_color = "#059669"
            elif progress >= 0.75:
                icon = ft.icons.ROCKET_LAUNCH
                icon_color = "#D97706"
                bg_color = "#FFFBEB"
                status_text = f"Quase lá! {remaining_months} meses"
                status_color = "#D97706"
            else:
                icon = ft.icons.SAVINGS
                icon_color = "#2563EB"
                bg_color = "#EFF6FF"
                status_text = f"{remaining_months} meses restantes"
                status_color = "#6B7280"

            goal_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(icon, color=icon_color, size=22),  # Reduzido de 26
                            bgcolor=bg_color,
                            border_radius=25,  # Reduzido de 30
                            padding=ft.padding.all(12)  # Reduzido de 14
                        ),
                        ft.Column([
                            ft.Text(goal['name'], size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 17
                            ft.Text(status_text, size=12, color=status_color, weight=ft.FontWeight.NORMAL)  # Reduzido de 13
                        ], expand=True, spacing=3),  # Reduzido de 4
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color="#DC2626",
                            icon_size=18,  # Reduzido de 20
                            on_click=self.remove_goal(i),
                            tooltip="Remover meta"
                        )
                    ]),
                    ft.Container(height=16),  # Reduzido de 20
                    # Barra de progresso elegante
                    ft.Column([
                        ft.ProgressBar(
                            value=min(progress, 1.0),
                            bgcolor="#E5E7EB",
                            color="#059669" if progress >= 1.0 else "#2563EB",
                            height=8  # Reduzido de 10
                        ),
                        ft.Container(height=8),  # Reduzido de 12
                        ft.Row([
                            ft.Text(f"{saved_amount:,.0f} / {goal['total_cost']:,.0f} Kz",
                                    size=13, color="#6B7280"),  # Reduzido de 14
                            ft.Text(f"{progress * 100:.1f}%", size=13, weight=ft.FontWeight.BOLD,  # Reduzido de 14
                                    color="#059669" if progress >= 1.0 else "#2563EB")
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    ft.Container(height=16),  # Reduzido de 20
                    # Botão para adicionar pagamento elegante
                    ft.Container(
                        content=ft.Text("Investir na Meta", size=13, weight=ft.FontWeight.BOLD, color="#059669"),  # Reduzido de 14
                        bgcolor="#ECFDF5",
                        border=ft.border.all(1, "#A7F3D0"),
                        border_radius=20,  # Reduzido de 25
                        padding=ft.padding.symmetric(horizontal=16, vertical=10),  # Reduzido padding
                        on_click=lambda e, idx=i: self.show_add_payment_dialog(idx)
                    ) if progress < 1.0 else ft.Container(
                        content=ft.Text("Objetivo Alcançado!", size=13, weight=ft.FontWeight.BOLD, color="#059669"),  # Reduzido de 14
                        bgcolor="#ECFDF5",
                        border=ft.border.all(1, "#A7F3D0"),
                        border_radius=20,  # Reduzido de 25
                        padding=ft.padding.symmetric(horizontal=16, vertical=10)  # Reduzido padding
                    )
                ]),
                bgcolor="#FFFFFF",
                border=ft.border.all(1, "#E5E7EB"),
                border_radius=20,  # Reduzido de 24
                padding=ft.padding.all(20),  # Reduzido de 24
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12,  # Reduzido de 15
                    color="#1F293720",
                    offset=ft.Offset(0, 3)  # Reduzido de 4
                )
            )
            self.goals_list.controls.append(goal_card)

    def update_debts_list(self):
        """Atualiza a lista de dívidas"""
        self.debts_list.controls.clear()
        
        for i, debt in enumerate(self.debts):
            paid_amount = debt.get('paid_amount', 0)
            total_amount = debt['total_amount']
            remaining = total_amount - paid_amount
            progress = paid_amount / total_amount if total_amount > 0 else 0
            
            # Status da dívida
            if progress >= 1.0:
                icon = ft.icons.CHECK_CIRCLE
                icon_color = "#059669"
                bg_color = "#ECFDF5"
                status_text = "Quitada!"
                status_color = "#059669"
            elif remaining > 0:
                icon = ft.icons.WARNING
                icon_color = "#DC2626"
                bg_color = "#FEF2F2"
                status_text = f"Devendo: {remaining:,.0f} Kz"
                status_color = "#DC2626"
            else:
                icon = ft.icons.MONEY_OFF
                icon_color = "#F59E0B"
                bg_color = "#FFFBEB"
                status_text = "Em andamento"
                status_color = "#F59E0B"
            
            debt_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(icon, color=icon_color, size=22),  # Reduzido de 26
                            bgcolor=bg_color,
                            border_radius=25,  # Reduzido de 30
                            padding=ft.padding.all(12)  # Reduzido de 14
                        ),
                        ft.Column([
                            ft.Text(debt['description'], size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),  # Reduzido de 17
                            ft.Text(status_text, size=12, color=status_color, weight=ft.FontWeight.NORMAL),  # Reduzido de 13
                            ft.Text(f"Vencimento: {debt['due_date']}", size=10, color="#6B7280")  # Reduzido de 11
                        ], expand=True, spacing=1),  # Reduzido de 2
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color="#DC2626",
                            icon_size=18,  # Reduzido de 20
                            on_click=self.remove_debt(i),
                            tooltip="Remover dívida"
                        )
                    ]),
                    ft.Container(height=16),  # Reduzido de 20
                    # Barra de progresso de pagamento
                    ft.Column([
                        ft.ProgressBar(
                            value=min(progress, 1.0),
                            bgcolor="#E5E7EB",
                            color="#059669" if progress >= 1.0 else "#DC2626",
                            height=8  # Reduzido de 10
                        ),
                        ft.Container(height=8),  # Reduzido de 12
                        ft.Row([
                            ft.Text(f"{paid_amount:,.0f} / {total_amount:,.0f} Kz",
                                   size=13, color="#6B7280"),  # Reduzido de 14
                            ft.Text(f"{progress*100:.1f}% pago", size=13, weight=ft.FontWeight.BOLD,  # Reduzido de 14
                                   color="#059669" if progress >= 1.0 else "#DC2626")
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    ft.Container(height=16),  # Reduzido de 20
                    # Botão para pagar dívida
                    ft.Container(
                        content=ft.Text("Fazer Pagamento", size=13, weight=ft.FontWeight.BOLD, color="#059669"),  # Reduzido de 14
                        bgcolor="#ECFDF5",
                        border=ft.border.all(1, "#A7F3D0"),
                        border_radius=20,  # Reduzido de 25
                        padding=ft.padding.symmetric(horizontal=16, vertical=10),  # Reduzido padding
                        on_click=lambda e, idx=i: self.show_debt_payment_dialog(idx)
                    ) if progress < 1.0 else ft.Container(
                        content=ft.Text("Dívida Quitada!", size=13, weight=ft.FontWeight.BOLD, color="#059669"),  # Reduzido de 14
                        bgcolor="#ECFDF5",
                        border=ft.border.all(1, "#A7F3D0"),
                        border_radius=20,  # Reduzido de 25
                        padding=ft.padding.symmetric(horizontal=16, vertical=10)  # Reduzido padding
                    )
                ]),
                bgcolor="#FFFFFF",
                border=ft.border.all(1, "#E5E7EB"),
                border_radius=20,  # Reduzido de 24
                padding=ft.padding.all(20),  # Reduzido de 24
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12,  # Reduzido de 15
                    color="#1F293720",
                    offset=ft.Offset(0, 3)  # Reduzido de 4
                )
            )
            self.debts_list.controls.append(debt_card)

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

    def update_finance_view(self):
        """Atualiza a vista de renda e dívidas"""
        self.create_finance_view()
        if hasattr(self, 'main_container') and hasattr(self, 'finance_view'):
            current_view = self.main_container.content
            if current_view == self.finance_view or self.navigation_bar.selected_index == 2:
                self.main_container.content = self.finance_view

    def update_summary_view(self):
        """Atualiza a vista de resumo"""
        self.create_summary_view()
        if hasattr(self, 'main_container') and hasattr(self, 'summary_view'):
            current_view = self.main_container.content
            if current_view == self.summary_view or self.navigation_bar.selected_index == 3:
                self.main_container.content = self.summary_view

    def update_all_views(self):
        """Atualiza todas as vistas"""
        current_index = getattr(self.navigation_bar, 'selected_index', 0)

        if current_index == 0:
            self.update_expenses_view()
        elif current_index == 1:
            self.update_goals_view()
        elif current_index == 2:
            self.update_finance_view()
        elif current_index == 3:
            self.update_summary_view()

        self.page.update()


def main(page: ft.Page):
    """Função principal da aplicação"""
    app = FinancialApp(page)


if __name__ == "__main__":
    ft.app(target=main)
