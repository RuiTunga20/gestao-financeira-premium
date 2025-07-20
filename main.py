import flet as ft
import time
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Produto:
    id: int
    nome: str
    descricao: str
    preco: float
    categoria: str
    imagem: str
    disponivel: bool = True


@dataclass
class ItemCarrinho:
    produto: Produto
    quantidade: int
    observacoes: str = ""


class BryzzaFoodApp:
    def __init__(self):
        # Cores do tema (baseadas em tons quentes de brasa)
        self.cores = {
            'primary': '#D32F2F',  # Vermelho brasa
            'secondary': '#FF5722',  # Laranja fogo
            'accent': '#5D4037',  # Marrom escuro
            'background': '#FFF8E1',  # Creme claro
            'surface': '#FFFFFF',  # Branco
            'text_primary': '#212121',  # Cinza escuro
            'text_secondary': '#757575'  # Cinza médio
        }

        self.carrinho: List[ItemCarrinho] = []
        self.total_carrinho = 0.0
        self.usuario_logado = False
        self.dados_usuario = {}

        # Base de dados dos produtos
        self.produtos = [
            # COMBOS PREMIUM
            Produto(1, "Combo Família Supremo",
                    "1/2 frango, lombo suíno (2 bifes), 2 salsichas, batatas fritas, arroz, farofa e molho especial. Serve 2 pessoas.",
                    45.90, "combos", "🔥"),
            Produto(2, "Combo BBQ Costelinha",
                    "Costelinha suína marinada com molho BBQ, batatas fritas, arroz, farofa e molho exclusivo. Serve 2 pessoas.",
                    52.90, "combos", "🍖"),
            Produto(3, "Combo Picanha Premium",
                    "4 bifes de picanha grelhados, batatas fritas douradas, arroz soltinho, farofa crocante e molho especial. Serve 2 pessoas.",
                    59.90, "combos", "🥩"),

            # CARNES GRELHADAS
            Produto(4, "Picanha Angus Especial",
                    "Tiras de picanha Angus na brasa, com cebola caramelizada e batatas fritas. Sabor incomparável!",
                    39.90, "carnes", "🥩"),
            Produto(5, "Frango Grelhado Completo",
                    "1/2 frango suculento grelhado no carvão, temperos especiais, acompanha arroz e batatas.",
                    28.90, "carnes", "🍗"),
            Produto(6, "Alcatra na Brasa",
                    "Bife de alcatra grelhado no ponto, suculento e temperado com ervas especiais.",
                    35.90, "carnes", "🥩"),

            # HAMBÚRGUERS GOURMET  
            Produto(7, "Burger Angus Premium",
                    "Hambúrguer bovino Angus 170g, compota de bacon, cebola caramelizada, queijo derretido no pão brioche.",
                    32.90, "hamburguers", "🍔"),
            Produto(8, "Burger da Casa",
                    "Hambúrguer artesanal 150g, alface, tomate, cebola roxa, molho especial e batatas rústicas.",
                    27.90, "hamburguers", "🍔"),

            # ACOMPANHAMENTOS
            Produto(9, "Batatas Fritas Premium",
                    "Batatas corte especial, douradas e crocantes, temperadas com ervas.",
                    12.90, "acompanhamentos", "🍟"),
            Produto(10, "Farofa da Casa",
                    "Farofa artesanal crocante com bacon e temperos especiais.",
                    8.90, "acompanhamentos", "🌾"),
            Produto(11, "Queijo Coalho Grelhado",
                    "Queijo coalho enrolado no bacon, assado na brasa até dourar.",
                    15.90, "acompanhamentos", "🧀"),

            # BEBIDAS
            Produto(12, "Refrigerante Lata 350ml",
                    "Coca-Cola, Guaraná Antarctica, Fanta ou Sprite.",
                    4.90, "bebidas", "🥤"),
            Produto(13, "Suco Natural 500ml",
                    "Laranja, limão, acerola ou maracujá. Fresquinho e natural.",
                    7.90, "bebidas", "🧃"),
            Produto(14, "Água Mineral 500ml",
                    "Água mineral natural gelada.",
                    2.90, "bebidas", "💧"),
        ]

    def main(self, page: ft.Page):
        page.title = "BryzzaFood Brasas - O Sabor da Brasa"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = self.cores['background']
        page.padding = 0
        page.spacing = 0

        # Configurar tema customizado
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=self.cores['primary'],
                secondary=self.cores['secondary'],
                background=self.cores['background'],
                surface=self.cores['surface'],
            )
        )

        # Estados da aplicação
        self.page = page
        self.categoria_selecionada = "todos"
        self.tela_atual = "home"

        # Componentes principais
        self.app_bar = self.criar_app_bar()
        self.conteudo_principal = ft.Container()
        self.navegacao_inferior = self.criar_navegacao_inferior()

        # Layout principal
        page.add(
            ft.Column([
                self.app_bar,
                ft.Container(
                    content=self.conteudo_principal,
                    expand=True,
                    padding=0,
                ),
                self.navegacao_inferior
            ], spacing=0)
        )

        # Carregar tela inicial
        self.carregar_tela_home()
        page.update()

    def criar_app_bar(self):
        self.contador_carrinho = ft.Text("0", size=12, weight=ft.FontWeight.BOLD, color="white")

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text("BryzzaFood", size=20, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("O Sabor da Brasa", size=12, color="white", opacity=0.9)
                    ], spacing=2),
                    expand=True
                ),
                ft.Container(
                    content=ft.Stack([
                        ft.IconButton(
                            icon=ft.icons.SHOPPING_CART,
                            icon_color="white",
                            icon_size=28,
                            on_click=self.abrir_carrinho
                        ),
                        ft.Container(
                            content=self.contador_carrinho,
                            bgcolor=self.cores['secondary'],
                            border_radius=10,
                            padding=ft.padding.all(4),
                            top=5,
                            right=5,
                            width=20,
                            height=20,
                        )
                    ]),
                    width=50,
                    height=50
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=self.cores['primary'],
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            height=80
        )

    def criar_navegacao_inferior(self):
        return ft.Container(
            content=ft.Row([
                self.criar_botao_nav("home", ft.icons.HOME, "Início"),
                self.criar_botao_nav("cardapio", ft.icons.RESTAURANT_MENU, "Cardápio"),
                self.criar_botao_nav("pedidos", ft.icons.RECEIPT_LONG, "Pedidos"),
                self.criar_botao_nav("perfil", ft.icons.PERSON, "Perfil"),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            bgcolor=self.cores['surface'],
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.colors.GREY_300),
            height=70
        )

    def criar_botao_nav(self, tela, icone, texto):
        ativo = self.tela_atual == tela
        cor = self.cores['primary'] if ativo else self.cores['text_secondary']

        return ft.Container(
            content=ft.Column([
                ft.Icon(icone, color=cor, size=24),
                ft.Text(texto, size=10, color=cor, weight=ft.FontWeight.BOLD if ativo else ft.FontWeight.NORMAL)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            on_click=lambda e, t=tela: self.navegar_para(t),
            padding=ft.padding.all(8),
            border_radius=8
        )

    def navegar_para(self, tela):
        self.tela_atual = tela

        if tela == "home":
            self.carregar_tela_home()
        elif tela == "cardapio":
            self.carregar_tela_cardapio()
        elif tela == "pedidos":
            self.carregar_tela_pedidos()
        elif tela == "perfil":
            self.carregar_tela_perfil()

        self.navegacao_inferior.content = ft.Row([
            self.criar_botao_nav("home", ft.icons.HOME, "Início"),
            self.criar_botao_nav("cardapio", ft.icons.RESTAURANT_MENU, "Cardápio"),
            self.criar_botao_nav("pedidos", ft.icons.RECEIPT_LONG, "Pedidos"),
            self.criar_botao_nav("perfil", ft.icons.PERSON, "Perfil"),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

        self.page.update()

    def carregar_tela_home(self):
        banner = ft.Container(
            content=ft.Column([
                ft.Text("🔥 O Melhor dos Grelhados",
                        size=24, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
                ft.Text("Sabor autêntico e porções generosas",
                        size=16, color="white", opacity=0.9, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Ver Cardápio",
                    bgcolor=self.cores['secondary'],
                    color="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=25),
                        padding=ft.padding.symmetric(horizontal=30, vertical=15)
                    ),
                    on_click=lambda e: self.navegar_para("cardapio")
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=self.cores['primary'],
            padding=ft.padding.all(30),
            margin=ft.margin.all(0),
            gradient=ft.LinearGradient([
                ft.colors.with_opacity(0.8, self.cores['primary']),
                ft.colors.with_opacity(0.9, self.cores['accent'])
            ])
        )

        # Produtos em destaque
        destaques = ft.Container(
            content=ft.Column([
                ft.Text("🏆 Produtos em Destaque", size=20, weight=ft.FontWeight.BOLD, color=self.cores['primary']),
                ft.Container(height=10),
                ft.Row([
                    self.criar_card_produto_destaque(self.produtos[0]),  # Combo Família
                    self.criar_card_produto_destaque(self.produtos[2]),  # Combo Picanha
                ], scroll=ft.ScrollMode.AUTO),
            ]),
            padding=ft.padding.all(20)
        )

        # Vantagens
        vantagens = ft.Container(
            content=ft.Column([
                ft.Text("🚀 Por que escolher BryzzaFood?", size=18, weight=ft.FontWeight.BOLD,
                        color=self.cores['primary']),
                ft.Container(height=15),
                ft.Row([
                    self.criar_card_vantagem("⚡", "Entrega Rápida", "30-45 min"),
                    self.criar_card_vantagem("🔥", "Sabor Autêntico", "Brasa do carvão"),
                    self.criar_card_vantagem("💯", "Qualidade", "Ingredientes premium"),
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ]),
            padding=ft.padding.all(20),
            bgcolor=self.cores['surface'],
            margin=ft.margin.only(top=10)
        )

        self.conteudo_principal.content = ft.Column([
            banner,
            destaques,
            vantagens
        ], scroll=ft.ScrollMode.AUTO, spacing=0)

    def criar_card_produto_destaque(self, produto):
        return ft.Container(
            content=ft.Column([
                ft.Text(produto.imagem, size=40),
                ft.Text(produto.nome, size=14, weight=ft.FontWeight.BOLD,
                        color=self.cores['text_primary'], text_align=ft.TextAlign.CENTER),
                ft.Text(f"R$ {produto.preco:.2f}", size=16, weight=ft.FontWeight.BOLD,
                        color=self.cores['primary']),
                ft.ElevatedButton(
                    "Adicionar",
                    bgcolor=self.cores['primary'],
                    color="white",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                    on_click=lambda e, p=produto: self.adicionar_ao_carrinho(p)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            bgcolor=self.cores['surface'],
            padding=ft.padding.all(15),
            border_radius=15,
            width=160,
            height=200,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.with_opacity(0.3, "black"))
        )

    def criar_card_vantagem(self, icone, titulo, descricao):
        return ft.Container(
            content=ft.Column([
                ft.Text(icone, size=30),
                ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD, color=self.cores['primary']),
                ft.Text(descricao, size=12, color=self.cores['text_secondary'])
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            padding=ft.padding.all(15),
            width=100
        )

    def carregar_tela_cardapio(self):
        # Filtros de categoria
        categorias = ft.Container(
            content=ft.Row([
                self.criar_filtro_categoria("todos", "Todos"),
                self.criar_filtro_categoria("combos", "Combos"),
                self.criar_filtro_categoria("carnes", "Carnes"),
                self.criar_filtro_categoria("hamburguers", "Hambúrguers"),
                self.criar_filtro_categoria("acompanhamentos", "Acompanhamentos"),
                self.criar_filtro_categoria("bebidas", "Bebidas"),
            ], scroll=ft.ScrollMode.AUTO),
            padding=ft.padding.symmetric(horizontal=20, vertical=15)
        )

        # Lista de produtos
        produtos_filtrados = self.filtrar_produtos()
        lista_produtos = ft.Column([
            self.criar_card_produto(produto) for produto in produtos_filtrados
        ], spacing=10)

        self.conteudo_principal.content = ft.Column([
            categorias,
            ft.Container(
                content=lista_produtos,
                padding=ft.padding.symmetric(horizontal=20),
                expand=True
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=0)

    def criar_filtro_categoria(self, categoria, nome):
        ativo = self.categoria_selecionada == categoria

        return ft.Container(
            content=ft.Text(nome, size=14, weight=ft.FontWeight.BOLD if ativo else ft.FontWeight.NORMAL,
                            color="white" if ativo else self.cores['primary']),
            bgcolor=self.cores['primary'] if ativo else self.cores['surface'],
            padding=ft.padding.symmetric(horizontal=15, vertical=8),
            border_radius=20,
            border=ft.border.all(1, self.cores['primary']) if not ativo else None,
            on_click=lambda e, cat=categoria: self.filtrar_categoria(cat)
        )

    def filtrar_categoria(self, categoria):
        self.categoria_selecionada = categoria
        self.carregar_tela_cardapio()
        self.page.update()

    def filtrar_produtos(self):
        if self.categoria_selecionada == "todos":
            return self.produtos
        return [p for p in self.produtos if p.categoria == self.categoria_selecionada]

    def criar_card_produto(self, produto):
        return ft.Container(
            content=ft.Row([
                # Imagem/Emoji do produto
                ft.Container(
                    content=ft.Text(produto.imagem, size=40),
                    width=80,
                    height=80,
                    bgcolor=self.cores['background'],
                    border_radius=10,
                    alignment=ft.alignment.center
                ),
                # Informações do produto
                ft.Container(
                    content=ft.Column([
                        ft.Text(produto.nome, size=16, weight=ft.FontWeight.BOLD, color=self.cores['text_primary']),
                        ft.Text(produto.descricao, size=12, color=self.cores['text_secondary'], max_lines=2),
                        ft.Container(height=5),
                        ft.Row([
                            ft.Text(f"R$ {produto.preco:.2f}", size=18, weight=ft.FontWeight.BOLD,
                                    color=self.cores['primary']),
                            ft.Container(expand=True),
                            ft.ElevatedButton(
                                "Adicionar",
                                bgcolor=self.cores['primary'],
                                color="white",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=15),
                                    padding=ft.padding.symmetric(horizontal=15, vertical=8)
                                ),
                                on_click=lambda e, p=produto: self.adicionar_ao_carrinho(p)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ], spacing=5),
                    expand=True,
                    padding=ft.padding.only(left=15)
                )
            ], alignment=ft.CrossAxisAlignment.START),
            bgcolor=self.cores['surface'],
            padding=ft.padding.all(15),
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.with_opacity(0.2, "black"))
        )

    def adicionar_ao_carrinho(self, produto):
        # Verificar se produto já existe no carrinho
        for item in self.carrinho:
            if item.produto.id == produto.id:
                item.quantidade += 1
                break
        else:
            self.carrinho.append(ItemCarrinho(produto, 1))

        self.atualizar_contador_carrinho()
        self.mostrar_notificacao(f"{produto.nome} adicionado ao carrinho!")

    def atualizar_contador_carrinho(self):
        total_itens = sum(item.quantidade for item in self.carrinho)
        self.total_carrinho = sum(item.produto.preco * item.quantidade for item in self.carrinho)
        self.contador_carrinho.value = str(total_itens)
        self.page.update()

    def mostrar_notificacao(self, mensagem):
        snack = ft.SnackBar(
            content=ft.Text(mensagem, color="white"),
            bgcolor=self.cores['secondary'],
            duration=2000
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def abrir_carrinho(self, e):
        if not self.carrinho:
            self.mostrar_notificacao("Seu carrinho está vazio!")
            return

        # Criar lista de itens do carrinho
        itens_carrinho = ft.Column([
            self.criar_item_carrinho(item) for item in self.carrinho
        ], spacing=10)

        # Total do carrinho
        total_container = ft.Container(
            content=ft.Row([
                ft.Text("Total:", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(f"R$ {self.total_carrinho:.2f}", size=20, weight=ft.FontWeight.BOLD,
                        color=self.cores['primary'])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=self.cores['background'],
            padding=ft.padding.all(15),
            border_radius=10
        )

        # Modal do carrinho
        modal_carrinho = ft.AlertDialog(
            title=ft.Text("🛒 Seu Carrinho", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    itens_carrinho,
                    ft.Container(height=10),
                    total_container
                ], spacing=10),
                width=400,
                height=400
            ),
            actions=[
                ft.TextButton("Continuar Comprando", on_click=lambda e: self.fechar_modal(modal_carrinho)),
                ft.ElevatedButton(
                    "Finalizar Pedido",
                    bgcolor=self.cores['primary'],
                    color="white",
                    on_click=lambda e: self.finalizar_pedido(modal_carrinho)
                )
            ]
        )

        self.page.overlay.append(modal_carrinho)
        modal_carrinho.open = True
        self.page.update()

    def criar_item_carrinho(self, item):
        return ft.Container(
            content=ft.Row([
                ft.Text(item.produto.imagem, size=30),
                ft.Container(
                    content=ft.Column([
                        ft.Text(item.produto.nome, size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(f"R$ {item.produto.preco:.2f}", size=12, color=self.cores['primary'])
                    ], spacing=2),
                    expand=True,
                    padding=ft.padding.only(left=10)
                ),
                ft.Row([
                    ft.IconButton(
                        icon=ft.icons.REMOVE,
                        icon_size=16,
                        on_click=lambda e, it=item: self.alterar_quantidade_carrinho(it, -1),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.with_opacity(0.1, self.cores['primary']),
                            shape=ft.CircleBorder()
                        )
                    ),
                    ft.Text(str(item.quantidade), size=14, weight=ft.FontWeight.BOLD),
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        icon_size=16,
                        on_click=lambda e, it=item: self.alterar_quantidade_carrinho(it, 1),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.with_opacity(0.1, self.cores['primary']),
                            shape=ft.CircleBorder()
                        )
                    )
                ], spacing=5)
            ], alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=self.cores['surface'],
            padding=ft.padding.all(10),
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_200)
        )

    def alterar_quantidade_carrinho(self, item, delta):
        item.quantidade += delta
        if item.quantidade <= 0:
            self.carrinho.remove(item)

        self.atualizar_contador_carrinho()
        # Recarregar o modal do carrinho
        self.page.overlay.clear()
        self.abrir_carrinho(None)

    def fechar_modal(self, modal):
        modal.open = False
        self.page.overlay.remove(modal)
        self.page.update()

    def finalizar_pedido(self, modal_carrinho):
        self.fechar_modal(modal_carrinho)

        # Criar modal de finalização
        endereco_field = ft.TextField(label="Endereço de entrega", width=300)
        telefone_field = ft.TextField(label="Telefone", width=300)
        observacoes_field = ft.TextField(label="Observações", multiline=True, width=300)

        pagamento_options = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="dinheiro", label="Dinheiro"),
                ft.Radio(value="cartao", label="Cartão"),
                ft.Radio(value="pix", label="PIX")
            ]),
            value="pix"
        )

        modal_checkout = ft.AlertDialog(
            title=ft.Text("🏠 Finalizar Pedido", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    endereco_field,
                    telefone_field,
                    observacoes_field,
                    ft.Text("Forma de pagamento:", weight=ft.FontWeight.BOLD),
                    pagamento_options,
                    ft.Container(
                        content=ft.Text(f"Total: R$ {self.total_carrinho:.2f}",
                                        size=18, weight=ft.FontWeight.BOLD, color=self.cores['primary']),
                        alignment=ft.alignment.center,
                        padding=ft.padding.all(10),
                        bgcolor=self.cores['background'],
                        border_radius=5
                    )
                ], spacing=10),
                width=350,
                height=450
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.fechar_modal(modal_checkout)),
                ft.ElevatedButton(
                    "Confirmar Pedido",
                    bgcolor=self.cores['primary'],
                    color="white",
                    on_click=lambda e: self.confirmar_pedido(modal_checkout, endereco_field.value,
                                                             telefone_field.value, observacoes_field.value,
                                                             pagamento_options.value)
                )
            ]
        )

        self.page.overlay.append(modal_checkout)
        modal_checkout.open = True
        self.page.update()

    def confirmar_pedido(self, modal, endereco, telefone, observacoes, pagamento):
        if not endereco or not telefone:
            self.mostrar_notificacao("⚠️ Preencha endereço e telefone!")
            return

        # Simular processamento do pedido
        self.fechar_modal(modal)

        # Gerar número do pedido
        numero_pedido = f"BF{int(time.time())}"

        # Limpar carrinho
        self.carrinho.clear()
        self.atualizar_contador_carrinho()

        # Modal de confirmação
        modal_sucesso = ft.AlertDialog(
            title=ft.Text("✅ Pedido Confirmado!", size=20, weight=ft.FontWeight.BOLD, color=self.cores['primary']),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"Número do pedido: {numero_pedido}", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Tempo estimado: 30-45 minutos", size=14),
                    ft.Container(height=10),
                    ft.Text("🚴‍♂️ Seu pedido está sendo preparado!", size=14, text_align=ft.TextAlign.CENTER),
                    ft.Text("Você pode acompanhar o status na aba 'Pedidos'", size=12,
                            color=self.cores['text_secondary'], text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                width=300,
                height=150
            ),
            actions=[
                ft.ElevatedButton(
                    "OK",
                    bgcolor=self.cores['primary'],
                    color="white",
                    on_click=lambda e: self.fechar_modal(modal_sucesso)
                )
            ]
        )

        self.page.overlay.append(modal_sucesso)
        modal_sucesso.open = True
        self.page.update()

    def carregar_tela_pedidos(self):
        # Simular histórico de pedidos
        pedidos_exemplo = [
            {"numero": "BF1721234567", "status": "Entregue", "total": 45.90, "data": "18/07/2025"},
            {"numero": "BF1721134567", "status": "A caminho", "total": 32.90, "data": "Hoje"},
            {"numero": "BF1721034567", "status": "Preparando", "total": 52.90, "data": "Hoje"},
        ]

        lista_pedidos = ft.Column([
            self.criar_card_pedido(pedido) for pedido in pedidos_exemplo
        ], spacing=15)

        self.conteudo_principal.content = ft.Container(
            content=ft.Column([
                ft.Text("📋 Meus Pedidos", size=24, weight=ft.FontWeight.BOLD, color=self.cores['primary']),
                ft.Container(height=20),
                lista_pedidos
            ]),
            padding=ft.padding.all(20)
        )

    def criar_card_pedido(self, pedido):
        cor_status = {
            "Entregue": ft.colors.GREEN,
            "A caminho": self.cores['secondary'],
            "Preparando": self.cores['primary']
        }

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(f"Pedido #{pedido['numero'][-8:]}", size=14, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text(pedido['status'], size=12, color="white", weight=ft.FontWeight.BOLD),
                        bgcolor=cor_status.get(pedido['status'], ft.colors.GREY),
                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                        border_radius=10
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text(f"R$ {pedido['total']:.2f}", size=16, weight=ft.FontWeight.BOLD,
                            color=self.cores['primary']),
                    ft.Text(pedido['data'], size=12, color=self.cores['text_secondary'])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=5),
                ft.Row([
                    ft.ElevatedButton(
                        "Detalhes",
                        style=ft.ButtonStyle(
                            color=self.cores['primary'],
                            bgcolor=ft.colors.TRANSPARENT,
                            side=ft.BorderSide(1, self.cores['primary'])
                        ),
                        on_click=lambda e: self.mostrar_notificacao("Funcionalidade em desenvolvimento")
                    ),
                    ft.ElevatedButton(
                        "Repetir Pedido",
                        bgcolor=self.cores['primary'],
                        color="white",
                        on_click=lambda e: self.mostrar_notificacao("Produtos adicionados ao carrinho!")
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], spacing=8),
            bgcolor=self.cores['surface'],
            padding=ft.padding.all(15),
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.with_opacity(0.2, "black"))
        )

    def carregar_tela_perfil(self):
        self.conteudo_principal.content = ft.Container(
            content=ft.Column([
                # Header do perfil
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.PERSON, size=60, color="white"),
                        ft.Text("João Silva", size=20, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("joao.silva@email.com", size=14, color="white", opacity=0.8)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    bgcolor=self.cores['primary'],
                    padding=ft.padding.all(30),
                    border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20)
                ),

                # Opções do perfil
                ft.Container(
                    content=ft.Column([
                        self.criar_opcao_perfil(ft.icons.PERSON, "Dados Pessoais"),
                        self.criar_opcao_perfil(ft.icons.LOCATION_ON, "Endereços"),
                        self.criar_opcao_perfil(ft.icons.PAYMENT, "Formas de Pagamento"),
                        self.criar_opcao_perfil(ft.icons.HISTORY, "Histórico de Pedidos"),
                        self.criar_opcao_perfil(ft.icons.HELP, "Ajuda"),
                        self.criar_opcao_perfil(ft.icons.SETTINGS, "Configurações"),
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "Sair",
                            bgcolor=ft.colors.RED,
                            color="white",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=25),
                                padding=ft.padding.symmetric(horizontal=40, vertical=12)
                            ),
                            on_click=lambda e: self.mostrar_notificacao("Logout realizado!")
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    padding=ft.padding.all(20)
                )
            ], spacing=0),
            scroll=ft.ScrollMode.AUTO
        )

    def criar_opcao_perfil(self, icone, texto):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icone, size=24, color=self.cores['primary']),
                ft.Text(texto, size=16, color=self.cores['text_primary']),
                ft.Container(expand=True),
                ft.Icon(ft.icons.ARROW_FORWARD_IOS, size=16, color=self.cores['text_secondary'])
            ], alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(15),
            border_radius=10,
            on_click=lambda e: self.mostrar_notificacao(f"{texto} - Funcionalidade em desenvolvimento"),
            bgcolor=self.cores['surface'],
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.with_opacity(0.1, "black"))
        )


# Executar aplicação
def main(page: ft.Page):
    app = BryzzaFoodApp()
    app.main(page)


if __name__ == "__main__":
    ft.app(target=main, port=8080)