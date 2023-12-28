import discord
from modules.logs import logger
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.User import UserInfo, UserProfile, UserLeveling, UserStats, UserInv
from models.Guild import GuildInfo, GuildSettingsMod, GuildSettingsMusic, GuildSettingsAudit, GuildSettingsSubs, GuildSettingsLeveling, GuildSettingsNotifications, GuildSettingsCommands, GuildSettingsFun, GuildSettingsRoles, GuildSettingsChannels

engine = create_engine("postgresql://postgres:zrxroot@localhost:5432/RinoBot")
connection = engine.connect()

with Session(autoflush=False, bind=engine) as session:
    people = session.query(text('now()')).first()

def get_user_info(user_id, guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_user_info = session.query(UserInfo).filter_by(user_id=user_id, guild_id=guild_id).first()
        if existing_user_info is not None:
            return existing_user_info
        else:
            return None
        
def create_user_info(user_id, guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_user_info = session.query(UserInfo).filter_by(user_id=user_id, guild_id=guild_id).first()

        if existing_user_info is None:
            new_user = UserInfo(
                user_id=user_id,
                guild_id=guild_id
            )
            session.add(new_user)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'UserInfo user_id {user_id} guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_user_profile(user_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_user_profile = session.query(UserProfile).filter_by(user_id=user_id).first()

        if existing_user_profile is None:
            new_user = UserProfile(
                user_id=user_id
            )
            session.add(new_user)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'UserProfile user_id {user_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def get_user_leveling(user_id, guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_user_leveling = session.query(UserLeveling).filter_by(user_id=user_id, guild_id=guild_id).first()
        if existing_user_leveling is not None:
            return existing_user_leveling
        else:
            return None

def add_voice_connection(user_id, guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_user_leveling = session.query(UserLeveling).filter_by(user_id=user_id, guild_id=guild_id).first()
        if existing_user_leveling is not None:
            existing_user_leveling.voice_connections += 1
            session.commit()
            return True
        else:
            return None

def add_voice_time(user_id, guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_user_leveling = session.query(UserLeveling).filter_by(user_id=user_id, guild_id=guild_id).first()
        if existing_user_leveling is not None:
            existing_user_leveling.all_voice_time += 5
            session.commit()
            return True
        else:
            return None

def create_user_leveling(user_id, guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_user_leveling = session.query(UserLeveling).filter_by(user_id=user_id, guild_id=guild_id).first()

        if existing_user_leveling is None:
            new_user = UserLeveling(
                user_id=user_id, 
                guild_id=guild_id
            )
            session.add(new_user)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'UserLeveling user_id {user_id} guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_user_stats(user_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_user_stats = session.query(UserStats).filter_by(user_id=user_id).first()

        if existing_user_stats is None:
            new_user = UserStats(
                user_id=user_id
            )
            session.add(new_user)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'UserStats user_id {user_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_user_inv(user_id, guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_user_inv = session.query(UserInv).filter_by(user_id=user_id, guild_id=guild_id).first()

        if existing_user_inv is None:
            new_user = UserInv(
                user_id=user_id, 
                guild_id=guild_id
            )
            session.add(new_user)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'UserInv user_id {user_id} guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_user(member: discord.Member):
    user_id = member.id
    guild_id = member.guild.id

    if member.bot:
        return

    create_user_info(user_id, guild_id)
    create_user_profile(user_id)
    create_user_leveling(user_id, guild_id)
    create_user_stats(user_id)
    create_user_inv(user_id, guild_id)



def create_guild_info(guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_guild_info = session.query(GuildInfo).filter_by(guild_id=guild_id).first()

        if existing_guild_info is None:
            new_guild = GuildInfo(
                guild_id=guild_id
            )
            session.add(new_guild)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'GuildInfo guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_guild_settings_mod(guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_guild_settings_mod = session.query(GuildSettingsMod).filter_by(guild_id=guild_id).first()

        if existing_guild_settings_mod is None:
            new_guild = GuildSettingsMod(
                guild_id=guild_id
            )
            session.add(new_guild)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'GuildSettingsMod guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_guild_settings_music(guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_guild_settings_music = session.query(GuildSettingsMusic).filter_by(guild_id=guild_id).first()

        if existing_guild_settings_music is None:
            new_guild = GuildSettingsMusic(
                guild_id=guild_id
            )
            session.add(new_guild)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'GuildSettingsMusic guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_guild_settings_audit(guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_guild_settings_audit = session.query(GuildSettingsAudit).filter_by(guild_id=guild_id).first()

        if existing_guild_settings_audit is None:
            new_guild = GuildSettingsAudit(
                guild_id=guild_id
            )
            session.add(new_guild)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'GuildSettingsAudit guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_guild_settings_subs(guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_guild_settings_subs = session.query(GuildSettingsSubs).filter_by(guild_id=guild_id).first()

        if existing_guild_settings_subs is None:
            new_guild = GuildSettingsSubs(
                guild_id=guild_id
            )
            session.add(new_guild)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'GuildSettingsSubs guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_guild_settings_leveling(guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_guild_settings_leveling = session.query(GuildSettingsLeveling).filter_by(guild_id=guild_id).first()

        if existing_guild_settings_leveling is None:
            new_guild = GuildSettingsLeveling(
                guild_id=guild_id
            )
            session.add(new_guild)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'GuildSettingsLeveling guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def get_guild_settings_notifications(guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_guild_settings_notifications = session.query(GuildSettingsNotifications).filter_by(guild_id=guild_id).first()
        if existing_guild_settings_notifications is not None:
            return existing_guild_settings_notifications
        else:
            return None
    
def create_guild_settings_notifications(guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_guild_settings_notifications = session.query(GuildSettingsNotifications).filter_by(guild_id=guild_id).first()

        if existing_guild_settings_notifications is None:
            new_guild = GuildSettingsNotifications(
                guild_id=guild_id
            )
            session.add(new_guild)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'GuildSettingsNotifications guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_guild_settings_commands(guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_guild_settings_commands = session.query(GuildSettingsCommands).filter_by(guild_id=guild_id).first()

        if existing_guild_settings_commands is None:
            new_guild = GuildSettingsCommands(
                guild_id=guild_id
            )
            session.add(new_guild)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'GuildSettingsCommands guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_guild_settings_fun(guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_guild_settings_fun = session.query(GuildSettingsFun).filter_by(guild_id=guild_id).first()

        if existing_guild_settings_fun is None:
            new_guild = GuildSettingsFun(
                guild_id=guild_id
            )
            session.add(new_guild)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'GuildSettingsFun guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_guild_settings_roles(guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_guild_settings_roles = session.query(GuildSettingsRoles).filter_by(guild_id=guild_id).first()

        if existing_guild_settings_roles is None:
            new_guild = GuildSettingsRoles(
                guild_id=guild_id
            )
            session.add(new_guild)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'GuildSettingsRoles guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass

def create_guild_settings_channels(guild_id):
    with Session(autoflush=False, bind=engine) as session:
        existing_guild_settings_channels = session.query(GuildSettingsChannels).filter_by(guild_id=guild_id).first()

        if existing_guild_settings_channels is None:
            new_guild = GuildSettingsChannels(
                guild_id=guild_id
            )
            session.add(new_guild)
            
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logger.error(f'GuildSettingsChannels guild_id {guild_id} ↔ Произошла ошибка при создании записи:', e)
        else:
            pass


def create_guild(guild: discord.Guild):
    guild_id = guild.id

    create_guild_info(guild_id)
    create_guild_settings_mod(guild_id)
    create_guild_settings_music(guild_id)
    create_guild_settings_audit(guild_id)
    create_guild_settings_subs(guild_id)
    create_guild_settings_leveling(guild_id)
    create_guild_settings_notifications(guild_id)
    create_guild_settings_commands(guild_id)
    create_guild_settings_fun(guild_id)
    create_guild_settings_roles(guild_id)
    create_guild_settings_channels(guild_id)


# select_query = select(text('current_timestamp'))
# with Session(engine) as session:
#     for row in session.execute(select_query):
#         print(row)
# for row in connection.execute(select_query):
#     print(row)
