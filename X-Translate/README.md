# X Translate

[**日本語**](https://github.com/zerofdest/comprehension/blob/main/X-Translate/README.md) | [English](https://github.com/zerofdest/comprehension/blob/main/X-Translate/README.en.md) | [繁體中文](https://github.com/zerofdest/comprehension/blob/main/X-Translate/README.zh-hant.md)

[X（旧Twitter）](https://x.com/) 向けの自動翻訳ユーザースクリプト（Userscript）です。X 標準のひどい Grok 翻訳を Google 翻訳に置き換えるほか、PLaMo 3 Translate などのローカル翻訳モデルや、その他の外部翻訳サービスにも接続できます。

デフォルトでは Google 翻訳を使用するため、モデルの導入や API キーの設定は不要です。外部翻訳サービスを有効にすると、そのサービスが優先的に使用され、リクエストに失敗した場合は自動的に Google 翻訳へフォールバックします。

- Grok 翻訳
  - 翻訳品質がひどく、自動翻訳などでも頻繁に不具合が発生します。
- Google 翻訳
  - 本スクリプトで完全自動翻訳が可能です。全体的な翻訳品質は Grok よりやや良く、翻訳の遅延はやや大きめです。
- `plamo-3-translate-0.8b-Q4_K_M` のローカル実行
  - 高い翻訳品質と極めて低い遅延を両立し、ページ内のポストをほぼ瞬時に翻訳できます。

## 機能一覧

- **ポストの自動翻訳**：ポストがブラウザの表示領域に入ると自動的に翻訳します。X 標準の翻訳ボタンを一つずつクリックする必要はありません。タイムライン、返信、プロフィールページ内のポストなどに対応しています。
- **プロフィールの自己紹介（Bio）の自動翻訳**：空でない自己紹介文の翻訳を自動的に試みます。X が付与する言語タグに依存せず、翻訳サービス側で原文の言語を判定します。
- **原文と翻訳文の切り替え**：`Show translation` / `Hide translation` で表示を切り替えます。同じページ要素の翻訳結果は再利用されるため、切り替えるたびに翻訳リクエストを送信する必要はありません。
- **X 標準の翻訳機能の置き換え**：認識可能な標準翻訳ボタンの動作を置き換え、翻訳ボタンのないポストや自己紹介文にもボタンを追加します。コミュニティノート（Community Notes）の認識可能な標準翻訳ボタンにも対応しています。
- **原文言語のフィルタリング**：ポストの `lang` 属性に基づき、翻訳先言語と同じ言語のコンテンツは翻訳対象外とします。中国語（簡体字、`zh`）と中国語（繁体字、`zh-TW`）の相互翻訳もスキップします。自己紹介文にはこのフィルタリングを適用しません。
- **翻訳先言語のカスタマイズ**：検索可能な言語選択リストを用意しています。デフォルトはブラウザの言語設定に従い、いつでも初期設定に戻せます。
- **外部翻訳サービスのカスタマイズ**：GET / POST リクエスト、Google Translate / OpenAI のレスポンス形式、OpenAI Compatible のリクエストボディ、カスタム JSON ボディ、任意の API キーに対応しています。
- **PLaMo の言語ホワイトリスト**：PLaMo 使用時は、ホワイトリストの条件を満たすポストのみを外部サービスへ送信します。非対応言語や有効な言語タグがないポストは Google 翻訳で処理します。自己紹介文の言語はモデルが自動判定します。他の翻訳サービスを利用する際はホワイトリストを無効にできます。
- **自動フォールバック**：外部サービスのタイムアウト、エラー、不正な翻訳結果、空の翻訳結果が発生した場合は自動的に Google 翻訳を試みます。PLaMo モードでは、文字を含むテキストの翻訳結果が原文と完全に一致する場合もフォールバックします。Google 翻訳自体にもメイン・予備のエンドポイントがあり、必要に応じて原文言語の自動判定で再試行します。
- **リンクと絵文字の保持**：原文のリンク、インライン画像（画像形式の絵文字を含む）、改行の保持を試みます。翻訳サービスがプレースホルダーを欠落させた場合は、不足しているリンクや画像を翻訳文の末尾に追加します。
- **同時実行数の制御と動的ページへの対応**：自動翻訳タスクを最大 5 件同時に実行し、表示領域の上部にあるコンテンツを優先します。ページの動的な変化を監視し、スクロールによる追加読み込みやページ遷移に対応するとともに、内容が変化したポストに古い翻訳結果が表示されるのを防ぎます。

## インストール

1. [Violentmonkey](https://violentmonkey.github.io/) などのユーザースクリプトマネージャーをブラウザにインストールします。
2. [X-Translate.user.js](https://raw.githubusercontent.com/zerofdest/comprehension/main/X-Translate/X-Translate.user.js) を開き、マネージャーの案内に従ってスクリプトをインストールします。または、`.user.js` ファイルをマネージャーにインポートすることもできます。
3. [x.com](https://x.com/) を開くか再読み込みすると、スクリプトが動作を開始します。

スクリプトの対象 URL は `https://x.com/*` のみです。インストール直後は Google 翻訳を使用するため、追加設定は不要です。

## 使い方

### 翻訳先言語の設定

X のページでブラウザのユーザースクリプトマネージャーのアイコンをクリックし、**X Translate** の **Set translation language** を選択します。

表示された `Translation Language` ウィンドウで、希望する言語を検索して選択します。例：

| 言語 | 言語コード |
| --- | --- |
| English | `en` |
| Japanese | `ja` |
| Chinese | `zh` |
| Chinese (Traditional) | `zh-TW` |
| Korean | `ko` |

言語を選択するとページが自動的に再読み込みされます。`Reset to browser default` をクリックすると、ブラウザのデフォルト言語に戻せます。

### 原文・翻訳文の表示

翻訳条件を満たすポストや自己紹介文が表示領域に入ると、スクリプトが自動的に翻訳を開始します。

| ボタンの状態 | 意味 |
| --- | --- |
| `Translating...` | 翻訳中 |
| `Hide translation` | 翻訳文を表示中。クリックすると原文に戻ります |
| `Show translation` | 原文を表示中。クリックすると翻訳文を表示し、未翻訳の場合は翻訳を開始します |

翻訳に失敗した場合は、`Show translation` をクリックして手動で再試行できます。

### Translator settings

ユーザースクリプトマネージャーの X Translate メニューから **Translator settings** を選択すると、外部翻訳サービスを設定できます。

| 設定項目 | デフォルト値 | 説明 |
| --- | --- | --- |
| Enable external translator (fallback to Google Translate) | オフ | 有効にすると外部サービスを優先し、失敗時は Google 翻訳へフォールバック |
| Use PLaMo (apply source-language whitelist) | オン | ポストに PLaMo の原文言語ホワイトリストを適用。他のサービスを使用する場合は通常オフにする |
| Request Method | GET | GET と POST に対応 |
| Translation endpoint URL | `http://127.0.0.1:8001/translate-auto?q=$q` | 外部翻訳 API の URL |
| Response Style | Google Translate | サービスの実際のレスポンス形式に合わせて Google Translate または OpenAI を選択 |
| API Type（POST のみ） | OpenAI Compatible | 組み込みの OpenAI リクエスト形式、または Custom JSON を使用 |
| API Key（POST のみ、任意） | 空欄 | 入力した場合は `Authorization: Bearer ...` として送信 |
| Model Name（OpenAI Compatible POST のみ） | 空欄 | モデル名。このリクエスト形式を使用する場合は必須 |
| Request Body（Custom POST のみ） | `{"q":"$q","sl":"$slCode","tl":"$tlCode"}` | カスタム JSON リクエストボディ |

`Save` をクリックすると設定が保存され、ページが自動的に再読み込みされます。`Cancel` は変更を破棄します。`Reset defaults` はウィンドウ内の設定をデフォルト値に戻し、その後 `Save` をクリックすると反映されます。

> **注意：** `Use PLaMo` はモデルを起動するためのスイッチではなく、モデルの翻訳先言語も変更しません。外部サービスはデフォルトで無効になっているため、この項目にチェックが入っていても Google 翻訳のみが使用されます。

### 他の翻訳サービスへの接続

`Enable external translator` を有効にし、`Use PLaMo` を無効にしてから、サービスの API 仕様に従ってリクエスト方式、URL、レスポンス形式を設定してください。ホワイトリストを無効にしても、翻訳先と同じ言語のポストを除外するフィルタリングは無効になりません。

#### GET

URL には `$q` が必須です。例：

```text
http://127.0.0.1:8001/translate?q=$q&sl=$sl&tl=$tl
```

これは一般的な API 形式の例であり、すべてのサービスが `sl` と `tl` を読み取るわけではありません。

| URL プレースホルダー | 置換内容 |
| --- | --- |
| `$q` | 翻訳対象テキスト |
| `$sl` / `$slCode` | 原文言語コード。不明な場合は `auto` |
| `$tl` / `$tlCode` | 翻訳先言語コード |

URL 内のプレースホルダーは自動的に URL エンコードされます。使用できるのはパスまたはクエリパラメーター内のみです。

#### POST：OpenAI Compatible

例えば、OpenAI Chat Completions 形式および JSON Object レスポンスに対応するサービスへ接続する場合：

| 設定項目 | 設定例 |
| --- | --- |
| Request Method | POST |
| Translation endpoint URL | `http://127.0.0.1:8080/v1/chat/completions` |
| API Type | OpenAI Compatible |
| API Key | サービスの要件に応じて入力。認証不要のローカルサービスでは空欄で可 |
| Model Name | サービスが実際に提供しているモデル名 |
| Response Style | OpenAI |

スクリプトは `system` / `user` メッセージを自動生成し、`sentence` と `src` を含む JSON を返すようモデルに指示します。また、`response_format: {"type":"json_object"}`、`temperature: 0`、`stream: false` を設定します。サービスはこれらのリクエストフィールドに対応している必要があります。対応していない場合は Custom リクエストボディを使用してください。

#### POST：Custom

`API Type: Custom` を選択し、翻訳サービスの仕様に合わせて JSON オブジェクトを記述します。例：

```json
{
  "q": "$q",
  "sl": "$slCode",
  "tl": "$tlCode"
}
```

カスタム JSON の文字列値には、以下のプレースホルダーを使用できます（ネストされたオブジェクトや配列内の文字列も含む）。

| リクエストボディのプレースホルダー | 置換内容 |
| --- | --- |
| `$q` | 翻訳対象テキスト |
| `$sl` | 原文言語の英語名 |
| `$tl` | 翻訳先言語の英語名 |
| `$slCode` | 原文言語コード |
| `$tlCode` | 翻訳先言語コード |

テキストは自動的に JSON エスケープされます。リクエストボディまたは URL の少なくとも一方に `$q` が必要です。

#### 対応するレスポンス形式

**Google Translate**：

```json
{
  "sentences": [
    {"trans": "你好，世界！"}
  ],
  "src": "en"
}
```

Google 翻訳のメインエンドポイントが使用するネストされた配列形式にも対応しています。例：

```json
[[["你好，世界！", "Hello, world!", null, null]], null, "en"]
```

**OpenAI**：

```json
{
  "choices": [
    {
      "message": {
        "content": "{\"sentence\":\"你好，世界！\",\"src\":\"en\"}"
      }
    }
  ]
}
```

`choices[0].message.content` にプレーンテキストの翻訳文を直接格納する形式にも対応しています。リクエスト形式とレスポンス形式は独立して設定でき、GET と Google Translate、POST と OpenAI を必ず組み合わせる必要はありません。

### プライバシーと利用上の制限

- Google 翻訳モードでは、翻訳対象テキストが Google に送信されます。ローカル翻訳を有効にすると、条件を満たして正常に処理されたテキストはローカルで翻訳できますが、ホワイトリストの条件を満たさない内容や翻訳に失敗した内容は Google に送信される場合があります。現バージョンには Google 翻訳へのフォールバックを無効にする設定がないため、完全オフラインの翻訳モードではありません。
- スクリプトは `GM_xmlhttpRequest` を使用してクロスオリジンの API にアクセスします。外部サービスには信頼できる URL のみを設定し、信頼できないサービスに機密テキストや API キーを送信しないでください。API キーはユーザースクリプトマネージャーのスクリプト設定に保存されます。
- 外部翻訳リクエストのタイムアウトは 60 秒、自動翻訳の同時実行数は最大 5 件です。手動で開始した翻訳には、この自動翻訳キューの上限は適用されません。
- Google 翻訳のエンドポイントや X のページ構造は変更される可能性があります。すべてのページ、表示言語、ブラウザのバージョンで常に動作することを保証するものではありません。

## PLaMo 3 Translate 0.8B のローカル実行（強く推奨）

PLaMo 3 シリーズの最新作。1B 未満の翻訳モデルの中では最高クラスと言っても過言ではありません。ただし、対応言語によって翻訳品質には差があります。

X Translate のデフォルトの外部サービス設定は、[PLaMo 3 Translate 0.8B](https://huggingface.co/pfnet/plamo-3-translate-0.8b) の `Q4_K_M` 量子化 GGUF モデルを使用するサンプルスクリプト [plamo_flusher_bridge.py](https://github.com/zerofdest/comprehension/blob/main/X-Translate/plamo_flusher_bridge.py) に対応しています。

PLaMo 3 Translate は Preferred Networks（PFN）が開発した翻訳専用モデルで、中国語の簡体字・繁体字を含む 53 種類の言語コードに対応し、コンテキストや用語集も利用できます。デフォルトの GGUF ファイルは約 0.57 GB です。実行時には別途メモリまたは VRAM が必要です。

この Python スクリプトは llama.cpp の起動、PLaMo の PFML3 翻訳プロンプトの生成、モデルのレスポンスの Google Translate 互換形式への変換を行います。1 つのモデルプロセスで X Translate と YoutubeLiveChatFlusher の両方に対応できます。

```text
X Translate                GET /translate-auto
                                      |
                                      v
                           plamo_flusher_bridge.py :8001
                                      |
                                      v
                           llama-server :8000
                           POST /v1/completions
                                      |
                                      v
                           PLaMo 3 Translate GGUF
```

### 1. 実行環境とモデルのダウンロード

以下は Windows を例とした手順です。

- [Python](https://www.python.org/downloads/)：Python 3.10 以降を推奨します。サンプルのブリッジスクリプトは Python 標準ライブラリのみを使用するため、サードパーティーの Python 依存パッケージをインストールする必要はありません。
- [llama.cpp Releases](https://github.com/ggml-org/llama.cpp/releases)：PLaMo 3 Translate に対応する Windows ビルドをダウンロードします。ハードウェアに合わせて CPU、CUDA、Vulkan などのバックエンドを選択し、解凍して実行に必要なファイルをすべて保持してください。CUDA ビルドで追加のランタイムライブラリが必要な場合は、該当リリースの説明に従ってダウンロードしてください。
  - 推奨バージョン：[b12359](https://github.com/ggml-org/llama.cpp/releases/tag/b12359)
- [PLaMo 3 Translate 0.8B GGUF（公式モデルリポジトリ）](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF)：[`plamo-3-translate-0.8b-Q4_K_M.gguf`](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF/resolve/main/plamo-3-translate-0.8b-Q4_K_M.gguf) をダウンロードします。
- サンプル起動スクリプト：[plamo_flusher_bridge.py](https://github.com/zerofdest/comprehension/blob/main/X-Translate/plamo_flusher_bridge.py)

モデルの [PLaMo Community License](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF#license) も遵守してください。

### 2. Python スクリプトの設定変更

テキストエディターで `plamo_flusher_bridge.py` を開き、少なくとも以下の 3 つのパラメーターを確認してください。

```python
LLAMA_SERVER_EXE = Path(r"I:\llama.cpp\llama-server.exe")
GGUF_MODEL_FILE = Path(r"I:\_models\plamo-3-translate-0.8b-Q4_K_M.gguf")

TARGET_LANG = "zh-hant"
```

**2 つのファイルパスは必ず自身の PC 上の実際のパスに変更し、`TARGET_LANG` を希望する翻訳先言語に設定してください。** 例の `I:` ドライブのパスはあくまで一例であり、同じディレクトリを使用する必要はありません。

例：

```python
LLAMA_SERVER_EXE = Path(r"D:\llama.cpp\llama-server.exe")
GGUF_MODEL_FILE = Path(r"D:\models\plamo-3-translate-0.8b-Q4_K_M.gguf")
TARGET_LANG = "en"
```

よく使われる言語コードの対応表：

| 翻訳先言語 | X Translate | Python / PLaMo |
| --- | --- | --- |
| 中国語（繁体字） | `zh-TW` | `zh-hant`（Python のデフォルト） |
| 中国語（簡体字） | `zh` | `zh-hans` |
| 英語 | `en` | `en` |
| 日本語 | `ja` | `ja` |
| 韓国語 | `ko` | `ko` |

全言語の一覧は [PLaMo の公式モデル説明](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF#supported-languages) を参照してください。

**重要：ローカル翻訳では、Python スクリプトの `TARGET_LANG` が X Translate の翻訳先言語設定より優先されます。** これは PLaMo や他のモデルの言語コードの互換性を考慮したものです。\
現在のサンプル Python スクリプトでは、両エンドポイントで固定の `TARGET_LANG` を使用し、渡された `sl` と `tl` のクエリパラメーターを無視します。ブラウザ側で言語を変更しても Python 側の翻訳先言語は自動的には更新されません。Python の設定を変更した後は、スクリプトを再起動してください。

その他の任意設定：

| パラメーター | デフォルト値 | 用途 |
| --- | --- | --- |
| `HOST` / `PORT` | `127.0.0.1` / `8001` | 外部翻訳ブリッジサービスのアドレス |
| `LLAMA_HOST` / `LLAMA_PORT` | `127.0.0.1` / `8000` | llama-server バックエンドのアドレス |
| `LLAMA_STARTUP_TIMEOUT` | `120` | モデルの読み込みを待機する時間（秒） |
| `ENABLE_TRANSLATE` | `False` | 原文言語固定の `/translate` エンドポイントも有効にするかどうか |
| `SOURCE_LANG` | `ja` | `/translate` の固定原文言語。`/translate-auto` には影響しない |
| `AUTO_CONTEXT` | X のポストを想定 | `/translate-auto` が使用するコンテキストプロンプト |
| `CONTEXT` | 日本の VTuber 配信の視聴者コメントを想定 | `/translate` が使用するコンテキストプロンプト |

`AUTO_CONTEXT` と `CONTEXT` は、それぞれ環境変数 `PLAMO_AUTO_CONTEXT` と `PLAMO_CONTEXT` でもカスタマイズできます。

llama.cpp のデフォルト起動パラメーターの主な設定：

| パラメーター | サンプルのデフォルト値 | 説明 |
| --- | --- | --- |
| `--n-gpu-layers` | `99` | 可能な限りモデルのレイヤーを GPU にオフロード。CPU のみの場合は `0` に変更可能 |
| `--ctx-size` | `3072` | サーバー全体のコンテキスト容量 |
| `--parallel` | `4` | 並列推論スロット数 |
| `--temp` | `0` | 決定論的なデコード設定を使用 |
| `--n-predict` | `376` | デフォルトの最大生成トークン数 |
| `--jinja` | 有効 | Jinja テンプレートのサポートを有効化 |
| `--no-prefill-assistant` | 有効 | assistant prefill を無効化 |

これらはサンプルスクリプトのパラメーターであり、公式の汎用推奨値ではありません。コンテキスト容量には PFML3 プロンプト、用語集、原文、翻訳文も収める必要があります。長いポストでは、1 推論スロットの容量や生成上限を超える可能性があります。ハードウェアやテキストの長さに応じて `--ctx-size` / `--n-predict` を増やすか、`--parallel` を減らしてください。実際のスロット容量は llama-server の起動ログを参照してください。

### 3. 任意：用語集の設定

`plamo_flusher_bridge.py` と同じディレクトリに UTF-8 エンコードの `glossary.json` を作成します。例：

```json
[
  {"source": "ひなの", "target": "Hinano"},
  {"source": "スト6", "target": "Street Fighter 6"}
]
```

ブリッジスクリプトは翻訳リクエストのたびに用語集を読み込み、原文中に実際に一致する用語のみを PFML3 プロンプトに追加します。一致箇所が重複する場合は長い用語を優先し、同じ用語は 1 回のみ追加します。両エンドポイントでこのファイルを共有します。

- **`glossary.json` がなくても正常に動作します。** `/translate-auto` のみを使用する場合も同様です。
- ファイルの変更内容は次回の翻訳リクエストから読み込まれるため、ブリッジサービスの再起動は不要です。
- ファイルは JSON 配列とし、各要素には空でない `source` と `target` の文字列を含めてください。不正な JSON やトップレベルが配列でない場合、翻訳リクエストが失敗します。
- 用語集はモデルに対するプロンプトとして渡されるものであり、強制的な文字列置換ではありません。すべての場面で指定した訳語が使用されることを保証するものではありません。

### 4. ローカル翻訳サービスの起動

Python スクリプトのあるディレクトリで CMD または PowerShell を開き、以下を実行します。

```bat
py plamo_flusher_bridge.py
```

`python` コマンドを使用する場合：

```bat
python plamo_flusher_bridge.py
```

事前に llama-server を手動で起動する必要はありません。Python スクリプトがモデルサービスを起動し、`/health` を確認して、モデルの準備が整い次第翻訳リクエストの処理を開始します。デフォルト設定では以下のようなログが表示されます。

```text
PLaMo model ready (HTTP /health 200).
Japanese endpoint (/translate) is disabled.
Auto -> zh-hant:     http://127.0.0.1:8001/translate-auto?q=$q
Press Ctrl+C to stop both services.
```

サンプルでは 2 つの API パスが用意されており、初期状態は以下のとおりです。

| URL | 原文言語 | 翻訳先言語 | デフォルトの状態 |
| --- | --- | --- | --- |
| `http://127.0.0.1:8001/translate-auto?q=$q` | モデルが自動判定 | `TARGET_LANG` | 有効 |
| `http://127.0.0.1:8001/translate?q=$q` | `SOURCE_LANG`（デフォルトは `ja`） | `TARGET_LANG` | 無効 |

別のターミナルから動作確認ができます（`curl.exe` がテキストを URL のクエリパラメーター用に自動エンコードします）。

```bat
curl.exe --noproxy "*" -G "http://127.0.0.1:8001/translate-auto" --data-urlencode "q=Hello, world!"
```

サービスが正常に動作していれば、以下のような JSON が返ります（翻訳文はモデルや設定によって異なります）。

```json
{"sentences":[{"trans":"你好，世界！"}],"src":"auto"}
```

ここでの `src: "auto"` は自動判定モードを示すものであり、モデルが実際に判定した言語コードではありません。

利用中は Python のターミナルを起動したままにしてください。`Ctrl+C` を押すと、ブリッジサービスとそれが起動した llama-server の両方を停止できます。

### 5. X Translate で PLaMo を有効にする

X のページを開き、ユーザースクリプトマネージャーから **Translator settings** に移動し、以下のように設定します。

| 設定項目 | 値 |
| --- | --- |
| Enable external translator (fallback to Google Translate) | オン |
| Use PLaMo (apply source-language whitelist) | オン |
| Request Method | GET |
| Translation endpoint URL | `http://127.0.0.1:8001/translate-auto?q=$q` |
| Response Style | Google Translate |

`Save` をクリックするとページが自動的に再読み込みされ、ポストや自己紹介文の翻訳にローカルの PLaMo が優先的に使用されるようになります。`Set translation language` の設定が Python の `TARGET_LANG` と一致していることも確認してください。

ここで URL を `/translate` にしないでください。このエンドポイントは原文言語を固定したライブ配信チャットの翻訳用であり、デフォルトでは無効です。

### トラブルシューティング

| 問題 | 確認事項 |
| --- | --- |
| Python が llama-server または GGUF を見つけられない | `LLAMA_SERVER_EXE` / `GGUF_MODEL_FILE` が実際に存在するファイルを指しているか確認 |
| ポートが既に使用されている | `8000` または `8001` を使用中のサービスを停止するか、Python のポート設定を変更。`PORT` を変更した場合はクライアントの URL も更新 |
| モデルを読み込めない | llama.cpp のバージョンが PLaMo 3 に対応しているか、バックエンドのランタイムライブラリが揃っているか、メモリ / VRAM に空きがあるか確認 |
| ブラウザで接続権限のエラーが出る | ユーザースクリプトマネージャーでローカルアドレスへのアクセスが許可されているか、Python サービスが起動しているか確認 |
| 依然として Google 翻訳が使用される | 外部翻訳が有効か、URL が正しいか、原文言語がホワイトリストの条件を満たすか確認。Python のログとブラウザ開発者ツールのフォールバック警告も確認 |
| 意図しない言語に翻訳される | Python の `TARGET_LANG` を変更して再起動し、X Translate の翻訳先言語も調整 |
| 長いポストの翻訳が途中で切れる | コンテキスト容量、`--n-predict`、並列スロット数、GET リクエストの長さ制限を確認。ブリッジは 1～5000 文字を受け付けるが、デフォルトのトークン容量でその範囲のすべての翻訳を完了できるとは限らない |
| `/translate` が 404 を返す | このエンドポイントはデフォルトで無効。利用する場合は `ENABLE_TRANSLATE = True` に設定して再起動 |

ブリッジサービスはデフォルトでローカルの `127.0.0.1` のみで待ち受けます。API キーによる認証はなく、クロスオリジンアクセスを許可しています。ローカルアドレスでの待ち受けを維持し、LAN やインターネットへ直接公開しないことを推奨します。GET リクエストのテキストがローカルの HTTP アクセスログに記録される場合もあります。

## YoutubeLiveChatFlusher との併用

同じ `plamo_flusher_bridge.py` を [YoutubeLiveChatFlusher](https://github.com/ys-j/YoutubeLiveChatFlusher)（YouTube Live のチャットを弾幕形式で表示するブラウザ拡張機能）にも直接接続できます。別のモデルインスタンスを起動する必要はありません。

まず、Python スクリプトで原文言語固定のエンドポイントを有効にします。

```python
ENABLE_TRANSLATE = True
SOURCE_LANG = "ja"
TARGET_LANG = "zh-hant"
```

保存後、`plamo_flusher_bridge.py` を再実行してください。`SOURCE_LANG` はデフォルトで日本語に固定されているため、日本語のライブ配信コメントに適しています。`TARGET_LANG` は必要に応じて変更できますが、両エンドポイントは同じ翻訳先言語を共有します。

YoutubeLiveChatFlusher の **Translator** 設定で **External service** を選択し、翻訳を有効にして以下のように設定します。

| 設定項目 | 値 |
| --- | --- |
| Request Method | GET |
| URL | `http://127.0.0.1:8001/translate?q=$q` |
| Response Style | Google Translate |

両プロジェクトは同時に動作させることができます。X Translate は `/translate-auto` で原文言語を自動判定し、YoutubeLiveChatFlusher は `/translate` で原文言語を固定し、ライブ配信コメント専用のコンテキストを使用します。両者は同じ PLaMo モデルと用語集を共有します。X Translate のみを使用する場合は、`ENABLE_TRANSLATE = False` のままで構いません。

## License

X Translate Userscript：MIT（スクリプトのメタデータを参照）。PLaMo モデル、llama.cpp、YoutubeLiveChatFlusher にはそれぞれのライセンスが適用されます。
