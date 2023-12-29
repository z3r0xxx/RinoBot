from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship 
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class GuildInfo(Base):
    __tablename__ = "guilds"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"GuildInfo(id={self.id!r}, guild_id={self.guild_id!r})"
    

class GuildSettingsMod(Base):
    __tablename__ = "guilds_settings_mod"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"GuildSettingsMod(id={self.id!r}, guild_id={self.guild_id!r})"
    

class GuildSettingsMusic(Base):
    __tablename__ = "guilds_settings_music"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"GuildSettingsMusic(id={self.id!r}, guild_id={self.guild_id!r})"
    

class GuildSettingsAudit(Base):
    __tablename__ = "guilds_settings_audit"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"GuildSettingsAudit(id={self.id!r}, guild_id={self.guild_id!r})"
    

class GuildSettingsSubs(Base):
    __tablename__ = "guilds_settings_subs"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"GuildSettingsSubs(id={self.id!r}, guild_id={self.guild_id!r})"
    

class GuildSettingsLeveling(Base):
    __tablename__ = "guilds_settings_leveling"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"GuildSettingsLeveling(id={self.id!r}, guild_id={self.guild_id!r})"
    

class GuildSettingsNotifications(Base):
    __tablename__ = "guilds_settings_notifications"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(Integer())
    is_welcome_guild: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_welcome_dm: Mapped[bool] = mapped_column(Boolean(), default=False)
    welcome_channel_message: Mapped[str] = mapped_column(String(), default='')
    welcome_dm_message: Mapped[str] = mapped_column(String(), default='')
    welcome_channel_id: Mapped[int] = mapped_column(Integer(), default=0)

    def __repr__(self) -> str:
        return f"GuildSettingsNotifications(id={self.id!r}, guild_id={self.guild_id!r})"
    

class GuildSettingsCommands(Base):
    __tablename__ = "guilds_settings_commands"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"GuildSettingsCommands(id={self.id!r}, guild_id={self.guild_id!r})"
    

class GuildSettingsFun(Base):
    __tablename__ = "guilds_settings_fun"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"GuildSettingsFun(id={self.id!r}, guild_id={self.guild_id!r})"
    

class GuildSettingsRoles(Base):
    __tablename__ = "guilds_settings_roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"GuildSettingsRoles(id={self.id!r}, guild_id={self.guild_id!r})"
    

class GuildSettingsChannels(Base):
    __tablename__ = "guilds_settings_channels"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"GuildSettingsChannels(id={self.id!r}, guild_id={self.guild_id!r})"
