# -*- coding: utf-8 -*-
"""
Gestão Financeira Premium - VERSÃO UTF-8 CORRIGIDA
✅ Codificação UTF-8 declarada explicitamente
✅ TODAS as funcionalidades restauradas
✅ Compatível com Windows/APK
"""

import flet as ft
import json
import os
from datetime import datetime
import math
from collections import Counter
import sys
import traceback


class FinancialApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.data_file = "financial_data.json"
        self.setup_page()
        self.load_data()
        self.check_new_month()
        self.create_components()
        self.setup_navigation()

    def setup_page(self):
        """Configuração inicial da página"""
        self.page.title = "Gestão Financeira Premium"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = "#FAFBFF"
        self.page.padding = 0

    def load_data(self):
        """Carrega dados de arquivo local (UTF-8 safe)"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self.base_salary = float(data.get("salary", 0.0))
                self.accumulated_balance = float(data.get("accumulated_balance", 0.0))
                self.salary = self.base_salary + self.accumulated_balance
                self.expenses = data.get("expenses", [])
                self.goals = data.get("goals", [])
                self.debts = data.get("debts", [])
                self.current_month = data.get("current_month", datetime.now().strftime("%m/%Y"))

                print(f"✅ Dados carregados: {len(self.expenses)} despesas, {len(self.goals)} metas")
            else:
                self.base_salary = 0.0
                self.accumulated_balance = 0.0
                self.salary = 0.0
                self.expenses = []
                self.goals = []
                self.debts = []
                self.current_month = datetime.now().strftime("%m/%Y")
                print("📁 Primeira execução - dados inicializados")

        except Exception as e:
            print(f"⚠️ Erro ao carregar dados: {e}")
            self.base_salary = 0.0
            self.accumulated_balance = 0.0
            self.salary = 0.0
            self.expenses = []
            self.goals = []
            self.debts = []
            self.current_month = datetime.now().strftime("%m/%Y")

    def save_data(self):
        """Salva dados em arquivo local (UTF-8 safe)"""
        try:
            data = {
                "salary": self.base_salary,
                "accumulated_balance": self.accumulated_balance,
                "expenses": self.expenses,
                "goals": self.goals,
                "debts": self.debts,
                "current_month": self.current_month
            }

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"💾 Dados salvos em {self.data_file}")

        except Exception as e:
            print(f"❌ Erro ao salvar dados: {e}")

    def check_new_month(self):
        """Verifica transição de mês"""
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
        real_expenses = [expense for expense in self.expenses if expense['amount'] > 0]

        if not real_expenses:
            return [], 0, "", []

        descriptions = [expense['description'].lower().strip() for expense in real_expenses]
        description_counter = Counter(descriptions)
        most_common = description_counter.most_common(5)

        expense_by_desc = {}
        for expense in real_expenses:
            desc = expense['description'].lower().strip()
            expense_by_desc[desc] = expense_by_desc.get(desc, 0) + expense['amount']

        highest_spending = max(expense_by_desc.items(), key=lambda x: x[1]) if expense_by_desc else ("", 0)
        top_expenses = sorted(real_expenses, key=lambda x: x['amount'], reverse=True)[:3]

        return most_common, highest_spending[1], highest_spending[0], top_expenses

    def create_elegant_card(self, content, accent_color="#2563EB"):
        """Cria card elegante"""
        return ft.Container(
            content=content,
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=20,
            padding=ft.padding.all(20),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color="#1F293740",
                offset=ft.Offset(0, 6)
            )
        )

    def create_premium_button(self, text, on_click, icon=None, color="#2563EB"):
        """Cria botão premium"""
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

    def create_stats_card(self, icon, title, value, unit, color, bg_color):
        """Cria card de estatística"""
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
                ft.Text(unit, size=10, color="#9CA3AF") if unit else ft.Container(height=12)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=20,
            padding=ft.padding.all(20),
            width=125,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color="#1F293720",
                offset=ft.Offset(0, 4)
            )
        )

    def create_components(self):
        """Cria todos os componentes"""
        self.create_expenses_view()
        self.create_goals_view()
        self.create_finance_view()
        self.create_summary_view()

        self.main_container = ft.Container(
            content=self.expenses_view,
            expand=True,
            padding=ft.padding.all(16),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#FAFBFF", "#F1F5F9", "#E2E8F0"]
            )
        )

    def create_expenses_view(self):
        """Cria vista de despesas"""
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

                # Breakdown do salário
                ft.Column([
                    ft.Row([
                        ft.Text("Salário Base:", size=13, color="#6B7280"),
                        ft.Text(f"{self.base_salary} Kz", size=13, weight=ft.FontWeight.BOLD, color="#2563EB")
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

                # Rendas extras
                ft.Column([
                    ft.Row([
                        ft.Text("Rendas Extras:", size=11, color="#6B7280"),
                        ft.Text(
                            f"+{sum(abs(expense['amount']) for expense in self.expenses if expense['amount'] < 0):,.0f} Kz",
                            size=11, weight=ft.FontWeight.BOLD, color="#059669")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=6)
                ]) if any(expense['amount'] < 0 for expense in self.expenses) else ft.Container(),

                # Stats principais
                ft.Row([
                    self.create_stats_card("💰", "Salário Total", f"{self.salary:,.0f}", "Kz", "#2563EB", "#EFF6FF"),
                    self.create_stats_card("💸", "Gastos", f"{total_spent:,.0f}", "Kz", "#EC4899", "#FDF2F8"),
                    self.create_stats_card("💎", "Saldo", f"{current_balance:,.0f}", "Kz",
                                           "#059669" if current_balance >= 0 else "#DC2626",
                                           "#ECFDF5" if current_balance >= 0 else "#FEF2F2")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=15),

                # Barra de progresso
                ft.Column([
                    ft.Row([
                        ft.Text("Orçamento Utilizado", size=12, color="#4B5563", weight=ft.FontWeight.BOLD),
                        ft.Text(f"{(total_spent / self.salary * 100):,.1f}%" if self.salary > 0 else "0%",
                                size=12, color="#2563EB", weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=6),
                    ft.ProgressBar(
                        value=min(total_spent / self.salary, 1.0) if self.salary > 0 else 0,
                        bgcolor="#E5E7EB",
                        color="#EC4899" if total_spent > self.salary * 0.8 else "#059669",
                        height=8
                    )
                ])
            ])
        )

        # Campos de despesas
        self.expense_description = ft.Container(
            content=ft.TextField(
                label="Descrição da Despesa",
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
                label="Valor (Kz)",
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

        # Análise de gastos
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

        # Lista de despesas
        self.expenses_list = ft.ListView(
            spacing=12,
            padding=ft.padding.all(0),
            height=280
        )
        self.update_expenses_list()

        # Vista completa
        self.expenses_view = ft.Column([
            ft.Text("Controle de Despesas", size=32, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text("Gerencie suas finanças com elegância", size=16, color="#6B7280"),
            ft.Container(height=28),
            self.salary_field,
            ft.Container(height=24),
            self.quick_summary_card,
            ft.Container(height=24),
            spending_analysis,
            ft.Container(height=32),
            ft.Text("Nova Despesa", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),
            self.expense_description,
            ft.Container(height=16),
            self.expense_amount,
            ft.Container(height=24),
            self.create_premium_button("Adicionar Despesa", self.add_expense, ft.icons.ADD_CIRCLE, "#2563EB"),
            ft.Container(height=32),
            ft.Text("Histórico de Despesas", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),
            self.create_elegant_card(self.expenses_list)
        ], scroll=ft.ScrollMode.AUTO)

    def create_goals_view(self):
        """Cria vista de metas"""
        _, current_balance = self.calculate_totals()

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
                                "Pronto para seus objetivos!" if current_balance > 0 else "Ajuste seus gastos",
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

        # Campos de metas
        self.goal_name = ft.Container(
            content=ft.TextField(
                label="Nome do Artigo",
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
                label="Custo Total (Kz)",
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
                label="Valor a Poupar por Mês (Kz)",
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
            content=ft.Text("Tempo estimado: -- meses", size=16, color="#D97706", weight=ft.FontWeight.BOLD),
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

        # Vista completa
        self.goals_view = ft.Column([
            ft.Text("Metas de Poupança", size=32, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text("Transforme sonhos em objetivos alcançáveis", size=16, color="#6B7280"),
            ft.Container(height=28),
            self.savings_potential_card,
            ft.Container(height=32),
            ft.Text("Nova Meta", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
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
            ft.Text("Minhas Metas", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),
            self.create_elegant_card(self.goals_list)
        ], scroll=ft.ScrollMode.AUTO)

    def create_finance_view(self):
        """Cria vista de renda e dívidas"""
        _, current_balance = self.calculate_totals()
        total_debts = sum(debt.get('total_amount', 0) - debt.get('paid_amount', 0) for debt in self.debts)
        total_extra_income = sum(abs(expense['amount']) for expense in self.expenses if expense['amount'] < 0)
        debt_ratio = (total_debts / self.salary * 100) if self.salary > 0 else 0

        # Resumo financeiro
        self.finance_summary_card = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("💰", size=32),
                    ft.Column([
                        ft.Text("Panorama Financeiro", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Rendas extras e controle de dívidas", size=14, color="#6B7280")
                    ], expand=True, spacing=4)
                ], spacing=16),
                ft.Container(height=20),

                ft.Row([
                    self.create_stats_card("💸", "Renda Extra", f"{total_extra_income:,.0f}", "Kz", "#059669",
                                           "#ECFDF5"),
                    self.create_stats_card("💳", "Em Dívidas", f"{total_debts:,.0f}", "Kz", "#DC2626", "#FEF2F2"),
                    self.create_stats_card("📊", "% Comprometido", f"{debt_ratio:.1f}%", "",
                                           "#DC2626" if debt_ratio > 30 else "#F59E0B" if debt_ratio > 20 else "#059669",
                                           "#FEF2F2" if debt_ratio > 30 else "#FFFBEB" if debt_ratio > 20 else "#ECFDF5")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=16),

                ft.Container(
                    content=ft.Text(
                        "ALERTA! Endividamento Alto! Evite novas dívidas!" if debt_ratio > 30
                        else "CUIDADO! Mantenha abaixo de 30%!" if debt_ratio > 20
                        else "Endividamento Controlado!" if debt_ratio > 0
                        else "Sem Dívidas Ativas!",
                        size=14, weight=ft.FontWeight.BOLD,
                        color="#DC2626" if debt_ratio > 30 else "#F59E0B" if debt_ratio > 20 else "#059669"
                    ),
                    bgcolor="#FEF2F2" if debt_ratio > 30 else "#FFFBEB" if debt_ratio > 20 else "#ECFDF5",
                    border_radius=25,
                    padding=ft.padding.symmetric(horizontal=16, vertical=10)
                )
            ])
        )

        # Campos de renda extra
        self.extra_income_description = ft.Container(
            content=ft.TextField(
                label="Descrição da Renda Extra",
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

        self.extra_income_amount = ft.Container(
            content=ft.TextField(
                label="Valor (Kz)",
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

        # Campos de dívidas
        self.debt_description = ft.Container(
            content=ft.TextField(
                label="Descrição da Dívida",
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#DC2626",
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

        self.debt_total_amount = ft.Container(
            content=ft.TextField(
                label="Valor Total (Kz)",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFFFFF",
                border_color="#E5E7EB",
                focused_border_color="#DC2626",
                color="#1F2937",
                label_style=ft.TextStyle(color="#6B7280"),
                border_radius=16,
                content_padding=ft.padding.all(20),
                on_change=self.calculate_debt_impact
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
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

        self.debt_impact_estimate = ft.Container(
            content=ft.Text("Impacto no endividamento: -- %", size=16, color="#6B7280", weight=ft.FontWeight.BOLD),
            bgcolor="#F8FAFC",
            border_radius=25,
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        )

        # Lista de dívidas
        self.debts_list = ft.ListView(
            spacing=16,
            padding=ft.padding.all(0),
            height=300
        )
        self.update_debts_list()

        # Vista completa
        self.finance_view = ft.Column([
            ft.Text("Renda & Dívidas", size=32, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text("Gerencie rendas extras e controle dívidas", size=16, color="#6B7280"),
            ft.Container(height=28),
            self.finance_summary_card,
            ft.Container(height=32),
            ft.Text("Adicionar Renda Extra", size=22, weight=ft.FontWeight.BOLD, color="#059669"),
            ft.Text("Freelances, vendas, bonificações, etc.", size=14, color="#6B7280"),
            ft.Container(height=16),
            self.extra_income_description,
            ft.Container(height=16),
            self.extra_income_amount,
            ft.Container(height=20),
            self.create_premium_button("Adicionar Renda", self.add_extra_income, ft.icons.ADD_CIRCLE, "#059669"),
            ft.Container(height=32),
            ft.Text("Adicionar Dívida", size=22, weight=ft.FontWeight.BOLD, color="#DC2626"),
            ft.Text("Pense bem antes de se endividar!", size=14, color="#DC2626"),
            ft.Container(height=16),
            self.debt_description,
            ft.Container(height=16),
            self.debt_total_amount,
            ft.Container(height=16),
            self.debt_due_date,
            ft.Container(height=16),
            self.debt_impact_estimate,
            ft.Container(height=20),
            self.create_premium_button("Adicionar Dívida", self.add_debt, ft.icons.WARNING, "#DC2626"),
            ft.Container(height=32),
            ft.Text("Minhas Dívidas", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),
            self.create_elegant_card(self.debts_list)
        ], scroll=ft.ScrollMode.AUTO)

    def create_summary_view(self):
        """Cria vista de resumo/dashboard"""
        total_spent, current_balance = self.calculate_totals()
        most_common, highest_amount, highest_desc, top_expenses = self.analyze_spending_patterns()

        # Stats principais
        stats_row = ft.Row([
            self.create_stats_card("💰", "Salário Total", f"{self.salary:,.0f}", "Kz", "#2563EB", "#EFF6FF"),
            self.create_stats_card("💸", "Gastos", f"{total_spent:,.0f}", "Kz", "#EC4899", "#FDF2F8"),
            self.create_stats_card("💎", "Saldo", f"{current_balance:,.0f}", "Kz",
                                   "#059669" if current_balance >= 0 else "#DC2626",
                                   "#ECFDF5" if current_balance >= 0 else "#FEF2F2")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Top 3 gastos
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
                                content=ft.Text(f"#{i + 1}", size=18, color="#FFFFFF", weight=ft.FontWeight.BOLD),
                                bgcolor="#DC2626" if i == 0 else "#F59E0B" if i == 1 else "#6B7280",
                                border_radius=25,
                                padding=ft.padding.all(8),
                                width=35,
                                height=35
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

        # Análise por categoria
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

        # Análise de metas e dívidas
        active_goals = len(self.goals)
        total_goal_value = sum(goal['total_cost'] for goal in self.goals)
        total_saved_for_goals = sum(goal.get('saved_amount', 0) for goal in self.goals)

        active_debts = len(
            [debt for debt in self.debts if debt.get('total_amount', 0) - debt.get('paid_amount', 0) > 0])
        total_debts = sum(debt.get('total_amount', 0) - debt.get('paid_amount', 0) for debt in self.debts)
        total_paid_debts = sum(debt.get('paid_amount', 0) for debt in self.debts)

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
                            ft.Text("Metas", size=10, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(str(active_goals), size=20, weight=ft.FontWeight.BOLD, color="#059669")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#ECFDF5",
                        border_radius=18,
                        padding=ft.padding.all(20),
                        expand=True
                    ),
                    ft.Container(),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Total", size=10, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{total_goal_value:,.0f}", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),
                            ft.Text("Kz", size=12, color="#9CA3AF")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#F8FAFC",
                        border_radius=18,
                        padding=ft.padding.all(20),
                        expand=True
                    ),
                    ft.Container(),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Pago", size=10, color="#6B7280", weight=ft.FontWeight.BOLD),
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

        debts_analysis = self.create_elegant_card(
            ft.Column([
                ft.Row([
                    ft.Text("💳", size=32),
                    ft.Column([
                        ft.Text("Status das Dívidas", size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Controle do seu endividamento", size=14, color="#6B7280")
                    ], expand=True, spacing=4)
                ], spacing=16),
                ft.Container(height=24),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Dívidas", size=10, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(str(active_debts), size=20, weight=ft.FontWeight.BOLD,
                                    color="#DC2626" if active_debts > 0 else "#059669")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#FEF2F2" if active_debts > 0 else "#ECFDF5",
                        border_radius=18,
                        padding=ft.padding.all(20),
                        expand=True
                    ),
                    ft.Container(),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Devendo", size=10, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{total_debts:,.0f}", size=20, weight=ft.FontWeight.BOLD,
                                    color="#DC2626" if total_debts > 0 else "#059669"),
                            ft.Text("Kz", size=12, color="#9CA3AF")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="#FEF2F2" if total_debts > 0 else "#ECFDF5",
                        border_radius=18,
                        padding=ft.padding.all(20),
                        expand=True
                    ),
                    ft.Container(),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Já Pago", size=10, color="#6B7280", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{total_paid_debts:,.0f}", size=20, weight=ft.FontWeight.BOLD, color="#059669"),
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

        # Transações recentes
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

        # Vista completa
        self.summary_view = ft.Column([
            ft.Text("Dashboard Financeiro", size=28, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text(f"Visão completa do mês {self.current_month}", size=14, color="#6B7280"),
            ft.Container(height=20),
            stats_row,
            ft.Container(height=20),
            top_expenses_card,
            ft.Container(height=20),
            spending_insights,
            ft.Container(height=20),
            goals_analysis,
            ft.Container(height=20),
            debts_analysis,
            ft.Container(height=25),
            ft.Text("Transações Recentes", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=12),
            self.create_elegant_card(
                recent_expenses_list if recent_expenses else ft.Text("Nenhuma transação registrada ainda", size=14,
                                                                     color="#6B7280")
            )
        ], scroll=ft.ScrollMode.AUTO)

    def setup_navigation(self):
        """Configura navegação"""
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.CREDIT_CARD_OUTLINED,
                    label="Despesas",
                    selected_icon=ft.icons.CREDIT_CARD
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.SAVINGS_OUTLINED,
                    label="Metas",
                    selected_icon=ft.icons.SAVINGS
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.ACCOUNT_BALANCE_OUTLINED,
                    label="Renda & Dívidas",
                    selected_icon=ft.icons.ACCOUNT_BALANCE
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.ANALYTICS_OUTLINED,
                    label="Dashboard",
                    selected_icon=ft.icons.ANALYTICS
                )
            ],
            on_change=self.navigation_changed,
            bgcolor="#FFFFFF",
            indicator_color="#EFF6FF",
            selected_index=0,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW
        )

        self.page.add(
            ft.Column([
                self.main_container,
                self.navigation_bar
            ], expand=True, spacing=0)
        )

    # DIÁLOGOS DE INVESTIMENTO/PAGAMENTO
    def show_add_payment_dialog(self, goal_index):
        """Diálogo para investir na meta"""
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
                        self.goals[goal_index]['saved_amount'] = self.goals[goal_index].get('saved_amount', 0) + amount

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
                        print(f"✅ Investimento em meta: {amount} Kz")
                    else:
                        error_text.value = f"Saldo insuficiente! Disponível: {current_balance:,.0f} Kz"
                        error_text.color = "#DC2626"
                        self.page.update()
            except ValueError:
                error_text.value = "Valor inválido!"
                error_text.color = "#DC2626"
                self.page.update()

        error_text = ft.Text("", size=12)

        dialog = ft.AlertDialog(
            title=ft.Text(f"Investir na Meta", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),
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
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False) or self.page.update()),
                ft.ElevatedButton("Investir", on_click=add_payment, bgcolor="#059669", color="#FFFFFF")
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_debt_payment_dialog(self, debt_index):
        """Diálogo para pagar dívida"""
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
                            self.debts[debt_index]['paid_amount'] = self.debts[debt_index].get('paid_amount',
                                                                                               0) + amount

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
                            print(f"✅ Pagamento de dívida: {amount} Kz")
                        else:
                            error_text.value = f"Valor maior que a dívida restante: {remaining_debt:,.0f} Kz"
                            error_text.color = "#DC2626"
                            self.page.update()
                    else:
                        error_text.value = f"Saldo insuficiente! Disponível: {current_balance:,.0f} Kz"
                        error_text.color = "#DC2626"
                        self.page.update()
            except ValueError:
                error_text.value = "Valor inválido!"
                error_text.color = "#DC2626"
                self.page.update()

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
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False) or self.page.update()),
                ft.ElevatedButton("Pagar", on_click=add_payment, bgcolor="#059669", color="#FFFFFF")
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    # FUNÇÕES DE NAVEGAÇÃO E EVENTOS
    def navigation_changed(self, e):
        """Muda navegação"""
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
        """Atualiza salário"""
        try:
            self.base_salary = float(e.control.value) if e.control.value else 0.0
            self.salary = self.base_salary + self.accumulated_balance
            self.save_data()
            self.update_all_views()
        except ValueError:
            pass

    def add_extra_income(self, e):
        """Adiciona renda extra"""
        description_field = self.extra_income_description.content
        amount_field = self.extra_income_amount.content

        if not description_field.value or not amount_field.value:
            return

        try:
            amount = float(amount_field.value)
            self.accumulated_balance += amount
            self.salary = self.base_salary + self.accumulated_balance

            income_entry = {
                'description': f"Renda Extra: {description_field.value}",
                'amount': -amount,
                'date': datetime.now().strftime("%d/%m/%Y")
            }

            self.expenses.append(income_entry)
            self.save_data()

            description_field.value = ""
            amount_field.value = ""

            self.update_all_views()
        except ValueError:
            pass

    def calculate_debt_impact(self, e):
        """Calcula impacto da dívida"""
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
        """Adiciona dívida"""
        description_field = self.debt_description.content
        amount_field = self.debt_total_amount.content
        due_date_field = self.debt_due_date.content

        if not description_field.value or not amount_field.value:
            return

        try:
            amount = float(amount_field.value)
            current_debts = sum(debt.get('total_amount', 0) - debt.get('paid_amount', 0) for debt in self.debts)
            new_debt_ratio = ((current_debts + amount) / self.salary * 100) if self.salary > 0 else 0

            if new_debt_ratio > 30:
                self.show_debt_confirmation_dialog(amount, new_debt_ratio)
                return

            self.create_debt(amount, description_field, amount_field, due_date_field)

        except ValueError:
            pass

    def show_debt_confirmation_dialog(self, amount, debt_ratio):
        """Confirmação para dívida alta"""
        title = "PERIGO EXTREMO!" if debt_ratio > 50 else "CUIDADO!"
        message = (f"Esta dívida levará seu endividamento para {debt_ratio:.1f}% da renda!\n\n" +
                   ("ISTO É MUITO PERIGOSO!" if debt_ratio > 50 else "Mais de 30% é considerado alto risco.") +
                   "\n\nTem certeza que deseja continuar?")
        color = "#DC2626" if debt_ratio > 50 else "#F59E0B"

        dialog = ft.AlertDialog(
            title=ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=color),
            content=ft.Text(message, size=14, color="#1F2937"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False) or self.page.update()),
                ft.ElevatedButton("Continuar Mesmo Assim", on_click=lambda e: self.confirm_add_debt(dialog, amount),
                                  bgcolor=color, color="#FFFFFF")
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def confirm_add_debt(self, dialog, amount):
        """Confirma adição da dívida"""
        description_field = self.debt_description.content
        amount_field = self.debt_total_amount.content
        due_date_field = self.debt_due_date.content

        self.create_debt(amount, description_field, amount_field, due_date_field)
        dialog.open = False
        self.page.update()

    def create_debt(self, amount, description_field, amount_field, due_date_field):
        """Cria a dívida"""
        debt = {
            'description': description_field.value,
            'total_amount': amount,
            'paid_amount': 0,
            'due_date': due_date_field.value if due_date_field.value else "Sem prazo",
            'created_date': datetime.now().strftime("%d/%m/%Y")
        }

        self.debts.append(debt)
        self.save_data()

        description_field.value = ""
        amount_field.value = ""
        due_date_field.value = ""
        self.debt_impact_estimate.content.value = "Impacto no endividamento: -- %"
        self.debt_impact_estimate.bgcolor = "#F8FAFC"

        self.update_all_views()

    def remove_debt(self, index):
        """Remove dívida"""

        def remove(e):
            self.debts.pop(index)
            self.save_data()
            self.update_all_views()

        return remove

    def add_expense(self, e):
        """Adiciona despesa"""
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

            description_field.value = ""
            amount_field.value = ""

            self.update_all_views()
        except ValueError:
            pass

    def remove_expense(self, index):
        """Remove despesa"""

        def remove(e):
            self.expenses.pop(index)
            self.save_data()
            self.update_all_views()

        return remove

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
                    self.goal_time_estimate.content.value = f"Tempo estimado: {months} meses"
                else:
                    self.goal_time_estimate.content.value = "Tempo estimado: -- meses"

                self.page.update()
        except ValueError:
            self.goal_time_estimate.content.value = "Tempo estimado: -- meses"
            self.page.update()

    def add_goal(self, e):
        """Adiciona meta"""
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

            name_field.value = ""
            total_cost_field.value = ""
            monthly_saving_field.value = ""
            self.goal_time_estimate.content.value = "Tempo estimado: -- meses"

            self.update_all_views()
        except ValueError:
            pass

    def remove_goal(self, index):
        """Remove meta"""

        def remove(e):
            self.goals.pop(index)
            self.save_data()
            self.update_all_views()

        return remove

    # FUNÇÕES DE ATUALIZAÇÃO DAS LISTAS
    def update_expenses_list(self):
        """Atualiza lista de despesas"""
        self.expenses_list.controls.clear()

        for i, expense in enumerate(reversed(self.expenses)):
            is_goal_payment = expense['description'].startswith("Pagamento:")
            is_extra_income = expense['description'].startswith("Renda Extra:")
            is_debt_payment = expense['description'].startswith("Pagamento Dívida:")

            if is_extra_income:
                icon = ft.icons.TRENDING_UP
                icon_color = "#059669"
                bg_color = "#ECFDF5"
                border_color = "#A7F3D0"
                text_color = "#059669"
                amount_color = "#059669"
            elif is_goal_payment or is_debt_payment:
                icon = ft.icons.SAVINGS if is_goal_payment else ft.icons.CREDIT_CARD
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
                        content=ft.Icon(icon, color=icon_color, size=20),
                        bgcolor=bg_color,
                        border_radius=30,
                        padding=ft.padding.all(12)
                    ),
                    ft.Column([
                        ft.Text(expense['description'], size=15, weight=ft.FontWeight.NORMAL, color=text_color),
                        ft.Text(expense['date'], size=12, color="#6B7280")
                    ], expand=True, spacing=4),
                    ft.Column([
                        ft.Text(
                            f"+{abs(expense['amount']):,.0f} Kz" if is_extra_income
                            else f"{expense['amount']:,.0f} Kz",
                            size=15, weight=ft.FontWeight.BOLD, color=amount_color
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color="#DC2626",
                            icon_size=18,
                            on_click=self.remove_expense(len(self.expenses) - 1 - i),
                            tooltip="Remover entrada"
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=0)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor="#FFFFFF",
                border=ft.border.all(1, border_color),
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
        """Atualiza lista de metas COM BOTÃO INVESTIR"""
        self.goals_list.controls.clear()

        for i, goal in enumerate(self.goals):
            saved_amount = goal.get('saved_amount', 0)
            progress = saved_amount / goal['total_cost'] if goal['total_cost'] > 0 else 0
            remaining_cost = goal['total_cost'] - saved_amount
            remaining_months = math.ceil(remaining_cost / goal['monthly_saving']) if goal[
                                                                                         'monthly_saving'] > 0 and remaining_cost > 0 else 0

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

                    ft.Column([
                        ft.ProgressBar(
                            value=min(progress, 1.0),
                            bgcolor="#E5E7EB",
                            color="#059669" if progress >= 1.0 else "#2563EB",
                            height=10
                        ),
                        ft.Container(height=12),
                        ft.Row([
                            ft.Text(f"{saved_amount:,.0f} / {goal['total_cost']:,.0f} Kz", size=14, color="#6B7280"),
                            ft.Text(f"{progress * 100:.1f}%", size=14, weight=ft.FontWeight.BOLD,
                                    color="#059669" if progress >= 1.0 else "#2563EB")
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    ft.Container(height=20),

                    # BOTÃO INVESTIR NA META RESTAURADO
                    ft.Container(
                        content=ft.Text("Investir na Meta", size=14, weight=ft.FontWeight.BOLD, color="#059669"),
                        bgcolor="#ECFDF5",
                        border=ft.border.all(1, "#A7F3D0"),
                        border_radius=25,
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        on_click=lambda e, idx=i: self.show_add_payment_dialog(idx)
                    ) if progress < 1.0 else ft.Container(
                        content=ft.Text("Objetivo Alcançado!", size=14, weight=ft.FontWeight.BOLD, color="#059669"),
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

    def update_debts_list(self):
        """Atualiza lista de dívidas COM BOTÃO PAGAR"""
        self.debts_list.controls.clear()

        for i, debt in enumerate(self.debts):
            paid_amount = debt.get('paid_amount', 0)
            total_amount = debt['total_amount']
            remaining = total_amount - paid_amount
            progress = paid_amount / total_amount if total_amount > 0 else 0

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
                            content=ft.Icon(icon, color=icon_color, size=26),
                            bgcolor=bg_color,
                            border_radius=30,
                            padding=ft.padding.all(14)
                        ),
                        ft.Column([
                            ft.Text(debt['description'], size=17, weight=ft.FontWeight.BOLD, color="#1F2937"),
                            ft.Text(status_text, size=13, color=status_color, weight=ft.FontWeight.NORMAL),
                            ft.Text(f"Vencimento: {debt['due_date']}", size=11, color="#6B7280")
                        ], expand=True, spacing=2),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color="#DC2626",
                            icon_size=20,
                            on_click=self.remove_debt(i),
                            tooltip="Remover dívida"
                        )
                    ]),
                    ft.Container(height=20),

                    ft.Column([
                        ft.ProgressBar(
                            value=min(progress, 1.0),
                            bgcolor="#E5E7EB",
                            color="#059669" if progress >= 1.0 else "#DC2626",
                            height=10
                        ),
                        ft.Container(height=12),
                        ft.Row([
                            ft.Text(f"{paid_amount:,.0f} / {total_amount:,.0f} Kz", size=14, color="#6B7280"),
                            ft.Text(f"{progress * 100:.1f}% pago", size=14, weight=ft.FontWeight.BOLD,
                                    color="#059669" if progress >= 1.0 else "#DC2626")
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    ft.Container(height=20),

                    # BOTÃO FAZER PAGAMENTO RESTAURADO
                    ft.Container(
                        content=ft.Text("Fazer Pagamento", size=14, weight=ft.FontWeight.BOLD, color="#059669"),
                        bgcolor="#ECFDF5",
                        border=ft.border.all(1, "#A7F3D0"),
                        border_radius=25,
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        on_click=lambda e, idx=i: self.show_debt_payment_dialog(idx)
                    ) if progress < 1.0 else ft.Container(
                        content=ft.Text("Dívida Quitada!", size=14, weight=ft.FontWeight.BOLD, color="#059669"),
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
            self.debts_list.controls.append(debt_card)

    # FUNÇÕES DE ATUALIZAÇÃO DE VISTAS
    def update_expenses_view(self):
        """Atualiza vista de despesas"""
        self.create_expenses_view()
        if hasattr(self, 'main_container') and hasattr(self, 'expenses_view'):
            current_view = self.main_container.content
            if current_view == self.expenses_view or self.navigation_bar.selected_index == 0:
                self.main_container.content = self.expenses_view

    def update_goals_view(self):
        """Atualiza vista de metas"""
        self.create_goals_view()
        if hasattr(self, 'main_container') and hasattr(self, 'goals_view'):
            current_view = self.main_container.content
            if current_view == self.goals_view or self.navigation_bar.selected_index == 1:
                self.main_container.content = self.goals_view

    def update_finance_view(self):
        """Atualiza vista de renda e dívidas"""
        self.create_finance_view()
        if hasattr(self, 'main_container') and hasattr(self, 'finance_view'):
            current_view = self.main_container.content
            if current_view == self.finance_view or self.navigation_bar.selected_index == 2:
                self.main_container.content = self.finance_view

    def update_summary_view(self):
        """Atualiza vista de resumo"""
        self.create_summary_view()
        if hasattr(self, 'main_container') and hasattr(self, 'summary_view'):
            current_view = self.main_container.content
            if current_view == self.summary_view or self.navigation_bar.selected_index == 3:
                self.main_container.content = self.summary_view

    def update_all_views(self):
        """Atualiza todas as vistas"""
        current_index = getattr(self.navigation_bar, 'selected_index', 0)

        # Recria todas as vistas para garantir atualização
        self.create_expenses_view()
        self.create_goals_view()
        self.create_finance_view()
        self.create_summary_view()

        # Atualiza vista atual
        if current_index == 0:
            self.main_container.content = self.expenses_view
        elif current_index == 1:
            self.main_container.content = self.goals_view
        elif current_index == 2:
            self.main_container.content = self.finance_view
        elif current_index == 3:
            self.main_container.content = self.summary_view

        self.page.update()
        print(f"✅ Todas as vistas atualizadas")


def main(page: ft.Page):
    """Função principal"""
    try:
        print("🚀 Iniciando Gestão Financeira Premium...")
        app = FinancialApp(page)
        print("✅ App carregado com sucesso!")
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {e}")
        print(traceback.format_exc())

        page.title = "Erro - Gestão Financeira"
        page.add(
            ft.Column([
                ft.Icon(ft.icons.ERROR, size=64, color="#DC2626"),
                ft.Text("Erro ao carregar aplicativo", size=24, weight=ft.FontWeight.BOLD, color="#DC2626"),
                ft.Text(str(e), size=14, color="#6B7280"),
                ft.ElevatedButton("Fechar", on_click=lambda e: page.window_close())
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )


if __name__ == "__main__":
    try:
        print("🚀 Iniciando Gestão Financeira Premium...")

        if len(sys.argv) > 1 and "--web" in sys.argv:
            print("🌐 Modo desenvolvimento web")
            ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000)
        else:
            print("📱 Modo aplicativo (APK)")
            ft.app(target=main, view=ft.AppView.FLET_APP)

    except Exception as e:
        print(f"❌ ERRO CRÍTICO no entry point: {e}")
        print(traceback.format_exc())
        sys.exit(1)