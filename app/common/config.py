import sqlalchemy as sa
from dataclasses import dataclass
from os import path, environ

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

@dataclass
class Config:
    """
    기본 Configuration
    """

    BASE_DIR: str = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DEBUG: bool = False
    # DB_URL: str = environ.get("DB_URL", "mysql+pymysql://travis@localhost/notification_api?charset=utf8mb4")
    # DB_URL: str = environ.get("DB_URL", "mssql+pymssql://pharmdba:pharmbio!@#$@112.221.63.59:14233/PHARMDev")
    
    DB_URL: str = sa.engine.URL.create(
                                            drivername="mssql+pymssql",
                                            username="pharmdba",
                                            password="pharmbio!@#$",
                                            host="112.221.63.59",
                                            port="14233" ,
                                            database="PHARM",
                                        )
    

@dataclass
class LocalConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class ProdConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


@dataclass
class TestConfig(Config):
    # DB_URL: str = "mysql+pymysql://travis@localhost/notification_test?charset=utf8mb4"
    # DB_URL: str = environ.get("DB_URL", "mssql+pymssql://pharmdba:pharmbio!@#$@112.221.63.59:14233/PHARMDev")
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True
    DB_URL: str = sa.engine.URL.create(
                                        drivername="mssql+pymssql",
                                        username="pharmdba",
                                        password="pharmbio!@#$",
                                        host="112.221.63.59",
                                        port="14233" ,
                                        database="PHARMDev",
                                    )


def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("API_ENV", "local")]()
