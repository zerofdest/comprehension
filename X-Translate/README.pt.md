# X Translate

[日本語](README.md) | [English](README.en.md) | [繁體中文（台灣）](README.zh-hant.md) | [العربية](README.ar.md) | [Español](README.es.md) | **Português**

Script de usuário (Userscript) para tradução automática no [X (Twitter)](https://x.com/). Permite substituir a péssima tradução nativa do Grok no X pelo Google Translate, além de integrar modelos de tradução locais, como o PLaMo 3 Translate, ou outros serviços externos de tradução.

Por padrão, utiliza o Google Translate, sem necessidade de executar um modelo ou configurar uma chave de API. Ao ativar um serviço externo de tradução, o script tenta utilizá-lo primeiro e recorre automaticamente ao Google Translate caso a solicitação falhe.

- Tradução do Grok
  - Qualidade de tradução péssima e bugs frequentes em funções como a tradução automática.
- Google Translate
  - Este script permite a tradução totalmente automática. A qualidade geral da tradução é um pouco superior à do Grok, mas a latência é ligeiramente maior.
- Execução local de `plamo-3-translate-0.8b-Q4_K_M`
  - Boa qualidade de tradução e latência extremamente baixa: as traduções aparecem na página quase instantaneamente.

## Funcionalidades

- **Tradução automática de publicações**: traduz as publicações assim que entram na área visível do navegador, sem precisar clicar individualmente nos botões de tradução nativos do X. Compatível com publicações da linha do tempo, respostas, perfis, entre outras.
- **Tradução automática de biografias (Bio)**: tenta traduzir automaticamente biografias não vazias. O serviço de tradução identifica o idioma de origem sem depender das etiquetas de idioma fornecidas pelo X.
- **Alternância entre o original e a tradução**: use `Show translation` / `Hide translation` para alternar a exibição. A tradução de um mesmo elemento da página pode ser reutilizada sem enviar uma nova solicitação a cada alternância.
- **Substituição da tradução nativa do X**: assume o controle dos botões nativos de tradução que consegue identificar e adiciona botões às publicações e biografias que não os possuem. Também é compatível com os controles nativos de tradução identificáveis das Notas da Comunidade (Community Notes).
- **Filtragem por idioma de origem**: utiliza o atributo `lang` das publicações para ignorar o conteúdo que já está no idioma de destino. O chinês simplificado (`zh`) e o chinês tradicional (`zh-TW`) também são ignorados mutuamente. Esse filtro não se aplica às biografias.
- **Idioma de destino personalizável**: oferece uma lista de idiomas com busca, utiliza por padrão o idioma do navegador e permite restaurar a configuração padrão a qualquer momento.
- **Serviços de tradução personalizados**: aceita solicitações GET / POST, formatos de resposta do Google Translate / OpenAI, corpos de solicitação compatíveis com OpenAI, corpos JSON personalizados e chaves de API opcionais.
- **Lista de idiomas permitidos do PLaMo**: ao utilizar o PLaMo, somente as publicações com idiomas incluídos na lista são enviadas ao serviço externo. Publicações em idiomas não suportados ou sem uma etiqueta de idioma válida são processadas pelo Google Translate. O modelo identifica automaticamente o idioma das biografias. A lista pode ser desativada ao integrar outros serviços de tradução.
- **Fallback automático**: se o serviço externo exceder o tempo limite, retornar um erro ou produzir uma tradução inválida ou vazia, o script tenta utilizar o Google Translate. No modo PLaMo, o fallback também é acionado quando o conteúdo contém letras e a tradução é idêntica ao original. O próprio Google Translate dispõe de interfaces principal e alternativa, além de novas tentativas com detecção automática do idioma de origem quando necessário.
- **Preservação de links e emojis**: tenta preservar os links, as imagens incorporadas (incluindo emojis em formato de imagem) e as quebras de linha do original. Caso o serviço de tradução perca os marcadores de posição, os links ou imagens ausentes são adicionados ao final da tradução.
- **Controle de concorrência e compatibilidade com páginas dinâmicas**: executa até 5 tarefas de tradução automática simultaneamente, priorizando o conteúdo na parte superior da área visível. Monitora alterações dinâmicas da página, permite o carregamento durante a rolagem e a navegação entre páginas e evita exibir traduções desatualizadas em publicações que foram alteradas.

## Instalação

1. Instale um gerenciador de scripts de usuário no navegador, como o [Violentmonkey](https://violentmonkey.github.io/).
2. Abra [X-Translate.user.js](https://raw.githubusercontent.com/zerofdest/comprehension/main/X-Translate/X-Translate.user.js) e siga as instruções do gerenciador para instalar o script. Também é possível importar o arquivo `.user.js` diretamente no gerenciador.
3. Abra ou recarregue [x.com](https://x.com/) para que o script comece a funcionar.

O script é executado somente nas páginas que correspondem a `https://x.com/*`. Após a instalação, utiliza o Google Translate por padrão, sem necessidade de configuração adicional.

## Instruções de uso

### Configurar o idioma de tradução

Em uma página do X, clique no ícone do gerenciador de scripts de usuário do navegador, localize **X Translate** e selecione **Set translation language**.

Na janela `Translation Language`, procure e selecione o idioma desejado, por exemplo:

| Idioma | Código do idioma |
| --- | --- |
| English | `en` |
| Japanese | `ja` |
| Chinese | `zh` |
| Chinese (Traditional) | `zh-TW` |
| Korean | `ko` |

Após selecionar um idioma, a página será recarregada automaticamente. Clique em `Reset to browser default` para restaurar o idioma padrão do navegador.

### Exibir o original ou a tradução

Quando as publicações e biografias que atendem aos critérios de tradução entram na área visível, o script envia automaticamente as solicitações de tradução.

| Estado do botão | Significado |
| --- | --- |
| `Translating...` | Tradução em andamento |
| `Hide translation` | A tradução está sendo exibida; clique para voltar ao original |
| `Show translation` | O original está sendo exibido; clique para mostrar a tradução. Se ainda não houver tradução, será enviada uma solicitação |

Caso a tradução falhe, clique em `Show translation` para tentar novamente de forma manual.

### Translator settings

Selecione **Translator settings** no menu do X Translate no gerenciador de scripts de usuário para configurar um serviço externo de tradução.

| Configuração | Valor padrão | Descrição |
| --- | --- | --- |
| Enable external translator (fallback to Google Translate) | Desativado | Prioriza o serviço externo e recorre ao Google Translate em caso de falha |
| Use PLaMo (apply source-language whitelist) | Ativado | Aplica às publicações a lista de idiomas de origem permitidos do PLaMo; normalmente é desativado ao integrar outros serviços |
| Request Method | GET | Aceita GET e POST |
| Translation endpoint URL | `http://127.0.0.1:8001/translate-X?q=$q` | Endereço da API externa de tradução |
| Response Style | Google Translate | Selecione o formato real de resposta do serviço: Google Translate ou OpenAI |
| API Type (somente POST) | OpenAI Compatible | Utiliza o formato integrado de solicitação OpenAI ou Custom JSON |
| API Key (somente POST, opcional) | Vazio | Se preenchida, a chave é enviada por meio de `Authorization: Bearer ...` |
| Model Name (somente POST com OpenAI Compatible) | Vazio | Nome do modelo; obrigatório ao utilizar esse formato de solicitação |
| Request Body (somente POST com Custom) | `{"q":"$q","sl":"$slCode","tl":"$tlCode"}` | Corpo JSON personalizado da solicitação |

Clique em `Save` para salvar e recarregar a página automaticamente; em `Cancel` para descartar as alterações; ou em `Reset defaults` para restaurar os valores padrão da janela e depois em `Save` para aplicá-los.

> **Atenção:** `Use PLaMo` não inicia o modelo nem altera seu idioma de destino. O serviço externo está desativado por padrão, portanto o script utiliza apenas o Google Translate mesmo que essa opção esteja marcada.

### Integração com outros serviços de tradução

Ative `Enable external translator`, desative `Use PLaMo` e configure o método de solicitação, a URL e o formato de resposta de acordo com as especificações da API do serviço. Desativar a lista de idiomas permitidos não desativa o filtro de publicações que já estão no idioma de destino.

#### GET

A URL deve conter `$q`, por exemplo:

```text
http://127.0.0.1:8001/translate?q=$q&sl=$sl&tl=$tl
```

Este é um exemplo de formato de interface genérico; isso não significa que todos os serviços utilizem `sl` e `tl`.

| Marcador de posição na URL | Valor de substituição |
| --- | --- |
| `$q` | Texto a ser traduzido |
| `$sl` / `$slCode` | Código do idioma de origem; `auto` se desconhecido |
| `$tl` / `$tlCode` | Código do idioma de destino |

Os marcadores de posição da URL são codificados automaticamente para uso em URLs e só podem aparecer no caminho ou nos parâmetros de consulta.

#### POST: OpenAI Compatible

Por exemplo, para integrar um serviço compatível com o formato OpenAI Chat Completions e com respostas do tipo JSON Object:

| Configuração | Exemplo |
| --- | --- |
| Request Method | POST |
| Translation endpoint URL | `http://127.0.0.1:8080/v1/chat/completions` |
| API Type | OpenAI Compatible |
| API Key | Preencha conforme os requisitos do serviço; pode ser deixada em branco para serviços locais sem autenticação |
| Model Name | Nome do modelo disponibilizado pelo serviço |
| Response Style | OpenAI |

O script constrói automaticamente as mensagens `system` / `user`, solicita ao modelo um JSON contendo `sentence` e `src` e define `response_format: {"type":"json_object"}`, `temperature: 0` e `stream: false`. O serviço precisa ser compatível com esses campos da solicitação; caso contrário, é possível utilizar um corpo de solicitação Custom.

#### POST: Custom

Selecione `API Type: Custom` e escreva um objeto JSON de acordo com os requisitos do serviço de tradução, por exemplo:

```json
{
  "q": "$q",
  "sl": "$slCode",
  "tl": "$tlCode"
}
```

Os valores de texto do JSON personalizado aceitam os seguintes marcadores de posição (incluindo strings em objetos e arrays aninhados):

| Marcador de posição no corpo da solicitação | Valor de substituição |
| --- | --- |
| `$q` | Texto a ser traduzido |
| `$sl` | Nome do idioma de origem em inglês |
| `$tl` | Nome do idioma de destino em inglês |
| `$slCode` | Código do idioma de origem |
| `$tlCode` | Código do idioma de destino |

Os caracteres do texto são escapados automaticamente para JSON. O corpo da solicitação ou a URL deve conter `$q` em pelo menos um deles.

#### Formatos de resposta suportados

**Google Translate**:

```json
{
  "sentences": [
    {"trans": "你好，世界！"}
  ],
  "src": "en"
}
```

Também é aceito o formato de arrays aninhados utilizado pela interface principal do Google Translate, por exemplo:

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

`choices[0].message.content` também pode conter diretamente a tradução em texto simples. Os formatos de solicitação e resposta são configurados de forma independente: GET não precisa ser usado com Google Translate, nem POST precisa ser usado com OpenAI.

### Privacidade e limitações de uso

- O modo Google Translate envia ao Google o texto a ser traduzido. Com a tradução local ativada, os textos que atendem aos critérios e são processados com sucesso podem ser traduzidos localmente, mas o conteúdo que não corresponde à lista de idiomas permitidos ou cuja tradução falha ainda pode ser enviado ao Google. A versão atual não oferece uma opção para desativar o fallback para o Google, portanto não se trata de um modo de tradução estritamente offline.
- O script utiliza `GM_xmlhttpRequest` para acessar interfaces de outras origens. Ao configurar serviços externos, utilize apenas URLs confiáveis; não envie textos sensíveis ou chaves de API a serviços não confiáveis. A chave de API é armazenada nas configurações do script no gerenciador de scripts de usuário.
- O tempo limite das solicitações externas de tradução é de 60 segundos, e o limite de traduções automáticas simultâneas é de 5. As traduções acionadas manualmente não estão sujeitas a esse limite da fila automática.
- As interfaces do Google Translate e a estrutura das páginas do X podem mudar. Não há garantia de que todas as funcionalidades permaneçam disponíveis em todas as páginas, idiomas de interface e versões de navegador.

## Execução local do PLaMo 3 Translate 0.8B (fortemente recomendada)

A mais recente criação do PLaMo 3: não seria exagero considerá-lo o melhor modelo de tradução com menos de 1B de parâmetros, embora a qualidade da tradução varie entre os idiomas suportados.

A configuração padrão do serviço externo do X Translate é compatível com o script de exemplo [plamo_flusher_bridge.py](plamo_flusher_bridge.py), que utiliza o modelo GGUF com quantização `Q4_K_M` do [PLaMo 3 Translate 0.8B](https://huggingface.co/pfnet/plamo-3-translate-0.8b).

O PLaMo 3 Translate é um modelo especializado em tradução desenvolvido pela Preferred Networks (PFN). Suporta 53 códigos de idioma (incluindo chinês simplificado e tradicional), além de contexto e glossários. O arquivo GGUF padrão tem aproximadamente 0,57 GB; a execução também exige memória RAM ou memória de vídeo (VRAM) adicional.

O script Python é responsável por iniciar o llama.cpp, construir os prompts de tradução PFML3 do PLaMo e converter as respostas do modelo para um formato compatível com o Google Translate. Um único processo do modelo pode atender simultaneamente ao X Translate e ao YoutubeLiveChatFlusher.

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

### 1. Baixar o ambiente de execução e o modelo

Os passos a seguir utilizam o Windows como exemplo:

- [Python](https://www.python.org/downloads/): recomenda-se o Python 3.10 ou posterior. O script de integração de exemplo utiliza apenas a biblioteca padrão do Python e não requer dependências de terceiros.
- [llama.cpp Releases](https://github.com/ggml-org/llama.cpp/releases): baixe uma versão compilada para Windows compatível com o PLaMo 3 Translate. Escolha um backend CPU, CUDA ou Vulkan de acordo com seu hardware, extraia o arquivo e mantenha todos os arquivos necessários à execução. Se a compilação CUDA exigir bibliotecas de runtime adicionais, baixe-as conforme as instruções da versão correspondente.
  - Versão recomendada: [b12359](https://github.com/ggml-org/llama.cpp/releases/tag/b12359).
- [PLaMo 3 Translate 0.8B GGUF (repositório oficial do modelo)](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF): baixe [`plamo-3-translate-0.8b-Q4_K_M.gguf`](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF/resolve/main/plamo-3-translate-0.8b-Q4_K_M.gguf).
- Script de inicialização de exemplo: [plamo_flusher_bridge.py](plamo_flusher_bridge.py).

Respeite também a licença do modelo, [PLaMo Community License](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF#license).

### 2. Alterar as configurações do script Python

Abra `plamo_flusher_bridge.py` em um editor de texto e verifique pelo menos os três parâmetros a seguir:

```python
LLAMA_SERVER_EXE = Path(r"I:\llama.cpp\llama-server.exe")
GGUF_MODEL_FILE = Path(r"I:\_models\plamo-3-translate-0.8b-Q4_K_M.gguf")

TARGET_LANG = "zh-hant"
```

**Substitua os dois caminhos de arquivo pelos caminhos reais em seu computador e configure `TARGET_LANG` com o idioma de destino desejado.** Os caminhos da unidade `I:` são apenas exemplos; não é necessário utilizar o mesmo diretório.

Por exemplo:

```python
LLAMA_SERVER_EXE = Path(r"D:\llama.cpp\llama-server.exe")
GGUF_MODEL_FILE = Path(r"D:\models\plamo-3-translate-0.8b-Q4_K_M.gguf")
TARGET_LANG = "en"
```

Correspondência dos códigos de idioma mais comuns:

| Idioma de destino | X Translate | Python / PLaMo |
| --- | --- | --- |
| Chinês tradicional | `zh-TW` | `zh-hant` (padrão do Python) |
| Chinês simplificado | `zh` | `zh-hans` |
| Inglês | `en` | `en` |
| Japonês | `ja` | `ja` |
| Coreano | `ko` | `ko` |

Consulte a lista completa de idiomas na [documentação oficial do modelo PLaMo](https://huggingface.co/pfnet/plamo-3-translate-0.8b-GGUF#supported-languages).

**Importante: na tradução local, o `TARGET_LANG` do script Python tem prioridade sobre o idioma de destino configurado no X Translate.** Isso se deve a possíveis problemas de compatibilidade entre os códigos de idioma do PLaMo e os de outros modelos.\
Atualmente, o exemplo em Python utiliza um `TARGET_LANG` fixo para ambos os endpoints e ignora os parâmetros de consulta `sl` e `tl` recebidos. Alterar o idioma no navegador não atualiza automaticamente o idioma de destino no Python. É necessário reiniciar o script após modificar suas configurações.

Outros parâmetros opcionais:

| Parâmetro | Valor padrão | Finalidade |
| --- | --- | --- |
| `HOST` / `PORT` | `127.0.0.1` / `8001` | Endereço do serviço intermediário de tradução externa |
| `LLAMA_HOST` / `LLAMA_PORT` | `127.0.0.1` / `8000` | Endereço do backend llama-server |
| `LLAMA_STARTUP_TIMEOUT` | `120` | Tempo de espera para o carregamento do modelo (segundos) |
| `AUTO_CONTEXT` | Contexto de publicações do X | Prompt de contexto para o X Translate |
| `ENABLE_FLUSHER` | `False` | Define se o endpoint de integração com o [YoutubeLiveChatFlusher](https://github.com/ys-j/YoutubeLiveChatFlusher) também será ativado |
| `CONTEXT` | Contexto de comentários do público em transmissões ao vivo japonesas | Prompt de contexto para a integração com o [YoutubeLiveChatFlusher](https://github.com/ys-j/YoutubeLiveChatFlusher) |

Se tiver interesse em exibir os comentários do YouTube sobre o vídeo e traduzi-los, consulte [Integração com o YoutubeLiveChatFlusher](#integração-com-o-youtubelivechatflusher).

`AUTO_CONTEXT` e `CONTEXT` também podem ser personalizados por meio das variáveis de ambiente `PLAMO_AUTO_CONTEXT` e `PLAMO_CONTEXT`, respectivamente.

Principais parâmetros padrão de inicialização do llama.cpp:

| Parâmetro | Valor padrão do exemplo | Descrição |
| --- | --- | --- |
| `--n-gpu-layers` | `99` | Transfere para a GPU o máximo possível de camadas do modelo; para utilizar somente a CPU, altere para `0` |
| `--ctx-size` | `3072` | Orçamento total de contexto do serviço |
| `--parallel` | `4` | Número de slots de inferência paralela |
| `--temp` | `0` | Utiliza uma configuração de decodificação determinística |
| `--n-predict` | `376` | Número máximo padrão de tokens gerados |
| `--jinja` | Ativado | Ativa o suporte a templates Jinja |
| `--no-prefill-assistant` | Ativado | Desativa o prefill do assistente |

Esses são os parâmetros do script de exemplo, e não valores oficialmente recomendados para todos os usos. O orçamento de contexto também precisa acomodar o prompt PFML3, o glossário, o texto original e a tradução. Publicações longas podem exceder a capacidade de um único slot de inferência ou atingir o limite de geração. É possível aumentar `--ctx-size` / `--n-predict` ou reduzir `--parallel`, conforme o hardware e o comprimento do texto. A capacidade real de cada slot é informada no log de inicialização do llama-server.

### 3. Opcional: configurar um glossário

Crie um arquivo `glossary.json` com codificação UTF-8 no mesmo diretório de `plamo_flusher_bridge.py`, por exemplo:

```json
[
  {"source": "ひなの", "target": "Hinano"},
  {"source": "スト6", "target": "Street Fighter 6"}
]
```

O script de integração lê o glossário a cada tradução e acrescenta ao prompt PFML3 apenas os termos que realmente correspondem ao texto original. Em caso de correspondências sobrepostas, os termos mais longos têm prioridade, e cada termo é incluído somente uma vez. Ambos os endpoints compartilham esse arquivo.

- **O script funciona normalmente sem `glossary.json`**, inclusive quando se utiliza apenas `/translate-X`.
- Após modificar o arquivo, o novo conteúdo será lido na próxima tradução, sem necessidade de reiniciar o serviço intermediário.
- O arquivo deve ser um array JSON cujos itens contenham as strings não vazias `source` e `target`. Um JSON inválido ou cuja estrutura de nível superior não seja um array fará a solicitação de tradução falhar.
- O glossário é usado como prompt para o modelo, e não como substituição obrigatória de strings. Não é possível garantir que o modelo utilize rigorosamente as traduções especificadas em todos os contextos.

### 4. Iniciar o serviço de tradução local

Abra o CMD ou PowerShell no diretório do script Python e execute:

```bat
py plamo_flusher_bridge.py
```

Se utilizar o comando `python`:

```bat
python plamo_flusher_bridge.py
```

Não é necessário iniciar o llama-server manualmente com antecedência. O script Python inicia o serviço do modelo, verifica `/health` e começa a processar as solicitações de tradução quando o modelo estiver pronto. O log padrão contém as seguintes informações:

```text
PLaMo model ready (HTTP /health 200).
Flusher endpoint (/translate) is disabled.
Auto (X posts) -> zh-hant: http://127.0.0.1:8001/translate-X?q=$q
Backend: http://127.0.0.1:8000/v1/completions  model=plamo-3-translate
Request sl/tl parameters are ignored by both endpoints.
Glossary file: F:\_repositories\comprehension\X-Translate\glossary.json
Press Ctrl+C to stop both services.
```

Por padrão, são fornecidos dois caminhos de API:

| URL | Idioma de origem | Idioma de destino | Estado padrão |
| --- | --- | --- | --- |
| `http://127.0.0.1:8001/translate-X?q=$q` | Detecção automática pelo modelo | `TARGET_LANG` | Ativado |
| `http://127.0.0.1:8001/translate?q=$q` | Detecção automática pelo modelo | `TARGET_LANG` | Desativado |

É possível testar em outro terminal (`curl.exe` codifica automaticamente o texto como parâmetro de consulta da URL):

```bat
curl.exe --noproxy "*" -G "http://127.0.0.1:8001/translate-X" --data-urlencode "q=Hello, world!"
```

Se o serviço estiver funcionando corretamente, retornará um JSON semelhante ao seguinte (a tradução depende do modelo e da configuração):

```json
{"sentences":[{"trans":"你好，世界！"}],"src":"auto"}
```

`src: "auto"` representa o modo de detecção automática, e não o código do idioma realmente identificado pelo modelo.

Mantenha o terminal Python aberto durante a utilização do serviço. Pressione `Ctrl+C` para interromper tanto o serviço intermediário quanto o llama-server iniciado por ele.

### 5. Ativar o PLaMo no X Translate

Abra uma página do X, acesse **Translator settings** no gerenciador de scripts de usuário e utilize a seguinte configuração:

| Configuração | Valor |
| --- | --- |
| Enable external translator (fallback to Google Translate) | Ativado |
| Use PLaMo (apply source-language whitelist) | Ativado |
| Request Method | GET |
| Translation endpoint URL | `http://127.0.0.1:8001/translate-X?q=$q` |
| Response Style | Google Translate |

Clique em `Save`. Após o recarregamento automático da página, o PLaMo local terá prioridade na tradução de publicações e biografias. Verifique também se `Set translation language` corresponde ao `TARGET_LANG` do Python.

Não utilize `/translate` como URL aqui: esse endpoint foi desenvolvido para traduzir chats de transmissões ao vivo e está desativado por padrão.

### Perguntas frequentes

| Problema | Solução |
| --- | --- |
| **Traduções incompletas de publicações longas** | Aumente `--n-predict` e `--ctx-size` de acordo com as informações de Token usage exibidas na janela CMD de `plamo_flusher_bridge.py` |
| O Python não encontra o llama-server ou o GGUF | Verifique se `LLAMA_SERVER_EXE` / `GGUF_MODEL_FILE` apontam para arquivos que realmente existem |
| Porta já em uso | Interrompa o serviço que utiliza `8000` ou `8001`, ou altere as portas no Python; se modificar `PORT`, atualize também a URL do cliente |
| O modelo não carrega | Verifique se a versão do llama.cpp é compatível com o PLaMo 3, se todas as bibliotecas de runtime do backend estão disponíveis e se há memória RAM / VRAM suficiente |
| O navegador indica um problema de permissão de conexão | Verifique se o gerenciador de scripts de usuário permite acesso a endereços locais e se o serviço Python está em execução |
| O Google Translate continua sendo utilizado | Verifique se a tradução externa está ativada, se a URL está correta e se o idioma de origem está na lista de idiomas permitidos. Consulte os logs do Python e os avisos de fallback nas ferramentas de desenvolvedor do navegador |
| A tradução está no idioma de destino incorreto | Modifique `TARGET_LANG` no Python, reinicie o script e ajuste também o idioma de destino do X Translate |
| `/translate` retorna 404 | Esse endpoint está desativado por padrão; para utilizá-lo, defina `ENABLE_FLUSHER = True` e reinicie o script |

Por padrão, o serviço intermediário escuta somente no endereço local `127.0.0.1`, não utiliza autenticação por chave de API e permite acesso entre origens. Recomenda-se manter o endereço de escuta local e não expor diretamente o serviço à rede local ou à Internet. Os textos das solicitações GET também podem aparecer nos logs locais de acesso HTTP.

## Integração com o YoutubeLiveChatFlusher

O mesmo `plamo_flusher_bridge.py` também pode ser integrado diretamente ao [YoutubeLiveChatFlusher](https://github.com/ys-j/YoutubeLiveChatFlusher) (extensão de navegador que exibe os comentários do YouTube Live sobre o vídeo), sem necessidade de iniciar uma segunda instância do modelo.

Primeiro, ative o endpoint do Flusher no script Python:

```python
ENABLE_FLUSHER = True
```

Salve as alterações e execute novamente `plamo_flusher_bridge.py`. `TARGET_LANG` pode ser alterado conforme a necessidade, mas ambos os endpoints compartilham o mesmo idioma de destino.

Nas configurações **Translator** do YoutubeLiveChatFlusher, selecione **External service**, ative a tradução e configure o seguinte:

| Configuração | Valor |
| --- | --- |
| Request Method | GET |
| URL | `http://127.0.0.1:8001/translate?q=$q` |
| Response Style | Google Translate |

Os dois projetos podem ser executados simultaneamente: o X Translate e o YoutubeLiveChatFlusher compartilham o mesmo modelo PLaMo e o mesmo glossário, diferenciando-se apenas pela URL e pelo contexto. Se utilizar apenas o X Translate, mantenha `ENABLE_FLUSHER = False`.

## License

X Translate Userscript: MIT (consulte os metadados do script). O modelo PLaMo, o llama.cpp e o YoutubeLiveChatFlusher estão sujeitos às suas respectivas licenças.
