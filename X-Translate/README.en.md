# X Translate

[日本語](README.md) | **English** | [繁體中文（台灣）](README.zh-hant.md)

An automatic translation userscript for [X (Twitter)](https://x.com/). It replaces X's lousy built-in Grok translations with Google Translate and can also connect to local translation models such as PLaMo 3 Translate or other external translation services.

Google Translate is used by default, with no model deployment or API key required. When an external translator is enabled, the script tries that service first and automatically falls back to Google Translate if the request fails.

- Grok translation
  - Terrible translation quality, with frequent bugs in automatic translation and other features.
- Google Translate
  - This script supports fully automatic translation. Overall translation quality is slightly better than Grok's, with slightly higher latency.
- Locally hosted `plamo-3-translate-0.8b-Q4_K_M`
  - Good translation quality with extremely low latency, translating posts on the page almost instantly.

## Features

- **Automatic post translation**: Automatically translates posts as they enter the browser viewport, without having to click X's native translation button on each post. Supports timelines, replies, posts on profile pages, and more.
- **Automatic profile bio translation**: Automatically attempts to translate non-empty bios. The translation service identifies the source language without relying on X's language tags.
- **Toggle between original and translated text**: Use `Show translation` / `Hide translation` to switch views. Translations are reused for the same page element without sending a new request on every toggle.
- **Replace X's native translation**: Takes over recognizable native translation buttons and adds buttons to posts and bios that lack them. Also supports recognizable native translation entry points for Community Notes.
- **Source-language filtering**: Uses the post's `lang` attribute to skip content in the target language. Simplified Chinese (`zh`) and Traditional Chinese (`zh-TW`) are also skipped when translating into one another. Bios are exempt from this filter.
- **Custom target language**: Provides a searchable language list, defaults to the browser language, and allows resetting to the default at any time.
- **Custom translation services**: Supports GET / POST requests, Google Translate / OpenAI response formats, OpenAI Compatible request bodies, custom JSON bodies, and optional API keys.
- **PLaMo language allowlist**: In PLaMo mode, only posts that meet the allowlist criteria are sent to the external service. Posts in unsupported languages or without valid language tags are handled by Google Translate. The model automatically detects the language of bios. The allowlist can be disabled when using another translator.
- **Automatic fallback**: Automatically tries Google Translate if the external service times out, returns an error, or produces an invalid or empty translation. In PLaMo mode, text containing letters that is returned completely unchanged also triggers fallback. Google Translate itself has primary and backup endpoints and retries with automatic source-language detection when necessary.
- **Preserve links and emoji**: Attempts to preserve links, inline images (including image-based emoji), and line breaks. If the translation service drops placeholders, missing links or images are appended to the translation.
- **Concurrency control and dynamic page support**: Runs up to 5 automatic translation tasks concurrently, prioritizing content higher in the viewport. Monitors dynamic page changes, supports infinite scrolling and page navigation, and prevents stale translations from being displayed on posts whose content has changed.

## Installation

1. Install a userscript manager in your browser, such as [Violentmonkey](https://violentmonkey.github.io/).
2. Open [X-Translate.user.js](https://raw.githubusercontent.com/zerofdest/comprehension/main/X-Translate/X-Translate.user.js) and follow the manager's installation prompts. Alternatively, import the `.user.js` file into the manager.
3. Open or refresh [x.com](https://x.com/) to start using the script.

The script only matches `https://x.com/*`. Google Translate is used by default after installation, with no additional configuration required.

## Usage

### Set the translation language

On an X page, click the browser's userscript manager icon, find **X Translate**, and select **Set translation language**.

In the `Translation Language` dialog, search for and select your preferred language, for example:

| Language | Language code |
| --- | --- |
| English | `en` |
| Japanese | `ja` |
| Chinese | `zh` |
| Chinese (Traditional) | `zh-TW` |
| Korean | `ko` |

The page reloads automatically after you select a language. Click `Reset to browser default` to restore the browser's default language.

### Show original or translated text

Eligible posts and bios are translated automatically when they enter the viewport.

| Button state | Meaning |
| --- | --- |
| `Translating...` | Translation in progress |
| `Hide translation` | The translation is currently displayed; click to restore the original text |
| `Show translation` | The original text is currently displayed; click to show the translation or start a request if none exists yet |

If translation fails, click `Show translation` to retry manually.

### Translator settings

Select **Translator settings** from the X Translate menu in your userscript manager to configure an external translation service.

| Setting | Default | Description |
| --- | --- | --- |
| Enable external translator (fallback to Google Translate) | Off | Tries the external service first when enabled; falls back to Google Translate on failure |
| Use PLaMo (apply source-language whitelist) | On | Applies the PLaMo source-language allowlist to posts; normally disabled when using other services |
| Request Method | GET | Supports GET and POST |
| Translation endpoint URL | `http://127.0.0.1:8001/translate-auto?q=$q` | External translation API endpoint |
| Response Style | Google Translate | Select Google Translate or OpenAI to match the service's actual response format |
| API Type (POST only) | OpenAI Compatible | Uses the built-in OpenAI request format or Custom JSON |
| API Key (POST only, optional) | Empty | Sent as `Authorization: Bearer ...` when provided |
| Model Name (OpenAI Compatible POST only) | Empty | Model name; required for this request format |
| Request Body (Custom POST only) | `{"q":"$q","sl":"$slCode","tl":"$tlCode"}` | Custom JSON request body |

Click `Save` to save the settings and reload the page automatically. `Cancel` discards changes. `Reset defaults` restores the settings in the dialog to their defaults; click `Save` afterward to apply them.

> **Note:** `Use PLaMo` does not start the model or change its target language. The external translator is disabled by default, so the script still uses only Google Translate even if this option is checked.

### Connect to other translation services

Enable `Enable external translator`, disable `Use PLaMo`, and enter the request method, URL, and response format according to the service's API specification. Disabling the allowlist does not disable same-language post filtering.

#### GET

The URL must contain `$q`, for example:

```text
http://127.0.0.1:8001/translate?q=$q&sl=$sl&tl=$tl
```

This is an example of a generic API format; not all services read `sl` and `tl`.

| URL placeholder | Replacement |
| --- | --- |
| `$q` | Text to translate |
| `$sl` / `$slCode` | Source language code; `auto` if unknown |
| `$tl` / `$tlCode` | Target language code |

URL placeholders are automatically URL-encoded and are only allowed in the path or query parameters.

#### POST: OpenAI Compatible

For example, to connect to a service that supports the OpenAI Chat Completions format and JSON Object responses:

| Setting | Example |
| --- | --- |
| Request Method | POST |
| Translation endpoint URL | `http://127.0.0.1:8080/v1/chat/completions` |
| API Type | OpenAI Compatible |
| API Key | Enter as required by the service; leave empty for local services without authentication |
| Model Name | The actual model name provided by the service |
| Response Style | OpenAI |

The script automatically constructs `system` / `user` messages, instructs the model to return JSON containing `sentence` and `src`, and sets `response_format: {"type":"json_object"}`, `temperature: 0`, and `stream: false`. The service must support these request fields; otherwise, use a Custom request body.

#### POST: Custom

Select `API Type: Custom` and write a JSON object according to the translation service's requirements, for example:

```json
{
  "q": "$q",
  "sl": "$slCode",
  "tl": "$tlCode"
}
```

String values in custom JSON support the following placeholders, including strings inside nested objects and arrays:

| Request body placeholder | Replacement |
| --- | --- |
| `$q` | Text to translate |
| `$sl` | English name of the source language |
| `$tl` | English name of the target language |
| `$slCode` | Source language code |
| `$tlCode` | Target language code |

Text is automatically JSON-escaped. At least one occurrence of `$q` must be present in the request body or URL.

#### Supported response formats

**Google Translate**:

```json
{
  "sentences": [
    {"trans": "你好，世界！"}
  ],
  "src": "en"
}
```

The nested array format used by the primary Google Translate endpoint is also supported, for example:

```json
[[["你好，世界！", "Hello, world!", null, null]], null, "en"]
```

**OpenAI**:

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

`choices[0].message.content` can also contain the translated text directly as plain text. Request and response formats are configured independently: GET does not have to be paired with Google Translate, nor POST with OpenAI.

### Privacy and limitations

- Google Translate mode sends text to Google for translation. When local translation is enabled, eligible text that is successfully processed can be translated locally, but text that fails the allowlist check or cannot be translated may still be sent to Google. This version has no option to disable Google fallback and is therefore not a strictly offline translation mode.
- The script accesses cross-origin APIs through `GM_xmlhttpRequest`. Only use trusted URLs for external services, and do not send sensitive text or API keys to untrusted services. API keys are stored in the userscript manager's script settings.
- External translation requests have a 60-second timeout, and automatic translation is limited to 5 concurrent tasks. Manually triggered translations are not subject to this automatic queue limit.
- Google Translate endpoints and X's page structure may change. Functionality is not guaranteed on every page, in every interface language, or on every browser version.

## Local deployment of PLaMo 3 Translate 0.8B (highly recommended)

The latest work in the PLaMo 3 series. Arguably the best translation model in the sub-1B class, although quality varies across supported languages.

X Translate's default external translator configuration is designed for the example script `plamo_flusher_bridge.py`, using the `Q4_K_M` GGUF quantization of [PLaMo 3 Translate 0.8B](https://huggingface.co/pfnet/plamo-3-translate-0.8b).

PLaMo 3 Translate is a dedicated translation model developed by Preferred Networks (PFN). It supports 53 language codes (including Simplified and Traditional Chinese), context, and glossaries. The default GGUF file is approximately 0.57 GB; additional RAM or VRAM is required at runtime.

The Python script starts llama.cpp, constructs PLaMo's PFML3 translation prompt, and converts the model response into a Google Translate-compatible format. A single model process can serve both X Translate and YoutubeLiveChatFlusher.

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

### 1. Download the runtime and model

The following instructions use Windows as an example:

- [Python](https://www.python.org/downloads/): Python 3.10 or later is recommended. The example bridge script only uses the Python standard library; no third-party Python dependencies are required.
- [llama.cpp Releases](https://github.com/ggml-org/llama.cpp/releases): Download a Windows build that supports PLaMo 3 Translate. Select the CPU, CUDA, Vulkan, or other backend appropriate for your hardware, extract the archive, and keep all required runtime files. If the CUDA build requires additional runtime libraries, download them according to the corresponding release instructions.
  - Recommended version: [b12359](https://github.com/ggml-org/llama.cpp/releases/tag/b12359).
- [PLaMo 3 Translate 0.8B GGUF (official model repository)](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF): Download [`plamo-3-translate-0.8b-Q4_K_M.gguf`](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF/resolve/main/plamo-3-translate-0.8b-Q4_K_M.gguf).
- Example startup script: [plamo_flusher_bridge.py](plamo_flusher_bridge.py)

Please also comply with the model's [PLaMo Community License](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF#license).

### 2. Configure the Python script

Open `plamo_flusher_bridge.py` in a text editor and check at least the following three parameters:

```python
LLAMA_SERVER_EXE = Path(r"I:\llama.cpp\llama-server.exe")
GGUF_MODEL_FILE = Path(r"I:\_models\plamo-3-translate-0.8b-Q4_K_M.gguf")

TARGET_LANG = "zh-hant"
```

**Make sure to replace both file paths with the actual paths on your computer and set `TARGET_LANG` to your desired target language.** The `I:` drive paths are only examples; you do not need to use the same directories.

For example:

```python
LLAMA_SERVER_EXE = Path(r"D:\llama.cpp\llama-server.exe")
GGUF_MODEL_FILE = Path(r"D:\models\plamo-3-translate-0.8b-Q4_K_M.gguf")
TARGET_LANG = "en"
```

Common language code mappings:

| Target language | X Translate | Python / PLaMo |
| --- | --- | --- |
| Traditional Chinese | `zh-TW` | `zh-hant` (Python default) |
| Simplified Chinese | `zh` | `zh-hans` |
| English | `en` | `en` |
| Japanese | `ja` | `ja` |
| Korean | `ko` | `ko` |

For the complete language list, see the [official PLaMo model documentation](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF#supported-languages).

**Important: The Python script's `TARGET_LANG` overrides the target language set in X Translate for local translation.** This accounts for language code compatibility issues between PLaMo and other models.\
The current Python example uses a fixed `TARGET_LANG` for both endpoints and ignores incoming `sl` and `tl` query parameters. Changing the language in the browser does not automatically update the Python target language. Restart the script after changing the Python configuration.

Other optional parameters:

| Parameter | Default | Purpose |
| --- | --- | --- |
| `HOST` / `PORT` | `127.0.0.1` / `8001` | External translation bridge address |
| `LLAMA_HOST` / `LLAMA_PORT` | `127.0.0.1` / `8000` | llama-server backend address |
| `LLAMA_STARTUP_TIMEOUT` | `120` | Time to wait for the model to load (seconds) |
| `ENABLE_TRANSLATE` | `False` | Whether to also enable the fixed-source-language `/translate` endpoint |
| `SOURCE_LANG` | `ja` | Fixed source language of `/translate`; does not affect `/translate-auto` |
| `AUTO_CONTEXT` | X post context | Context prompt used by `/translate-auto` |
| `CONTEXT` | Japanese VTuber livestream viewer comments | Context prompt used by `/translate` |

`AUTO_CONTEXT` and `CONTEXT` can also be customized using the `PLAMO_AUTO_CONTEXT` and `PLAMO_CONTEXT` environment variables, respectively.

Key default llama.cpp startup parameters:

| Parameter | Example default | Description |
| --- | --- | --- |
| `--n-gpu-layers` | `99` | Offloads as many model layers as possible to the GPU; set to `0` for CPU-only inference |
| `--ctx-size` | `3072` | Total context budget for the server |
| `--parallel` | `4` | Number of parallel inference slots |
| `--temp` | `0` | Uses deterministic decoding settings |
| `--n-predict` | `376` | Default maximum number of generated tokens |
| `--jinja` | Enabled | Enables Jinja template support |
| `--no-prefill-assistant` | Enabled | Disables assistant prefill |

These are parameters of the example script, not official general-purpose recommendations. The context budget must also accommodate the PFML3 prompt, glossary, source text, and translation. Longer posts may exceed a single inference slot's capacity or hit the generation limit. Increase `--ctx-size` / `--n-predict` or reduce `--parallel` as appropriate for your hardware and text length. Refer to the llama-server startup logs for the actual slot capacity.

### 3. Optional: configure a glossary

Create a UTF-8 encoded `glossary.json` in the same directory as `plamo_flusher_bridge.py`, for example:

```json
[
  {"source": "ひなの", "target": "Hinano"},
  {"source": "スト6", "target": "Street Fighter 6"}
]
```

The bridge reads the glossary on every translation request and adds only terms that actually match the source text to the PFML3 prompt. Longer terms take priority when matches overlap, and each term is added only once. Both endpoints share this file.

- **The script works without `glossary.json`**, including when only `/translate-auto` is used.
- Changes to the file are read on the next translation request; no bridge restart is required.
- The file must be a JSON array with entries containing non-empty `source` and `target` strings. Invalid JSON or a non-array root causes the translation request to fail.
- The glossary is supplied as a model prompt, not enforced string replacement, so the model is not guaranteed to use the specified translations in every situation.

### 4. Start the local translation service

Open CMD or PowerShell in the Python script's directory and run:

```bat
py plamo_flusher_bridge.py
```

If you use the `python` command instead:

```bat
python plamo_flusher_bridge.py
```

There is no need to start llama-server manually beforehand. The Python script starts the model service itself, checks `/health`, and begins handling translation requests when the model is ready. The default logs include messages like these:

```text
PLaMo model ready (HTTP /health 200).
Japanese endpoint (/translate) is disabled.
Auto -> zh-hant:     http://127.0.0.1:8001/translate-auto?q=$q
Press Ctrl+C to stop both services.
```

Two API paths are provided by the example, with the following default states:

| URL | Source language | Target language | Default state |
| --- | --- | --- | --- |
| `http://127.0.0.1:8001/translate-auto?q=$q` | Automatically detected by the model | `TARGET_LANG` | Enabled |
| `http://127.0.0.1:8001/translate?q=$q` | `SOURCE_LANG` (default `ja`) | `TARGET_LANG` | Disabled |

Test from another terminal (`curl.exe` automatically encodes the text as a URL query parameter):

```bat
curl.exe --noproxy "*" -G "http://127.0.0.1:8001/translate-auto" --data-urlencode "q=Hello, world!"
```

If the service is working, it returns JSON similar to the following (the translation depends on the model and configuration):

```json
{"sentences":[{"trans":"你好，世界！"}],"src":"auto"}
```

Here, `src: "auto"` indicates automatic detection mode, not the actual language code detected by the model.

Keep the Python terminal running while using the service. Press `Ctrl+C` to stop both the bridge and the llama-server process it started.

### 5. Enable PLaMo in X Translate

Open X and go to **Translator settings** in your userscript manager. Use the following configuration:

| Setting | Value |
| --- | --- |
| Enable external translator (fallback to Google Translate) | On |
| Use PLaMo (apply source-language whitelist) | On |
| Request Method | GET |
| Translation endpoint URL | `http://127.0.0.1:8001/translate-auto?q=$q` |
| Response Style | Google Translate |

Click `Save`. After the page reloads automatically, local PLaMo translation is prioritized for posts and bios. Make sure that `Set translation language` matches the Python script's `TARGET_LANG`.

Do not use `/translate` as the URL here: that endpoint is designed for fixed-source-language livestream chat translation and is disabled by default.

### Troubleshooting

| Problem | What to check |
| --- | --- |
| Python cannot find llama-server or the GGUF file | Make sure `LLAMA_SERVER_EXE` / `GGUF_MODEL_FILE` point to existing files |
| Port already in use | Stop the service occupying `8000` or `8001`, or change the Python ports; if you change `PORT`, update the client URL accordingly |
| Model fails to load | Check whether your llama.cpp version supports PLaMo 3, whether all backend runtime libraries are available, and whether you have sufficient RAM / VRAM |
| Browser reports a connection permission issue | Check whether the userscript manager allows access to local addresses and confirm the Python service is running |
| Still using Google Translate | Make sure the external translator is enabled, the URL is correct, and the source language meets the allowlist criteria; check Python logs and fallback warnings in the browser developer tools |
| Wrong target language | Change `TARGET_LANG` in Python and restart; also adjust the target language in X Translate |
| Long posts are translated incompletely | Check the context budget, `--n-predict`, parallel slots, and GET request length limits. The bridge accepts 1–5000 characters, but the default token budget does not guarantee translation of every input within that range |
| `/translate` returns 404 | This endpoint is disabled by default; set `ENABLE_TRANSLATE = True` and restart if needed |

By default, the bridge listens only on local address `127.0.0.1`, has no API key authentication, and allows cross-origin access. Keep the local binding and avoid exposing it directly to your LAN or the Internet. Text in GET requests may also appear in local HTTP access logs.

## Use with YoutubeLiveChatFlusher

The same `plamo_flusher_bridge.py` can also connect directly to [YoutubeLiveChatFlusher](https://github.com/ys-j/YoutubeLiveChatFlusher), a browser extension for displaying YouTube Live chat as scrolling comments. No second model instance is required.

First, enable the fixed-source-language endpoint in the Python script:

```python
ENABLE_TRANSLATE = True
SOURCE_LANG = "ja"
TARGET_LANG = "zh-hant"
```

Save the file and run `plamo_flusher_bridge.py` again. `SOURCE_LANG` is fixed to Japanese by default, making it suitable for Japanese livestream comments. `TARGET_LANG` can be changed as needed, but both endpoints share the same target language.

In YoutubeLiveChatFlusher's **Translator** settings, select **External service**, enable translation, and configure it as follows:

| Setting | Value |
| --- | --- |
| Request Method | GET |
| URL | `http://127.0.0.1:8001/translate?q=$q` |
| Response Style | Google Translate |

Both projects can run at the same time: X Translate uses `/translate-auto` for automatic source-language detection, while YoutubeLiveChatFlusher uses `/translate` with a fixed source language and its own livestream comment context. Both share the same PLaMo model and glossary. If you only use X Translate, leave `ENABLE_TRANSLATE = False`.

## License

X Translate Userscript: MIT (see the script metadata). The PLaMo model, llama.cpp, and YoutubeLiveChatFlusher are subject to their respective licenses.
