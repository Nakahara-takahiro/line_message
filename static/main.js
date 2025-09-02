// コピーボタンの機能実装
document.addEventListener('DOMContentLoaded', function () {
    const copyButton = document.getElementById('copy_button');
    const outputTextarea = document.getElementById('converted_output');

    copyButton.addEventListener('click', function () {
        // テキストエリアの内容をクリップボードにコピー
        navigator.clipboard.writeText(outputTextarea.value)
            .then(function () {
                // コピー成功時の処理
                const originalText = copyButton.textContent;
                copyButton.textContent = 'コピー完了！';

                // 2秒後に元のテキストに戻す
                setTimeout(function () {
                    copyButton.textContent = originalText;
                }, 2000);
            })
            .catch(function (err) {
                // コピー失敗時の処理（古いブラウザ対応）
                console.error('コピーに失敗しました:', err);

                // フォールバック処理
                outputTextarea.select();
                document.execCommand('copy');

                const originalText = copyButton.textContent;
                copyButton.textContent = 'コピー完了！';

                setTimeout(function () {
                    copyButton.textContent = originalText;
                }, 2000);
            });
    });
});// すべて消去ボタンの処理
    document.getElementById('clear_button').addEventListener('click', function() {
      if (confirm('すべての内容を消去しますか？')) {
        // フォームを送信して消去処理を実行
        const form = document.querySelector('form');
        const actionInput = document.createElement('input');
        actionInput.type = 'hidden';
        actionInput.name = 'action';
        actionInput.value = 'clear';
        form.appendChild(actionInput);
        form.submit();
      }
    });