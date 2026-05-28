from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)

    pedidos = relationship("Pedido", back_populates="usuario")

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    preco = Column(Float, nullable=False)

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    data_pedido = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="Pendente")
    total = Column(Float, nullable=False)

    usuario = relationship("Usuario", back_populates="pedidos")
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

class Restaurante(Base):
    __tablename__ = "restaurantes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False)
    chave_admin = Column(String(50), nullable=False, default="admin321")