from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Session, relationship
from typing import List
import datetime
import os

from .database import engine, Base, get_db
from . import schemas

class Restaurante(Base):
    __tablename__ = "restaurantes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False)
    chave_admin = Column(String(50), nullable=False)
    produtos = relationship("Produto", back_populates="restaurante")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    restaurante_id = Column(Integer, ForeignKey("restaurantes.id"))
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    preco = Column(Float, nullable=False)
    restaurante = relationship("Restaurante", back_populates="produtos")

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    restaurante_id = Column(Integer, ForeignKey("restaurantes.id"))
    data_pedido = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="Preparando")
    total = Column(Float, nullable=False)
    itens = relationship("ItemPedido", back_populates="pedido")

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="iFrango API", description="Módulo Refatorado - Engenharia de Software")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def inicializar_base_dados():
    db = next(get_db())
    try:
        if db.query(Restaurante).count() == 0:
            r1 = Restaurante(nome="FrangoAlert HQ", chave_admin="frango123")
            r2 = Restaurante(nome="Hot Chicken Co.", chave_admin="hot123")
            r3 = Restaurante(nome="Rei do Assado", chave_admin="rei123")
            db.add_all([r1, r2, r3])
            db.commit()

            p1 = Produto(nome="Balde Frango Crocante (G)", descricao="12 pedaços artesanais de peito e coxinha da asa.", preco=54.90, restaurante_id=r1.id)
            p2 = Produto(nome="Combo FrangoAlert Especial", descricao="Balde médio + Batata rústica turbinada + 2 molhos.", preco=69.90, restaurante_id=r1.id)
            p3 = Produto(nome="Sanduíche Crispy Master", descricao="Pão brioche, sobrecoxa empanada crocante, maionese e picles.", preco=28.50, restaurante_id=r2.id)
            db.add_all([p1, p2, p3])
            db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home():
    caminho_html = os.path.join(os.path.dirname(__file__), "index.html")
    with open(caminho_html, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/restaurantes", response_model=schemas.RestauranteOut)
def cadastrar_restaurante(rest: schemas.RestauranteCreate, db: Session = Depends(get_db)):
    if db.query(Restaurante).filter(Restaurante.nome == rest.nome).first():
        raise HTTPException(status_code=400, detail="Restaurante já existe.")
    novo = Restaurante(nome=rest.nome, chave_admin=rest.chave_admin)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@app.get("/restaurantes", response_model=List[schemas.RestauranteOut])
def listar_restaurantes(db: Session = Depends(get_db)):
    return db.query(Restaurante).all()

@app.post("/restaurantes/login", response_model=schemas.RestauranteOut)
def login_restaurante(dados: schemas.LoginData, db: Session = Depends(get_db)):
    restaurante = db.query(Restaurante).filter(Restaurante.nome == dados.identificador).first()
    if not restaurante or restaurante.chave_admin != dados.senha:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    return restaurante

@app.post("/usuarios", response_model=schemas.UsuarioOut)
def cadastrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    novo = Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@app.post("/usuarios/login", response_model=schemas.UsuarioOut)
def login_usuario(dados: schemas.LoginData, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.identificador).first()
    if not usuario or usuario.senha != dados.senha:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    return usuario

@app.get("/produtos/restaurante/{restaurante_id}", response_model=List[schemas.ProdutoOut])
def listar_produtos_restaurante(restaurante_id: int, db: Session = Depends(get_db)):
    return db.query(Produto).filter(Produto.restaurante_id == restaurante_id).all()

@app.post("/produtos", response_model=schemas.ProdutoOut)
def criar_produto(prod: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = Produto(**prod.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@app.put("/produtos/{produto_id}", response_model=schemas.ProdutoOut)
def editar_produto(produto_id: int, prod: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    db_prod = db.query(Produto).filter(Produto.id == produto_id).first()
    if not db_prod:
        raise HTTPException(status_code=404)
    db_prod.nome = prod.nome
    db_prod.descricao = prod.descricao
    db_prod.preco = prod.preco
    db.commit()
    db.refresh(db_prod)
    return db_prod

@app.post("/pedidos", response_model=schemas.PedidoOut)
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    total = sum([db.query(Produto).get(i.produto_id).preco * i.quantidade for i in pedido.itens])
    novo = Pedido(usuario_id=pedido.usuario_id, restaurante_id=pedido.restaurante_id, total=total)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    
    for item in pedido.itens:
        preco = db.query(Produto).get(item.produto_id).preco
        db.add(ItemPedido(pedido_id=novo.id, produto_id=item.produto_id, quantidade=item.quantidade, preco_unitario=preco))
    db.commit()
    db.refresh(novo)
    return novo

@app.put("/pedidos/{pedido_id}/status", response_model=schemas.PedidoOut)
def atualizar_status_pedido(pedido_id: int, status_data: schemas.PedidoUpdate, db: Session = Depends(get_db)):
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    db_pedido.status = status_data.status
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@app.get("/pedidos/usuario/{usuario_id}", response_model=List[schemas.PedidoOut])
def listar_pedidos_cliente(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(Pedido).filter(Pedido.usuario_id == usuario_id).order_by(Pedido.id.desc()).all()

@app.get("/pedidos/restaurante/{restaurante_id}", response_model=List[schemas.PedidoOut])
def listar_pedidos_restaurante(restaurante_id: int, db: Session = Depends(get_db)):
    return db.query(Pedido).filter(Pedido.restaurante_id == restaurante_id).order_by(Pedido.id.desc()).all()