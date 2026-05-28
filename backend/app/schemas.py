from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RestauranteCreate(BaseModel):
    nome: str
    chave_admin: str

class RestauranteOut(BaseModel):
    id: int
    nome: str
    class Config:
        from_attributes = True

class LoginData(BaseModel):
    identificador: str
    senha: str

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    class Config:
        from_attributes = True

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    preco: float
    restaurante_id: int

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id: int
    class Config:
        from_attributes = True

class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int

class ItemPedidoOut(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float
    produto: Optional[ProdutoOut] = None
    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    usuario_id: int
    restaurante_id: int
    itens: List[ItemPedidoCreate]

class PedidoUpdate(BaseModel):
    status: str

class PedidoOut(BaseModel):
    id: int
    usuario_id: int
    restaurante_id: int
    data_pedido: datetime
    status: str
    total: float
    itens: List[ItemPedidoOut]
    class Config:
        from_attributes = True