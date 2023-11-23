from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class UserInfo(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer())
    guild_id: Mapped[int] = mapped_column(Integer())
    all_msg: Mapped[int] = mapped_column(Integer(), default=0)
    del_msg: Mapped[int] = mapped_column(Integer(), default=0)
    edit_msg: Mapped[int] = mapped_column(Integer(), default=0)

    def __repr__(self) -> str:
        return f"UserInfo(id={self.id!r}, user_id={self.user_id!r}, all_msg={self.all_msg!r})"
    

class UserProfile(Base):
    __tablename__ = "users_profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer())
    color_blocks: Mapped[str] = mapped_column(String(), default='0')
    color_background: Mapped[str] = mapped_column(String(), default='0')
    color_background_progress: Mapped[str] = mapped_column(String(), default='0')
    color_font: Mapped[str] = mapped_column(String(), default='0')
    color_progress: Mapped[str] = mapped_column(String(), default='0')
    background_shading: Mapped[str] = mapped_column(String(), default='0')
    is_user_back: Mapped[bool] = mapped_column(Boolean(), default=False)
    user_background: Mapped[str] = mapped_column(String(), default='0')

    def __repr__(self) -> str:
        return f"UserProfile(id={self.id!r}, user_id={self.user_id!r})"


class UserLeveling(Base):
    __tablename__ = "users_leveling"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer())
    guild_id: Mapped[int] = mapped_column(Integer())
    exp: Mapped[int] = mapped_column(Integer(), default=100)
    all_voice_time: Mapped[int] = mapped_column(Integer(), default=0)
    voice_connections: Mapped[int] = mapped_column(Integer(), default=0)

    def __repr__(self) -> str:
        return f"UserLeveling(id={self.id!r}, user_id={self.user_id!r})"


class UserStats(Base):
    __tablename__ = "users_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer())
    all_idle_time: Mapped[int] = mapped_column(Integer(), default=0)
    all_dnd_time: Mapped[int] = mapped_column(Integer(), default=0)
    all_online_time: Mapped[int] = mapped_column(Integer(), default=0)
    all_offile_time: Mapped[int] = mapped_column(Integer(), default=0)

    def __repr__(self) -> str:
        return f"UserStats(id={self.id!r}, user_id={self.user_id!r})"


class UserInv(Base):
    __tablename__ = "users_inv"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer())
    guild_id: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"UserInv(id={self.id!r}, user_id={self.user_id!r})"