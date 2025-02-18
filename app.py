import flet as ft
from models import Produto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONN = "sqlite:///projeto02.db"

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def main(page: ft.Page):
    page.title = "Cadastro App"

    lista_produtos = ft.ListView()

    def carregar_produtos():
        lista_produtos.controls.clear()
        for p in session.query(Produto).all():
            lista_produtos.controls.append(
                ft.Container(
                    ft.Row(
                        [
                            ft.Text(p.titulo),
                            ft.Text(f"R$ {p.preco:.2f}"),
                            ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, p=p: editar_produto(p)),
                            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, p=p: excluir_produto(p)),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=ft.colors.BLACK12,
                    padding=15,
                    alignment=ft.alignment.center,
                    margin=3,
                    border_radius=10,
                )
            )
        page.update()

    def cadastrar(e):
        try:
            novo_produto = Produto(titulo=produto.value, preco=float(preco.value))
            session.add(novo_produto)
            session.commit()
            carregar_produtos()
            txt_erro.visible = False
            txt_acerto.visible = True
        except Exception as ex:
            print(f"Erro ao cadastrar: {ex}")
            txt_erro.visible = True
            txt_acerto.visible = False
        page.update()

    def editar_produto(produto):
        produto_edit.titulo = produto.titulo
        produto_edit.preco = produto.preco
        produto_edit.id = produto.id
        produto.value = produto.titulo
        preco.value = str(produto.preco)
        btn_produto.text = "Salvar Edição"
        btn_produto.on_click = salvar_edicao
        page.update()

    def salvar_edicao(e):
        try:
            produto_db = session.query(Produto).filter_by(id=produto_edit.id).first()
            if produto_db:
                produto_db.titulo = produto.value
                produto_db.preco = float(preco.value)
                session.commit()
                carregar_produtos()
                txt_erro.visible = False
                txt_acerto.visible = True
                btn_produto.text = "Cadastrar"
                btn_produto.on_click = cadastrar
                produto.value = ""
                preco.value = "0"
        except Exception as ex:
            print(f"Erro ao editar: {ex}")
            txt_erro.visible = True
            txt_acerto.visible = False
        page.update()

    def excluir_produto(produto):
        try:
            produto_db = session.query(Produto).filter_by(id=produto.id).first()
            if produto_db:
                session.delete(produto_db)
                session.commit()
                carregar_produtos()
                txt_erro.visible = False
                txt_acerto.visible = True
        except Exception as ex:
            print(f"Erro ao excluir: {ex}")
            txt_erro.visible = True
            txt_acerto.visible = False
        page.update()

    txt_erro = ft.Container(ft.Text('Erro ao cadastrar o Produto'), visible=False, bgcolor=ft.colors.RED, padding=10, alignment=ft.alignment.center)
    txt_acerto = ft.Container(ft.Text('Produto cadastrado com sucesso'), visible=False, bgcolor=ft.colors.GREEN, padding=10, alignment=ft.alignment.center)

    txt_titulo = ft.Text('Título do Produto:')
    produto = ft.TextField(label="Digite o título do produto...", text_align=ft.TextAlign.LEFT)
    txt_preco = ft.Text('Preço do Produto')
    preco = ft.TextField(value="0", label="Digite o preço do produto...", text_align=ft.TextAlign.LEFT)
    btn_produto = ft.ElevatedButton('Cadastrar', on_click=cadastrar)

    produto_edit = Produto(titulo="", preco=0)

    page.add(
        txt_acerto,
        txt_erro,
        txt_titulo,
        produto,
        txt_preco,
        preco,
        btn_produto,
        lista_produtos,
    )

    carregar_produtos()

ft.app(target=main)