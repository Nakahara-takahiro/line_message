from openai import OpenAI

class GPTService:
    """GPT API関連のサービスクラス"""
    
    def __init__(self, api_key: str):
        """GPTサービスの初期化"""
        if not api_key:
            raise ValueError("OpenAI API キーが設定されていません")
        self.client = OpenAI(api_key=api_key)
    
    def convert_text(self, input_text: str, style: str, model: str = "gpt-4o") -> str:
        """
        入力テキストを、選択されたスタイルに応じてLINEメッセージとして適切な表現に変換する
        
        Args:
            input_text: 変換対象のテキスト
            style: ラジオボタンで選択されたスタイル（casual_family, formal_family, standard_all）
            model: 使用するGPTモデル
            
        Returns:
            変換後のテキスト
        """
        # スタイルに応じた設定を取得
        style_config = self._get_style_config(style)
        
        prompt = (
            f"以下のメモから、{style_config['target_audience']}に向けた"
            f"{style_config['tone']}なLINEメッセージを作成してください。\n"
            "要件:\n"
            "- LINEで送信することを想定した自然な日本語にしてください\n"
            "- 読みやすく親しみやすい文章にしてください\n"
            "- 短文で複数文に分け、適切な改行を入れてください\n"
            "- 変換した文章のみを出力してください\n\n"
            f"メモ内容:\n{input_text}"
        )
        
        return self._call_gpt(prompt, model)
    
    def _get_style_config(self, style: str) -> dict:
        """
        スタイル選択に応じた設定を取得
        
        Args:
            style: 選択されたスタイル
            
        Returns:
            スタイル設定の辞書
        """
        style_configs = {
            "casual_family": {
                "target_audience": "30～50代子持ち女性",
                "tone": "カジュアル"
            },
            "formal_family": {
                "target_audience": "30～50代子持ち女性",
                "tone": "フォーマル"
            },
            "standard_all": {
                "target_audience": "全年齢",
                "tone": "標準"
            }
        }
        
        return style_configs.get(style, style_configs["casual_family"])
    
    def _call_gpt(self, prompt: str, model: str) -> str:
        """
        GPT APIを呼び出し
        
        Args:
            prompt: 送信するプロンプト
            model: 使用するモデル
            
        Returns:
            GPTからの応答
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "あなたは、LINEメッセージ作成のプロフェッショナルです。"
                    "与えられたメモを元に、指定された読者層に適した"
                    "自然で親しみやすいLINEメッセージを作成してください。"
                )
            },
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,  # 自然な文章生成のため適度な創造性を設定
                max_tokens=1000   # 適切な長さの応答を確保
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"GPT APIでエラーが発生しました: {str(e)}")

    # 旧メソッドとの互換性を保持（必要に応じて削除可能）
    def format_text(self, input_text: str, model: str = "gpt-4o") -> str:
        """
        後方互換性のための旧メソッド
        デフォルトでcasual_familyスタイルを使用
        """
        return self.convert_text(input_text, "casual_family", model)