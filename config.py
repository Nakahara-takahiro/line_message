import os
from dotenv import load_dotenv

class Config:
    """アプリケーション設定クラス"""
    
    def __init__(self):
        # 環境変数の読み込み
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.secret_key = os.getenv(
            "SECRET_KEY", 
            "Prod#1983$Ultra%Secure^Key&With*Complex()Chars+Random_String"
        )
        self.debug_mode = os.getenv("DEBUG", "False").lower() == "true"
        
        
        # ベースディレクトリの設定
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
