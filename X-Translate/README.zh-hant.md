# X Translate

[日本語](README.md) | [English](README.en.md) | **繁體中文（台灣）** | [العربية](README.ar.md) | [Español](README.es.md) | [Português](README.pt.md)

適用於 [X（Twitter）](https://x.com/) 的自動翻譯使用者腳本（Userscript）。支援使用 Google Translate 替代 X 原生的垃圾 Grok 翻譯，也可串接 PLaMo 3 Translate 等本機翻譯模型或其他外部翻譯服務。

預設使用 Google Translate，不需部署模型或設定 API Key。啟用外部翻譯服務後，腳本會優先嘗試該服務，並在請求失敗時自動回退至 Google Translate。

- Grok 翻譯
  - 翻譯效果垃圾，自動翻譯等經常出 Bug
- Google Translate
  - 本腳本支援全自動翻譯，整體翻譯品質比 Grok 略好，但翻譯延遲略高
- 本機部署 `plamo-3-translate-0.8b-Q4_K_M` 或 `Hy-MT2-1.8B-Q8_0`
  - 翻譯品質好且延遲極低，頁面內幾乎秒翻譯

## 功能一覽

- **自動翻譯貼文**：貼文進入瀏覽器可視範圍後自動翻譯，不需逐條點選 X 原生翻譯按鈕。支援時間軸、回覆及個人首頁中的貼文等。
- **自動翻譯個人簡介（Bio）**：對非空個人簡介自動嘗試翻譯，由翻譯服務辨識來源語言，不依賴 X 提供的語言標籤。
- **原文與譯文切換**：透過 `Show translation` / `Hide translation` 切換顯示；同一頁面元素的譯文可重複使用，不需每次切換都重新請求翻譯。
- **替換 X 原生翻譯**：接管可辨識的原生翻譯按鈕，並為沒有翻譯按鈕的貼文及個人簡介新增按鈕；相容可辨識的 Community Notes（社群註解）原生翻譯入口。
- **來源語言過濾**：根據貼文的 `lang` 屬性跳過與目標語言相同的內容。簡體中文（`zh`）與繁體中文（`zh-TW`）之間也會相互跳過。個人簡介不受此過濾規則限制。
- **自訂目標語言**：提供可搜尋的語言選擇清單，預設跟隨瀏覽器語言，並可隨時恢復預設設定。
- **自訂翻譯服務**：支援 GET / POST 請求、Google Translate / OpenAI 回應格式、OpenAI Compatible 請求主體、自訂 JSON 請求主體及可選 API Key。
- **自動回退**：外部服務逾時、回傳錯誤、回傳無效或空譯文時自動嘗試 Google Translate；PLaMo 模式下，包含字母且譯文與原文完全相同的內容也會觸發回退。Google Translate 本身提供主、備用介面及必要時的來源語言自動辨識重試。
- **保留連結和 Emoji**：嘗試保留原文中的連結、內嵌圖片（包括圖片形式的 Emoji）與換行；若翻譯服務遺失預留位置，則將缺少的連結或圖片附在譯文末尾。
- **並行控制與動態頁面相容**：最多同時執行 5 個自動翻譯工作，優先處理可視範圍上方的內容；監聽頁面動態變化，支援捲動載入與頁面切換，並避免將過期譯文顯示到已變化的貼文上。
- **PLaMo 語言白名單**：使用 PLaMo 時，僅向外部服務傳送符合白名單的貼文；不支援或缺少有效語言標籤的貼文交由 Google Translate 處理。個人簡介由模型自動辨識語言。串接其他翻譯服務時可關閉該白名單。
## 安裝

1. 在瀏覽器中安裝 Userscript 管理員，例如 [Violentmonkey](https://violentmonkey.github.io/) 
2. 開啟 [X-Translate.user.js](https://raw.githubusercontent.com/zerofdest/comprehension/main/X-Translate/X-Translate.user.js)，依照管理員提示安裝腳本。也可以將 `.user.js` 檔案匯入管理員。
3. 開啟或重新整理 [x.com](https://x.com/)，腳本即可開始運作。

腳本僅在符合 `https://x.com/*` 的網頁上執行。安裝後預設使用 Google Translate，不需要額外設定。

## 使用說明

### 設定翻譯語言

在 X 頁面點選瀏覽器的 Userscript 管理員圖示，找到 **X Translate**，選擇 **Set translation language**。

在跳出的 `Translation Language` 視窗中搜尋並選擇所需語言，例如：

| 語言 | 語言代碼 |
| --- | --- |
| English | `en` |
| Japanese | `ja` |
| Chinese | `zh` |
| Chinese (Traditional) | `zh-TW` |
| Korean | `ko` |

選擇語言後，頁面會自動重新整理。點選 `Reset to browser default` 可恢復瀏覽器預設語言。

### 顯示原文或譯文

符合翻譯條件的貼文及個人簡介進入可視範圍時，腳本會自動送出翻譯請求。

| 按鈕狀態 | 意義 |
| --- | --- |
| `Translating...` | 正在翻譯 |
| `Hide translation` | 目前顯示譯文，點選後恢復原文 |
| `Show translation` | 目前顯示原文，點選後顯示譯文；若尚無譯文則送出翻譯請求 |

如果翻譯失敗，可點選 `Show translation` 手動重試。

### Translator settings

在 Userscript 管理員的 X Translate 選單中選擇 **Translator settings**，可設定外部翻譯服務。

| 設定項 | 預設值 | 說明 |
| --- | --- | --- |
| Enable external translator (fallback to Google Translate) | 關閉 | 啟用後優先呼叫外部服務；失敗時回退至 Google Translate |
| Use PLaMo (apply source-language whitelist) | 開啟 | 對貼文套用 PLaMo 來源語言白名單；串接其他服務時通常關閉 |
| Request Method | GET | 支援 GET 和 POST |
| Translation endpoint URL | `http://127.0.0.1:8001/translate-X?q=$q` | 外部翻譯 API 位址 |
| Response Style | Google Translate | 選擇與服務實際回傳格式一致的選項：Google Translate 或 OpenAI |
| API Type（僅 POST） | OpenAI Compatible | 使用內建 OpenAI 請求格式或 Custom JSON |
| API Key（僅 POST，可選） | 空 | 非空時以 `Authorization: Bearer ...` 傳送 |
| Model Name（僅 OpenAI Compatible POST） | 空 | 模型名稱；使用該請求格式時必填 |
| Request Body（僅 Custom POST） | `{"q":"$q","sl":"$slCode","tl":"$tlCode"}` | 自訂 JSON 請求主體 |

點選 `Save` 儲存並自動重新整理頁面；`Cancel` 放棄修改；`Reset defaults` 將視窗中的設定恢復為預設值，隨後點選 `Save` 生效。

> **注意：** `Use PLaMo` 不是啟動模型的開關，也不會修改模型的目標語言。外部服務預設關閉，即使該選項已勾選，腳本仍只使用 Google Translate。

### 串接其他翻譯服務

啟用 `Enable external translator`，關閉 `Use PLaMo`，然後根據服務的 API 規範填寫請求方法、URL 和回應格式。關閉白名單並不會關閉同語言貼文過濾規則。

#### GET

URL 必須包含 `$q`，例如：

```text
http://127.0.0.1:8001/translate?q=$q&sl=$sl&tl=$tl
```

此處為通用介面格式範例，並不代表所有服務都會讀取 `sl` 和 `tl`。

| URL 預留位置 | 替換內容 |
| --- | --- |
| `$q` | 待翻譯文字 |
| `$sl` / `$slCode` | 來源語言代碼；未知時為 `auto` |
| `$tl` / `$tlCode` | 目標語言代碼 |

URL 中的預留位置會自動進行 URL 編碼，僅允許出現在路徑或查詢參數中。

#### POST：OpenAI Compatible

例如，串接一個支援 OpenAI Chat Completions 格式及 JSON Object 回應的服務：

| 設定項 | 範例 |
| --- | --- |
| Request Method | POST |
| Translation endpoint URL | `http://127.0.0.1:8080/v1/chat/completions` |
| API Type | OpenAI Compatible |
| API Key | 依服務要求填寫；本機不需驗證的服務可留空 |
| Model Name | 服務實際提供的模型名稱 |
| Response Style | OpenAI |

腳本會自動建構 `system` / `user` messages，要求模型回傳包含 `sentence` 和 `src` 的 JSON，並設定 `response_format: {"type":"json_object"}`、`temperature: 0`、`stream: false`。服務需要相容這些請求欄位；若不相容，可改用 Custom 請求主體。

#### POST：Custom

選擇 `API Type: Custom`，依翻譯服務的要求編寫 JSON 物件，例如：

```json
{
  "q": "$q",
  "sl": "$slCode",
  "tl": "$tlCode"
}
```

自訂 JSON 的字串值支援以下預留位置（包括巢狀物件及陣列內的字串）：

| 請求主體預留位置 | 替換內容 |
| --- | --- |
| `$q` | 待翻譯文字 |
| `$sl` | 來源語言的英文名稱 |
| `$tl` | 目標語言的英文名稱 |
| `$slCode` | 來源語言代碼 |
| `$tlCode` | 目標語言代碼 |

文字會自動進行 JSON 跳脫。請求主體或 URL 至少有一處包含 `$q`。

#### 支援的回應格式

**Google Translate**：

```json
{
  "sentences": [
    {"trans": "你好，世界！"}
  ],
  "src": "en"
}
```

也支援 Google Translate 主介面使用的巢狀陣列格式，例如：

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

`choices[0].message.content` 也可以直接包含純文字譯文。請求格式與回應格式獨立設定，不要求 GET 必須搭配 Google Translate 或 POST 必須搭配 OpenAI。

### 隱私與使用限制

- Google Translate 模式會將待翻譯文字傳送給 Google。啟用本機翻譯後，符合條件且成功處理的文字可在本機完成翻譯，但不符合白名單或翻譯失敗的內容仍可能被傳送至 Google。目前版本沒有關閉 Google 回退的選項，因此不屬於嚴格離線翻譯模式。
- 腳本使用 `GM_xmlhttpRequest` 存取跨來源介面，設定外部服務時僅使用可信任的 URL；不要將敏感文字或 API Key 交給不可信服務。API Key 儲存於 Userscript 管理員的腳本設定中。
- 外部翻譯請求的逾時為 60 秒，自動翻譯並行上限為 5；手動觸發不受該自動佇列上限限制。
- Google 翻譯介面及 X 頁面結構可能發生變化，相關功能不保證在所有頁面、所有語言介面和所有瀏覽器版本下始終可用。

## 本機部署 PLaMo 3 Translate 0.8B（強烈推薦）

PLaMo 3 最新力作，說是 1B 以下效果最好的翻譯模型也不為過，不過各支援語言的翻譯效果有所差異。

X Translate 的預設外部服務設定適用於範例腳本 [plamo_flusher_bridge.py](plamo_flusher_bridge.py)，使用 [PLaMo 3 Translate 0.8B](https://huggingface.co/pfnet/plamo-3-translate-0.8b) 的 `Q4_K_M` GGUF 量化模型。

PLaMo 3 Translate 是 Preferred Networks（PFN）開發的專用翻譯模型，支援 53 種語言代碼（包含簡體及繁體中文），並支援上下文及術語表。預設 GGUF 檔案約 0.57 GB；實際執行還需要額外的記憶體或顯示記憶體（VRAM）。

該 Python 腳本負責啟動 llama.cpp、建立 PLaMo 的 PFML3 翻譯提示詞，並將模型回應轉換為 Google Translate 相容格式。一個模型程序即可同時服務 X Translate 和 YoutubeLiveChatFlusher。

```text
X Translate                GET /translate-X
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

### 1. 下載執行環境和模型

以下以 Windows 為例：

- [Python](https://www.python.org/downloads/)：建議 Python 3.10 或更新版本。範例橋接腳本僅使用 Python 標準函式庫，不需安裝第三方 Python 相依套件。
- [llama.cpp Releases](https://github.com/ggml-org/llama.cpp/releases)：下載支援 PLaMo 3 Translate 的 Windows 建構，依硬體選擇 CPU、CUDA 或 Vulkan 等後端，解壓縮並保留全部執行所需檔案。CUDA 建構如需額外的執行階段程式庫，也應依對應 Release 說明下載。
  - 推薦 [b12359](https://github.com/ggml-org/llama.cpp/releases/tag/b12359) 版本
- [PLaMo 3 Translate 0.8B GGUF（官方模型儲存庫）](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF)：下載 [`plamo-3-translate-0.8b-Q4_K_M.gguf`](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF/resolve/main/plamo-3-translate-0.8b-Q4_K_M.gguf)。
- 範例啟動腳本：[plamo_flusher_bridge.py](plamo_flusher_bridge.py)

請同時遵守模型的 [PLaMo Community License](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF#license)。

### 2. 修改 Python 腳本設定

使用文字編輯器開啟 `plamo_flusher_bridge.py`，至少檢查以下三個參數：

```python
LLAMA_SERVER_EXE = Path(r"I:\llama.cpp\llama-server.exe")
GGUF_MODEL_FILE = Path(r"I:\_models\plamo-3-translate-0.8b-Q4_K_M.gguf")

TARGET_LANG = "zh-hant"
```

**務必將兩個檔案路徑替換為自己電腦上的實際路徑，並將 `TARGET_LANG` 設定為所需的翻譯目標語言。** 範例中的 `I:` 磁碟機路徑僅為示範，不要求使用相同目錄。

例如：

```python
LLAMA_SERVER_EXE = Path(r"D:\llama.cpp\llama-server.exe")
GGUF_MODEL_FILE = Path(r"D:\models\plamo-3-translate-0.8b-Q4_K_M.gguf")
TARGET_LANG = "en"
```

常用語言代碼對照：

| 目標語言 | X Translate | Python / PLaMo |
| --- | --- | --- |
| 繁體中文 | `zh-TW` | `zh-hant`（Python 預設） |
| 簡體中文 | `zh` | `zh-hans` |
| 英文 | `en` | `en` |
| 日文 | `ja` | `ja` |
| 韓文 | `ko` | `ko` |

完整語言清單請參閱 [PLaMo 官方模型說明](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF#supported-languages)。

**重要：在本機翻譯時，Python 腳本中的 `TARGET_LANG` 會優先於 X Translate 的目標語言設定。** 這是考量 PLaMo 及其他模型的語言代碼可能存在相容性問題。\
目前 Python 範例對兩個端點均使用固定的 `TARGET_LANG`，忽略傳入的 `sl` 和 `tl` 查詢參數；在瀏覽器內更改語言不會自動更新 Python 中的目標語言。修改 Python 設定後需要重新啟動腳本。

其他可選參數：

| 參數 | 預設值 | 用途 |
| --- | --- | --- |
| `HOST` / `PORT` | `127.0.0.1` / `8001` | 外部翻譯橋接服務位址 |
| `LLAMA_HOST` / `LLAMA_PORT` | `127.0.0.1` / `8000` | llama-server 後端位址 |
| `LLAMA_STARTUP_TIMEOUT` | `120` | 等待模型載入的時間（秒） |
| `AUTO_CONTEXT` | X 貼文情境 | 針對X-translate使用的上下文提示 |
| `ENABLE_FLUSHER` | `False` | 是否同時啟用接入[YoutubeLiveChatFlusher](https://github.com/ys-j/YoutubeLiveChatFlusher)的端點 |
| `CONTEXT` | 日本實況直播觀眾留言情境 | 接入[YoutubeLiveChatFlusher](https://github.com/ys-j/YoutubeLiveChatFlusher)時使用的上下文提示 |

對YouTube彈幕化及翻譯感興趣的參見[接入 YoutubeLiveChatFlusher](#接入-YoutubeLiveChatFlusher)

`AUTO_CONTEXT` 和 `CONTEXT` 也可分別透過環境變數 `PLAMO_AUTO_CONTEXT` 和 `PLAMO_CONTEXT` 自訂。

預設 llama.cpp 啟動參數中的主要設定如下：

| 參數 | 範例預設值 | 說明 |
| --- | --- | --- |
| `--n-gpu-layers` | `99` | 盡可能將模型層卸載至 GPU；純 CPU 可改為 `0` |
| `--ctx-size` | `3072` | 服務總上下文預算 |
| `--parallel` | `4` | 並行推論槽位數量 |
| `--temp` | `0` | 使用確定性解碼設定 |
| `--n-predict` | `376` | 預設最大生成 token 數 |
| `--jinja` | 啟用 | 啟用 Jinja 模板支援 |
| `--no-prefill-assistant` | 啟用 | 停用 assistant prefill |

這些是範例腳本的參數，不是官方通用推薦值。上下文預算還需容納 PFML3 提示、術語表、原文與譯文；較長貼文可能超出單一推論槽位的容量，或觸及生成上限。可依硬體和文字長度適當增大 `--ctx-size` / `--n-predict`，或降低 `--parallel`。實際槽位容量以 llama-server 啟動記錄為準。

### 3. 可選：設定術語表

在 `plamo_flusher_bridge.py` 同目錄建立 UTF-8 編碼的 `glossary.json`，例如：

```json
[
  {"source": "ひなの", "target": "Hinano"},
  {"source": "スト6", "target": "Street Fighter 6"}
]
```

橋接腳本會在每次翻譯時讀取術語表，僅將原文中實際符合的術語加入 PFML3 提示詞；重疊比對時優先使用較長的術語，同一術語僅加入一次。兩個端點共用此檔案。

- **沒有 `glossary.json` 也可正常執行**，包括僅使用 `/translate-X` 的情況。
- 修改檔案後，下次翻譯即可讀取新內容，不需重新啟動橋接服務。
- 檔案應為 JSON 陣列，項目包含非空的 `source` 和 `target` 字串。無效 JSON 或最上層結構不是陣列會導致翻譯請求失敗。
- 術語表作為模型提示，而非強制字串替換，不能保證模型在所有情境下都嚴格採用指定譯名。

### 4. 啟動本機翻譯服務

在 Python 腳本所在目錄開啟 CMD 或 PowerShell，執行：

```bat
py plamo_flusher_bridge.py
```

如果使用 `python` 指令：

```bat
python plamo_flusher_bridge.py
```

不需要事先手動啟動 llama-server。Python 腳本會自行啟動模型服務，檢查 `/health`，在模型就緒後開始處理翻譯請求。預設記錄包含以下資訊：

```text
PLaMo model ready (HTTP /health 200).
Flusher endpoint (/translate) is disabled.
Auto (X posts) -> zh-hant: http://127.0.0.1:8001/translate-X?q=$q
Backend: http://127.0.0.1:8000/v1/completions  model=plamo-3-translate
Request sl/tl parameters are ignored by both endpoints.
Glossary file: F:\_repositories\comprehension\X-Translate\glossary.json
Press Ctrl+C to stop both services.
```

預設提供兩個 API 路徑：

| URL | 來源語言 | 目標語言 | 預設狀態 |
| --- | --- | --- | --- |
| `http://127.0.0.1:8001/translate-X?q=$q` | 模型自動辨識 | `TARGET_LANG` | 啟用 |
| `http://127.0.0.1:8001/translate?q=$q` | 模型自動辨識 | `TARGET_LANG` | 停用 |

可在另一個終端機測試（`curl.exe` 會將文字自動編碼為 URL 查詢參數）：

```bat
curl.exe --noproxy "*" -G "http://127.0.0.1:8001/translate-X" --data-urlencode "q=Hello, world!"
```

如果服務正常，將回傳類似以下 JSON（譯文因模型及設定而異）：

```json
{"sentences":[{"trans":"你好，世界！"}],"src":"auto"}
```

其中 `src: "auto"` 代表自動辨識模式，並不是模型辨識出的實際語言代碼。

使用期間保持 Python 終端機執行；按下 `Ctrl+C` 可停止橋接服務以及由它啟動的 llama-server。

### 5. 在 X Translate 中啟用 PLaMo

開啟 X 頁面，在 Userscript 管理員中進入 **Translator settings**，使用以下設定：

| 設定項 | 值 |
| --- | --- |
| Enable external translator (fallback to Google Translate) | 開啟 |
| Use PLaMo (apply source-language whitelist) | 開啟 |
| Request Method | GET |
| Translation endpoint URL | `http://127.0.0.1:8001/translate-X?q=$q` |
| Response Style | Google Translate |

點選 `Save`，頁面自動重新整理後，即可優先使用本機 PLaMo 翻譯貼文及個人簡介。請同時確認 `Set translation language` 與 Python 的 `TARGET_LANG` 一致。

不要將此處的 URL 填成 `/translate`：後者是為直播聊天室翻譯設計的介面，且預設停用。

### 常見問題

| 問題 | 疑難排解方法 |
| --- | --- |
| **長貼文譯文不完整** | 根據plamo_flusher_bridge.py的cmd窗口的Token usage信息增大`--n-predict`與`--ctx-size` |
| Python 找不到 llama-server 或 GGUF | 檢查 `LLAMA_SERVER_EXE` / `GGUF_MODEL_FILE` 是否指向實際存在的檔案 |
| 連接埠已被佔用 | 停止佔用 `8000` 或 `8001` 的服務，或修改 Python 連接埠；若修改 `PORT`，同步更新用戶端 URL |
| 模型無法載入 | 檢查 llama.cpp 版本是否支援 PLaMo 3、後端執行階段程式庫是否齊全，以及可用記憶體 / 顯示記憶體（VRAM） |
| 瀏覽器提示連線權限問題 | 檢查 Userscript 管理員是否允許存取本機位址，並確認 Python 服務已啟動 |
| 仍在使用 Google Translate | 確認已啟用外部翻譯、URL 正確、來源語言符合白名單；檢查 Python 記錄及瀏覽器開發人員工具中的回退警告 |
| 翻譯為錯誤的目標語言 | 修改 Python 的 `TARGET_LANG` 並重新啟動，同時調整 X Translate 的目標語言 |
| `/translate` 回傳 404 | 該端點預設關閉；如需使用，請設定 `ENABLE_FLUSHER = True` 並重新啟動 |

橋接服務預設僅監聽本機 `127.0.0.1`，沒有 API Key 驗證，且允許跨來源存取。建議保留本機監聽位址，不要直接公開至區域網路或網際網路。GET 請求文字也可能出現在本機 HTTP 存取記錄中。

## 接入 YoutubeLiveChatFlusher

同一個 `plamo_flusher_bridge.py` 也可以直接串接 [YoutubeLiveChatFlusher](https://github.com/ys-j/YoutubeLiveChatFlusher)（YouTube Live 彈幕瀏覽器擴充功能），不需額外啟動第二個模型執行個體。

首先，在 Python 腳本中開啟Flusher端點：

```python
ENABLE_FLUSHER = True
```

儲存後重新執行 `plamo_flusher_bridge.py`。`TARGET_LANG` 可依需求修改，但兩個端點共用同一個目標語言。

在 YoutubeLiveChatFlusher 的 **Translator** 設定中選擇 **External service**，啟用翻譯並設定如下：

| 設定項 | 值 |
| --- | --- |
| Request Method | GET |
| URL | `http://127.0.0.1:8001/translate?q=$q` |
| Response Style | Google Translate |

兩個專案可以同時執行：X Translate 與 YoutubeLiveChatFlusher 共用同一個 PLaMo 模型及術語表，差異只在於URL 與 context。若只使用 X Translate，保持 `ENABLE_FLUSHER = False` 即可。

## License

X Translate Userscript: MIT（見腳本中繼資料）。PLaMo 模型、llama.cpp 及 YoutubeLiveChatFlusher 分別適用各自的授權條款。
