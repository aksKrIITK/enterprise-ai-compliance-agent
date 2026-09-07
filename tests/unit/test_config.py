from app.core.config import Settings, get_settings


def test_settings_default_values():
    settings = Settings()
    assert settings.PROJECT_NAME == "EnterpriseOps AI - Compliance Investigation Platform"
    assert settings.ENVIRONMENT == "development"
    assert settings.LOG_LEVEL == "INFO"
    assert settings.POSTGRES_PORT == 5432
    assert settings.REDIS_PORT == 6379


def test_database_url_formatting():
    settings = Settings(
        POSTGRES_USER="test_user",
        POSTGRES_PASSWORD="test_password",
        POSTGRES_HOST="db_host",
        POSTGRES_PORT=5432,
        POSTGRES_DB="test_db"
    )
    expected_url = "postgresql+asyncpg://test_user:test_password@db_host:5432/test_db"
    assert settings.get_database_url() == expected_url


def test_redis_url_formatting():
    settings = Settings(
        REDIS_HOST="cache_host",
        REDIS_PORT=6379,
        REDIS_DB=1
    )
    expected_url = "redis://cache_host:6379/1"
    assert settings.get_redis_url() == expected_url


def test_singleton_get_settings():
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2
