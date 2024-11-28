from app.core.config import CORE_SETTINGS
from app.models.pollution_data import Base
from alembic import context
from sqlalchemy import create_engine

# Target metadata for migrations
target_metadata = Base.metadata
def get_url():
    """
    Get the database URL from CoreSettings.
    """
    return CORE_SETTINGS.DATABASE_URL

def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    """
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """
    Run migrations in 'online' mode.
    """
    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# Determine migration mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
