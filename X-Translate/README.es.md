# X Translate

[日本語](README.md) | [English](README.en.md) | [繁體中文（台灣）](README.zh-hant.md) | [العربية](README.ar.md) | **Español** | [Português](README.pt.md)

Script de usuario (Userscript) de traducción automática para [X (Twitter)](https://x.com/). Permite sustituir la pésima traducción nativa de Grok en X por Google Translate, así como integrar modelos de traducción locales, como PLaMo 3 Translate, u otros servicios de traducción externos.

De forma predeterminada utiliza Google Translate, sin necesidad de desplegar un modelo ni configurar una clave de API. Al habilitar un servicio de traducción externo, el script intenta utilizarlo primero y recurre automáticamente a Google Translate si la solicitud falla.

- Traducción de Grok
  - Traducciones pésimas y errores frecuentes en funciones como la traducción automática.
- Google Translate
  - Este script permite traducir de forma totalmente automática. La calidad general de la traducción es ligeramente superior a la de Grok, aunque la latencia es algo mayor.
- Ejecución local de `plamo-3-translate-0.8b-Q4_K_M`
  - Buena calidad de traducción y latencia extremadamente baja: las traducciones aparecen en la página casi al instante.

## Funciones

- **Traducción automática de publicaciones**: traduce las publicaciones cuando entran en el área visible del navegador, sin tener que pulsar individualmente los botones de traducción nativos de X. Compatible con publicaciones de la cronología, respuestas, perfiles, etc.
- **Traducción automática de biografías (Bio)**: intenta traducir automáticamente las biografías no vacías. El servicio de traducción identifica el idioma de origen sin depender de las etiquetas de idioma de X.
- **Alternancia entre el original y la traducción**: utiliza `Show translation` / `Hide translation` para alternar la visualización. La traducción de un mismo elemento de la página se puede reutilizar sin realizar una nueva solicitud cada vez.
- **Sustitución de la traducción nativa de X**: asume el control de los botones de traducción nativos que puede reconocer y añade botones a las publicaciones y biografías que carecen de ellos. También es compatible con los controles de traducción nativos reconocibles de las Notas de la comunidad (Community Notes).
- **Filtrado por idioma de origen**: utiliza el atributo `lang` de las publicaciones para omitir el contenido que ya está en el idioma de destino. El chino simplificado (`zh`) y el chino tradicional (`zh-TW`) también se omiten mutuamente. Este filtro no se aplica a las biografías.
- **Idioma de destino configurable**: ofrece una lista de idiomas con búsqueda. Por defecto utiliza el idioma del navegador y permite restaurar esa configuración en cualquier momento.
- **Servicios de traducción personalizados**: admite solicitudes GET / POST, formatos de respuesta de Google Translate / OpenAI, cuerpos de solicitud compatibles con OpenAI, cuerpos JSON personalizados y claves de API opcionales.
- **Lista de idiomas permitidos de PLaMo**: al utilizar PLaMo, solo se envían al servicio externo las publicaciones cuyo idioma figura en la lista. Google Translate se encarga de las publicaciones con idiomas no admitidos o sin una etiqueta de idioma válida. El modelo detecta automáticamente el idioma de las biografías. La lista se puede desactivar al integrar otros servicios de traducción.
- **Alternativa automática en caso de fallo**: si el servicio externo agota el tiempo de espera, devuelve un error o produce una traducción vacía o no válida, se intenta utilizar Google Translate. En el modo PLaMo, también se activa esta alternativa cuando el contenido contiene letras y la traducción es idéntica al original. Google Translate dispone de interfaces principal y alternativa, además de reintentos con detección automática del idioma de origen cuando es necesario.
- **Conservación de enlaces y emojis**: intenta conservar los enlaces, las imágenes en línea (incluidos los emojis en formato de imagen) y los saltos de línea del original. Si el servicio pierde los marcadores de posición, los enlaces o imágenes que faltan se añaden al final de la traducción.
- **Control de concurrencia y compatibilidad con páginas dinámicas**: ejecuta hasta 5 tareas de traducción automática simultáneas, dando prioridad al contenido situado en la parte superior del área visible. Detecta cambios dinámicos de la página, admite la carga durante el desplazamiento y la navegación entre páginas, y evita mostrar traducciones obsoletas en publicaciones que han cambiado.

## Instalación

1. Instala un gestor de scripts de usuario en el navegador, como [Violentmonkey](https://violentmonkey.github.io/).
2. Abre [X-Translate.user.js](https://raw.githubusercontent.com/zerofdest/comprehension/main/X-Translate/X-Translate.user.js) e instala el script siguiendo las indicaciones del gestor. También puedes importar el archivo `.user.js` directamente.
3. Abre o recarga [x.com](https://x.com/) para que el script empiece a funcionar.

El script solo se ejecuta en páginas que coinciden con `https://x.com/*`. Tras la instalación utiliza Google Translate por defecto, sin configuración adicional.

## Instrucciones de uso

### Configurar el idioma de traducción

En una página de X, pulsa el icono del gestor de scripts de usuario del navegador, busca **X Translate** y selecciona **Set translation language**.

En la ventana `Translation Language`, busca y selecciona el idioma deseado, por ejemplo:

| Idioma | Código de idioma |
| --- | --- |
| English | `en` |
| Japanese | `ja` |
| Chinese | `zh` |
| Chinese (Traditional) | `zh-TW` |
| Korean | `ko` |

La página se recarga automáticamente al seleccionar un idioma. Pulsa `Reset to browser default` para restaurar el idioma predeterminado del navegador.

### Mostrar el original o la traducción

Cuando las publicaciones y biografías que cumplen las condiciones de traducción entran en el área visible, el script envía automáticamente las solicitudes de traducción.

| Estado del botón | Significado |
| --- | --- |
| `Translating...` | Traducción en curso |
| `Hide translation` | Se muestra la traducción; pulsa para volver al original |
| `Show translation` | Se muestra el original; pulsa para ver la traducción. Si todavía no existe, se envía una solicitud de traducción |

Si la traducción falla, puedes pulsar `Show translation` para reintentar manualmente.

### Translator settings

Selecciona **Translator settings** en el menú de X Translate del gestor de scripts de usuario para configurar un servicio de traducción externo.

| Opción | Valor predeterminado | Descripción |
| --- | --- | --- |
| Enable external translator (fallback to Google Translate) | Desactivado | Da prioridad al servicio externo y recurre a Google Translate si falla |
| Use PLaMo (apply source-language whitelist) | Activado | Aplica a las publicaciones la lista de idiomas de origen permitidos de PLaMo; normalmente se desactiva al integrar otros servicios |
| Request Method | GET | Admite GET y POST |
| Translation endpoint URL | `http://127.0.0.1:8001/translate-X?q=$q` | Dirección de la API de traducción externa |
| Response Style | Google Translate | Selecciona el formato real de respuesta del servicio: Google Translate u OpenAI |
| API Type (solo POST) | OpenAI Compatible | Utiliza el formato de solicitud integrado de OpenAI o Custom JSON |
| API Key (solo POST, opcional) | Vacío | Si no está vacío, se envía mediante `Authorization: Bearer ...` |
| Model Name (solo POST con OpenAI Compatible) | Vacío | Nombre del modelo; obligatorio con este formato de solicitud |
| Request Body (solo POST con Custom) | `{"q":"$q","sl":"$slCode","tl":"$tlCode"}` | Cuerpo JSON personalizado de la solicitud |

Pulsa `Save` para guardar y recargar automáticamente la página; `Cancel` para descartar los cambios; o `Reset defaults` para restaurar los valores predeterminados de la ventana y después `Save` para aplicarlos.

> **Nota:** `Use PLaMo` no inicia el modelo ni modifica su idioma de destino. El servicio externo está desactivado por defecto, por lo que el script solo utiliza Google Translate aunque esta opción esté marcada.

### Integración de otros servicios de traducción

Activa `Enable external translator`, desactiva `Use PLaMo` y configura el método de solicitud, la URL y el formato de respuesta según las especificaciones de la API del servicio. Desactivar la lista de idiomas permitidos no desactiva el filtro de publicaciones que ya están en el idioma de destino.

#### GET

La URL debe contener `$q`, por ejemplo:

```text
http://127.0.0.1:8001/translate?q=$q&sl=$sl&tl=$tl
```

Este es un ejemplo de formato de interfaz genérico; no implica que todos los servicios lean `sl` y `tl`.

| Marcador de posición en la URL | Valor de sustitución |
| --- | --- |
| `$q` | Texto que se va a traducir |
| `$sl` / `$slCode` | Código del idioma de origen; `auto` si se desconoce |
| `$tl` / `$tlCode` | Código del idioma de destino |

Los marcadores de posición de la URL se codifican automáticamente para su uso en URL y solo pueden aparecer en la ruta o en los parámetros de consulta.

#### POST: OpenAI Compatible

Por ejemplo, para integrar un servicio compatible con el formato OpenAI Chat Completions y con respuestas de tipo JSON Object:

| Opción | Ejemplo |
| --- | --- |
| Request Method | POST |
| Translation endpoint URL | `http://127.0.0.1:8080/v1/chat/completions` |
| API Type | OpenAI Compatible |
| API Key | Según los requisitos del servicio; puede dejarse vacío para servicios locales sin autenticación |
| Model Name | Nombre del modelo que ofrece el servicio |
| Response Style | OpenAI |

El script construye automáticamente los mensajes `system` / `user`, solicita al modelo un JSON con `sentence` y `src`, y establece `response_format: {"type":"json_object"}`, `temperature: 0` y `stream: false`. El servicio debe ser compatible con estos campos de solicitud; de lo contrario, puedes utilizar un cuerpo de solicitud Custom.

#### POST: Custom

Selecciona `API Type: Custom` y escribe un objeto JSON según los requisitos del servicio, por ejemplo:

```json
{
  "q": "$q",
  "sl": "$slCode",
  "tl": "$tlCode"
}
```

Los valores de cadena del JSON personalizado admiten los siguientes marcadores de posición (incluidas las cadenas de objetos y matrices anidados):

| Marcador de posición en el cuerpo de la solicitud | Valor de sustitución |
| --- | --- |
| `$q` | Texto que se va a traducir |
| `$sl` | Nombre en inglés del idioma de origen |
| `$tl` | Nombre en inglés del idioma de destino |
| `$slCode` | Código del idioma de origen |
| `$tlCode` | Código del idioma de destino |

El texto se escapa automáticamente para JSON. Al menos el cuerpo de la solicitud o la URL debe contener `$q`.

#### Formatos de respuesta admitidos

**Google Translate**:

```json
{
  "sentences": [
    {"trans": "你好，世界！"}
  ],
  "src": "en"
}
```

También admite el formato de matrices anidadas utilizado por la interfaz principal de Google Translate, por ejemplo:

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

`choices[0].message.content` también puede contener directamente la traducción en texto plano. Los formatos de solicitud y respuesta se configuran de forma independiente: GET no tiene por qué utilizar Google Translate ni POST tiene por qué utilizar OpenAI.

### Privacidad y limitaciones de uso

- El modo Google Translate envía a Google el texto que se va a traducir. Con la traducción local habilitada, el texto que cumple las condiciones y se procesa correctamente puede traducirse de forma local, pero el contenido que no cumple la lista de idiomas permitidos o cuya traducción falla todavía puede enviarse a Google. La versión actual no permite desactivar esta alternativa a Google, por lo que no constituye un modo de traducción estrictamente sin conexión.
- El script utiliza `GM_xmlhttpRequest` para acceder a interfaces de otros orígenes. Utiliza únicamente URL de confianza al configurar servicios externos; no envíes texto sensible ni claves de API a servicios que no sean de confianza. La clave de API se almacena en la configuración del script del gestor de scripts de usuario.
- El tiempo de espera de las solicitudes de traducción externas es de 60 segundos y el límite de traducciones automáticas simultáneas es de 5. Las traducciones iniciadas manualmente no están sujetas a este límite de la cola automática.
- Las interfaces de Google Translate y la estructura de las páginas de X pueden cambiar. No se garantiza que todas las funciones estén siempre disponibles en todas las páginas, idiomas de interfaz y versiones de navegador.

## Despliegue local de PLaMo 3 Translate 0.8B (muy recomendado)

La última creación de PLaMo 3: no sería exagerado considerarlo el mejor modelo de traducción de menos de 1B de parámetros, aunque la calidad de traducción varía según el idioma admitido.

La configuración predeterminada del servicio externo de X Translate es compatible con el script de ejemplo [plamo_flusher_bridge.py](plamo_flusher_bridge.py), que utiliza el modelo GGUF con cuantización `Q4_K_M` de [PLaMo 3 Translate 0.8B](https://huggingface.co/pfnet/plamo-3-translate-0.8b).

PLaMo 3 Translate es un modelo especializado en traducción desarrollado por Preferred Networks (PFN). Admite 53 códigos de idioma (incluidos el chino simplificado y el tradicional), así como contexto y glosarios. El archivo GGUF predeterminado ocupa aproximadamente 0,57 GB; durante la ejecución se necesita memoria RAM o memoria de vídeo (VRAM) adicional.

El script de Python se encarga de iniciar llama.cpp, construir los prompts de traducción PFML3 de PLaMo y convertir la respuesta del modelo a un formato compatible con Google Translate. Un único proceso del modelo puede prestar servicio a X Translate y YoutubeLiveChatFlusher simultáneamente.

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

### 1. Descargar el entorno de ejecución y el modelo

Los siguientes pasos utilizan Windows como ejemplo:

- [Python](https://www.python.org/downloads/): se recomienda Python 3.10 o posterior. El script puente de ejemplo solo utiliza la biblioteca estándar de Python y no requiere dependencias de terceros.
- [llama.cpp Releases](https://github.com/ggml-org/llama.cpp/releases): descarga una compilación para Windows compatible con PLaMo 3 Translate. Selecciona un backend CPU, CUDA o Vulkan, según tu hardware, descomprime el archivo y conserva todos los archivos necesarios para la ejecución. Si la compilación CUDA requiere bibliotecas de ejecución adicionales, descárgalas según las instrucciones de la versión correspondiente.
  - Versión recomendada: [b12359](https://github.com/ggml-org/llama.cpp/releases/tag/b12359).
- [PLaMo 3 Translate 0.8B GGUF (repositorio oficial del modelo)](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF): descarga [`plamo-3-translate-0.8b-Q4_K_M.gguf`](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF/resolve/main/plamo-3-translate-0.8b-Q4_K_M.gguf).
- Script de inicio de ejemplo: [plamo_flusher_bridge.py](plamo_flusher_bridge.py).

Respeta también la licencia del modelo, [PLaMo Community License](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF#license).

### 2. Modificar la configuración del script de Python

Abre `plamo_flusher_bridge.py` en un editor de texto y comprueba como mínimo estos tres parámetros:

```python
LLAMA_SERVER_EXE = Path(r"I:\llama.cpp\llama-server.exe")
GGUF_MODEL_FILE = Path(r"I:\_models\plamo-3-translate-0.8b-Q4_K_M.gguf")

TARGET_LANG = "zh-hant"
```

**Asegúrate de sustituir las dos rutas de archivo por las rutas reales de tu equipo y de establecer `TARGET_LANG` en el idioma al que quieras traducir.** Las rutas de la unidad `I:` solo son ejemplos; no es necesario utilizar el mismo directorio.

Por ejemplo:

```python
LLAMA_SERVER_EXE = Path(r"D:\llama.cpp\llama-server.exe")
GGUF_MODEL_FILE = Path(r"D:\models\plamo-3-translate-0.8b-Q4_K_M.gguf")
TARGET_LANG = "en"
```

Correspondencia de códigos de idiomas habituales:

| Idioma de destino | X Translate | Python / PLaMo |
| --- | --- | --- |
| Chino tradicional | `zh-TW` | `zh-hant` (valor predeterminado de Python) |
| Chino simplificado | `zh` | `zh-hans` |
| Inglés | `en` | `en` |
| Japonés | `ja` | `ja` |
| Coreano | `ko` | `ko` |

Consulta la lista completa en la [documentación oficial del modelo PLaMo](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF#supported-languages).

**Importante: en la traducción local, `TARGET_LANG` del script de Python tiene prioridad sobre el idioma de destino configurado en X Translate.** Esto se debe a posibles problemas de compatibilidad entre los códigos de idioma de PLaMo y los de otros modelos.\
Actualmente, el ejemplo de Python utiliza un `TARGET_LANG` fijo para ambos endpoints e ignora los parámetros de consulta `sl` y `tl` recibidos. Cambiar el idioma en el navegador no actualiza automáticamente el idioma de destino en Python. Debes reiniciar el script después de modificar su configuración.

Otros parámetros opcionales:

| Parámetro | Valor predeterminado | Finalidad |
| --- | --- | --- |
| `HOST` / `PORT` | `127.0.0.1` / `8001` | Dirección del servicio puente de traducción externo |
| `LLAMA_HOST` / `LLAMA_PORT` | `127.0.0.1` / `8000` | Dirección del backend llama-server |
| `LLAMA_STARTUP_TIMEOUT` | `120` | Tiempo de espera para la carga del modelo (segundos) |
| `AUTO_CONTEXT` | Contexto de publicaciones de X | Prompt de contexto para X Translate |
| `ENABLE_FLUSHER` | `False` | Habilita también el endpoint para integrar [YoutubeLiveChatFlusher](https://github.com/ys-j/YoutubeLiveChatFlusher) |
| `CONTEXT` | Contexto de comentarios del público en directos japoneses | Prompt de contexto para la integración con [YoutubeLiveChatFlusher](https://github.com/ys-j/YoutubeLiveChatFlusher) |

Si te interesa mostrar los comentarios de YouTube superpuestos al vídeo y traducirlos, consulta [Integración con YoutubeLiveChatFlusher](#integración-con-youtubelivechatflusher).

`AUTO_CONTEXT` y `CONTEXT` también se pueden personalizar mediante las variables de entorno `PLAMO_AUTO_CONTEXT` y `PLAMO_CONTEXT`, respectivamente.

Principales parámetros predeterminados de inicio de llama.cpp:

| Parámetro | Valor predeterminado del ejemplo | Descripción |
| --- | --- | --- |
| `--n-gpu-layers` | `99` | Descarga a la GPU tantas capas del modelo como sea posible; para usar solo la CPU, cambia el valor a `0` |
| `--ctx-size` | `3072` | Presupuesto total de contexto del servicio |
| `--parallel` | `4` | Número de ranuras de inferencia simultánea |
| `--temp` | `0` | Utiliza una configuración de decodificación determinista |
| `--n-predict` | `376` | Número máximo predeterminado de tokens generados |
| `--jinja` | Activado | Habilita la compatibilidad con plantillas Jinja |
| `--no-prefill-assistant` | Activado | Desactiva el prefill del asistente |

Estos son los parámetros del script de ejemplo, no valores recomendados oficialmente para todos los usos. El presupuesto de contexto debe incluir también el prompt PFML3, el glosario, el original y la traducción. Las publicaciones largas pueden superar la capacidad de una sola ranura de inferencia o alcanzar el límite de generación. Puedes aumentar `--ctx-size` / `--n-predict` o reducir `--parallel` según el hardware y la longitud del texto. La capacidad real de cada ranura se indica en el registro de inicio de llama-server.

### 3. Opcional: configurar un glosario

Crea un archivo `glossary.json` con codificación UTF-8 en el mismo directorio que `plamo_flusher_bridge.py`, por ejemplo:

```json
[
  {"source": "ひなの", "target": "Hinano"},
  {"source": "スト6", "target": "Street Fighter 6"}
]
```

El script puente lee el glosario en cada traducción y solo añade al prompt PFML3 los términos que realmente coinciden con el texto original. Si hay coincidencias solapadas, da prioridad a los términos más largos y añade cada término una sola vez. Ambos endpoints comparten este archivo.

- **El script funciona correctamente sin `glossary.json`**, incluso si solo utilizas `/translate-X`.
- Los cambios del archivo se leen en la siguiente traducción, sin reiniciar el servicio puente.
- El archivo debe ser una matriz JSON con elementos que contengan las cadenas no vacías `source` y `target`. Un JSON no válido o cuya estructura de nivel superior no sea una matriz provocará un fallo en la solicitud de traducción.
- El glosario se utiliza como prompt del modelo, no como una sustitución obligatoria de cadenas. No garantiza que el modelo emplee siempre las traducciones especificadas en todos los contextos.

### 4. Iniciar el servicio de traducción local

Abre CMD o PowerShell en el directorio del script de Python y ejecuta:

```bat
py plamo_flusher_bridge.py
```

Si utilizas el comando `python`:

```bat
python plamo_flusher_bridge.py
```

No es necesario iniciar llama-server manualmente de antemano. El script de Python inicia el servicio del modelo, comprueba `/health` y comienza a procesar las solicitudes de traducción cuando el modelo está listo. El registro predeterminado contiene la siguiente información:

```text
PLaMo model ready (HTTP /health 200).
Flusher endpoint (/translate) is disabled.
Auto (X posts) -> zh-hant: http://127.0.0.1:8001/translate-X?q=$q
Backend: http://127.0.0.1:8000/v1/completions  model=plamo-3-translate
Request sl/tl parameters are ignored by both endpoints.
Glossary file: F:\_repositories\comprehension\X-Translate\glossary.json
Press Ctrl+C to stop both services.
```

Se proporcionan dos rutas de API por defecto:

| URL | Idioma de origen | Idioma de destino | Estado predeterminado |
| --- | --- | --- | --- |
| `http://127.0.0.1:8001/translate-X?q=$q` | Detección automática por el modelo | `TARGET_LANG` | Activado |
| `http://127.0.0.1:8001/translate?q=$q` | Detección automática por el modelo | `TARGET_LANG` | Desactivado |

Puedes realizar una prueba en otra terminal (`curl.exe` codifica automáticamente el texto como parámetro de consulta de la URL):

```bat
curl.exe --noproxy "*" -G "http://127.0.0.1:8001/translate-X" --data-urlencode "q=Hello, world!"
```

Si el servicio funciona correctamente, devolverá un JSON similar al siguiente (la traducción depende del modelo y de la configuración):

```json
{"sentences":[{"trans":"你好，世界！"}],"src":"auto"}
```

`src: "auto"` indica el modo de detección automática, no el código del idioma que el modelo ha detectado realmente.

Mantén abierta la terminal de Python mientras utilices el servicio. Pulsa `Ctrl+C` para detener tanto el servicio puente como el llama-server que ha iniciado.

### 5. Habilitar PLaMo en X Translate

Abre X, entra en **Translator settings** desde el gestor de scripts de usuario y utiliza la siguiente configuración:

| Opción | Valor |
| --- | --- |
| Enable external translator (fallback to Google Translate) | Activado |
| Use PLaMo (apply source-language whitelist) | Activado |
| Request Method | GET |
| Translation endpoint URL | `http://127.0.0.1:8001/translate-X?q=$q` |
| Response Style | Google Translate |

Pulsa `Save`. Tras la recarga automática de la página, PLaMo local tendrá prioridad para traducir las publicaciones y biografías. Comprueba también que `Set translation language` coincida con `TARGET_LANG` en Python.

No utilices `/translate` como URL aquí: este endpoint está diseñado para traducir chats de directos y está desactivado por defecto.

### Preguntas frecuentes

| Problema | Solución |
| --- | --- |
| **Traducciones incompletas de publicaciones largas** | Aumenta `--n-predict` y `--ctx-size` según la información de Token usage que aparece en la ventana CMD de `plamo_flusher_bridge.py` |
| Python no encuentra llama-server o el GGUF | Comprueba que `LLAMA_SERVER_EXE` / `GGUF_MODEL_FILE` apunten a archivos que realmente existen |
| Puerto ocupado | Detén el servicio que utiliza `8000` o `8001`, o cambia los puertos en Python; si modificas `PORT`, actualiza también la URL del cliente |
| No se puede cargar el modelo | Comprueba que la versión de llama.cpp sea compatible con PLaMo 3, que estén disponibles las bibliotecas de ejecución del backend y que haya suficiente memoria RAM / VRAM |
| El navegador indica un problema de permisos de conexión | Comprueba si el gestor de scripts de usuario permite el acceso a direcciones locales y si el servicio de Python está en ejecución |
| Se sigue utilizando Google Translate | Comprueba que la traducción externa esté habilitada, que la URL sea correcta y que el idioma de origen figure en la lista permitida. Revisa el registro de Python y los avisos de uso de la alternativa en las herramientas de desarrollo del navegador |
| La traducción aparece en un idioma de destino incorrecto | Modifica `TARGET_LANG` en Python, reinicia el script y ajusta también el idioma de destino de X Translate |
| `/translate` devuelve 404 | Este endpoint está desactivado por defecto; para utilizarlo, establece `ENABLE_FLUSHER = True` y reinicia el script |

Por defecto, el servicio puente solo escucha en la dirección local `127.0.0.1`, no utiliza autenticación mediante clave de API y permite el acceso entre orígenes. Se recomienda conservar esta dirección de escucha local y no exponer directamente el servicio a la red local ni a Internet. El texto de las solicitudes GET también puede aparecer en los registros locales de acceso HTTP.

## Integración con YoutubeLiveChatFlusher

El mismo `plamo_flusher_bridge.py` también se puede integrar directamente con [YoutubeLiveChatFlusher](https://github.com/ys-j/YoutubeLiveChatFlusher) (extensión de navegador que muestra los comentarios de YouTube Live superpuestos al vídeo), sin necesidad de iniciar una segunda instancia del modelo.

Primero, habilita el endpoint de Flusher en el script de Python:

```python
ENABLE_FLUSHER = True
```

Guarda los cambios y vuelve a ejecutar `plamo_flusher_bridge.py`. Puedes cambiar `TARGET_LANG` según tus necesidades, pero ambos endpoints comparten el mismo idioma de destino.

En la configuración **Translator** de YoutubeLiveChatFlusher, selecciona **External service**, habilita la traducción y configura lo siguiente:

| Opción | Valor |
| --- | --- |
| Request Method | GET |
| URL | `http://127.0.0.1:8001/translate?q=$q` |
| Response Style | Google Translate |

Ambos proyectos pueden ejecutarse simultáneamente: X Translate y YoutubeLiveChatFlusher comparten el mismo modelo PLaMo y el mismo glosario, y solo se diferencian en la URL y el contexto. Si solo utilizas X Translate, deja `ENABLE_FLUSHER = False`.

## License

X Translate Userscript: MIT (véanse los metadatos del script). El modelo PLaMo, llama.cpp y YoutubeLiveChatFlusher están sujetos a sus respectivas licencias.
