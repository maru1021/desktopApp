import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 実行時のアプリケーションのディレクトリを取得
if getattr(sys, 'frozen', False):  # PyInstallerでコンパイルされた場合
    BASE_DIR = os.path.dirname(sys.executable)
else:  # 通常のPythonスクリプトとして実行される場合
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# データベースファイルのパスを設定
DB_PATH = os.path.join(BASE_DIR, "organization.db")

# SQLAlchemyエンジンの設定
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, connect_args={"check_same_thread": False})

# SQLAlchemyセットアップ
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
# テーブル作成
Base.metadata.create_all(engine)