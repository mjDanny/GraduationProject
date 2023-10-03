import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

created = None  # создана ли сессия


def global_init(db_file):
    global created

    if created:
        return

    if not db_file or not db_file.strip():
        raise Exception('Файл базы данных не подключен')

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f'Подключение к {conn_str} успешно')

    # создание движка для работы с БД
    engine = sa.create_engine(conn_str, echo=False)
    created = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global created
    return created()
