"""
LINEメッセージ変換アプリ

このアプリケーションは、作成したテキストをLINEメッセージとして適切な表現に変換するアプリケーションです。
"""

import os
from flask import Flask, render_template, request, session, send_file, redirect, url_for, jsonify, flash, get_flashed_messages

from config import Config
from services.gpt_service import GPTService


# アプリケーションの初期化
config = Config()
app = Flask(__name__)
app.secret_key = config.secret_key

# 独自CSPポリシー（必要に応じて調整）

#Talisman

# CSRF保護を有効化

# セキュリティヘッダー追加

# サービスクラスのインスタンス化
gpt_service = GPTService(config.openai_api_key)

@app.route("/", methods=['GET', 'POST'])
def index():
    """メッセージ変換ページ"""
    try:
        converted_text = ""
        input_text = ""
        selected_style = "casual_family"  # デフォルト値
        
        if request.method == 'POST':
            # 消去ボタンが押された場合の処理
            if request.form.get('action') == 'clear':
                # すべての値を初期状態にリセット
                input_text = ""
                selected_style = "casual_family"
                converted_text = ""
                return render_template('index.html',
                                     input_text=input_text,
                                     selected_style=selected_style,
                                     converted_text=converted_text)
            
            # フォームデータを取得
            input_text = request.form.get('input_words', '').strip()
            selected_style = request.form.get('style', 'casual_family')
            
            # 入力値の検証
            if not input_text:
                flash("テキストを入力してください。")
                return render_template('index.html', 
                                     input_text=input_text, 
                                     selected_style=selected_style,
                                     converted_text=converted_text)
            
            try:
                # GPTサービスを使用してテキストを変換
                # gpt_service.pyの実装に依存するが、一般的なメソッド名を想定
                converted_text = gpt_service.convert_text(input_text, selected_style)
                
            except Exception as gpt_error:
                flash(f"テキスト変換中にエラーが発生しました: {str(gpt_error)}")
                converted_text = ""
        
        return render_template('index.html',
                             input_text=input_text,
                             selected_style=selected_style,
                             converted_text=converted_text)
                             
    except Exception as e:
        return render_template('error.html', error_message=str(e)), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html',
                           error_message="ページが見つかりませんでした。"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
                           error_message="サーバー内部エラーが発生しました。"), 500

if __name__ == "__main__":
    app.run(debug=True)