from openai import OpenAI

class GPTService:
    """GPT API関連のサービスクラス"""
    
    def __init__(self, api_key: str):
        """GPTサービスの初期化"""
        if not api_key:
            raise ValueError("OpenAI API キーが設定されていません")
        self.client = OpenAI(api_key=api_key)
    
    def format_text(self, input_text: str, model: str = "gpt-4o") -> str:
        """
        入力テキストを官公庁文書として適切な日本語に整形
        
        Args:
            input_text: 整形対象のテキスト
            model: 使用するGPTモデル
            
        Returns:
            整形後のテキスト
        """
        prompt = (
            "以下の単語の羅列から、官公庁の提出文書として自然な日本語に整形してください。"
            "整形した文章のみ出力してください。\n"
            "短文で複数文に分け、接続詞は最低限にしてください。\n"
            f"{input_text}"
        )
        
        return self._call_gpt(prompt, model)
    
    def extract_issues(self, combined_text: str, model: str = "gpt-4o") -> str:
        """
        入力テキストから支援課題を抽出
        
        Args:
            combined_text: 課題抽出対象のテキスト
            model: 使用するGPTモデル
            
        Returns:
            抽出された課題リスト
        """
        prompt = (
            "以下の情報から、支援計画書作成のための主要な課題を抽出してください。\n"
            "具体的で実用的な課題として、箇条書きで整理してください。\n"
            "各課題は簡潔に1-2行で記述し、支援の優先順位を考慮してください。\n\n"
            f"{combined_text}"
        )
        
        return self._call_gpt(prompt, model)
    
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
                "content": "あなたは、話し言葉のようにわかりやすい日本語に整形するプロの編集者です。"
            },
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"